# Scholarship Intelligence Crawler — Technical Note

**Author:** AI Engineer Intern Candidate  
**Project:** Edxso AI Engineer Intern — Assignment 2  
**System:** Scholarship Intelligence Crawler (Atlas Funding Engine Component)  

---

## 1. Architecture

The Scholarship Intelligence Crawler is designed as a decoupled, multi-stage AI web intelligence pipeline. Unlike brittle, single-site scrapers or static mock dashboards, this system continuously discovers, crawls, classifies, structures, verifies, score-evaluates, stores, and audits real scholarship opportunities for Indian students.

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

---

## 2. Technology Choices (100% Free & Open Source Stack)

* **Language & Core:** Python 3.13 (Native typing, high performance).
* **Crawling & Scraping:** `Requests`, `BeautifulSoup4`, and custom header-rotators.
* **Extraction & Structuring:** Regex NLP patterns combined with structured Pydantic schema validation.
* **Database & Persistence:** `SQLite 3` with full relational schema (`scholarships`, `scholarship_evidence`, `scholarship_snapshots`, `change_events`, `verification_results`, `crawl_runs`).
* **Backend API:** `FastAPI` + `Uvicorn` for REST endpoints (`/api/scholarships`, `/api/analytics`, `/api/crawl/run`).
* **Interactive Dashboard:** `Streamlit` with custom CSS components for visual score breakdowns and evidence audits.
* **Testing:** `Pytest` automated test suite.

---

## 3. Discovery Methodology

Discovery operates beyond hard-coded URL scrapers:
1. **Seed Ingestion:** Initiates from 20+ verified seed portals (National Scholarship Portal, AICTE, UGC, UP State Portal, Reliance Foundation, Tata Trusts, HDFC Parivartan, Infosys STEM Stars, Chevening, USIEF, IIT Bombay, DU).
2. **Internal Link & Anchor Parsing:** Crawls candidate anchor links (`<a>` tags) matching keywords (`scholarship`, `yojana`, `stipend`, `fellowship`, `grant`).
3. **Domain Classification:** Deterministically classifies domain suffix and host structure:
   * **Government (100% Base):** `.gov.in`, `.nic.in`, `.gov`, `scholarships.gov.in`, `aicte-india.org`, `ugc.ac.in`.
   * **University (95% Base):** `.edu.in`, `.ac.in`, `iitb.ac.in`, `du.ac.in`.
   * **Corporate CSR (90% Base):** `tata.com`, `tatatrusts.org`, `reliancefoundation.org`, `hdfcbank.com`.
   * **NGO / Trust (85% Base):** `narotamsekhsaria.org`, `sitaramjindalfoundation.org`, `kcmet.org`.
   * **Aggregator (40% Non-Authoritative):** `buddy4study.com`, `collegedunia.com`, `shiksha.com` (Used for discovery only; never marked as primary source).

---

## 4. Extraction Methodology

Raw HTML page text and structured tables are parsed into a normalized 24-field universal scholarship schema:

$$\text{Scholarship Record} = \{ \text{Title}, \text{Provider}, \text{SourceType}, \text{OfficialURL}, \text{AppURL}, \text{Amount}, \text{Eligibility}, \text{Academic}, \text{Income}, \text{Gender}, \text{Category}, \text{ClosingDate}, \text{Documents}, \dots \}$$

Every extracted field is bound to an **Evidence Record**:
$$\text{Evidence} = \{ \text{Field}, \text{ExtractedValue}, \text{SourceURL}, \text{EvidenceSnippet}, \text{SHA256Hash} \}$$

---

## 5. Verification Methodology

Verification is evidence-grounded and objective. A scholarship is only marked `VERIFIED` if:
$$\text{Confidence Score} \ge 95.0\% \quad \text{AND} \quad \text{IsOfficialDomain} = \text{True}$$
Otherwise, the record is flagged as `REVIEW_REQUIRED`.

---

## 6. Confidence-Score Methodology

The confidence score is computed via a transparent mathematical formula rather than arbitrary LLM output:

$$\text{Confidence} = (S \times 0.25) + (E \times 0.25) + (F \times 0.15) + (C \times 0.15) + (A \times 0.20)$$

* **$S$ (Source Authenticity, 25%):** Govt=100%, Univ=95%, CSR=90%, NGO=85%, Aggregator=40%.
* **$E$ (Evidence Coverage, 25%):** Percentage of core fields grounded by exact source text snippets.
* **$F$ (Freshness, 15%):** Active future deadline=100%, Expiring soon=80%, Expired/Stale=30%.
* **$C$ (Consistency & Completeness, 15%):** Percentage of required fields populated without internal contradiction.
* **$A$ (Official Application Link, 20%):** Valid official portal link=100%, missing/third-party redirect=20-60%.

---

## 7. Anti-Hallucination Architecture

To prevent fabricated claims:
1. **Explicit Default Preservation:** If the source document does not specify an income limit or age restriction, the field is explicitly stored as `"Not specified"`. The system never infers values like `"₹5 Lakh"`.
2. **Numeric Grounding Audit:** Field values containing monetary amounts or percentage cutoffs are audited against raw source text. If numbers are absent in source text, the claim is rejected.
3. **Traceability Chain:** Every database field links to an evidence hash and exact source snippet: `Database -> Field -> Evidence Record -> Official Source -> URL`.

---

## 8. Change Detection

The system maintains continuous record history across repeated crawl runs:
1. **Snapshot Capturing:** On Crawl Run $N$, a complete JSON snapshot of all scholarship attributes is serialized.
2. **Field-Level Diffing:** On Crawl Run $N+1$, Snapshot $N$ is compared field-by-field against fresh extracted data.
3. **Delta Logging:** Modified deadlines, revised amounts, or updated application links trigger a `change_event` without silently overwriting historical records.

---

## 9. Stale / Expired Detection

Scholarship freshness is continuously monitored:
* **Passed Deadlines:** Automatically assigned status `EXPIRED` when closing date precedes current date.
* **Expiring Soon:** Assigned status `EXPIRING_SOON` when closing date is within 15 days.
* **Removed / 404 Pages:** Assigned status `NO_LONGER_VERIFIABLE` when official source web page returns HTTP 404/410.

---

## 10. Demonstrated Dataset & Limitations

### Demonstrated Dataset Metrics
* **Total Discovered Real Scholarships:** 20
* **Primary-Source Verified Records:** 15 (75.0%)
* **Records with Confidence $\ge 95\%$:** 15 (75.0%)
* **Source Types Covered:** 5 (Government, Corporate CSR, NGO/Trust, University, International)
* **Change Detection Examples Demonstrated:** 2
* **Expired / Stale Examples Demonstrated:** 2

### Current Limitations & Future Scope
* **CAPTCHA / Advanced JS:** Static scraper relies on HTML/DOM text; dynamic JS rendering is handled via Playwright fallback.
* **PDF Extraction:** PDF notifications are converted via text extraction rules; OCR for scanned images can be integrated in production.
