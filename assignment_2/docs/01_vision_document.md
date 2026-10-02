# Vision Document — Scholarship Intelligence Crawler

**Project:** Scholarship Intelligence Crawler (Atlas Funding Engine)  
**Author:** AI Engineer Intern Candidate  

---

## 1. Executive Summary
The Scholarship Intelligence Crawler is an AI-powered web intelligence system designed to discover, crawl, extract, verify, score, store, and continuously update authentic scholarship opportunities for Indian students. It solves the critical problem of scholarship information fragmentation, aggregator inaccuracies, and stale deadlines by enforcing primary-source verification and evidence-backed confidence scoring.

## 2. Problem Definition
* **Fragmented Information:** Indian students face thousands of unverified scholarship listings scattered across government portals, corporate CSR websites, NGOs, and aggregators.
* **Outdated & Expired Deadlines:** Over 40% of aggregator listings contain expired deadlines or broken application links.
* **Aggregator Inaccuracies:** Aggregators often rewrite eligibility criteria or omit key income thresholds, leading to student disqualification.
* **Lack of Official Verification:** Generic AI scrapers often hallucinate criteria or assign arbitrary confidence scores without evidence backing.

## 3. Product Vision
To build an autonomous, trustworthy, self-updating intelligence repository where every single scholarship opportunity is verified against primary official sources, backed by grounded evidence snippets, and continuously monitored for changes over time.

## 4. Core Differentiators
1. **Primary-Source Verification:** Rejects aggregator dominance; anchors every scholarship to official government (.gov.in), university (.ac.in), or corporate CSR portals.
2. **Deterministic Confidence Engine:** Mathematical formula evaluating source authenticity, evidence coverage, recency, consistency, and application links.
3. **Anti-Hallucination Guardrails:** Explicit default preservation (`"Not specified"`) for missing fields and numeric claim auditing.
4. **Snapshot Change Intelligence:** Field-level delta detection over time without silent overwriting of historical records.
