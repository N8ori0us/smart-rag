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
        all_chunks = self.read_local_documents()
        scored_chunks = []
        query_words = set(query.lower().split())

        for chunk in all_chunks:
            score = 0 
            content_lower = chunk["content"].lower()
            for word in query_words:
                if word in content_lower:
                    score += 1
            if score > 0:
                scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        selected_chunks = [
            f"[{chunk['source']}]:\n{chunk['content']}\n---"
            for _, chunk in scored_chunks[:top_k]
        ]
        return "\n\n".join(selected_chunks)
