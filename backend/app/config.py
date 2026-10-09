import os

# API Configurations
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

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
