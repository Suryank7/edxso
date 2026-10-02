import re
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Any
from crawler.classifier import SourceClassifier
from crawler.scraper import WebScraper
from crawler.seed_sources import SEED_SOURCES

class DiscoveryEngine:
    """
    Automated Discovery Engine for Scholarship Intelligence Crawler.
    Discovers new scholarship opportunities from seed sources, internal web links, and domain structures.
    Filters out junk pages, classifies candidate domains, and identifies authoritative primary sources.
    """

    SCHOLARSHIP_KEYWORDS = [
        'scholarship', 'fellowship', 'grant', 'stipend', 'financial-aid',
        'financial assistance', 'schemes', 'yojana', 'shishavrutti', 'bursary'
    ]

    def __init__(self):
        self.scraper = WebScraper()
        self.discovered_urls = set()

    def discover_candidates_from_page(self, base_url: str, html_text: str = "") -> List[Dict[str, Any]]:
        """
        Parses page links, filters relevant scholarship URLs, and classifies their source types.
        """
        candidates = []
        if not html_text:
            page_data = self.scraper.fetch_page(base_url)
            if page_data["status_code"] != 200:
                return candidates
            parsed = self.scraper.parse_content(base_url, page_data["raw_html"])
            links = parsed["links"]
        else:
            parsed = self.scraper.parse_content(base_url, html_text)
            links = parsed["links"]

        for item in links:
            url = item["url"]
            text = item["text"].lower()
            
            # Normalize URL
            parsed_u = urlparse(url)
            clean_url = f"{parsed_u.scheme}://{parsed_u.netloc}{parsed_u.path}"

            if clean_url in self.discovered_urls:
                continue

            # Check keyword relevance in URL or link text
            is_relevant = any(kw in clean_url.lower() or kw in text for kw in self.SCHOLARSHIP_KEYWORDS)
            
            if is_relevant:
                self.discovered_urls.add(clean_url)
                classification = SourceClassifier.classify_url(clean_url)
                candidates.append({
                    "url": clean_url,
                    "anchor_text": item["text"],
                    "discovered_from": base_url,
                    "domain": classification["domain"],
                    "source_type": classification["source_type"],
                    "is_official": classification["is_official"],
                    "authenticity_score": classification["authenticity_score"],
                    "reason": classification["reason"]
                })

        return candidates

    def run_discovery_pipeline(self) -> List[Dict[str, Any]]:
        """
        Executes discovery workflow starting from SEED_SOURCES and returning classified candidates.
        """
        all_candidates = []
        for seed in SEED_SOURCES:
            classification = SourceClassifier.classify_url(seed["url"])
            candidate = {
                "url": seed["url"],
                "application_url": seed.get("application_url", ""),
                "provider": seed["provider"],
                "title": seed["title"],
                "source_type": classification["source_type"],
                "domain": classification["domain"],
                "is_official": classification["is_official"],
                "authenticity_score": classification["authenticity_score"],
                "reason": classification["reason"]
            }
            all_candidates.append(candidate)
        return all_candidates
