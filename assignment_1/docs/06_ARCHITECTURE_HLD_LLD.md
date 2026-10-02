# EDXSO Influencer Outreach AI (InfluenceFlow AI)
## Phase 4: High-Level Design (HLD) & Low-Level Design (LLD)

---

### 1. High-Level Design (HLD)

#### 1.1 Architectural Topology
The platform employs a modular service-oriented architecture designed to isolate concerns, provide independent scaling, and allow easy substitution of external LLM or data providers:

```mermaid
graph TD
    subgraph Presentation Layer
        UI[Next.js 15 Dashboard / React App]
    end

    subgraph API Gateway & Orchestration Layer
        Gateway[Node.js / Express API Gateway]
        Store[(File-Backed SQLite / JSON Store)]
        Shield[Duplicate Prevention Shield]
        Dispatch[Outreach Dispatcher & SMTP]
    end

    subgraph AI & Processing Layer
        FastAPI[Python FastAPI AI Microservice]
        FilterEng[Configurable Filtering Engine]
        BrandEng[Multi-Factor Brand-Fit Engine]
        PersEng[Grounded AI Personalization Engine]
        Guardrails[Word Count & Anti-Hallucination Validator]
    end

    subgraph External Providers
        SeedData[(52+ Seed Influencer Ingestion Pool)]
        LLM[Google Gemini / OpenAI GPT-4o]
        MailServer[Gmail SMTP Server]
    end

    UI -->|HTTP REST / JSON| Gateway
    Gateway --> Store
    Gateway --> Shield
    Shield --> Dispatch
    Dispatch --> MailServer

    Gateway -->|Async HTTP RPC| FastAPI
    FastAPI --> SeedData
    FastAPI --> FilterEng
    FastAPI --> BrandEng
    FastAPI --> PersEng
    PersEng --> Guardrails
    PersEng -.->|Optional Live Keys| LLM
```

---

### 2. Low-Level Design (LLD)

#### 2.1 Core Domain Models

```mermaid
classDiagram
    class CampaignConfig {
        +string campaign_id
        +string campaign_name
        +string brand
        +string niche
        +List~string~ sub_niches
        +List~string~ target_platforms
        +int min_followers
        +int max_followers
        +float min_engagement_rate
        +string target_geography
        +string target_audience
        +List~string~ preferred_content
        +BrandFitWeights brand_fit_weights
    }

    class CreatorProfile {
        +string creator_id
        +string name
        +string username
        +string platform
        +string profile_url
        +int follower_count
        +float engagement_rate
        +string category
        +string niche
        +List~string~ content_themes
        +string contact_email
        +string email_source
        +string email_confidence
        +string website
        +string audience_age
        +string audience_gender
        +string audience_geography
        +List~string~ recent_content
        +string discovery_source
        +string posting_frequency
    }

    class FilterEvaluation {
        +string status
        +List~string~ reasons
        +int criteria_passed
        +int criteria_total
    }

    class BrandFitBreakdown {
        +float niche_relevance
        +float audience_relevance
        +float engagement_score
        +float content_relevance
        +float geography_score
        +float contact_availability
        +float composite_score
        +List~string~ explanation
    }

    class PersonalizationResult {
        +string email_subject
        +string email_body
        +int email_word_count
        +string dm_body
        +int dm_word_count
        +List~string~ personalization_signals_used
        +GuardrailReport guardrails
    }

    class EnrichedCreator {
        +CreatorProfile profile
        +FilterEvaluation filter_evaluation
        +BrandFitBreakdown brand_fit
        +PersonalizationResult personalization
        +string review_status
        +string outreach_status
    }

    EnrichedCreator --> CreatorProfile
    EnrichedCreator --> FilterEvaluation
    EnrichedCreator --> BrandFitBreakdown
    EnrichedCreator --> PersonalizationResult
    CampaignConfig --> EnrichedCreator
```

---

### 3. Detailed Sequence Diagrams

#### 3.1 End-to-End Campaign Discovery & Qualification Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User as Partnerships Manager
    participant UI as Next.js Dashboard
    participant Gateway as Express Gateway (:5000)
    participant AI as Python AI Engine (:8000)
    participant Store as Data Store

    User->>UI: Click "Trigger AI Discovery & Ingestion"
    UI->>Gateway: POST /api/v1/campaigns/{id}/discover
    Gateway->>AI: POST /api/v1/pipeline/evaluate (CampaignConfig)
    
    activate AI
    AI->>AI: Load 52 Seed Creator Profiles
    loop For each creator
        AI->>AI: Evaluate Follower, Engagement, Niche, Content Rules
        AI->>AI: Compute 6-Factor Weighted Brand Fit Score
        alt Filter == PASS
            AI->>AI: Synthesize Grounded Email (60-90w) & DM (15-30w)
            AI->>AI: Validate Guardrails & Anti-Hallucination
        end
    end
    AI-->>Gateway: Return 52 EnrichedCreator Records
    deactivate AI

    Gateway->>Store: Persist Campaign Creators
    Gateway-->>UI: Return Enriched Results + Summary Funnel
    UI-->>User: Render Creator Table, Badges, & Funnel Cards
```

#### 3.2 Human Review, Duplicate Shield & Outreach Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User as Partnerships Manager
    participant UI as Next.js Dashboard
    participant Gateway as Express Gateway
    participant Shield as Duplicate Prevention Shield
    participant Dispatch as Outreach Dispatcher
    participant Store as Data Store

    User->>UI: Edit Pitch & Click "Send Outreach"
    UI->>Gateway: PATCH /campaigns/{id}/creators/{cid}/review (status: "Human Approved")
    UI->>Gateway: POST /api/v1/outreach/send (creator_id, channel, email, body)

    Gateway->>Shield: Check Uniqueness: (campaign_id + creator_id + channel)
    alt Already Sent or Simulated
        Shield-->>Gateway: Block Dispatch (duplicate_prevented: true)
        Gateway-->>UI: HTTP 200 (duplicate_prevented: true, message: "Duplicate Blocked")
        UI-->>User: Show Warning Toast "Creator Already Contacted!"
    else Unique Request
        Shield->>Dispatch: Proceed with Outreach
        alt DRY_RUN == true
            Dispatch->>Dispatch: Log Simulation Payload
            Dispatch->>Store: Save OutreachRecord (status: "SIMULATED")
        else DRY_RUN == false
            Dispatch->>Dispatch: Connect SMTP & Transmit Email
            Dispatch->>Store: Save OutreachRecord (status: "SENT")
        end
        Dispatch-->>Gateway: Success Confirmation
        Gateway-->>UI: Return Updated Outreach Record
        UI-->>User: Show Green Success Toast & Update Row Status
    end
```
