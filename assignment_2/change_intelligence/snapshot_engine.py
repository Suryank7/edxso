import json
from datetime import datetime, timezone
from typing import Dict, Any

class SnapshotEngine:
    """
    Snapshot Engine for Historical Record Integrity.
    Serializes current scholarship state into immutable JSON snapshots for change auditing.
    """

    @classmethod
    def capture_snapshot(cls, scholarship: Dict[str, Any], crawl_run_id: str) -> Dict[str, Any]:
        snapshot_data = {
            "title": scholarship.get("title"),
            "provider": scholarship.get("provider"),
            "amount": scholarship.get("amount"),
            "eligibility_criteria": scholarship.get("eligibility_criteria"),
            "academic_requirements": scholarship.get("academic_requirements"),
            "income_criteria": scholarship.get("income_criteria"),
            "closing_date": scholarship.get("closing_date"),
            "official_url": scholarship.get("official_url"),
            "application_url": scholarship.get("application_url"),
            "status": scholarship.get("status"),
            "confidence_score": scholarship.get("confidence_score")
        }
        
        return {
            "scholarship_id": scholarship.get("id"),
            "crawl_run_id": crawl_run_id,
            "snapshot_data": json.dumps(snapshot_data, indent=2),
            "captured_at": datetime.now(timezone.utc).isoformat()
        }
