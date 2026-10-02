import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from models import CampaignConfig, CreatorProfile, BrandFitWeights
from engines import FilteringEngine, BrandFitEngine, PersonalizationEngine

@pytest.fixture
def campaign():
    return CampaignConfig(
        campaign_name="AI Productivity SaaS Launch",
        brand="EDXSO AI",
        niche="Technology",
        min_followers=5000,
        max_followers=100000,
        min_engagement_rate=3.0,
        target_geography="India",
        target_audience="Students and software developers",
        preferred_content=["AI tools", "productivity", "coding tutorials"]
    )

@pytest.fixture
def qualified_creator():
    return CreatorProfile(
        creator_id="test_001",
        name="Rohan Sharma",
        username="rohan_tech",
        platform="Instagram",
        profile_url="https://instagram.com/rohan_tech",
        follower_count=42500,
        engagement_rate=5.8,
        category="Technology",
        niche="AI & Productivity",
        content_themes=["AI productivity tools", "developer setups"],
        contact_email="rohan@example.com",
        email_source="public_profile",
        email_confidence="high",
        website="https://rohan.dev",
        audience_age="18-24 (54%)",
        audience_gender="70% Male, 30% Female",
        audience_geography="India (72%)",
        recent_content=["Top 5 AI tools every computer science student needs"],
        discovery_source="Instagram Public Directory",
        posting_frequency="4 reels / week"
    )

@pytest.fixture
def low_engagement_creator(qualified_creator):
    profile = qualified_creator.model_copy()
    profile.creator_id = "test_002"
    profile.engagement_rate = 1.8 # Below 3%
    return profile

@pytest.fixture
def wrong_niche_creator(qualified_creator):
    profile = qualified_creator.model_copy()
    profile.creator_id = "test_003"
    profile.category = "Fashion & Beauty"
    profile.niche = "Sustainable Fashion"
    profile.content_themes = ["Thrift styling", "makeup"]
    profile.recent_content = ["Spring fashion haul"]
    return profile

@pytest.fixture
def macro_creator(qualified_creator):
    profile = qualified_creator.model_copy()
    profile.creator_id = "test_004"
    profile.follower_count = 350000 # Above 100k
    return profile

def test_filtering_qualified_creator(qualified_creator, campaign):
    result = FilteringEngine.evaluate(qualified_creator, campaign)
    assert result.status == "PASS"
    assert result.criteria_passed >= 4
    assert any("42,500 followers" in r for r in result.reasons)
    assert any("5.8% engagement" in r for r in result.reasons)

def test_filtering_low_engagement(low_engagement_creator, campaign):
    result = FilteringEngine.evaluate(low_engagement_creator, campaign)
    assert result.status == "FAIL"
    assert any("1.8% engagement rate falls below" in r for r in result.reasons)

def test_filtering_wrong_niche(wrong_niche_creator, campaign):
    result = FilteringEngine.evaluate(wrong_niche_creator, campaign)
    assert result.status == "FAIL"
    assert any("unrelated to target campaign niche" in r for r in result.reasons)

def test_filtering_macro_influencer(macro_creator, campaign):
    result = FilteringEngine.evaluate(macro_creator, campaign)
    assert result.status == "FAIL"
    assert any("exceeds maximum ceiling" in r for r in result.reasons)

def test_brand_fit_scoring(qualified_creator, campaign):
    fit = BrandFitEngine.calculate(qualified_creator, campaign)
    assert 0 <= fit.composite_score <= 100
    assert fit.composite_score >= 80 # Highly aligned
    assert fit.niche_relevance == 95.0
    assert fit.engagement_score == 88.0
    assert len(fit.explanation) >= 4

def test_personalization_guardrails(qualified_creator, campaign):
    result = PersonalizationEngine.generate(qualified_creator, campaign)
    assert 60 <= result.email_word_count <= 90
    assert 15 <= result.dm_word_count <= 30
    assert result.guardrails.email_word_count_compliant is True
    assert result.guardrails.dm_word_count_compliant is True
    assert result.guardrails.zero_fabrication_checked is True
    # Grounding check: Recent post must be in the email body
    assert "Top 5 AI tools every computer science student needs" in result.email_body
    assert "EDXSO AI" in result.email_body
