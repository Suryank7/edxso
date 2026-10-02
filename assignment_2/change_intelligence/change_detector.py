import json
from datetime import datetime, timezone
from typing import Dict, Any, List

class ChangeDetector:
    """
    Change Intelligence & Delta Detection Engine.
    Compares consecutive snapshot states (Snapshot N vs Snapshot N+1) field by field.
    Emits granular change events for modified deadlines, amounts, eligibility, or status.
    """

    MONITORED_FIELDS = [
        ("closing_date", "DEADLINE_CHANGE"),
        ("amount", "AMOUNT_CHANGE"),
        ("eligibility_criteria", "ELIGIBILITY_CHANGE"),
        ("application_url", "APPLICATION_URL_CHANGE"),
        ("status", "STATUS_CHANGE")
    ]

    @classmethod
    def detect_changes(cls, old_snapshot_json: str, new_scholarship: Dict[str, Any], source_url: str) -> List[Dict[str, Any]]:
        changes = []
        if not old_snapshot_json:
            return changes

        try:
            old_data = json.loads(old_snapshot_json)
        except Exception:
            return changes

        for field_name, change_type in cls.MONITORED_FIELDS:
            old_val = str(old_data.get(field_name, "")).strip()
            new_val = str(new_scholarship.get(field_name, "")).strip()

            if old_val and new_val and old_val != new_val:
                changes.append({
                    "scholarship_id": new_scholarship.get("id"),
                    "field_name": field_name,
                    "old_value": old_val,
                    "new_value": new_val,
                    "change_type": change_type,
                    "detected_at": datetime.now(timezone.utc).isoformat(),
                    "source_url": source_url,
                    "evidence_text": f"Change detected during re-crawl. Field '{field_name}' updated from '{old_val}' to '{new_val}'."
                })

        return changes
