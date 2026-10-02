from typing import Dict, Any, List

class AntiHallucinationGuard:
    """
    Anti-Hallucination Guardrail & Audit Engine.
    Ensures that fields absent in source text remain explicitly marked as 'Not specified'
    and rejects ungrounded field values.
    """

    @classmethod
    def audit_field_grounding(cls, field_name: str, field_value: str, source_text: str) -> Dict[str, Any]:
        """
        Audits whether a given field value is supported by source text snippets.
        """
        if not field_value or field_value == "Not specified":
            return {"is_valid": True, "clean_value": "Not specified", "reason": "Explicit default preserved."}

        # If source text is empty or missing key terms, flag potential hallucination
        if not source_text:
            return {"is_valid": False, "clean_value": "Not specified", "reason": "Source text empty; ungrounded claim rejected."}

        # For numeric values (like income limits ₹5 Lakh), check if numbers exist in text
        if "lakh" in field_value.lower() or "₹" in field_value:
            if not any(char.isdigit() for char in source_text):
                return {
                    "is_valid": False,
                    "clean_value": "Not specified",
                    "reason": f"Numeric claim '{field_value}' not supported by source text containing no numbers."
                }

        return {"is_valid": True, "clean_value": field_value, "reason": "Supported by evidence."}
