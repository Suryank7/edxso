import pytest
from verification.anti_hallucination import AntiHallucinationGuard
from extraction.nlp_extractor import NLPExtractor

def test_missing_income_defaults_not_specified():
    text_without_income = "The scholarship provides tuition fee coverage for undergraduate students admitted to B.Tech."
    res = NLPExtractor.extract_income(text_without_income)
    assert res["value"] == "Not specified"

def test_anti_hallucination_guard_numeric_rejection():
    # Attempting to claim ₹5 Lakh when source text contains no numbers
    audit = AntiHallucinationGuard.audit_field_grounding("income_criteria", "₹5 Lakh per annum", "Eligibility: Female students only.")
    assert audit["is_valid"] is False
    assert audit["clean_value"] == "Not specified"
