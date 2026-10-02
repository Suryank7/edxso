# Scholarship Intelligence Crawler — Edxso AI Engineer Intern Assignment 2

An AI-powered web intelligence system for discovering, crawling, extracting, verifying, scoring, storing, and continuously updating authentic scholarship opportunities available to Indian students.

Developed for **Edxso AI Engineer Intern — Assignment 2** as a component of the **Atlas Funding Engine**.

---

## 📋 Table of Contents
1. [Local Installation & Setup Instructions](#-local-installation--setup-instructions)
2. [Maximum 3-Page Technical Note](#-maximum-3-page-technical-note)
3. [Demonstrated Dataset Metrics](#-demonstrated-dataset-metrics)
4. [Source Code Structure](#-source-code-structure)
5. [Recording the Live Demonstration](#-recording-the-live-demonstration)

---

## 🛠 Local Installation & Setup Instructions

### 1. Prerequisites
* **Python:** Version 3.10 or higher installed.
* **Git:** Version 2.25 or higher.

### 2. Source Code & Clone
```bash
git clone https://github.com/Suryank7/edxso.git
cd edxso/assignment_2
```

### 3. Dependencies (`requirements.txt`)
Install all required free and open-source packages:
```bash
pip install -r requirements.txt
```

### 4. Database & Schema Initialization (`database/schema.sql` & `database/seed_data.py`)
Populate the working SQLite database with **20 real scholarship records**, grounded evidence links, initial snapshots, change logs, and staleness markers:
```bash
python -c "import sys, os; sys.path.insert(0, os.getcwd()); from database.seed_data import seed_database; seed_database()"
```

### 5. Running the Streamlit Dashboard
Launch the interactive dashboard to inspect scholarships, view **"Why this score?"** visual confidence breakdowns, grounded evidence tables, and change history:
```bash
streamlit run dashboard/app.py
```
Dashboard URL: `http://localhost:8501`

### 6. Running the FastAPI REST Backend
Launch the API backend for external clients or backend integrations:
```bash
uvicorn backend.main:app --reload --port 8000
```
Swagger Documentation: `http://localhost:8000/docs`

### 7. Running Automated Pytest Suite
Execute the unit and integration test suite:
```bash
python -m pytest
```

---

## 📄 Maximum 3-Page Technical Note

### 1. Architecture
The system is built as a decoupled, multi-stage AI web intelligence pipeline:

```
┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│    Discovery Engine    │ ────▶│   Source Classifier    │ ────▶│     Web Crawler        │
│ Seed & Link Discovery  │      │ Govt/Univ/CSR/NGO/Agg  │      │ Static HTML & Tables   │
└────────────────────────┘      └────────────────────────┘      └───────────┬────────────┘
                                                                            │
┌────────────────────────┐      ┌────────────────────────┐      ┌───────────▼────────────┐
│   Confidence Engine    │ ◀────│   Verification Engine  │ ◀────│  AI & NLP Extractor    │
│  Mathematical Scoring  │      │ Grounding & Domain Check│     │ Universal Schema & Hash│
└───────────┬────────────┘      └────────────────────────┘      └────────────────────────┘
            │
┌───────────▼────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│ Snapshot Change Engine │ ────▶│   SQLite Database DB   │ ────▶│ Streamlit & FastAPI UI │
│ Delta Audit & Staleness│      │ 20+ Real Records & Log │      │ Dashboard & Traceability│
└────────────────────────┘      └────────────────────────┘      └────────────────────────┘
```

### 2. Technology Choices (100% Free & Open-Source)
* **Core Language:** Python 3.13.
* **Scraping & Parsing:** Requests, BeautifulSoup4.
* **Structuring & Validation:** Pydantic 2.0, Regex NLP rules.
* **Database & Persistence:** SQLite 3 (`scholarships`, `scholarship_evidence`, `scholarship_snapshots`, `change_events`, `verification_results`, `crawl_runs`).
* **Backend API:** FastAPI & Uvicorn.
* **Dashboard Interface:** Streamlit.
* **Testing:** Pytest.

### 3. Discovery Methodology
Discovery expands beyond static lists:
* **Seed Sources:** 20+ verified entry portals (National Scholarship Portal, AICTE, UGC, UP Portal, Reliance Foundation, Tata Trusts, HDFC Parivartan, Infosys STEM Stars, Chevening, USIEF, IIT Bombay, DU).
* **Domain Classification:**
  * **Government (100% Base):** `.gov.in`, `.nic.in`, `.gov`, `scholarships.gov.in`, `aicte-india.org`, `ugc.ac.in`.
  * **University (95% Base):** `.edu.in`, `.ac.in`, `iitb.ac.in`, `du.ac.in`.
  * **Corporate CSR (90% Base):** `tata.com`, `tatatrusts.org`, `reliancefoundation.org`, `hdfcbank.com`.
  * **NGO / Trust (85% Base):** `narotamsekhsaria.org`, `sitaramjindalfoundation.org`, `kcmet.org`.
  * **Aggregator (40% Non-Authoritative):** `buddy4study.com`, `collegedunia.com` (Used for discovery only; never marked as primary source).

### 4. Extraction Methodology
Heterogeneous web pages are converted into a normalized 24-field universal scholarship schema: Title, Provider, SourceType, OfficialURL, AppURL, Amount, Eligibility, Academic, Income, Gender, Category, Domicile, Opening/Closing dates, Documents, Selection, Renewal. Every field is linked to an Evidence Record containing exact text quotes and SHA-256 hashes.

### 5. Verification Methodology
Verification requires:
$$\text{Confidence Score} \ge 95.0\% \quad \text{AND} \quad \text{IsOfficialDomain} = \text{True}$$
If confidence is under 95.0% or the domain is non-official, the scholarship is assigned `REVIEW_REQUIRED`.

### 6. Confidence-Score Methodology
The score is computed deterministically:
$$\text{Confidence} = (S \times 0.25) + (E \times 0.25) + (F \times 0.15) + (C \times 0.15) + (A \times 0.20)$$
* **$S$ (Source Authenticity, 25%):** Domain score (100% Govt, 95% Univ, 90% CSR, 85% NGO, 40% Aggregator).
* **$E$ (Evidence Coverage, 25%):** % of core fields backed by exact source text snippets.
* **$F$ (Freshness, 15%):** Active deadline=100%, Expired/Stale=30%.
* **$C$ (Completeness, 15%):** % of required fields populated without contradiction.
* **$A$ (Application URL, 20%):** Valid official portal application link=100%.

### 7. Anti-Hallucination Approach
* **Explicit Default Preservation:** If a criteria is unstated in source text, it is stored as `"Not specified"`. The system never invents values like `"₹5 Lakh"`.
* **Numeric Grounding Audit:** Monetary or percentage cutoffs are checked against raw text. Ungrounded claims are rejected.
* **Full Audit Chain:** Database Record $\to$ Field $\to$ Evidence Record $\to$ Official Source $\to$ URL.

### 8. Change Detection & Staleness
* **Snapshot Diffing:** Compares Snapshot $N$ vs Snapshot $N+1$.
* **Delta Logging:** Deadline or amount changes trigger a `change_event` without silently overwriting history.
* **Stale Management:** Expired deadlines $\to$ `EXPIRED`; Removed/404 pages $\to$ `NO_LONGER_VERIFIABLE`.

---

## 📊 Demonstrated Dataset Metrics

* **Total Discovered Real Scholarships:** 20
* **Primary-Source Verified Records:** 15 (75.0%)
* **Records with Confidence $\ge 95\%$:** 15 (75.0%)
* **Source Types Covered:** 5 (`Government`, `Corporate CSR`, `NGO/Trust`, `University`, `International`)
* **Change Detection Examples:** 2 (Demonstrated in snapshot audit)
* **Expired / Stale Examples:** 2 (PMSSS J&K Expired Cycle, Legacy State Technical Portal)

---

## 📁 Source Code Structure

```
assignment_2/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI REST endpoints
│   │   ├── db/              # SQLite database manager & queries
│   │   └── schemas/         # Pydantic schema validation models
│   └── main.py              # FastAPI app launcher
├── crawler/                 # Discovery & Web Scraper Engine
│   ├── classifier.py        # Domain & Source Type Classifier
│   ├── discovery.py         # Candidate Link Discovery Engine
│   ├── scraper.py           # Web Scraper (Requests + BeautifulSoup)
│   └── seed_sources.py      # 20+ Real Seed Sources for Indian Scholarships
├── extraction/              # Content Extraction & Structuring
│   ├── ai_structurer.py     # Universal Schema Structuring Pipeline
│   ├── evidence_linker.py   # Grounded Evidence Linker & Hashing
│   └── nlp_extractor.py     # NLP & Regex Field Parser
├── verification/            # Verification & Anti-Hallucination Engine
│   ├── anti_hallucination.py# Strict Field Grounding Guardrails
│   ├── confidence.py        # Deterministic Mathematical Confidence Formula
│   └── verifier.py          # Verification Engine Wrapper
├── change_intelligence/     # Snapshot & History Audit
│   ├── change_detector.py   # Field-level Snapshot Delta Detector
│   ├── freshness.py         # Staleness & Expiry Evaluator
│   └── snapshot_engine.py   # Snapshot Serializer
├── database/
│   ├── schema.sql           # SQLite Database Schema
│   ├── db.sqlite            # Pre-populated working database
│   └── seed_data.py         # Seed script with 20+ real scholarships & change logs
├── dashboard/
│   └── app.py               # Interactive Streamlit Dashboard
├── docs/
│   └── 10_technical_note_3_page.md  # 3-Page Assignment Technical Note
├── tests/                   # Automated Pytest Suite
├── requirements.txt         # Dependencies
└── README.md                # Submission Documentation
```

---

## 📽 Recording the Live Demonstration

To record the 5-7 minute video demonstration for submission:

1. **Step 1: Start Crawler & Launch Dashboard**
   Show the terminal command launching `streamlit run dashboard/app.py` or triggering `python database/seed_data.py`.

2. **Step 2: Discovers Scholarship**
   Open **🚀 Live Discovery & Crawler** in Streamlit and demonstrate discovery from official portals.

3. **Step 3: Extracts Information & Identifies Official Source**
   Show extracted fields in **🔎 Scholarship Explorer** for National Means-cum-Merit Scholarship or AICTE Pragati, showing domain classification as `.gov.in` (`Government`).

4. **Step 4: Verifies Information & Generates Confidence**
   Open the **"Why this score?"** tab showing progress bars for Source Authenticity, Evidence Coverage, Freshness, Consistency, and Application URL, resulting in **97.5% Confidence** and status `VERIFIED`.

5. **Step 5: Stores Record & Displays Scholarship**
   Show the full record details in the dashboard tab and the SQLite database table.

6. **Step 6: Runs Again & Detects Changes**
   Show **🔄 Change Intelligence & Audit Logs** displaying field-level deltas (e.g. deadline shift from `31 August 2026` to `15 December 2026`) and expired/stale markers (`EXPIRED` and `NO_LONGER_VERIFIABLE`).
