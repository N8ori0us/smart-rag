import json
import time
import urllib.request
import urllib.error
from app.config import API_URL, HEADERS

def get_embedding(text):
    # Sends a text chunk over the wire to generate its mathematical array.
    from app.config import API_KEY, HEADERS
    import json
    import urllib.request

    url = "https://openrouter.ai/api/v1/embeddings"

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
        print(f"⚠️  [Embedding Failure]: {str(e)}")
        return [0.0] * 1536

def send_prompt_to_server(payload):
    max_retries = 3
    backoff_delay = 2
    start_total_time = time.time()

    for attempt in range(max_retries + 1):
        try:
            start_network_time = time.time()
            req = urllib.request.Request(
                API_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers=HEADERS,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                
                # FIX: Fallback gracefully to handle both array lists and direct dictionary structures
                choices = res_data.get('choices', [])
                if isinstance(choices, list) and len(choices) > 0:
                    ai_response = choices[0].get('message', {}).get('content', '')
                else:
                    ai_response = res_data.get('choices', {}).get('message', {}).get('content', '')

                end_time = time.time()
                latency = end_time - start_network_time
                total_elapsed = end_time - start_total_time

                print(f"\n⏱️  [Metrics - API Latency: {latency:.2f}s | Total Script Runtime: {total_elapsed:.2f}s]")
                return {
                    "content": ai_response,
                    "latency": latency,
                    "total_elapsed": total_elapsed
                }

        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                print(f"\n⚠️  [429 Rate Limited] Retry {attempt + 1}/{max_retries}. Pausing for {backoff_delay}s...")
                time.sleep(backoff_delay)
                backoff_delay *= 2
                continue
            return f"An HTTP error occurred during the request: {e.code} - {e.reason}"
        except Exception as e:
            return f"An error occurred during the request: {str(e)}"
    
    return "Error: Maximum retry limit reached."
