# VectorHire ATS

### AI-Powered Resume Analyzer & Candidate Profiler

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

**VectorHire ATS** is an AI-driven Applicant Tracking System built with **Python, Streamlit, Sentence Transformers, and scikit-learn**.

It analyzes candidate resumes against a Job Description (JD) using a combination of **weighted skill matching, semantic similarity, and experience-level analysis**. The results are presented through an interactive dashboard with candidate profiles, skill analysis, qualification status, and ATS scoring.

> **From Resume → NLP Processing → Semantic Matching → Skill Analysis → ATS Score → Candidate Profile**

---

## Key Features

* 📄 **PDF & DOCX Resume Parsing**
* 📝 **Job Description Processing**
* 🧠 **Semantic Resume–JD Matching**
* 🎯 **Weighted Skill Matching**
* 💼 **Experience-Level Analysis**
* 👤 **Structured Candidate Profiling**
* 📊 **Composite ATS Scoring**
* 🏆 **Candidate Leaderboard**
* 🔍 **Candidate-Level Breakdown**
* 📌 **Job Requirement Analysis**
* ⚙️ **Configurable Skill Weights**
* 🔐 **Local Processing**
* ⚡ **Cached Embedding Model**
* 🐍 **Python + Streamlit Architecture**
* 📦 **uv-based Reproducible Environment**

---

# Overview

Traditional resume screening systems often depend heavily on exact keyword matching.

VectorHire ATS combines **rule-based skill extraction** with **semantic embeddings** to measure how closely a candidate's resume aligns with the requirements of a Job Description.

### Core Components

| Component           | Purpose                                            |
| ------------------- | -------------------------------------------------- |
| Resume Parser       | Extracts text from PDF/DOCX resumes                |
| JD Parser           | Extracts requirements from the Job Description     |
| Skill Extractor     | Detects configured skills using pattern matching   |
| Embedding Model     | Converts text into semantic vector representations |
| Similarity Engine   | Calculates resume–JD semantic similarity           |
| Experience Analyzer | Extracts and compares years of experience          |
| Scoring Engine      | Combines individual scores into an ATS score       |
| Streamlit Dashboard | Displays candidate analysis interactively          |

---

# How It Works

```text
                 ┌──────────────────────┐
                 │   Job Description    │
                 │      PDF / DOCX      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    JD Text Parser    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  JD Preprocessing    │
                 └──────────┬───────────┘
                            │
                            │
      ┌─────────────────────┴─────────────────────┐
      │                                           │
      ▼                                           ▼
┌───────────────┐                         ┌──────────────────┐
│ Skills        │                         │ Semantic         │
│ Extraction    │                         │ Embeddings       │
│               │                         │                  │
│ skills.json   │                         │ MiniLM           │
└───────┬───────┘                         └────────┬─────────┘
        │                                          │
        │                                          │
        │                ┌─────────────────────────┘
        │                │
        ▼                ▼
┌───────────────┐   ┌──────────────────┐
│ Weighted      │   │ Cosine           │
│ Skill Score   │   │ Similarity       │
└───────┬───────┘   └────────┬─────────┘
        │                    │
        └─────────┬──────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │ Experience Analysis │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │    ATS Score Engine │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Candidate Profile   │
        │ & Qualification     │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Streamlit Dashboard │
        └─────────────────────┘
```

---

# System Architecture

VectorHire follows a lightweight AI application architecture:

```text
┌──────────────────────────────────────────────────────┐
│                  Streamlit Frontend                  │
│                                                      │
│ Upload JD │ Upload Resumes │ Threshold │ Dashboard  │
└─────────────────────────┬────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────┐
│                Document Processing                   │
│                                                      │
│ PDF → pdfplumber        DOCX → docx2txt             │
└─────────────────────────┬────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────┐
│                 Text Processing                      │
│                                                      │
│ Cleaning │ Normalization │ Pattern Extraction       │
└───────────────┬─────────────────────┬────────────────┘
                │                     │
                ▼                     ▼
      ┌──────────────────┐   ┌────────────────────────┐
      │ Skill Extraction │   │ Sentence Transformers  │
      │   Regex + JSON   │   │   all-MiniLM-L6-v2     │
      └────────┬─────────┘   └───────────┬────────────┘
               │                         │
               ▼                         ▼
      ┌──────────────────┐     ┌──────────────────────┐
      │ Weighted Skill   │     │ Semantic Similarity  │
      │ Score            │     │ Cosine Similarity    │
      └────────┬─────────┘     └──────────┬───────────┘
               │                          │
               └────────────┬─────────────┘
                            ▼
                  ┌─────────────────────┐
                  │ Experience Matching │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    ATS Score        │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Candidate Dashboard │
                  └─────────────────────┘
```

