import os

# API Configurations
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    # Check current directory (root) first, then look inside the backend subdirectory
    for env_path in [".env", "backend/.env", "../.env"]:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip() and not line.startswith("#") and "=" in line:
                            key, value = line.strip().split("=", 1)
                            if key.strip() == "OPENROUTER_API_KEY":
                                API_KEY = value.strip().strip("'").strip('"')
                                break
            except Exception:
                pass
        if API_KEY:
            break
        
# Vector Storage Parameters
VECTOR_DB_URL = "http://qdrant_db:6333"
COLLECTION_NAME = "smart_rag_collection"

# Browser Integrity Spoof Headers
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8080",
    "X-Title": "smart-rag-engine"
}

# Dynamic Model Assignments
MODEL_TIERS = {
    "ideate": "nvidia/nemotron-3.5-lightning:free",
    "execute": "cohere/north-mini-code:free"
}
