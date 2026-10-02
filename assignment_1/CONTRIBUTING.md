# Contributing to EDXSO Influencer Outreach AI

Thank you for contributing to **EDXSO Influencer Outreach AI (InfluenceFlow AI)**.

## Monorepo Architecture
- `apps/web`: Next.js 15 Frontend Dashboard.
- `apps/api`: Node.js/Express API Gateway and duplicate outreach shield.
- `apps/ai-service`: Python FastAPI microservice for filtering, brand fit scoring, and grounded AI personalization.
- `packages/data`: Canonical 52+ seed influencer dataset.
- `docs/`: Comprehensive SDLC blueprints and technical specifications.

## Engineering Guidelines
1. **Zero Hallucination Rule**: Never add features that synthesize or invent fake creator information, fake emails, or fake follower statistics.
2. **Explainability**: Every filtering modification must include itemized, human-readable pass/fail reason strings.
3. **Guardrails**: All email generation must be bounded strictly to 60–90 words; Instagram DMs must be bounded to 15–30 words.
4. **Testing**: Run `python -m pytest apps/ai-service/tests` and `npm --prefix apps/api test` before submitting changes.
