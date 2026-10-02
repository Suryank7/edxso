# Live Demonstration Script (5-7 Minutes)

**Project:** Scholarship Intelligence Crawler — Edxso Assignment 2  

---

### Step 1: Launch Application & Verify Database (0:00 - 1:00)
1. Open terminal and run database verification check:
   ```bash
   python -c "import sys, os; sys.path.insert(0, os.getcwd()); from backend.app.db.database import execute_query; print('Total:', execute_query('SELECT count(*) as c FROM scholarships')[0]['c']); print('Verified:', execute_query('SELECT count(*) as c FROM scholarships WHERE is_verified=1')[0]['c'])"
   ```
2. Demonstrate output showing **20 Real Scholarships**, **15 Verified (75%)**, **15 with Confidence $\ge 95\%$**, **5 Source Types**, **2 Change Events**, **2 Expired Examples**.

### Step 2: Open Streamlit Dashboard (1:00 - 3:00)
1. Launch Streamlit: `streamlit run dashboard/app.py`.
2. Show top KPI metrics: Total Discovered (20), Verified (15), Review Required (3), Active (16), Expired/Stale (2), Avg Confidence (95.1%).
3. Show Source Type Distribution chart covering Government, Corporate CSR, NGO/Trust, International, and University.

### Step 3: Inspect "Why this score?" Confidence Breakdown & Source Evidence (3:00 - 5:00)
1. Select **National Means-cum-Merit Scholarship Scheme (NMMSS)**.
2. Open **"Why this score?"** tab. Point out the 5 progress bars:
   * Source Authenticity: 100% (Official `.gov.in` domain)
   * Evidence Coverage: 100%
   * Freshness: 100%
   * Consistency: 100%
   * Application Link: 100%
   * **Final Score:** 97.5% ➔ Status: `VERIFIED`.
3. Open **Source Evidence Traceability** tab. Show the table mapping Database Field ➔ Extracted Value ➔ Evidence Quote ➔ SHA-256 Hash ➔ Official Source URL.

### Step 4: Demonstrate Change Intelligence & Stale Detection (5:00 - 6:30)
1. Navigate to **Change Intelligence & Audit Logs** section.
2. Show field delta logs for scholarships where closing dates were updated in Run #2. Point out `Old Value` vs `New Value` and `Detected Timestamp`.
3. Show Expired & Stale examples:
   * **PMSSS J&K 2025 (Expired Cycle):** Closing date past today ➔ Marked `EXPIRED`.
   * **Legacy State Technical Portal:** 404 page response ➔ Marked `NO_LONGER_VERIFIABLE`.

### Step 5: Test Live Candidate Discovery (6:30 - 7:00)
1. Navigate to **Live Discovery & Crawler** tab.
2. Test Domain Classifier with `https://scholarships.gov.in`. Point out domain classification response showing `Government`, `is_official: True`, `authenticity_score: 100.0`.
