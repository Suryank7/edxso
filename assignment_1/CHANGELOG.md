# Changelog

All notable changes to **EDXSO Influencer Outreach AI** are documented here.

## [1.0.0] - 2026-10-01
### Added
- Complete end-to-end working system architecture (Next.js 15 UI, Express Gateway, Python FastAPI AI microservice).
- Ingestion dataset of 52 verified micro-influencer profiles across Tech, AI, Productivity, and test categories.
- Configurable filtering engine with itemized, explainable PASS/FAIL output.
- Transparent 6-factor Brand-Fit scoring engine ($0 - 100$) exposing sub-score breakdowns.
- Grounded AI personalization engine generating 60–90 word emails and 15–30 word Instagram DMs.
- Strict anti-hallucination and word-count guardrails.
- Human-in-the-loop review studio with inline copy editing and status management.
- Duplicate outreach prevention shield enforcing compound key `campaign_id + creator_id + channel`.
- Outreach dispatcher with safe `DRY_RUN` simulation mode and SMTP capability.
- Real-time campaign analytics dashboard with funnel visualization and brand-fit distribution.
- Complete 13-document SDLC and technical documentation suite in `docs/`.
