from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class EvidenceSchema(BaseModel):
    field_name: str
    extracted_value: str
    source_url: str
    evidence_text: str
    evidence_hash: Optional[str] = None
    extracted_at: Optional[str] = None

class ScholarshipSchema(BaseModel):
    id: int
    scholarship_uuid: str
    title: str
    provider: str
    source_type: str
    official_url: str
    application_url: Optional[str] = None
    amount: Optional[str] = None
    benefits_summary: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    academic_requirements: Optional[str] = None
    education_level: Optional[str] = None
    income_criteria: Optional[str] = None
    age_criteria: Optional[str] = None
    gender_criteria: Optional[str] = None
    category_criteria: Optional[str] = None
    domicile: Optional[str] = None
    institution_requirements: Optional[str] = None
    opening_date: Optional[str] = None
    closing_date: Optional[str] = None
    documents_required: Optional[str] = None
    selection_process: Optional[str] = None
    renewal_terms: Optional[str] = None
    status: str
    confidence_score: float
    is_verified: int
    last_verified_at: str
    created_at: str
    updated_at: str

class AnalyticsSchema(BaseModel):
    total_discovered: int
    verified_count: int
    review_required_count: int
    active_count: int
    expired_count: int
    recently_updated_count: int
    average_confidence: float
    source_distribution: Dict[str, int]
