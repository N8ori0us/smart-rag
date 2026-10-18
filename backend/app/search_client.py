import os
import json
import urllib.request
import urllib.error
from consensus_processor import ConsensusProcessor

class WebSearchClient:
    def __init__(self) -> None:
        self.api_key: str | None = os.getenv("TAVILY_API_KEY")
        self.base_url: str = "https://api.tavily.com"

# Primary endpoints are `/search`, `/extract`, `/crawl`, `/map`, and `/research`.

    def _execute_api_call(self, endpoint: str, payload: dict) -> dict:
        if not self.api_key:
            print("[Search Core Warning]: missing TAVILY_API_KEY. Search bypassed.")
            return {"error": "Missing API configuration."}

        payload["api_key"] = self.api_key
        target_url = f"{self.base_url}{endpoint}"

        try:
            req = urllib.request.Request(
                target_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))

        except urllib.error.URLError as e:
            print(f"[Network Failure]: Failed to clear {endpoint} threshold: {str(e.reason)}")
            return {"error": str(e)}
        except Exception as e:
            print(f"[Runtime Failure]: Exception occurring inside {endpoint} loop {str(e)}")
            return {"error": str(e)}
            
    # === ENDPOINT 1: /search (Unbiased Discovery and Consensus) ===
    def consensus_search(self, query_string: str, sample_size: int = 10) -> dict:
        if not self.api_key:
            print("[Search Core Warning]: missing TAVILY_API_KEY. Search bypassed.")
            return {"consensus_groups": [], "raw_results_count": 0}

        payload = {
            "query": query_string,
            "search_depth" :"advanced",
            "include_answer": False,
            "max_results": sample_size
        }
        raw_data = self._execute_api_call("/search", payload)
        results = raw_data.get("results", [])
        return ConsensusProcessor.cluster_and_rate_perspectives(results, query_string)

    # === ENDPOINT 2: /extract (Headless Text Content Extraction) ===
    def extract_content(self, urls: list[str]) -> dict:
        payload = {"urls": urls, "extract_depth": "basic"}
        return self._execute_api_call("/extract", payload)
    
    # === ENDPOINT 3: /map (Sitemap URL Inventory Tracking) ===    
    def map_urls(self, target_domain: str) -> dict:
        payload = {"url": target_domain}
        return self._execute_api_call("/map", payload)
    
    # === ENDPOINT 4: /crawl (Automated Local Directory Scraping Ingestion) ===    
    def crawl_site(self, target_url: str, max_pages: int = 10) -> dict:
        payload = {"url": target_url, "max_pages": max_pages}
        return self._execute_api_call("/crawl", payload)
    
    # === ENDPOINT 5: /research (Asynchronous Deep Research Agent Engine) ===    
    def deep_research(self, query_string: str,depth: str = "advanced") -> dict:
        payload = {"query": query_string,  "research_depth": depth}
        return self._execute_api_call("/research", payload)
