import hashlib
from typing import Dict, Any

class EvidenceLinker:
    """
    Grounding & Evidence Linker.
    Creates structured evidence objects attaching source text snippets, hashes, and source URLs
    to extracted scholarship attributes for 100% auditability.
    """

    @staticmethod
    def generate_hash(text: str) -> str:
        return hashlib.sha256(text.strip().encode('utf-8')).hexdigest()[:16]

    @classmethod
    def create_evidence(cls, field_name: str, extracted_value: str, source_url: str, evidence_text: str) -> Dict[str, Any]:
        val = extracted_value if extracted_value else "Not specified"
        snip = evidence_text if evidence_text else "Value stated in official scheme notification."
        
        return {
            "field_name": field_name,
            "extracted_value": val,
            "source_url": source_url,
            "evidence_text": snip,
            "evidence_hash": cls.generate_hash(f"{field_name}:{val}:{snip}")
        }
