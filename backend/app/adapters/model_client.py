import json
import time
import urllib.request
import urllib.error
from app.core.config import API_URL, HEADERS

class OpenRouterClient:
    def generate_completion(self, prompt_content: str, system_instruction: str, model_target: str) -> str:
        """Dispatches dynamic prompt payload message arrays upstream to OpenRouter handles."""
        payload = {
            "model": model_target,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt_content}
            ]
        }
        
        max_retries = 3
        backoff_delay = 2
        start_network_time = time.time()

        for attempt in range(max_retries + 1):
            try:
                req = urllib.request.Request(
                    API_URL,
                    data=json.dumps(payload).encode("utf-8"),
                    headers=HEADERS,
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    choices = res_data.get('choices', [])
                    
                    if isinstance(choices, list) and len(choices) > 0:
                        return choices[0].get('message', {}).get('content', '')
                    return res_data.get('choices', {}).get('message', {}).get('content', '')

            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < max_retries:
                    print(f" [429 Rate Limited] Retry {attempt + 1}/{max_retries}. Pausing {backoff_delay}s...")
                    time.sleep(backoff_delay)
                    backoff_delay *= 2
                    continue
                return f"An HTTP error occurred during the request: {e.code} - {e.reason}"
            except Exception as e:
                return f"An error occurred during the request: {str(e)}"
        
        return "Error: Maximum retry limit reached."
