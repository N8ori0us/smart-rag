import os

class DocumentManager:
    def __init__(self, data_dir="/app/data"):
        self.data_dir = data_dir

    def read_local_documents(self):
        chunks = []
        if not os.path.exists(self.data_dir):
            return chunks 

        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith((".md", ".txt")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            text = f.read()
                            chunks.extend(self.chunk_text(text, source_name=file))
                    except Exception as e:
                        print(f"⚠️  [Ingestion Warning] Could not read {file}: {str(e)}")
        return chunks

    def chunk_text(self, text, size=500, overlap=100, source_name=""):
        file_chunks = []
        start = 0
        while start < len(text):
            end = min(start + size, len(text))
            segment = text[start:end]
            file_chunks.append({
                "source": source_name, 
                "content": segment.strip()
            })
            start += (size - overlap)
        return file_chunks

    def retrieve_context(self, query, top_k=3):
        """Generates a query embedding and calculates cosine similarities across your documents."""
        import math
        from app.model_client import get_embedding

        # 1. Transform the user's active search query into high-dimensional vector space
        query_vector = get_embedding(query)
        
        # Calculate query magnitude (|B|) natively
        query_mag = math.sqrt(sum(q * q for q in query_vector))
        if query_mag == 0:
            return ""

        all_chunks = self.read_local_documents()
        scored_chunks = []

        for chunk in all_chunks:
            # 2. Transform the local document text chunk into a matching vector array over the wire
            chunk_vector = get_embedding(chunk["content"])
            
            # 3. Calculate Dot Product (A · B) and Chunk Magnitude (|A|) simultaneously
            dot_product = 0.0
            chunk_sum_sq = 0.0
            
            for q, c in zip(query_vector, chunk_vector):
                dot_product += q * c
                chunk_sum_sq += c * c
                
            chunk_mag = math.sqrt(chunk_sum_sq)
            if chunk_mag == 0:
                continue

            # 4. Compute the geometric Cosine Similarity score
            cosine_similarity = dot_product / (chunk_mag * query_mag)
            scored_chunks.append((cosine_similarity, chunk))

        # Sort chunks sequentially from highest semantic correlation down to lowest
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        selected_chunks = [
            f"[{chunk['source']} (Semantic Match Score: {score:.4f})]:\n{chunk['content']}\n---"
            for score, chunk in scored_chunks[:top_k]
        ]
        return "\n\n".join(selected_chunks)
