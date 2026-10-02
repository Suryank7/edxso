# Functional Requirements Document (FRD)

**Project:** Scholarship Intelligence Crawler  

---

| Requirement ID | Module | Description | Input | Expected Output | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-1** | Discovery Engine | Discover candidate scholarship URLs from seed entry points and web page links. | Seed URLs, Web pages | Classified Candidate URLs | High |
| **FR-2** | Source Classification | Classify candidate domain into Govt, Univ, Corporate CSR, NGO, or Aggregator. | Target URL | Domain Type & Authenticity Score | High |
| **FR-3** | Web Crawling | Fetch raw HTML, DOM elements, and structured tables with retry backoff. | Candidate URL | Raw HTML & Text Blocks | High |
| **FR-4** | Content Extraction | Parse unstructured text into 24 universal schema fields. | Clean Text | Structured Scholarship Record | High |
| **FR-5** | Evidence Extraction | Bind extracted fields to exact source text quotes and SHA-256 hashes. | Extracted Value, Source Text | Grounded Evidence Record | High |
| **FR-6** | Verification Engine | Evaluate primary domain authenticity and official source status. | Official URL, Domain Type | Verification Status | High |
| **FR-7** | Confidence Scoring | Compute weighted mathematical confidence score (0-100%). | Evidence, Recency, Completeness | Confidence Score % | High |
| **FR-8** | Change Detection | Compare snapshot N vs snapshot N+1 to detect field deltas. | Snapshots | Change Events Log | Medium |
| **FR-9** | Expiry Detection | Automatically flag expired deadlines and removed 404 pages. | Closing Date, HTTP Status | Lifecycle Status (`EXPIRED`, `NO_LONGER_VERIFIABLE`) | High |
| **FR-10**| Dashboard & Search | Filter, search, and visually inspect scholarships, evidence, and score breakdown. | User Filters | Visual Analytics & Detail View | High |
