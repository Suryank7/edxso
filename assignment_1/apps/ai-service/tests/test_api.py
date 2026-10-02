import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["service"] == "edxso-ai-service"

def test_get_creators_endpoint():
    res = client.get("/api/v1/creators?limit=10")
    assert res.status_code == 200
    creators = res.json()
    assert len(creators) == 10
    assert "name" in creators[0]
    assert "follower_count" in creators[0]

def test_full_pipeline_evaluate():
    payload = {
        "campaign_id": "camp_test_eval",
        "campaign_name": "Test AI Launch",
        "brand": "EDXSO AI",
        "niche": "Technology",
        "target_platforms": ["Instagram", "YouTube"],
        "min_followers": 5000,
        "max_followers": 100000,
        "min_engagement_rate": 3.0,
        "target_geography": "India",
        "target_audience": "Students and developers",
        "preferred_content": ["AI tools", "productivity"]
    }
    res = client.post("/api/v1/pipeline/evaluate", json=payload)
    assert res.status_code == 200
    enriched = res.json()
    assert len(enriched) >= 50
    # Verify structure of enriched creator
    first = enriched[0]
    assert "profile" in first
    assert "filter_evaluation" in first
    assert "brand_fit" in first
    assert first["filter_evaluation"]["status"] in ["PASS", "FAIL"]
    assert first["brand_fit"]["composite_score"] >= 0
