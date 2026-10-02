import pytest
import json
from change_intelligence.change_detector import ChangeDetector
from change_intelligence.snapshot_engine import SnapshotEngine

def test_change_detector_deadline_shift():
    old_snap = json.dumps({
        "title": "NSP Scheme",
        "closing_date": "31 August 2026",
        "amount": "₹12,000"
    })
    
    new_data = {
        "id": 1,
        "title": "NSP Scheme",
        "closing_date": "15 September 2026",
        "amount": "₹12,000"
    }

    changes = ChangeDetector.detect_changes(old_snap, new_data, "https://scholarships.gov.in")
    assert len(changes) == 1
    assert changes[0]["field_name"] == "closing_date"
    assert changes[0]["old_value"] == "31 August 2026"
    assert changes[0]["new_value"] == "15 September 2026"
    assert changes[0]["change_type"] == "DEADLINE_CHANGE"
