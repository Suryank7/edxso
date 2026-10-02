from datetime import datetime, timezone, date
import re
from typing import Dict, Any

class FreshnessEngine:
    """
    Staleness & Expiry Detection Engine.
    Evaluates closing dates, HTTP availability, and official notifications
    to assign lifecycle statuses: ACTIVE, EXPIRING_SOON, EXPIRED, REVIEW_REQUIRED, NO_LONGER_VERIFIABLE.
    """

    @classmethod
    def evaluate_scholarship_freshness(cls, scholarship: Dict[str, Any], http_status: int = 200) -> str:
        # If webpage returned HTTP 404 or 410, page was removed
        if http_status in [404, 410]:
            return "NO_LONGER_VERIFIABLE"

        closing_date_str = scholarship.get("closing_date", "")
        if not closing_date_str or closing_date_str in ["Rolling / Open", "Not specified"]:
            return scholarship.get("status", "ACTIVE")

        # Parse deadline if standard date format exists
        today = date.today()
        parsed_date = cls._parse_date_string(closing_date_str)
        
        if parsed_date:
            days_remaining = (parsed_date - today).days
            if days_remaining < 0:
                return "EXPIRED"
            elif days_remaining <= 15:
                return "EXPIRING_SOON"
            else:
                return "ACTIVE"

        return scholarship.get("status", "ACTIVE")

    @staticmethod
    def _parse_date_string(date_str: str) -> date:
        months = {
            'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
            'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
            'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'october': 10, 'oct': 10,
            'november': 11, 'nov': 11, 'december': 12, 'dec': 12
        }
        try:
            # Pattern: 31 August 2026 or 31 Aug 2026
            match = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', date_str)
            if match:
                day = int(match.group(1))
                month_name = match.group(2).lower()
                year = int(match.group(3))
                month = months.get(month_name)
                if month:
                    return date(year, month, day)
        except Exception:
            pass
        return None
