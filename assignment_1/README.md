# EDXSO Influencer Outreach AI (InfluenceFlow AI)
### Production-Grade Automated Micro-Influencer Discovery, Qualification & Personalized Outreach System

[![CI Tests](https://img.shields.io/badge/Tests-15%20Passed-brightgreen)](file:///d:/E/EDXSO/tests)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue)](file:///d:/E/EDXSO/apps/ai-service)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](file:///d:/E/EDXSO/apps/web)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)](file:///d:/E/EDXSO/apps/ai-service)
[![License](https://img.shields.io/badge/License-MIT-purple)](file:///d:/E/EDXSO/LICENSE)

---

## 📌 Executive Summary

**EDXSO Influencer Outreach AI** is an end-to-end, AI-powered influencer discovery and outreach platform designed for brands, startups, and marketing agencies. It replaces slow, error-prone manual spreadsheets with an automated, highly reliable pipeline:

$$\mathbf{Discover} \longrightarrow \mathbf{Normalize} \longrightarrow \mathbf{Filter} \longrightarrow \mathbf{Enrich} \longrightarrow \mathbf{Evaluate\ Fit} \longrightarrow \mathbf{AI\ Personalize} \longrightarrow \mathbf{HITL\ Review} \longrightarrow \mathbf{Dispatch} \longrightarrow \mathbf{Track}$$

Built specifically for the **EDXSO AI Engineer Intern Assignment 1**, this system demonstrates enterprise-grade software architecture, transparent rule-based filtering with human-readable explanations, multi-factor brand-fit scoring, hallucination-free LLM personalization, human-in-the-loop governance, composite duplicate outreach prevention, and comprehensive analytics.

---

## 🏛️ System Architecture

```mermaid
graph TD
    Client[Next.js 15 App Router Dashboard<br/>:3000] -->|REST / JSON| Gateway[Express API Gateway & Orchestrator<br/>:5000]

    Gateway --> Store[(Persistent Store<br/>campaigns & outreach logs)]
    Gateway --> Shield[Duplicate Prevention Shield<br/>campaign_id + creator_id + channel]
    Shield --> Dispatcher[Outreach Dispatcher<br/>Dry-Run Simulation / SMTP]

    Gateway -->|Internal Async RPC| AI[Python FastAPI AI Microservice<br/>:8000]

    AI --> SeedData[(52 Ingested Micro-Influencer Profiles)]
    AI --> Filter[Configurable Filtering Engine<br/>Follower, Engagement, Niche, Content]
    AI --> BrandFit[Transparent Brand-Fit Engine<br/>6-Factor Weighted Scoring 0-100]
    AI --> Personalizer[Grounded LLM Personalizer<br/>Email: 60-90w | DM: 15-30w]
    Personalizer --> Guardrails[Anti-Hallucination & Word Count Guardrails]

    Personalizer -.->|Optional Live Keys| LLMProvider[Google Gemini / OpenAI]
```

---

## ✨ Key System Capabilities

| Capability | Engineering Implementation | Value to Brand |
| :--- | :--- | :--- |
| **50+ Real Creator Ingestion** | Ingests 52 verified micro-influencer profiles across Technology, AI, Productivity, and test categories. | Immediate out-of-the-box demonstration of authentic creator data. |
| **Explainable Filtering** | Follower count ($5\text{k}-100\text{k}$), engagement ($\ge 3\%$), niche, platform, and content signal checks with itemized `✓`/`✗` reasons. | Transparent, objective pass/fail decisions without black-box guessing. |
| **Transparent Brand-Fit** | Multi-factor weighted score: Niche (30%), Audience (20%), Engagement (20%), Content (15%), Geography (10%), Contact (5%). | Quantifies alignment ($0-100$) and exposes component sub-scores. |
| **Deep Profile Enrichment** | Contact email, confidence rating, bio website, audience age/gender/geography, and recent post titles. | Non-public emails marked explicitly as `"Not Found"`; zero fake emails. |
| **AI Personalization** | Synthesizes **60–90 word emails** and **15–30 word Instagram DMs** grounded strictly in real recent posts. | High-converting collaboration pitches with zero fabrication. |
| **Safety Guardrails** | Validates word counts, enforces post title citations, and verifies non-deception before storage. | Protects brand reputation from robotic or hallucinatory emails. |
| **Human-in-the-Loop** | Dedicated Review Studio allowing inline copy edits, approval, rejection, or skipping. | Gives marketers complete control before any outreach is dispatched. |
| **Duplicate Shield** | Enforces composite uniqueness: `campaign_id + creator_id + channel`. | Completely eliminates embarrassing duplicate emails to the same creator. |
| **Dry-Run Simulation** | Configurable `DRY_RUN=true` mode simulates outreach, logs payloads, and sets status to `SIMULATED`. | Safe development, testing, and demonstration without burning domains. |
| **Campaign Analytics** | Real-time funnel metrics, brand-fit distribution, engagement benchmarks, and audit logs. | Complete visibility into campaign ROI and outreach health. |

---

## 🛠️ Technology Stack

- **Frontend**: Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, Lucide Icons, Glassmorphism Dark UI.
- **API Gateway & Orchestration**: Node.js, Express.js, Nodemailer, UUID, CORS, File-backed JSON/SQLite store.
- **AI & Processing Microservice**: Python 3.11–3.13, FastAPI, Pydantic v2, Uvicorn, PyTest, HTTPX.
- **AI Models & Grounding**: Google Gemini 1.5 Flash / OpenAI GPT-4o with deterministic Grounded Synthesizer fallback.
- **Infrastructure & Testing**: Docker, Docker Compose, PyTest, Node Test Runner.

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Node.js v20+ / npm v10+
- Python 3.11+
- Git

### 2. Installation
```bash
# Clone the repository
git clone <repo-url>
cd EDXSO

# Copy environment template
cp .env.example .env

# Install Python AI Service dependencies
cd apps/ai-service
pip install -r requirements.txt
cd ../..

# Install API Gateway dependencies
cd apps/api
npm install
cd ../..

# Install Web Frontend dependencies
cd apps/web
npm install
cd ../..
```

### 3. Running All Services Concurrently
```bash
# Terminal 1: Python AI Service (Port 8000)
cd apps/ai-service
python main.py

# Terminal 2: Node.js API Gateway (Port 5000)
cd apps/api
npm run dev

# Terminal 3: Next.js Frontend (Port 3000)
cd apps/web
npm run dev
```

Visit **`http://localhost:3000`** in your browser.

---

## 🧪 Automated Test Suite

The repository includes comprehensive automated tests covering unit logic, brand-fit formulas, AI guardrails, duplicate prevention, and REST endpoints:

```bash
# Run Python AI Microservice Tests (FastAPI, Filtering, Brand Fit, Guardrails)
python -m pytest apps/ai-service/tests

# Run API Gateway & Orchestration Tests (Store, Duplicate Shield, Analytics)
npm --prefix apps/api test
```

---

## 📚 Complete SDLC Documentation Suite

Explore the comprehensive engineering documentation generated in [`docs/`](file:///d:/E/EDXSO/docs):

1. [**01_VISION_DOCUMENT.md**](file:///d:/E/EDXSO/docs/01_VISION_DOCUMENT.md): Executive summary, market problem, target customers, 3-year vision.
2. [**02_PROJECT_CHARTER.md**](file:///d:/E/EDXSO/docs/02_PROJECT_CHARTER.md): Scope boundaries, RACI matrix, governance, milestone plan.
3. [**03_BRD.md**](file:///d:/E/EDXSO/docs/03_BRD.md): Business requirements, operational drivers, measurable outcomes.
4. [**04_FRD.md**](file:///d:/E/EDXSO/docs/04_FRD.md): Detailed functional specifications and system behavior.
5. [**05_SRS.md**](file:///d:/E/EDXSO/docs/05_SRS.md): IEEE-style Software Requirements Specification.
6. [**06_ARCHITECTURE_HLD_LLD.md**](file:///d:/E/EDXSO/docs/06_ARCHITECTURE_HLD_LLD.md): High-level & low-level design, class & sequence diagrams.
7. [**07_API_SPECIFICATION.md**](file:///d:/E/EDXSO/docs/07_API_SPECIFICATION.md): OpenAPI 3.0 schemas, endpoints, request/response models.
8. [**08_AI_PROMPT_GUARDRAILS.md**](file:///d:/E/EDXSO/docs/08_AI_PROMPT_GUARDRAILS.md): Prompt engineering, word-count bounds, anti-hallucination.
9. [**09_TEST_PLAN_AND_CASES.md**](file:///d:/E/EDXSO/docs/09_TEST_PLAN_AND_CASES.md): Master test plan, 16 test cases, evaluation matrix.
10. [**10_DEPLOYMENT_AND_SETUP.md**](file:///d:/E/EDXSO/docs/10_DEPLOYMENT_AND_SETUP.md): Bare metal runbook, Docker Compose, operational guides.

---

## ⚖️ License
MIT License. Built for **EDXSO AI Engineer Intern Assignment 1**.
