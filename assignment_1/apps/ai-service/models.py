from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class BrandFitWeights(BaseModel):
    niche_relevance: float = Field(default=0.30, ge=0.0, le=1.0)
    audience_relevance: float = Field(default=0.20, ge=0.0, le=1.0)
    engagement: float = Field(default=0.20, ge=0.0, le=1.0)
    content_relevance: float = Field(default=0.15, ge=0.0, le=1.0)
    geography: float = Field(default=0.10, ge=0.0, le=1.0)
    contact_availability: float = Field(default=0.05, ge=0.0, le=1.0)

class CampaignConfig(BaseModel):
    campaign_id: Optional[str] = "camp_default_001"
    campaign_name: str = "AI Productivity SaaS Launch"
    brand: str = "EDXSO AI"
    niche: str = "Technology"
    sub_niches: List[str] = Field(default_factory=lambda: ["AI & Productivity", "Web Development", "Student Productivity", "Developer Tools"])
    target_platforms: List[str] = Field(default_factory=lambda: ["Instagram", "YouTube"])
    min_followers: int = 5000
    max_followers: int = 100000
    min_engagement_rate: float = 3.0
    target_geography: str = "India"
    target_audience: str = "Students and software developers"
    preferred_content: List[str] = Field(default_factory=lambda: ["AI tools", "productivity", "coding tutorials", "workflow hacks"])
    collaboration_type: str = "Sponsored Content / Dedicated Video"
    brand_fit_weights: BrandFitWeights = Field(default_factory=BrandFitWeights)

class CreatorProfile(BaseModel):
    creator_id: str
    name: str
    username: str
    platform: str
    profile_url: str
    follower_count: int
    engagement_rate: float
    category: str
    niche: str
    content_themes: List[str]
    contact_email: str
    email_source: str
    email_confidence: str
    website: str
    audience_age: str
    audience_gender: str
    audience_geography: str
    recent_content: List[str]
    discovery_source: str
    posting_frequency: str
    brand_collaborations: List[str] = Field(default_factory=list)

class FilterEvaluation(BaseModel):
    status: str # "PASS" or "FAIL"
    reasons: List[str]
    criteria_passed: int
    criteria_total: int

class BrandFitBreakdown(BaseModel):
    niche_relevance: float = Field(..., description="0 to 100")
    audience_relevance: float = Field(..., description="0 to 100")
    engagement_score: float = Field(..., description="0 to 100")
    content_relevance: float = Field(..., description="0 to 100")
    geography_score: float = Field(..., description="0 to 100")
    contact_availability: float = Field(..., description="0 to 100")
    composite_score: float = Field(..., description="0 to 100")
    explanation: List[str]

class GuardrailReport(BaseModel):
    email_word_count_compliant: bool
    email_word_count: int
    dm_word_count_compliant: bool
    dm_word_count: int
    zero_fabrication_checked: bool
    no_guessed_email_checked: bool
    safety_passed: bool

class PersonalizationResult(BaseModel):
    email_subject: str
    email_body: str
    email_word_count: int
    dm_body: str
    dm_word_count: int
    personalization_signals_used: List[str]
    guardrails: GuardrailReport

class EnrichedCreator(BaseModel):
    profile: CreatorProfile
    filter_evaluation: FilterEvaluation
    brand_fit: BrandFitBreakdown
    personalization: Optional[PersonalizationResult] = None
    review_status: str = "Auto-generated" # Auto-generated, Human Approved, Edited, Rejected, Skipped
    outreach_status: str = "Pending" # Pending, Simulated, Sent, Failed, Skipped

class FilterRequest(BaseModel):
    campaign: CampaignConfig
    creators: Optional[List[CreatorProfile]] = None

class PersonalizationRequest(BaseModel):
    campaign: CampaignConfig
    creator: CreatorProfile

class BatchPersonalizationRequest(BaseModel):
    campaign: CampaignConfig
    creators: List[CreatorProfile]
