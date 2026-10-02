from urllib.parse import urlparse
import re
from typing import Dict, Any

class SourceClassifier:
    """
    Source Classification Engine for Scholarship Intelligence Crawler.
    Determines whether a web URL belongs to an official primary provider or an aggregator/third-party blog.
    """
    
    GOVT_DOMAINS = [
        r'\.gov\.in$', r'\.nic\.in$', r'\.gov$', r'scholarships\.gov\.in$',
        r'aicte-india\.org$', r'ugc\.ac\.in$', r'dst\.gov\.in$', r'dbtindia\.gov\.in$',
        r'mhrd\.gov\.in$', r'education\.gov\.in$', r'tribal\.gov\.in$'
    ]
    
    UNIV_DOMAINS = [
        r'\.edu\.in$', r'\.ac\.in$', r'\.edu$', r'iitb\.ac\.in$', r'iitm\.ac\.in$',
        r'du\.ac\.in$', r'bits-pilani\.ac\.in$', r'jnu\.ac\.in$', r'annauniv\.edu$'
    ]
    
    CORP_CSR_DOMAINS = [
        r'tata\.com$', r'tatatrusts\.org$', r'reliancefoundation\.org$', r'hdfcbank\.com$',
        r'infosys\.com$', r'adityabirlacapital\.com$', r'kotak\.com$', r'colgate\.co\.in$',
        r'loreal\.com$', r'sitaramjindalfoundation\.org$'
    ]
    
    NGO_TRUST_DOMAINS = [
        r'narotamsekhsaria\.org$', r'kcmindiatrust\.org$', r'inlaksfoundation\.org$',
        r'agaram\.in$', r'vinfoundation\.org$', r'fairandlovelyfoundation\.in$'
    ]
    
    INTL_DOMAINS = [
        r'chevening\.org$', r'usief\.org\.in$', r'cscuk\.fcdo\.gov\.uk$',
        r'rhodeshouse\.ox\.ac\.uk$', r'daad\.de$', r'fulbright-hays\.org$'
    ]
    
    AGGREGATOR_DOMAINS = [
        r'buddy4study\.com$', r'collegedunia\.com$', r'shiksha\.com$',
        r'careers360\.com$', r'sarkariresult\.com$', r'scholarshipsads\.com$',
        r'freshersnow\.com$', r'aglasem\.com$'
    ]

    @classmethod
    def classify_url(cls, url: str) -> Dict[str, Any]:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
            
        source_type = "Unknown"
        is_official = False
        authenticity_score = 50.0

        # Check Government
        for pattern in cls.GOVT_DOMAINS:
            if re.search(pattern, domain):
                return {
                    "domain": domain,
                    "source_type": "Government",
                    "is_official": True,
                    "authenticity_score": 100.0,
                    "reason": "Official government domain (.gov.in / .nic.in / verified ministry portal)"
                }

        # Check University
        for pattern in cls.UNIV_DOMAINS:
            if re.search(pattern, domain):
                return {
                    "domain": domain,
                    "source_type": "University",
                    "is_official": True,
                    "authenticity_score": 95.0,
                    "reason": "Accredited educational institution / university domain (.edu.in / .ac.in)"
                }

        # Check Corporate CSR
        for pattern in cls.CORP_CSR_DOMAINS:
            if re.search(pattern, domain):
                return {
                    "domain": domain,
                    "source_type": "Corporate CSR",
                    "is_official": True,
                    "authenticity_score": 90.0,
                    "reason": "Official corporate CSR / foundation website"
                }

        # Check International
        for pattern in cls.INTL_DOMAINS:
            if re.search(pattern, domain):
                return {
                    "domain": domain,
                    "source_type": "International",
                    "is_official": True,
                    "authenticity_score": 95.0,
                    "reason": "Official foreign embassy / bilateral scholarship council website"
                }

        # Check NGO/Trust
        for pattern in cls.NGO_TRUST_DOMAINS:
            if re.search(pattern, domain):
                return {
                    "domain": domain,
                    "source_type": "NGO/Trust",
                    "is_official": True,
                    "authenticity_score": 85.0,
                    "reason": "Registered philanthropic foundation / charitable trust portal"
                }

        # Check Aggregator
        for pattern in cls.AGGREGATOR_DOMAINS:
            if re.search(pattern, domain):
                return {
                    "domain": domain,
                    "source_type": "Aggregator",
                    "is_official": False,
                    "authenticity_score": 40.0,
                    "reason": "Third-party scholarship aggregator / listing website (Discovery only, non-authoritative)"
                }

        return {
            "domain": domain,
            "source_type": "General Website",
            "is_official": False,
            "authenticity_score": 50.0,
            "reason": "Standard web source (requires secondary verification)"
        }
