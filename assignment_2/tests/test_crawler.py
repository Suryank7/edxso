import pytest
from crawler.classifier import SourceClassifier
from crawler.seed_sources import SEED_SOURCES
from crawler.discovery import DiscoveryEngine

def test_source_classifier_gov():
    res = SourceClassifier.classify_url("https://scholarships.gov.in/schemeData")
    assert res["source_type"] == "Government"
    assert res["is_official"] is True
    assert res["authenticity_score"] == 100.0

def test_source_classifier_univ():
    res = SourceClassifier.classify_url("https://www.iitb.ac.in/academic/scholarships")
    assert res["source_type"] == "University"
    assert res["is_official"] is True
    assert res["authenticity_score"] == 95.0

def test_source_classifier_aggregator():
    res = SourceClassifier.classify_url("https://www.buddy4study.com/scholarships")
    assert res["source_type"] == "Aggregator"
    assert res["is_official"] is False
    assert res["authenticity_score"] == 40.0

def test_seed_sources_load():
    assert len(SEED_SOURCES) >= 20

def test_discovery_pipeline():
    engine = DiscoveryEngine()
    candidates = engine.run_discovery_pipeline()
    assert len(candidates) >= 20
    for cand in candidates:
        assert "url" in cand
        assert "authenticity_score" in cand
