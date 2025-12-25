import os
import requests
import json
import logging
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VlexClient")

class VlexClient:
    """
    Client for interacting with the vLex API.
    Reference: https://api.vlex.com/api/v1
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.vlex.com/api/v1"):
        self.api_key = api_key or os.environ.get("VLEX_API_KEY")
        if not self.api_key:
            logger.warning("VLEX_API_KEY not found in environment or arguments.")
        
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def search(self, query: str, jurisdiction: str = "us_federal", limit: int = 10) -> Dict[str, Any]:
        """
        Search for legal documents.
        """
        url = f"{self.base_url}/search"
        params = {
            "q": query,
            "jurisdiction": jurisdiction,
            "limit": limit
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Search failed: {e}")
            return {"error": str(e), "results": []}

    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """
        Retrieve full document or metadata by vLex ID.
        """
        url = f"{self.base_url}/documents/{doc_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve document {doc_id}: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    # Example usage for CLI testing
    import sys
    client = VlexClient()
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(json.dumps(client.search(query), indent=2))