---

# Project Structure

```text
VectorHire_ATS/
│
├── .venv/                  # Local virtual environment (not committed)
│
├── src/                    # Application source package
│
├── .gitignore              # Git ignore configuration
├── .python-version         # Project Python version
│
├── app.py                  # Main Streamlit application
│
├── pyproject.toml          # Project metadata & dependencies
├── requirements.txt        # Pip-compatible dependencies
│
├── skills.json             # Skill vocabulary & importance weights
│
├── uv.lock                 # Reproducible dependency lockfile
│
├── LICENSE                 # MIT License
└── README.md               # Project documentation
```

### Architecture Direction

The `src/` directory is intended to evolve into separate application modules:

```text
src/
├── parsing/
├── extraction/
├── scoring/
├── embeddings/
├── profiling/
└── ui/
```

This separation can improve maintainability as the application grows.

---

# Prerequisites

Before running VectorHire ATS, make sure you have:

* **Python** — version specified in `.python-version`
* **Git**
* **uv** — recommended
* Internet access for the initial embedding-model download

### Recommended Package Manager

[uv](https://docs.astral.sh/uv/) is recommended because the project includes:

```text
pyproject.toml
uv.lock
```

These files allow dependencies to be installed reproducibly.

`pip` is also supported through:

```text
requirements.txt
```

---

# Installation

## Option A — Using uv

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd VectorHire_ATS
```

### 2. Sync dependencies

```bash
uv sync
```

This creates/updates the project's `.venv` environment and installs the locked dependencies.

### 3. Run VectorHire ATS

```bash
uv run streamlit run app.py
```

---

## Option B — Using pip

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd VectorHire_ATS
```

### 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

---

## First Model Download

On the first execution, Sentence Transformers downloads:

```text
all-MiniLM-L6-v2
```

The model is approximately **80 MB** and is cached locally after the initial download.

Therefore:

```text
First Run
    │
    ├── Internet Required
    ├── Download Model
    └── Cache Locally
             │
             ▼
Future Runs
    │
    └── Load Cached Model
```

---

# Configuration

## `skills.json`

The `skills.json` file defines the skill vocabulary used by the application.

Example:

```json
{
  "python": 3,
  "sql": 2,
  "machine learning": 3,
  "deep learning": 3,
  "pandas": 2,
  "numpy": 2,
  "fastapi": 2,
  "docker": 2,
  "aws": 2,
  "communication": 1
}
```

### Weight System

| Weight | Meaning                    |
| -----: | -------------------------- |
|    `1` | Lower relative importance  |
|    `2` | Medium relative importance |
|    `3` | Higher relative importance |

The weights affect the **Skill Match** component of the ATS score.

### Matching Behavior

Skill names are matched case-insensitively.

For example:

```text
Python
python
PYTHON
```

are treated as the same configured skill.

---

# Usage

Start the application:

```bash
uv run streamlit run app.py
```

or:

```bash
streamlit run app.py
```

---

## Step 1 — Upload Job Description

Upload a Job Description in:

```text
PDF
DOCX
```

format through the Streamlit sidebar.

---

## Step 2 — Upload Candidate Resumes

Upload one or more candidate resumes.

Supported formats:

```text
PDF
DOCX
```

---

## Step 3 — Configure Qualification Threshold

Use the sidebar slider to define the minimum ATS score required for the application's qualification label.

---

## Step 4 — Run Analysis

VectorHire processes each candidate through the analysis pipeline:

```text
Resume
   ↓
Text Extraction
   ↓
Text Cleaning
   ↓
Skill Extraction
   ↓
Semantic Embedding
   ↓
Experience Extraction
   ↓
Score Calculation
   ↓
Candidate Profile
```

---

# Dashboard

The application provides three primary analysis areas.

## Leaderboard

Displays candidate-level results including:

* Candidate name
* ATS score
* Qualification status
* Ranking information

---

## Candidate Profile Breakdown

Provides detailed information for an individual candidate:

* Detected skills
* Matched skills
* Missing skills
* Experience
* Education
* Semantic score
* Skill score
* Experience score
* Structured candidate profile

---

## Job Requirements

Displays requirements extracted from the Job Description, including:

* Required skills
* Detected experience requirement
* Parsed job information

---

# Scoring Methodology

VectorHire ATS combines three scoring components.

| Component               |  Weight | Method                                           |
| ----------------------- | ------: | ------------------------------------------------ |
| **Skill Match**         | **45%** | Weighted overlap between resume and JD skills    |
| **Semantic Similarity** | **40%** | Cosine similarity between transformer embeddings |
| **Experience Match**    | **15%** | Candidate experience relative to JD requirement  |

### Final ATS Formula

```text
ATS Score =
    (Skill Score × 0.45)
  + (Semantic Score × 0.40)
  + (Experience Score × 0.15)
```

The resulting score represents the application's calculated alignment between the resume and the target Job Description.

---

## Skill Match

The application extracts configured skills from:

```text
Resume
   │
   ▼
Skill Dictionary
   │
   ▼
Detected Resume Skills
```

and compares them against the skills detected in the JD.

Weights from `skills.json` are used when calculating the skill component.

---

## Semantic Similarity

The application uses:

```text
Sentence Transformers
        │
        ▼
all-MiniLM-L6-v2
```

to generate embeddings.

Conceptually:

```text
Resume ─────────► Embedding Vector
                       │
                       │
                       ▼
                 Cosine Similarity
                       ▲
                       │
                       │
JD ───────────────► Embedding Vector
```

This allows the system to measure semantic alignment rather than relying exclusively on exact keyword matches.

---

## Experience Match

The current implementation extracts simple experience expressions such as:

```text
5 years
3+ years
2 year
```

The candidate's detected experience is compared against the experience requirement identified in the JD.

The resulting experience component is capped at the maximum score.

---

# Candidate Profiling

VectorHire can convert extracted resume information into a structured candidate profile.

Example:

```json
{
  "name": "Candidate Name",
  "experience": "3+ years",
  "education": "B.E. Computer Science",
  "skills": [
    "Python",
    "SQL",
    "Machine Learning",
    "FastAPI",
    "Docker"
  ]
}
```

This structured representation provides a foundation for future AI-powered recruitment workflows.

---

# Privacy & Data Processing

VectorHire ATS is designed for local processing.

```text
Resume / JD
     │
     ▼
Local Application
     │
     ├── PDF/DOCX Parsing
     ├── Text Processing
     ├── Skill Extraction
     ├── Embedding Generation
     └── Score Calculation
     │
     ▼
Local Dashboard
```

Resume and Job Description content is not intentionally sent to an external AI API by the core application.

> **Important:** Deployment environments should still be reviewed for logs, temporary files, hosting infrastructure, and dependency behavior before processing sensitive recruitment information.

---

# Known Limitations

### 1. Name Extraction

Name extraction currently relies on the first non-empty line of the resume.

This can be unreliable for documents containing:

* Logos
* Images
* Complex headers
* Tables
* Non-standard layouts

---

### 2. Experience Extraction

The current implementation primarily handles simple patterns such as:

```text
5 years
3+ years
2 year
```

It does not reliably parse date ranges such as:

```text
2019 – 2024
2020 – Present
Jan 2021 – Mar 2025
```

---

### 3. Skill Dictionary Dependency

Skill detection depends on the contents of:

```text
skills.json
```

If a skill is not included in the dictionary, the current rule-based extractor may not detect it.

---

### 4. PDF Extraction

Text extraction quality can vary depending on the structure of a PDF.

Image-only/scanned resumes may require OCR, which is not currently included in the core pipeline.

---

### 5. Semantic Similarity

Semantic similarity provides a text-alignment signal. It does not independently verify that a candidate actually possesses a claimed skill or that resume information is accurate.

---

### 6. Screening Assistance

ATS scores should be treated as **decision-support signals**, not as a standalone basis for employment decisions. Human review and appropriate recruitment processes remain important.

---

# Roadmap

## Resume Intelligence

* [ ] Advanced name extraction
* [ ] NER-based candidate information extraction
* [ ] Job-title extraction
* [ ] Company extraction
* [ ] Certification extraction
* [ ] Project extraction
* [ ] Improved education extraction
* [ ] Date-range experience parsing
* [ ] OCR support for scanned resumes

## Semantic Intelligence

* [ ] Advanced embedding models
* [ ] Skill synonym detection
* [ ] Semantic skill matching
* [ ] Domain-specific embeddings
* [ ] Vector database integration

## LLM & RAG

* [ ] LLM-powered candidate profiling
* [ ] Structured LLM outputs
* [ ] Resume summarization
* [ ] Skill-gap analysis
* [ ] RAG-based resume retrieval
* [ ] Resume/JD question answering

Potential technologies:

```text
FAISS
pgvector
Qdrant
Chroma
```

## Backend & Production

* [ ] FastAPI backend
* [ ] PostgreSQL database
* [ ] Authentication
* [ ] Role-based access control
* [ ] Docker
* [ ] CI/CD
* [ ] Cloud deployment
* [ ] Evaluation framework
* [ ] Observability
* [ ] MLOps / LLMOps

---

# Future AI Architecture

The current Streamlit application can evolve into a larger AI recruitment platform:

```text
                         ┌────────────────────┐
                         │      Frontend      │
                         │ Streamlit / React  │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │      FastAPI       │
                         │     Backend        │
                         └─────────┬──────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
          Resume Service      JD Service      Scoring Service
                 │                 │                 │
                 └─────────────────┼─────────────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │   NLP / AI Layer  │
                         ├────────────────────┤
                         │ Embeddings         │
                         │ NER                │
                         │ LLM                │
                         │ RAG                │
                         └─────────┬──────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
             ┌──────────────┐              ┌──────────────┐
             │ PostgreSQL   │              │ Vector DB    │
             │              │              │              │
             │ Candidate    │              │ Embeddings   │
             │ Profiles     │              │ Retrieval    │
             └──────────────┘              └──────────────┘
```

---

# Project Evolution

VectorHire is designed as an evolving AI Engineering project.

```text
Phase 1
Basic ATS
   │
   ▼
Regex Skill Matching
   │
   ▼
Phase 2
Candidate Profiling
   │
   ▼
Semantic Embeddings
   │
   ▼
Phase 3
Weighted ATS Scoring
   │
   ▼
Interactive Dashboard
   │
   ▼
Phase 4
LLM + RAG
   │
   ▼
Phase 5
FastAPI + PostgreSQL
   │
   ▼
Phase 6
Docker + Cloud
   │
   ▼
Phase 7
Evaluation + Observability
   │
   ▼
Production AI Platform
```

---

# Tech Stack

| Layer                  | Technology             | Purpose                             |
| ----------------------- | ---------------------- | ------------------------------------ |
| **Language**           | Python                  | Application development             |
| **Frontend/UI**        | Streamlit               | Interactive dashboard               |
| **NLP**                | Sentence Transformers   | Text embeddings                     |
| **Embedding Model**    | `all-MiniLM-L6-v2`      | Semantic representation             |
| **Similarity**         | scikit-learn            | Cosine similarity                   |
| **PDF Parsing**        | pdfplumber              | PDF text extraction                 |
| **DOCX Parsing**       | docx2txt                | Word document extraction            |
| **Data Processing**    | pandas                  | Data manipulation                   |
| **Pattern Matching**   | Python Regex            | Skill/experience extraction         |
| **Configuration**      | JSON                    | Skill vocabulary & weights          |
| **Dependency Manager** | uv                      | Environment & dependency management |

---

# Core Dependencies

```text
streamlit
sentence-transformers
scikit-learn
pdfplumber
docx2txt
pandas
```

Install through:

```bash
uv sync
```

or:

```bash
pip install -r requirements.txt
```

---

# Development

Run the application locally:

```bash
uv run streamlit run app.py
```

Before submitting changes, verify:

* Resume parsing
* JD parsing
* Skill extraction
* Semantic similarity
* Experience extraction
* ATS score calculation
* Qualification threshold
* Candidate dashboard

Changes to scoring or extraction logic should be tested with multiple resume/JD combinations.

---

# Contributing

Contributions are welcome.

### Contribution Workflow

```bash
git checkout -b feature/your-feature
```

Make your changes, test locally, then commit:

```bash
git add .
git commit -m "feat: improve resume skill extraction"
```

Push your branch:

```bash
git push origin feature/your-feature
```

Then open a Pull Request describing:

* What changed
* Why it changed
* How it was tested
* Any known limitations

---

# License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for complete license information.

---

# Author

## Raghul A

**Aspiring AI Engineer**

Focused on building practical AI applications using:

```text
Python
Machine Learning
Deep Learning
NLP
LLMs
RAG
AI Agents
FastAPI
Docker
Cloud
MLOps / LLMOps
```

### Connect

* **LinkedIn:** `www.linkedin.com/in/raghul-ai`
* **GitHub:** `github.com/raghul1822`

---

# Project Summary

VectorHire ATS demonstrates an end-to-end approach to building an AI-assisted resume analysis application.

```text
                 VECTORHIRE ATS

Resume + Job Description
            │
            ▼
     Document Parsing
            │
            ▼
      Text Processing
            │
      ┌─────┴─────┐
      ▼           ▼
    Skills     Embeddings
      │           │
      ▼           ▼
   Weighted    Semantic
   Matching    Similarity
      │           │
      └─────┬─────┘
            ▼
    Experience Analysis
            │
            ▼
       ATS Score
            │
            ▼
   Candidate Profile
            │
            ▼
   Interactive Dashboard
```


> **VectorHire ATS — Analyze resumes, understand candidate–job alignment, and turn unstructured documents into structured hiring signals.**


---


<p align="center">
  Built with ❤️ using Python, Streamlit & Sentence Transformers
</p>
