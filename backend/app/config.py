import os

# API Configurations
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    # Explicitly calculate the absolute workspace root path dynamically at runtime
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(current_dir)
    root_dir = os.path.dirname(backend_dir)
    
    for env_path in [
        os.path.join(root_dir, ".env"),
        os.path.join(backend_dir, ".env"),
        ".env"
    ]:
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
