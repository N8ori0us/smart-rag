from app.processors.document_manager import DocumentManager

class SyncOrchestrator:
    def __init__(self, data_dir: str) -> None:
        self.doc_manager = DocumentManager(data_dir=data_dir)

    def execute_filesystem_sync(self, core_engine) -> dict:
        """Crawls directories and streams fresh documentation coordinates into Qdrant."""
        chunks = self.doc_manager.read_local_documents()
        sync_success = core_engine.vector_client.sync_documents(chunks)

        if sync_success:
            return {
                "status": "success",
                "message": "Local knowledge base successfully indexed into vector storage.",
                "indexed_chunks_count": len(chunks)
            }
        return {
            "status": "failed",
            "message": "Ingestion loop failed to establish network contact with database container."
        }
