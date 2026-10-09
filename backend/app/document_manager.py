import os

class DocumentManager:
    def __init__(self, data_dir="/app/data"):
        self.data_dir = data_dir

    def read_local_documents(self):
        # Crawls your local data folder to find all markdown and text assets.
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
        # Splits raw text strings into fixed-size overlapping character segments.
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
