import json
import urllib.request
from app.model_client import get_embedding
from app.config import COLLECTION_NAME

class VectorClient:
    def __init__(self, collection_name="smart_rag_collection"):
        self.collection_name = collection_name
        self.base_url = "http://qdrant_db:6333"

    def create_collection(self):
        # Explicitly initializes the 1536-dim vector table inside Qdrant if it is missing.
        url = f"{self.base_url}/collections/{self.collection_name}"
        payload = {
            "vectors": {
                "size": 1536,
                "distance": "Cosine"
            }
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="PUT"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                print(f" [Qdrant Setup]: Created collection '{self.collection_name}' successfully.")
                return True
        except Exception:
            # Collection already exists, proceed quietly
            return True

    def sync_documents(self, chunks):
        # Push an array of text chunks into the database collection as vector points.
        # Ensure the vector table exists first
        self.create_collection()
        
        if not chunks:
            print("  [Vector Client]: No chunks provided to index.")
            return False

        points = []
        print(f" [Vector Client]: Transforming {len(chunks)} chunks into vector points...")

        for idx, chunk in enumerate(chunks):
            vector_array = get_embedding(chunk["content"])
            points.append({
                "id": idx + 1,
                "vector": vector_array,
                "payload": {
                    "source": chunk["source"],
                    "content": chunk["content"]
                }
            })

        points_url = f"{self.base_url}/collections/{self.collection_name}/points"
        payload = {"points": points}

        try:
            req = urllib.request.Request(
                points_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="PUT"
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                print(f"🚀 [Vector Client]: Successfully indexed {len(points)} points into Qdrant.")
                return True
        except Exception as e:
            print(f"  [Vector Client Failure]: Ingestion streaming crashed: {str(e)}")
            return False

    def search_similarity(self, query_text, top_k=3):
        # Generates a query vector and hits Qdrant's local REST API to execute a geometric search.
        query_vector = get_embedding(query_text)

        url = f"http://qdrant_db:6333/collections/{COLLECTION_NAME}/points/search"
        payload = {
            "vector": query_vector,
            "limit": top_k,
            "with_payload": True
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type":"application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                results = res_data.get("result", [])
                
                # THE CONTRACT: Collect raw primitive data structures, zero text formatting
                selected_chunks = []
                for hit in results:                  
                    selected_chunks.append({
                        "score": hit.get("score", 0.0),
                        "payload_data": hit.get("payload", {}),
                        "source": hit.get("payload", {}).get("source", "unknown"),
                        "content": hit.get("payload", {}).get("content", "")
                    })
                return selected_chunks
            
        except Exception as e:
            return []
