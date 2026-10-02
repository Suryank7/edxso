# EDXSO Influencer Outreach AI (InfluenceFlow AI)
## Phase 7: Master Test Plan, Test Cases & Evaluation Matrix

---

### 1. Master Testing Strategy

The quality assurance strategy spans five validation tiers:
1. **Unit Tests (Python & Node.js)**: Validates filtering rules, brand-fit formulas, duplicate checks, word count bounds, and local store operations.
2. **AI Guardrail & Anti-Hallucination Tests**: Evaluates LLM responses for factual grounding, citation accuracy, and format adherence.
3. **Integration Tests**: Tests inter-service communication between Express API Gateway (:5000) and Python AI Engine (:8000).
4. **Outreach & Duplicate Prevention Tests**: Simulates concurrent and repeated outreach requests to prove duplicate prevention.
5. **End-to-End User Journey Tests**: Verifies complete user workflows in the Next.js frontend using browser automation.

---

### 2. Comprehensive Test Case Matrix

| Test Case ID | Category | Description | Input Conditions | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-FLT-01** | Filtering | Qualified Micro-Influencer | 42,500 followers, 5.8% eng, Tech niche | Status: PASS, 5/5 criteria passed | **PASSED** |
| **TC-FLT-02** | Filtering | Below Engagement Benchmark | 55,000 followers, 1.8% eng (< 3.0%) | Status: FAIL, reason explains low engagement | **PASSED** |
| **TC-FLT-03** | Filtering | Wrong Campaign Niche | 48,000 followers, Fashion & Beauty niche | Status: FAIL, reason explains niche mismatch | **PASSED** |
| **TC-FLT-04** | Filtering | Follower Count Below Range | 3,200 followers (Nano influencer) | Status: FAIL, reason indicates below 5k | **PASSED** |
| **TC-FLT-05** | Filtering | Follower Count Above Ceiling | 320,000 followers (Macro influencer) | Status: FAIL, reason indicates above 100k | **PASSED** |
| **TC-FIT-01** | Brand Fit | High Synergy Calculation | Direct AI niche, high engagement, verified email | Composite score $\ge 85.0$, breakdown transparent | **PASSED** |
| **TC-FIT-02** | Brand Fit | Unverified Email Degradation | Contact availability is "Not Found" | Contact sub-score drops to 35, composite penalized | **PASSED** |
| **TC-AI-01** | AI Guardrails | Email Word Count Compliance | Qualified creator context | Word count is strictly $60 \le W \le 90$ | **PASSED** |
| **TC-AI-02** | AI Guardrails | Instagram DM Word Count Compliance | Qualified creator context | Word count is strictly $15 \le W \le 30$ | **PASSED** |
| **TC-AI-03** | AI Guardrails | Post Citation Grounding | `recent_content` containing real post title | Exact title or recognized subset cited in copy | **PASSED** |
| **TC-HITL-01**| HITL Review | Status Transition to Approved | Partnerships manager clicks "Approve" | Status transitions to "Human Approved" | **PASSED** |
| **TC-HITL-02**| HITL Review | Inline Copy Customization | User edits email body in UI modal | Copy updated, status transitions to "Edited" | **PASSED** |
| **TC-OUT-01** | Outreach | Dry-Run Email Dispatch | `DRY_RUN=true`, valid recipient email | Status: SIMULATED, delivery logged in store | **PASSED** |
| **TC-OUT-02** | Outreach | Missing Email Graceful Failure | Recipient email is "Not Found" | Dispatch aborted with clear validation error | **PASSED** |
| **TC-DUP-01** | Duplicate Shield| Repeat Send Interception | Send outreach to already-contacted creator | Blocked: `duplicate_prevented: true` | **PASSED** |
| **TC-ANL-01** | Analytics | Dynamic Funnel Aggregation | 52 creators, 36 qualified, 12 simulated | Funnel counts match exact database states | **PASSED** |

---

### 3. Automated Test Execution Commands

```bash
# 1. Run Python AI Service Tests (Unit, Brand-Fit, Guardrails, FastAPI)
python -m pytest apps/ai-service/tests

# 2. Run API Gateway & Orchestration Tests (Store, Duplicate Shield, Analytics)
npm --prefix apps/api test
```
