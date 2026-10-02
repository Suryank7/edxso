from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
import json
from datetime import datetime, timezone
from backend.app.db.database import execute_query, row_to_dict
from backend.app.schemas.scholarship import ScholarshipSchema, AnalyticsSchema
from crawler.discovery import DiscoveryEngine
from crawler.scraper import WebScraper
from crawler.classifier import SourceClassifier

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "Scholarship Intelligence Crawler API", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.get("/scholarships", response_model=List[Dict[str, Any]])
def get_scholarships(
    source_type: Optional[str] = None,
    status: Optional[str] = None,
    min_confidence: Optional[float] = None,
    search: Optional[str] = None
):
    query = "SELECT * FROM scholarships WHERE 1=1"
    params = []

    if source_type and source_type != "All":
        query += " AND source_type = ?"
        params.append(source_type)

    if status and status != "All":
        query += " AND status = ?"
        params.append(status)

    if min_confidence is not None:
        query += " AND confidence_score >= ?"
        params.append(min_confidence)

    if search:
        query += " AND (title LIKE ? OR provider LIKE ? OR eligibility_criteria LIKE ? OR domicile LIKE ?)"
        pattern = f"%{search}%"
        params.extend([pattern, pattern, pattern, pattern])

    query += " ORDER BY confidence_score DESC, updated_at DESC"
    rows = execute_query(query, tuple(params))
    return [row_to_dict(r) for r in rows]

@router.get("/scholarships/{scholarship_id}")
def get_scholarship_detail(scholarship_id: int):
    rows = execute_query("SELECT * FROM scholarships WHERE id = ?", (scholarship_id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Scholarship record not found")
    
    sch = row_to_dict(rows[0])
    
    # Get evidence
    ev_rows = execute_query("SELECT * FROM scholarship_evidence WHERE scholarship_id = ?", (scholarship_id,))
    sch["evidence"] = [row_to_dict(r) for r in ev_rows]
    
    # Get verification breakdown
    ver_rows = execute_query("SELECT * FROM verification_results WHERE scholarship_id = ?", (scholarship_id,))
    if ver_rows:
        ver_dict = row_to_dict(ver_rows[0])
        try:
            ver_dict["explanation"] = json.loads(ver_dict["explanation_json"])
        except Exception:
            ver_dict["explanation"] = {}
        sch["verification_breakdown"] = ver_dict

    # Get change events
    ch_rows = execute_query("SELECT * FROM change_events WHERE scholarship_id = ? ORDER BY detected_at DESC", (scholarship_id,))
    sch["change_history"] = [row_to_dict(r) for r in ch_rows]

    return sch

@router.get("/scholarships/{scholarship_id}/evidence")
def get_scholarship_evidence(scholarship_id: int):
    rows = execute_query("SELECT * FROM scholarship_evidence WHERE scholarship_id = ?", (scholarship_id,))
    return [row_to_dict(r) for r in rows]

@router.get("/scholarships/{scholarship_id}/changes")
def get_scholarship_changes(scholarship_id: int):
    rows = execute_query("SELECT * FROM change_events WHERE scholarship_id = ? ORDER BY detected_at DESC", (scholarship_id,))
    return [row_to_dict(r) for r in rows]

@router.get("/analytics", response_model=AnalyticsSchema)
def get_analytics():
    total_rows = execute_query("SELECT count(*) as c FROM scholarships")[0]['c']
    verified_count = execute_query("SELECT count(*) as c FROM scholarships WHERE is_verified = 1")[0]['c']
    review_req = execute_query("SELECT count(*) as c FROM scholarships WHERE status = 'REVIEW_REQUIRED'")[0]['c']
    active_count = execute_query("SELECT count(*) as c FROM scholarships WHERE status = 'ACTIVE'")[0]['c']
    expired_count = execute_query("SELECT count(*) as c FROM scholarships WHERE status IN ('EXPIRED', 'NO_LONGER_VERIFIABLE')")[0]['c']
    recently_updated = execute_query("SELECT count(*) as c FROM change_events")[0]['c']
    
    avg_conf_row = execute_query("SELECT AVG(confidence_score) as avg_c FROM scholarships")[0]['avg_c']
    avg_conf = round(avg_conf_row, 2) if avg_conf_row else 0.0

    dist_rows = execute_query("SELECT source_type, count(*) as count FROM scholarships GROUP BY source_type")
    dist = {r["source_type"]: r["count"] for r in dist_rows}

    return {
        "total_discovered": total_rows,
        "verified_count": verified_count,
        "review_required_count": review_req,
        "active_count": active_count,
        "expired_count": expired_count,
        "recently_updated_count": recently_updated,
        "average_confidence": avg_conf,
        "source_distribution": dist
    }

@router.post("/crawl/run")
def trigger_crawl_run():
    discovery = DiscoveryEngine()
    candidates = discovery.run_discovery_pipeline()
    return {
        "status": "success",
        "message": f"Discovery crawl executed successfully. Discovered and analyzed {len(candidates)} seed sources.",
        "candidates_discovered": len(candidates)
    }
