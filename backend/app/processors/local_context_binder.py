class LocalContextBinder:
    @staticmethod
    def retrieve_and_format(user_prompt: str, use_rag: bool, vector_client) -> str:
        """Queries local vector storage and formats chunks into a unified string context block."""
        if not use_rag:
            return ""

        print("[Orchestration Core]: Querying local vector storage collections...")
        raw_chunks = vector_client.search_similarity(user_prompt, limit=3)
        
        formatted_segments = []
        for chunk in raw_chunks:
            text_content = chunk.get("text_chunk") or chunk.get("content", "")
            source_file = chunk.get("source", "Local Ingestion Platter")
            score_metric = chunk.get("score", 0.0)
            formatted_segments.append(
                f"[{source_file} (Database Semantic Score: {score_metric:.4f})]:\n{text_content}\n---"
            )
        return "\n\n".join(formatted_segments) if formatted_segments else ""
