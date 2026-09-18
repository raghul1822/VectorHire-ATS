"""
VectorHire ATS — Unified Analyzer
==================================
A single consolidated Streamlit app that replaces app.py / app1.py / app2.py.

All resume/JD parsing logic (text extraction, cleaning, skill/name/experience/
education extraction) is written ONCE and shared. Only the SCORING METHOD
changes based on the mode selected in the sidebar:

    • Basic         -> mirrors the original app1.py formula
    • Intermediate  -> mirrors the original app2.py formula (incl. its known
                       quirks: unweighted skills, raw-text semantics, and a
                       flat +5 constant) — kept intact and labeled so you can
                       see exactly how it differs from Advanced.
    • Advanced      -> mirrors the original app.py formula (recommended)

This lets you compare all three scoring philosophies from one app instead of
maintaining three duplicate codebases.
"""

import json
import re
import docx2txt
import pandas as pd
import pdfplumber
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# ==========================
# PAGE CONFIGURATION
# ==========================
st.set_page_config(
    page_title="VectorHire AI ATS Profiler",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODE_THEMES = {
    "Basic":        {"grad": "#0284C7, #0EA5E9, #38BDF8", "icon": "🤖"},
    "Intermediate": {"grad": "#0F766E, #14B8A6, #2DD4BF", "icon": "📋"},
    "Advanced":     {"grad": "#4F46E5, #7C3AED, #9333EA", "icon": "🎯"},
}

def inject_styles(mode: str):
    """Render the gradient hero banner + card styling, themed by selected mode."""
    grad = MODE_THEMES[mode]["grad"]
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

        .hero-banner {{
            background: linear-gradient(135deg, {grad});
            padding: 2rem 2.5rem;
            border-radius: 18px;
            margin-bottom: 1.75rem;
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.20);
        }}
        .main-title {{
            font-size: 2.3rem; font-weight: 800; color: #FFFFFF;
            margin-bottom: 0.35rem; letter-spacing: -0.02em;
        }}
        .sub-title {{ font-size: 1.02rem; color: rgba(255,255,255,0.9); margin-bottom: 0; }}
        .mode-chip {{
            display: inline-block; background: rgba(255,255,255,0.18);
            color: #fff; padding: 4px 12px; border-radius: 999px;
            font-size: 0.8rem; font-weight: 600; margin-top: 0.6rem;
            border: 1px solid rgba(255,255,255,0.35);
        }}
        .skill-badge {{
            display: inline-block; background: linear-gradient(135deg, #E0F2FE, #BAE6FD);
            color: #075985; padding: 6px 14px; border-radius: 20px; margin: 3px;
            font-size: 0.85rem; font-weight: 600; border: 1px solid #7DD3FC;
        }}
        .missing-badge {{
            display: inline-block; background: linear-gradient(135deg, #FEE2E2, #FECACA);
            color: #991B1B; padding: 6px 14px; border-radius: 20px; margin: 3px;
            font-size: 0.85rem; font-weight: 600; border: 1px solid #FCA5A5;
        }}
        div[data-testid="stMetric"] {{
            background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px;
            padding: 1rem 1.1rem; box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
        }}
        div[data-testid="stMetric"] label {{ color: #6B7280 !important; font-weight: 600 !important; }}
        div[data-testid="stExpander"] {{
            border-radius: 14px !important; border: 1px solid #E5E7EB !important;
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04); margin-bottom: 0.75rem;
        }}
        section[data-testid="stSidebar"] {{ background: #F8FAFC; border-right: 1px solid #E5E7EB; }}
        div[data-testid="stDataFrame"] {{ border-radius: 14px; overflow: hidden; border: 1px solid #E5E7EB; }}
        button[data-baseweb="tab"] {{ font-weight: 600; border-radius: 10px 10px 0 0; }}
        hr {{ margin: 1.2rem 0; border-color: #E5E7EB; }}
    </style>
    """, unsafe_allow_html=True)


# ==========================
# RESOURCE CACHING
# ==========================
@st.cache_resource
def load_ai_model():
    """Cache Sentence Transformer model across app reruns."""
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_ai_model()

@st.cache_data
def load_skills_dataset():
    """Load and cache local skills mapping configuration."""
    try:
        with open("skills.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("'skills.json' not found. Using fallback empty dictionary.")
        return {}

SKILLS = load_skills_dataset()


# ==========================
# SHARED PARSING & EXTRACTION
# (written once, used by all three modes)
# ==========================
def extract_text(file) -> str:
    """Safely extract raw text from PDF and DOCX files."""
    try:
        if file.name.lower().endswith(".pdf"):
            text_pages = []
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text_pages.append(extracted)
            return "\n".join(text_pages)
        elif file.name.lower().endswith(".docx"):
            return docx2txt.process(file) or ""
    except Exception as e:
        st.error(f"Error processing {file.name}: {e}")
    return ""

def clean_text(text: str) -> str:
    """Normalize text while preserving common technical skill symbols (+, #, .)."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s\+\#\.]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def extract_skills(text: str) -> list[str]:
    """Extract matching skills using word-boundary (and underscore-aware) matching."""
    found = []
    text_lower = text.lower()
    for skill in SKILLS:
        pattern = r"(?:\b|_)" + re.escape(skill.lower()) + r"(?:\b|_)"
        if re.search(pattern, text_lower):
            found.append(skill)
    return list(set(found))

def extract_name(text: str) -> str:
    """Retrieve candidate name from the first meaningful top line."""
    for line in text.split("\n"):
        cleaned = line.strip()
        if len(cleaned) > 2 and not cleaned.lower().startswith("resume"):
            return cleaned
    return "Unknown Candidate"

def extract_experience(text: str) -> int:
    """Extract highest years of experience mentioned in text."""
    matches = re.findall(r'(\d+)\+?\s*(?:years|year)', text.lower())
    if matches:
        return max([int(m) for m in matches])
    return 0

def extract_education(text: str) -> list[str]:
    """Extract education degree patterns."""
    degree_keywords = [
        "b.tech", "b.e", "m.tech", "mca", "mba", "b.s", "m.s", "phd",
        "computer science", "engineering", "bachelor", "master"
    ]
    text_lower = text.lower()
    return [d for d in degree_keywords if re.search(r"\b" + re.escape(d) + r"\b", text_lower)]

def parse_candidate_profile(text: str) -> dict:
    """Build structured profile dict from text."""
    return {
        "name": extract_name(text),
        "skills": extract_skills(text),
        "experience_years": extract_experience(text),
        "education": extract_education(text)
    }


# ==========================
# SCORING PRIMITIVES
# ==========================
def semantic_score_batched(text_a: str, text_b: str) -> float:
    """Semantic similarity via ONE batched encode() call (efficient, used by Basic & Advanced)."""
    if not text_a or not text_b:
        return 0.0
    embeddings = model.encode([text_a, text_b])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(float(score) * 100, 2)

def semantic_score_separate(text_a: str, text_b: str) -> float:
    """Semantic similarity via TWO separate encode() calls (legacy behavior, used by Intermediate)."""
    if not text_a or not text_b:
        return 0.0
    vec_a = model.encode([text_a])
    vec_b = model.encode([text_b])
    score = cosine_similarity(vec_a, vec_b)[0][0]
    return round(float(score) * 100, 2)

def weighted_skill_score(resume_skills: list[str], jd_skills: list[str]) -> float:
    """Skill match weighted by skills.json importance (used by Basic & Advanced)."""
    if not jd_skills:
        return 0.0
    total_weight = sum(SKILLS.get(s, 1) for s in jd_skills)
    matched_weight = sum(SKILLS.get(s, 1) for s in jd_skills if s in resume_skills)
    return round((matched_weight / total_weight) * 100, 2) if total_weight > 0 else 0.0

def unweighted_skill_score(resume_skills: list[str], jd_skills: list[str]) -> float:
    """Plain overlap percentage, ignoring skill weights (legacy behavior, used by Intermediate)."""
    if not jd_skills:
        return 0.0
    matched = set(resume_skills) & set(jd_skills)
    return round((len(matched) / len(jd_skills)) * 100, 2)

def experience_score(resume_exp: int, jd_exp: int) -> float:
    """Experience ratio, capped at 100%."""
    if jd_exp == 0 or resume_exp >= jd_exp:
        return 100.0
    return round((resume_exp / jd_exp) * 100, 2)


# ---- Final ATS score per mode -------------------------------------------
def score_basic(semantic: float, skill: float) -> float:
    """app1.py formula: 50% semantic + 50% skill. No experience factor."""
    return round((semantic * 0.5) + (skill * 0.5), 2)

def score_intermediate(skill: float, semantic: float, exp: float) -> float:
    """app2.py formula (legacy, kept intact): includes a flat +5 constant bug."""
    return round((skill * 0.50) + (semantic * 0.30) + (exp * 0.15) + (100 * 0.05), 2)

def score_advanced(semantic: float, skill: float, exp: float) -> float:
    """app.py formula (recommended): 45% skill + 40% semantic + 15% experience."""
    return round((skill * 0.45) + (semantic * 0.40) + (exp * 0.15), 2)


# ==========================
# MAIN APP
# ==========================
def main():
    with st.sidebar:
        st.header("⚙️ Document Upload")
        jd_file = st.file_uploader(
            "📌 Upload Job Description",
            type=["pdf", "docx"],
            help="Upload target Job Description"
        )
        resumes = st.file_uploader(
            "📄 Upload Candidate Resumes",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            help="Upload candidate resumes"
        )

        st.divider()
        st.header("🧪 Scoring Method")
        mode = st.selectbox(
            "Choose which scoring approach to use",
            options=["Advanced", "Intermediate", "Basic"],
            index=0,
            help="Switch between the three original scoring philosophies without switching apps."
        )

        mode_notes = {
            "Basic": "Semantic (50%) + Weighted Skills (50%). No experience factor.",
            "Intermediate": "Skills (50%, unweighted) + Semantic-on-raw-text (30%) + Experience (15%) "
                             "+ a flat +5 legacy constant (5%). Kept as-is for comparison — inflates every score.",
            "Advanced": "Weighted Skills (45%) + Semantic-on-cleaned-text (40%) + Experience (15%). Recommended.",
        }
        st.caption(f"ℹ️ {mode_notes[mode]}")

        st.divider()
        threshold = st.slider("Qualification Threshold (%)", 0, 100, 60, 5)

    inject_styles(mode)
    icon = MODE_THEMES[mode]["icon"]
    st.markdown(f"""
        <div class="hero-banner">
            <div class="main-title">{icon} VectorHire ATS Analyzer</div>
            <div class="sub-title">Semantic matching, skill verification, and metadata profiling — in one unified app.</div>
            <div class="mode-chip">Scoring Method: {mode}</div>
        </div>
    """, unsafe_allow_html=True)

    if resumes and jd_file:
        raw_jd_text = extract_text(jd_file)
        clean_jd_text = clean_text(raw_jd_text)
        jd_skills = extract_skills(clean_jd_text)
        jd_exp = extract_experience(raw_jd_text)

        results = []

        for resume_file in resumes:
            raw_resume = extract_text(resume_file)
            clean_resume = clean_text(raw_resume)
            profile = parse_candidate_profile(raw_resume)
            resume_skills = profile["skills"]

            # ---- Mode-specific scoring ----
            if mode == "Basic":
                sem_score = semantic_score_batched(clean_resume, clean_jd_text)
                skill_score = weighted_skill_score(resume_skills, jd_skills)
                exp_score = None
                ats_score = score_basic(sem_score, skill_score)

            elif mode == "Intermediate":
                sem_score = semantic_score_separate(raw_resume, raw_jd_text)  # legacy: raw text
                skill_score = unweighted_skill_score(resume_skills, jd_skills)  # legacy: unweighted
                exp_score = experience_score(profile["experience_years"], jd_exp)
                ats_score = score_intermediate(skill_score, sem_score, exp_score)

            else:  # Advanced
                sem_score = semantic_score_batched(clean_resume, clean_jd_text)
                skill_score = weighted_skill_score(resume_skills, jd_skills)
                exp_score = experience_score(profile["experience_years"], jd_exp)
                ats_score = score_advanced(sem_score, skill_score, exp_score)

            matched_skills = sorted(set(resume_skills) & set(jd_skills))
            missing_skills = sorted(set(jd_skills) - set(resume_skills))

            results.append({
                "Candidate Name": profile["name"],
                "File Name": resume_file.name,
                "ATS Score": ats_score,
                "Skill Match": skill_score,
                "Semantic Similarity": sem_score,
                "Experience Match": exp_score,
                "Matched Skills": matched_skills,
                "Missing Skills": missing_skills,
                "Candidate Profile": profile,
                "Qualified": ats_score >= threshold
            })

        df_results = pd.DataFrame(results).sort_values(by="ATS Score", ascending=False)

        tab1, tab2, tab3 = st.tabs(["🏆 Leaderboard", "🔍 Candidate Profile Breakdown", "📌 Job Requirements"])

        # ---- Tab 1: Leaderboard ----
        with tab1:
            top_candidate = df_results.iloc[0]
            col1, col2, col3 = st.columns(3)
            col1.metric("Evaluated Resumes", len(df_results))
            col2.metric("Top Candidate", top_candidate["Candidate Name"])
            col3.metric("Highest ATS Score", f"{top_candidate['ATS Score']}%")

            st.subheader("Candidate Rankings")
            display_cols = ["Candidate Name", "File Name", "ATS Score", "Skill Match", "Semantic Similarity"]
            if mode != "Basic":
                display_cols.append("Experience Match")
            display_cols.append("Qualified")

            st.dataframe(
                df_results[display_cols],
                column_config={
                    "ATS Score": st.column_config.ProgressColumn(
                        "Overall ATS Score (%)", format="%.2f%%", min_value=0, max_value=100,
                    ),
                    "Qualified": st.column_config.CheckboxColumn("Qualified"),
                },
                use_container_width=True,
                hide_index=True
            )

        # ---- Tab 2: Candidate Profile Breakdown ----
        with tab2:
            for idx, row in df_results.iterrows():
                with st.expander(f"📄 {row['Candidate Name']} ({row['File Name']}) — {row['ATS Score']}% Score", expanded=(idx == 0)):
                    cols = st.columns(4 if mode != "Basic" else 3)
                    cols[0].metric("ATS Score", f"{row['ATS Score']}%")
                    cols[1].metric("🎯 Skill Score", f"{row['Skill Match']}%")
                    cols[2].metric("🧠 Semantic Score", f"{row['Semantic Similarity']}%")
                    if mode != "Basic":
                        cols[3].metric("💼 Exp Score", f"{row['Experience Match']}%")

                    if row["ATS Score"] >= threshold:
                        st.success("✅ Candidate meets minimum qualification score.")
                    else:
                        st.warning("⚠️ Candidate falls below qualification threshold.")

                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**Matched Required Skills:**")
                        if row["Matched Skills"]:
                            st.markdown("".join(f'<span class="skill-badge">{s}</span>' for s in row["Matched Skills"]), unsafe_allow_html=True)
                        else:
                            st.write("No direct skills matched.")

                        st.markdown("<br>**Missing Required Skills:**", unsafe_allow_html=True)
                        if row["Missing Skills"]:
                            st.markdown("".join(f'<span class="missing-badge">{s}</span>' for s in row["Missing Skills"]), unsafe_allow_html=True)
                        else:
                            st.write("None! All identified skills match.")

                    with c2:
                        st.markdown("**Structured Candidate Profile:**")
                        st.json(row["Candidate Profile"])

        # ---- Tab 3: Job Requirements ----
        with tab3:
            st.subheader("Parsed Job Requirements")
            st.write(f"**Required Experience Level:** {jd_exp} Year(s)")
            st.markdown("**Detected Required Skills:**")
            if jd_skills:
                st.markdown("".join(f'<span class="skill-badge">{s}</span>' for s in jd_skills), unsafe_allow_html=True)
            else:
                st.info("No matching skills detected in JD from database.")

    else:
        st.info("👈 Upload candidate resumes and a Job Description in the sidebar to run analysis.")


if __name__ == "__main__":
    main()