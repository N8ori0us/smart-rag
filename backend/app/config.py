import os

# API Configurations
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Browser Integrity Spoof Headers
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "HTTP-Referer": "http://localhost:8080",
    "X-Title": "smart-rag-engine"
}

# Dynamic Model Assignments
MODEL_TIERS = {
    "ideate": "nvidia/nemotron-3.5-lightning:free",
    "execute": "cohere/north-mini-code:free"
}
