import pytest
from verification.confidence import ConfidenceEngine

def test_confidence_formula_high_verified():
    scholarship = {
        "title": "NSP Central Sector Scheme",
        "provider": "Ministry of Education, Govt of India",
        "official_url": "https://scholarships.gov.in",
        "application_url": "https://scholarships.gov.in/apply",
        "amount": "₹12,000 per annum",
        "eligibility_criteria": "Income below 3.5 Lakh",
        "academic_requirements": "55% in Class 12",
        "income_criteria": "₹3.5 Lakh",
        "closing_date": "30 November 2026",
        "documents_required": "Marksheets, Income Certificate",
        "selection_process": "Merit List",
        "renewal_terms": "Satisfactory Academic Progress",
        "status": "ACTIVE"
    }
    evidence = [
        {"field_name": "title", "extracted_value": "NSP Central Sector Scheme"},
        {"field_name": "provider", "extracted_value": "Ministry of Education, Govt of India"},
        {"field_name": "amount", "extracted_value": "₹12,000 per annum"},
        {"field_name": "eligibility_criteria", "extracted_value": "Income below 3.5 Lakh"},
        {"field_name": "closing_date", "extracted_value": "30 November 2026"},
        {"field_name": "application_url", "extracted_value": "https://scholarships.gov.in/apply"}
    ]
    res = ConfidenceEngine.calculate_confidence(scholarship, evidence)
    assert res["final_confidence_score"] >= 95.0
    assert res["is_verified"] == 1
    assert res["verification_status"] == "VERIFIED"

def test_confidence_formula_aggregator_low():
    scholarship = {
        "title": "Random Blog Scholarship",
        "provider": "Unverified Third Party",
        "official_url": "https://www.buddy4study.com/info",
        "application_url": "",
        "amount": "Not specified",
        "status": "ACTIVE"
    }
    evidence = []
    res = ConfidenceEngine.calculate_confidence(scholarship, evidence)
    assert res["final_confidence_score"] < 95.0
    assert res["is_verified"] == 0
    assert res["verification_status"] == "REVIEW_REQUIRED"
