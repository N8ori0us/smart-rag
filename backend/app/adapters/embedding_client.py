import json
import urllib.request
from app.core.config import HEADERS

def get_embedding(text: str | list) -> list[float]:
    """Transforms raw text string vectors into 1536-dimensional float coordinate arrays."""
    url = "https://openrouter.ai"
    payload = {
        "model": "openai/text-embedding-3-small",
        "input": [text] if isinstance(text, str) else text    
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=HEADERS,
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            data_list = res_data.get("data", [])
            if isinstance(data_list, list) and len(data_list) > 0:
                return data_list[0].get("embedding", [0.0] * 1536)
            return [0.0] * 1536
    except Exception as e:
        print(f" [Embedding Failure]: {str(e)}")
        return [0.0] * 1536
