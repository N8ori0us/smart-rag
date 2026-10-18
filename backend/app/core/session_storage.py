import os
import json

class SessionStorage:
    def __init__(self, history_file: str = "/app/data/history.json") -> None:
        self.history_file = history_file

    def read_raw_data(self) -> dict | None:
        """Natively handles file reading operations from the storage platter."""
        if not os.path.exists(self.history_file):
            return None
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f" [Persistence Error] Failed to read state save file: {str(e)}")
            return None

    def write_raw_data(self, data: dict) -> bool:
        """Natively handles serializing session data maps back onto the host disk."""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f" [Persistence Error] Failed to write state save file: {str(e)}")
            return False
