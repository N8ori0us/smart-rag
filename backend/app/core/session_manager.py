from app.core.session_storage import SessionStorage

class SessionManager:
    def __init__(self, history_file: str = "/app/data/history.json") -> None:
        # Inject the dedicated low-level storage client component
        self.storage = SessionStorage(history_file=history_file)

    def load_session(self) -> dict:
        """Coordinates structural state hydration and enforces business fallback rules."""
        data = self.storage.read_raw_data()
        
        # Enforce predictable state shape primitives and system defaults
        if data is None:
            return {"mode": "ideate", "counter": 0, "history": []}

        print(" [Persistence] Successfully hydrated state machine memory from history.json.")
        return {
            "mode": data.get("mode", "ideate"),
            "counter": data.get("counter", 0),
            "history": data.get("history", [])
        }

    def save_session(self, mode: str, counter: int, history: list) -> bool:
        """Packages live application variables into a clean state dictionary layout."""
        session_blueprint = {
            "mode": mode,
            "counter": counter,
            "history": history
        }
        return self.storage.write_raw_data(session_blueprint)
