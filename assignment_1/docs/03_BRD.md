# EDXSO Influencer Outreach AI (InfluenceFlow AI)
## Phase 1: Business Requirements Document (BRD)

---

### 1. Business Problem Statement

Brands and digital agencies operating in hyper-competitive markets (e.g., AI software, developer tools, direct-to-consumer e-commerce, consumer tech) face an uphill battle executing micro-influencer campaigns. While micro-influencers ($5\text{k} - 100\text{k}$ followers) deliver $3\times$ higher conversion rates and $60\%$ higher engagement than celebrity influencers, recruiting them manually is painfully inefficient:

- **Labor Drain**: 20+ manual hours per campaign spent finding handles, copying follower counts into spreadsheets, and looking for email addresses.
- **Low Hit-Rate**: Over $90\%$ of standard pitch emails bounce or get ignored because the pitches are generic, robotic templates.
- **Brand Embarrassment**: Fragmented teams inadvertently pitch the same influencer multiple times with contradictory budgets, or reach out to influencers whose audience is incompatible with the brand's target demographic.
- **Lack of Governance**: Zero audit trails exist to track who was contacted, when, what was pitched, or what response occurred.

---

### 2. Business Objectives & Success Criteria

| ID | Business Goal | Metric / Benchmark | Measurement Method |
| :--- | :--- | :--- | :--- |
| **BO-1** | Accelerate Creator Discovery | Reduce discovery time from 20 hours to < 60 seconds for 50+ creators | Time-to-populate dataset |
| **BO-2** | Maximize Outreach Engagement | Increase email open/response rates from industry avg 3% to > 25% | Grounded personalization vs generic templates |
| **BO-3** | Eliminate Duplicate Outreaches | 100% duplicate prevention across teams and channels | Zero duplicate records in outreach log |
| **BO-4** | Transparent Creator Vetting | Provide clear explanation for 100% of qualified/rejected creators | Pass/Fail audit statements |
| **BO-5** | Ensure Brand Safety & Grounding | 0% fabricated facts, fake posts, or guessed emails | AI Guardrail validation pass rate |

---

### 3. Business Requirements Matrix

#### BR-1: Multi-Channel Micro-Influencer Discovery
- The system shall automatically ingest and normalize at least 50 creator profiles matching the campaign's target niche from permitted sources (YouTube, Instagram, directories).
- Each creator record must capture canonical handles, URLs, follower metrics, engagement percentages, recent post titles, and documented themes.

#### BR-2: Objective Qualification & Filtering Rules
- The system must filter creators based on campaign criteria: Follower Range ($5\text{k} - 100\text{k}$), Minimum Engagement Rate ($\ge 3\%$), Platform, and Niche alignment.
- Every creator must be flagged as either **PASS** or **FAIL** with an itemized, human-readable justification list.

#### BR-3: Data Enrichment & Integrity Safeguards
- The system must attempt to enrich every shortlisted creator with public business emails, websites, audience age/gender/geography breakdowns, and posting cadence.
- **Non-Negotiable Integrity**: If contact email or demographic info is not publicly verifiable, the system must record `"Not Found"` and never extrapolate or hallucinate fake data.

#### BR-4: Two-Tier AI Personalization
- For every qualified influencer, the system must generate:
  1. An email pitch strictly between **60 and 90 words**, referencing real recent content, creator niche, audience synergy, and a clear collaboration CTA.
  2. An Instagram DM pitch strictly between **15 and 30 words**, conversational and concise.

#### BR-5: Human-in-the-Loop Review & Governance
- Outreach must not send automatically without human oversight. The system must present an interactive review interface enabling users to:
  - Approve generated pitches
  - Inline edit email or DM copy
  - Mark creators as Skipped or Rejected

#### BR-6: Safe Sending Layer & Simulation Mode
- The system must support a `DRY_RUN` configuration mode (default `true`) allowing teams to simulate end-to-end outreach without sending live emails.
- When live sending is enabled, it must authenticate compliant SMTP/Gmail connections.

#### BR-7: Composite Duplicate Shield
- The system must enforce a unique composite constraint: `campaign_id + creator_id + channel`. Any attempt to re-send to an already contacted creator must be intercepted and reported.

#### BR-8: Campaign Performance Analytics
- Real-time dashboards must report discovery funnels, qualification conversion rates, Brand Fit score distributions, platform breakdowns, and delivery logs.
