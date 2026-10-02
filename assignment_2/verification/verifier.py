from typing import Dict, Any
from verification.confidence import ConfidenceEngine

class VerificationEngine:
    """
    Verification Engine combining domain credibility check, deterministic confidence scoring,
    and anti-hallucination validation.
    """

    @classmethod
    def verify_scholarship(cls, scholarship: Dict[str, Any], evidence_list: list) -> Dict[str, Any]:
        result = ConfidenceEngine.calculate_confidence(scholarship, evidence_list)
        return {
            "scholarship_id": scholarship.get("id"),
            "confidence_score": result["final_confidence_score"],
            "is_verified": result["is_verified"],
            "status": result["verification_status"],
            "source_authenticity_score": result["source_authenticity_score"],
            "evidence_coverage_score": result["evidence_coverage_score"],
            "freshness_score": result["freshness_score"],
            "consistency_score": result["consistency_score"],
            "application_url_score": result["application_url_score"],
            "explanation": result["explanation"]
        }
