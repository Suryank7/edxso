# EDXSO Influencer Outreach AI (InfluenceFlow AI)
## Phase 4: REST API Specification (OpenAPI 3.0 Standard)

---

### 1. Base URL & Protocol
- **Local API Gateway**: `http://localhost:5000`
- **Internal AI Service**: `http://localhost:8000`
- **Content-Type**: `application/json`

---

### 2. Endpoints Overview

#### 2.1 System Health
```http
GET /health
```
**Response (200 OK)**:
```json
{
  "status": "healthy",
  "service": "edxso-api-gateway",
  "version": "1.0.0",
  "dry_run_mode": true,
  "ai_service_url": "http://localhost:8000"
}
```

---

#### 2.2 List Campaigns
```http
GET /api/v1/campaigns
```
**Response (200 OK)**:
```json
[
  {
    "campaign_id": "camp_default_001",
    "campaign_name": "AI Productivity SaaS Launch",
    "brand": "EDXSO AI",
    "niche": "Technology",
    "sub_niches": ["AI & Productivity", "Web Development"],
    "target_platforms": ["Instagram", "YouTube"],
    "min_followers": 5000,
    "max_followers": 100000,
    "min_engagement_rate": 3.0,
    "target_geography": "India",
    "target_audience": "Students and software developers",
    "created_at": "2026-10-01T12:00:00.000Z",
    "status": "ACTIVE"
  }
]
```

---

#### 2.3 Create Campaign
```http
POST /api/v1/campaigns
```
**Request Body**:
```json
{
  "campaign_name": "Developer Productivity Launch",
  "brand": "EDXSO Workspace",
  "niche": "Technology",
  "sub_niches": ["Developer Tools", "AI Tools"],
  "target_platforms": ["Instagram", "YouTube"],
  "min_followers": 5000,
  "max_followers": 80000,
  "min_engagement_rate": 3.5,
  "target_geography": "India",
  "target_audience": "Tech students & junior developers",
  "preferred_content": ["AI tools", "productivity", "VS Code"],
  "collaboration_type": "Sponsored Video"
}
```
**Response (201 Created)**: Returns created campaign object with generated `campaign_id`.

---

#### 2.4 Trigger Discovery & AI Evaluation Pipeline
```http
POST /api/v1/campaigns/:id/discover
```
**Response (200 OK)**:
```json
{
  "campaign_id": "camp_default_001",
  "total_discovered": 52,
  "qualified_count": 36,
  "rejected_count": 16,
  "enriched_creators": [
    {
      "profile": {
        "creator_id": "cr_001",
        "name": "Rohan Sharma",
        "username": "rohan_techbytes",
        "platform": "Instagram",
        "follower_count": 42500,
        "engagement_rate": 5.8,
        "category": "Technology",
        "niche": "AI & Productivity",
        "contact_email": "contact.rohansharma@gmail.com",
        "email_confidence": "high"
      },
      "filter_evaluation": {
        "status": "PASS",
        "reasons": [
          "✓ 42,500 followers within target micro-influencer range",
          "✓ 5.8% engagement rate satisfies minimum 3.0% benchmark",
          "✓ Niche 'AI & Productivity' matches target campaign niche"
        ],
        "criteria_passed": 5,
        "criteria_total": 5
      },
      "brand_fit": {
        "niche_relevance": 95.0,
        "audience_relevance": 90.0,
        "engagement_score": 88.0,
        "content_relevance": 95.0,
        "geography_score": 95.0,
        "contact_availability": 100.0,
        "composite_score": 93.4,
        "explanation": ["Direct alignment with AI & productivity focus"]
      },
      "personalization": {
        "email_subject": "Collaboration: EDXSO AI x Rohan (AI & Productivity)",
        "email_body": "Hi Rohan,\n\nI came across your recent work on 'Top 5 AI tools every computer science student needs'...",
        "email_word_count": 72,
        "dm_body": "Hey Rohan! Loved your post on 'Top 5 AI tools...'. Your audience looks like a great fit...",
        "dm_word_count": 22,
        "guardrails": {
          "email_word_count_compliant": true,
          "dm_word_count_compliant": true,
          "zero_fabrication_checked": true,
          "safety_passed": true
        }
      },
      "review_status": "Auto-generated",
      "outreach_status": "Pending"
    }
  ]
}
```

---

#### 2.5 Update Human Review
```http
PATCH /api/v1/campaigns/:id/creators/:creatorId/review
```
**Request Body**:
```json
{
  "reviewStatus": "Human Approved",
  "editedEmail": "Updated custom collaboration copy...",
  "editedDm": "Updated short DM copy..."
}
```
**Response (200 OK)**: Returns updated `EnrichedCreator` object.

---

#### 2.6 Send Outreach (with Duplicate Prevention)
```http
POST /api/v1/outreach/send
```
**Request Body**:
```json
{
  "campaignId": "camp_default_001",
  "creatorId": "cr_001",
  "creatorName": "Rohan Sharma",
  "channel": "Email",
  "recipient": "contact.rohansharma@gmail.com",
  "subject": "Collaboration: EDXSO AI x Rohan",
  "messageBody": "Hi Rohan, loved your video..."
}
```
**Response (200 OK - Unique / First Send)**:
```json
{
  "success": true,
  "duplicate_prevented": false,
  "status": "SIMULATED",
  "message": "[DRY_RUN] Email simulated for Rohan Sharma (contact.rohansharma@gmail.com). No real email sent.",
  "record": {
    "outreach_id": "out_9a8b7c6d",
    "campaign_id": "camp_default_001",
    "creator_id": "cr_001",
    "status": "SIMULATED",
    "sent_at": "2026-10-01T12:30:00.000Z"
  }
}
```
**Response (200 OK - Duplicate Blocked)**:
```json
{
  "success": false,
  "duplicate_prevented": true,
  "message": "Duplicate outreach prevented: Creator 'Rohan Sharma' already contacted on channel 'Email' for campaign 'camp_default_001'.",
  "existing_record": { ... }
}
```

---

#### 2.7 Get Campaign Analytics
```http
GET /api/v1/campaigns/:id/analytics
```
**Response (200 OK)**:
```json
{
  "campaign_id": "camp_default_001",
  "funnel": {
    "discovered": 52,
    "qualified": 36,
    "rejected": 16,
    "enriched": 52,
    "messages_generated": 36,
    "outreach_simulated": 12,
    "outreach_sent": 0,
    "duplicates_prevented": 2
  },
  "brand_fit_distribution": {
    "elite": 18,
    "high": 18,
    "moderate": 10,
    "low": 6
  },
  "platform_breakdown": {
    "Instagram": 34,
    "YouTube": 18
  },
  "qualification_rate_percent": 69,
  "average_qualified_engagement": 5.42
}
```
