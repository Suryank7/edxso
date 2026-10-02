import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Any, List, Optional
import time
from urllib.parse import urljoin, urlparse

class WebScraper:
    """
    Robust web scraper for static and dynamic HTML pages.
    Extracts structured DOM content, text blocks, application links, and table data.
    """

    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    def __init__(self, timeout: int = 15, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def fetch_page(self, url: str) -> Dict[str, Any]:
        """
        Fetch HTML content from a target URL with automatic retries and error handling.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    return {
                        "url": url,
                        "status_code": 200,
                        "raw_html": response.text,
                        "content_type": response.headers.get('Content-Type', ''),
                        "error": None
                    }
                elif response.status_code in [404, 410]:
                    return {
                        "url": url,
                        "status_code": response.status_code,
                        "raw_html": "",
                        "error": f"Page Not Found or Removed (HTTP {response.status_code})"
                    }
            except Exception as e:
                retries += 1
                time.sleep(1.0 * retries)
        
        return {
            "url": url,
            "status_code": 500,
            "raw_html": "",
            "error": f"Failed after {self.max_retries} attempts"
        }

    def parse_content(self, url: str, raw_html: str) -> Dict[str, Any]:
        """
        Parse HTML content into structured text blocks, headings, meta tags, and links.
        """
        if not raw_html:
            return {"title": "", "text_blocks": [], "links": [], "tables": []}

        soup = BeautifulSoup(raw_html, 'html.parser')
        
        # Remove script and style elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        
        # Extract headings and main paragraphs
        text_blocks = []
        for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'td']):
            txt = p.get_text(strip=True)
            if len(txt) > 15:
                text_blocks.append(txt)

        # Extract outlinks (especially official portals and application links)
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(url, href)
            link_text = a.get_text(strip=True)
            if full_url.startswith("http"):
                links.append({"url": full_url, "text": link_text})

        # Extract structured table contents (often contains eligibility or dates)
        tables = []
        for table in soup.find_all('table'):
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            if rows:
                tables.append(rows)

        return {
            "title": title,
            "text_blocks": text_blocks,
            "full_text": "\n".join(text_blocks),
            "links": links,
            "tables": tables
        }
