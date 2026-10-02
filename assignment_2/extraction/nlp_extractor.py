import re
from typing import Dict, Any, List
from extraction.evidence_linker import EvidenceLinker

class NLPExtractor:
    """
    Rule-based & Regex Content Extractor for Scholarship Specifications.
    Parses raw text blocks to extract financial amounts, income thresholds, deadlines, and eligibility criteria.
    """

    AMOUNT_PATTERNS = [
        r'₹\s?[\d,]+(?:\s?(?:per annum|per month|p\.a\.|p\.m\.|one-time|lakh|crore))?',
        r'Rs\.\s?[\d,]+(?:\s?(?:per annum|per month|p\.a\.|p\.m\.|lakh))?',
        r'USD\s?[\d,]+', r'GBP\s?[\d,]+', r'£\s?[\d,]+', r'\$\s?[\d,]+',
        r'100%\s?tuition fee waiver', r'Full tuition fee', r'stipend of ₹\s?[\d,]+'
    ]

    INCOME_PATTERNS = [
        r'family income (?:less than|below|up to|does not exceed|not more than)\s?₹?\s?[\d\.,\s]+(?:lakh|lakhs|per annum)?',
        r'annual income (?:less than|below|up to|not exceeding)\s?₹?\s?[\d\.,\s]+(?:lakh|lakhs)?',
        r'income limit\s?:?\s?₹?\s?[\d\.,\s]+(?:lakh)?'
    ]

    DEADLINE_PATTERNS = [
        r'(?:closing date|deadline|last date|valid up to|end date)\s?:?\s?(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+\d{4}|\d{2}[/\.-]\d{2}[/\.-]\d{4})',
        r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})'
    ]

    @classmethod
    def extract_amount(cls, text: str) -> Dict[str, str]:
        for pattern in cls.AMOUNT_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return {"value": match.group(0), "evidence": match.group(0)}
        return {"value": "Not specified", "evidence": "No explicit monetary amount pattern matched in text."}

    @classmethod
    def extract_income(cls, text: str) -> Dict[str, str]:
        for pattern in cls.INCOME_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return {"value": match.group(0), "evidence": match.group(0)}
        return {"value": "Not specified", "evidence": "No income ceiling mentioned in text."}

    @classmethod
    def extract_deadline(cls, text: str) -> Dict[str, str]:
        for pattern in cls.DEADLINE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                val = match.group(1) if len(match.groups()) > 0 else match.group(0)
                return {"value": val, "evidence": f"Deadline statement: {match.group(0)}"}
        return {"value": "Rolling / Open", "evidence": "No fixed deadline specified."}

    @classmethod
    def extract_gender(cls, text: str) -> Dict[str, str]:
        txt_lower = text.lower()
        if 'female' in txt_lower or 'women' in txt_lower or 'girl' in txt_lower or 'girls' in txt_lower:
            return {"value": "Female candidates only", "evidence": "Text explicitly specifies eligibility for female / women students."}
        return {"value": "All Genders", "evidence": "No gender restriction mentioned."}

    @classmethod
    def extract_category(cls, text: str) -> Dict[str, str]:
        found = []
        for cat in ['SC', 'ST', 'OBC', 'EWS', 'Minority', 'General', 'PWD', 'Disability']:
            if re.search(rf'\b{cat}\b', text, re.IGNORECASE):
                found.append(cat)
        if found:
            return {"value": ", ".join(found), "evidence": f"Categories mentioned: {', '.join(found)}"}
        return {"value": "All Categories (General / Reserved)", "evidence": "Open to all social categories."}
