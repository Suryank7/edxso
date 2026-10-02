-- Scholarship Intelligence Crawler Database Schema (SQLite)

CREATE TABLE IF NOT EXISTS scholarships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scholarship_uuid TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    provider TEXT NOT NULL,
    source_type TEXT NOT NULL, -- Government, University, Corporate CSR, NGO/Trust, International, Aggregator
    official_url TEXT NOT NULL,
    application_url TEXT,
    amount TEXT,
    benefits_summary TEXT,
    eligibility_criteria TEXT,
    academic_requirements TEXT,
    education_level TEXT,
    income_criteria TEXT,
    age_criteria TEXT,
    gender_criteria TEXT,
    category_criteria TEXT,
    domicile TEXT,
    institution_requirements TEXT,
    opening_date TEXT,
    closing_date TEXT,
    documents_required TEXT,
    selection_process TEXT,
    renewal_terms TEXT,
    status TEXT NOT NULL DEFAULT 'REVIEW_REQUIRED', -- ACTIVE, EXPIRING_SOON, EXPIRED, REVIEW_REQUIRED, NO_LONGER_VERIFIABLE
    confidence_score REAL NOT NULL DEFAULT 0.0,
    is_verified INTEGER NOT NULL DEFAULT 0,
    last_verified_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scholarship_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scholarship_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    extracted_value TEXT NOT NULL,
    source_url TEXT NOT NULL,
    evidence_text TEXT NOT NULL,
    evidence_hash TEXT,
    extracted_at TEXT NOT NULL,
    FOREIGN KEY(scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS scholarship_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scholarship_id INTEGER NOT NULL,
    crawl_run_id TEXT NOT NULL,
    snapshot_data TEXT NOT NULL, -- JSON formatted snapshot of all fields
    captured_at TEXT NOT NULL,
    FOREIGN KEY(scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS change_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scholarship_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_type TEXT NOT NULL, -- DEADLINE_CHANGE, AMOUNT_CHANGE, ELIGIBILITY_CHANGE, APPLICATION_URL_CHANGE, STATUS_CHANGE
    detected_at TEXT NOT NULL,
    source_url TEXT NOT NULL,
    evidence_text TEXT,
    FOREIGN KEY(scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS verification_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scholarship_id INTEGER NOT NULL UNIQUE,
    source_authenticity_score REAL NOT NULL,
    evidence_coverage_score REAL NOT NULL,
    freshness_score REAL NOT NULL,
    consistency_score REAL NOT NULL,
    application_url_score REAL NOT NULL,
    final_confidence_score REAL NOT NULL,
    status TEXT NOT NULL,
    explanation_json TEXT NOT NULL, -- JSON detailed breakdown for UI "Why this score?"
    evaluated_at TEXT NOT NULL,
    FOREIGN KEY(scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crawl_runs (
    run_id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    sources_crawled INTEGER DEFAULT 0,
    scholarships_found INTEGER DEFAULT 0,
    status TEXT NOT NULL -- IN_PROGRESS, COMPLETED, FAILED
);

CREATE TABLE IF NOT EXISTS source_pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    domain TEXT NOT NULL,
    source_type TEXT NOT NULL,
    title TEXT,
    raw_html TEXT,
    crawled_at TEXT NOT NULL,
    http_status INTEGER DEFAULT 200
);
