# 🎯 VectorHire ATS

An AI-driven **Applicant Tracking System (ATS)** built with **Streamlit** and **Sentence Transformers**. It evaluates candidate resumes against a job description using semantic similarity, weighted skill matching, and experience-level scoring — then ranks candidates on an interactive dashboard.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Scoring Methodology](#-scoring-methodology)
- [Tech Stack](#-tech-stack)
- [Known Limitations](#-known-limitations)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧭 Overview

VectorHire ATS automates the first pass of resume screening by combining:

- **Semantic understanding** — transformer-based sentence embeddings, so matches aren't purely keyword-based.
- **Skill verification** — a configurable, weighted skills dictionary (`skills.json`).
- **Experience validation** — regex-based years-of-experience extraction from resume and JD text.

The result is a composite **ATS Score** per candidate, with a full breakdown of matched/missing skills and a structured candidate profile, rendered in a clean Streamlit dashboard.

---

## 📁 Project Structure

```
VectorHire_ATS/
├── .venv/                  # Virtual environment (managed by uv, not committed)
├── src/                    # Application source package
├── .gitignore              # Git ignore rules
├── .python-version         # Pinned Python version for the project
├── app.py                  # Main Streamlit application entry point
├── pyproject.toml          # Project metadata & dependency declarations
├── requirements.txt        # Pip-compatible dependency list
├── skills.json             # Skill dictionary with importance weights
├── uv.lock                 # Locked, reproducible dependency versions (uv)
└── README.md                # Project documentation (this file)
```

---

## ✅ Prerequisites

- Python version as pinned in [`.python-version`](.python-version)
- [uv](https://docs.astral.sh/uv/) (recommended) — a fast Python package/dependency manager
  *(pip works too, via `requirements.txt`)*

---

## ⚙️ Installation

### Option A — Using `uv` (recommended, matches `uv.lock`)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd VectorHire_ATS

# 2. Sync the environment from the lockfile
uv sync

# 3. Run the app
uv run streamlit run app.py
```

`uv sync` creates/updates `.venv/` and installs exact versions from `uv.lock`, ensuring a reproducible environment.

### Option B — Using `pip`

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd VectorHire_ATS

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

> ℹ️ On first run, `sentence-transformers` downloads the `all-MiniLM-L6-v2` embedding model (~80 MB). An internet connection is required for this one-time download; it is cached locally afterward.

---

## 🔧 Configuration

`skills.json` (project root) defines the skill vocabulary the app can detect, with an optional importance weight used in skill-match scoring:

```json
{
  "python": 3,
  "sql": 2,
  "machine learning": 3,
  "docker": 2,
  "communication": 1
}
```

- **Key** → skill name (matched case-insensitively).
- **Value** → weight (higher = more influence on the Skill Match score). Skills without an explicit weight default to `1`.

---

## ▶️ Usage

```bash
uv run streamlit run app.py
# or, if using pip:
streamlit run app.py
```

**Workflow:**

1. Upload a **Job Description** (PDF or DOCX) via the sidebar.
2. Upload one or more **candidate resumes** (PDF or DOCX).
3. Set the **qualification threshold** using the slider.
4. Review results across the tabs:
   - **🏆 Leaderboard** — ranked candidates with overall ATS scores
   - **🔍 Candidate Profile Breakdown** — per-candidate skill match, missing skills, and structured JSON profile
   - **📌 Job Requirements** — skills and experience level parsed from the uploaded JD

---

## 🧮 Scoring Methodology

Each resume is evaluated against the job description across three weighted dimensions:

| Component | Weight | Method |
|---|:---:|---|
| **Skill Match** | 45% | Weighted overlap of detected resume skills vs. JD-required skills, using `skills.json` weights |
| **Semantic Similarity** | 40% | Cosine similarity between sentence-transformer embeddings (`all-MiniLM-L6-v2`) of cleaned resume/JD text |
| **Experience Match** | 15% | Ratio of candidate's detected years of experience to the JD's required years (capped at 100%) |

```
ATS Score = (Skill Score × 0.45) + (Semantic Score × 0.40) + (Experience Score × 0.15)
```

A candidate is flagged **Qualified** once their ATS Score meets or exceeds the threshold configured in the sidebar.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | [Streamlit](https://streamlit.io/) |
| NLP Embeddings | [Sentence Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) |
| Similarity Scoring | [scikit-learn](https://scikit-learn.org/) (cosine similarity) |
| PDF Parsing | [pdfplumber](https://github.com/jsvine/pdfplumber) |
| DOCX Parsing | [docx2txt](https://github.com/ankushshah89/python-docx2txt) |
| Data Handling | [pandas](https://pandas.pydata.org/) |
| Dependency Management | [uv](https://docs.astral.sh/uv/) (`pyproject.toml` / `uv.lock`) |

---

## ⚠️ Known Limitations

- **Name extraction** relies on the first non-empty line of a resume — unreliable for resumes with headers, logos, or non-standard layouts.
- **Experience extraction** only matches simple patterns like `"5 years"` or `"3+ year"` — it does not parse date ranges (e.g., `"2019–2024"`).
- **Skill detection** is entirely dependent on `skills.json` — any skill not listed there will never be recognized.
- All processing runs **locally**; no resume or JD content is sent to external APIs.
- The AI model loads on first run and is cached afterward via `@st.cache_resource`, so the very first analysis may take longer.

---

## 🗺️ Roadmap

- [ ] Improve name extraction using a lightweight NER model
- [ ] Support date-range experience parsing (e.g., `"2019–2024"`)
- [ ] Add per-candidate PDF summary/report export
- [ ] Add authentication for multi-recruiter usage
- [ ] Containerize with Docker for one-command deployment
- [ ] Expand `src/` into a proper package (parsing, scoring, UI as separate modules)

---

## 🤝 Contributing

Contributions are welcome. To propose a change:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Install dependencies with `uv sync`
4. Commit your changes with clear, descriptive messages
5. Open a pull request describing the change and motivation

Please run the app locally and verify scoring output before submitting changes to extraction or scoring logic.

---

## 📄 License

This project is available under the **MIT License** — update this section with your organization's preferred license terms.

---

<p align="center">Built with ❤️ using Streamlit and Sentence Transformers</p>