from typing import Dict, Any
from crawler.classifier import SourceClassifier

class ConfidenceEngine:
    """
    Deterministic Mathematical Confidence Scoring Engine.
    Evaluates evidence, source domain authenticity, field completeness, recency, and application link validity.
    
    Formula:
      Final Confidence = (SourceScore * 0.25) + (EvidenceScore * 0.25) + 
                         (FreshnessScore * 0.15) + (ConsistencyScore * 0.15) + 
                         (ApplicationURLScore * 0.20)
                         
    Rule:
      Confidence >= 95.0% -> VERIFIED
      Confidence < 95.0%  -> REVIEW_REQUIRED
    """

    WEIGHT_SOURCE = 0.25
    WEIGHT_EVIDENCE = 0.25
    WEIGHT_FRESHNESS = 0.15
    WEIGHT_CONSISTENCY = 0.15
    WEIGHT_APPLICATION = 0.20

    @classmethod
    def calculate_confidence(cls, scholarship: Dict[str, Any], evidence_list: list) -> Dict[str, Any]:
        official_url = scholarship.get("official_url", "")
        app_url = scholarship.get("application_url", "")
        status = scholarship.get("status", "ACTIVE")

        # 1. Source Authenticity Score (0 - 100)
        classification = SourceClassifier.classify_url(official_url)
        source_score = classification["authenticity_score"]

        # 2. Evidence Coverage Score (0 - 100)
        # Check how many essential fields have grounded evidence
        essential_fields = ["title", "provider", "amount", "eligibility_criteria", "closing_date", "application_url"]
        evidence_fields = {e.get("field_name") for e in evidence_list if e.get("extracted_value") and e.get("extracted_value") != "Not specified"}
        covered_count = sum(1 for f in essential_fields if f in evidence_fields)
        evidence_score = (covered_count / len(essential_fields)) * 100.0

        # 3. Freshness & Recency Score (0 - 100)
        freshness_score = 100.0
        if status in ["EXPIRED", "NO_LONGER_VERIFIABLE"]:
            freshness_score = 30.0
        elif status == "EXPIRING_SOON":
            freshness_score = 80.0

        # 4. Field Consistency & Completeness Score (0 - 100)
        non_empty_count = 0
        total_fields = 10
        fields_to_check = [
            "title", "provider", "amount", "eligibility_criteria", "academic_requirements",
            "income_criteria", "closing_date", "documents_required", "selection_process", "renewal_terms"
        ]
        for f in fields_to_check:
            val = str(scholarship.get(f, ""))
            if val and val.lower() != "not specified":
                non_empty_count += 1
        consistency_score = (non_empty_count / total_fields) * 100.0

        # 5. Application URL Score (0 - 100)
        if app_url and app_url.startswith("http"):
            app_classification = SourceClassifier.classify_url(app_url)
            if app_classification["is_official"]:
                app_score = 100.0
            else:
                app_score = 60.0
        else:
            app_score = 20.0

        # Calculate Final Weighted Score
        final_confidence = (
            (source_score * cls.WEIGHT_SOURCE) +
            (evidence_score * cls.WEIGHT_EVIDENCE) +
            (freshness_score * cls.WEIGHT_FRESHNESS) +
            (consistency_score * cls.WEIGHT_CONSISTENCY) +
            (app_score * cls.WEIGHT_APPLICATION)
        )

        final_confidence = round(final_confidence, 2)
        is_verified = (final_confidence >= 95.0) and classification["is_official"]
        final_status = "VERIFIED" if is_verified else ("REVIEW_REQUIRED" if status == "ACTIVE" else status)

        return {
            "source_authenticity_score": round(source_score, 2),
            "evidence_coverage_score": round(evidence_score, 2),
            "freshness_score": round(freshness_score, 2),
            "consistency_score": round(consistency_score, 2),
            "application_url_score": round(app_score, 2),
            "final_confidence_score": final_confidence,
            "is_verified": 1 if is_verified else 0,
            "verification_status": final_status,
            "explanation": {
                "source_type": classification["source_type"],
                "domain_reason": classification["reason"],
                "evidence_fields_covered": list(evidence_fields),
                "is_official_domain": classification["is_official"],
                "application_url_valid": app_url.startswith("http")
            }
        }
