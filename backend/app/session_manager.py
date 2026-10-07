import os
import json

class SessionManager:
    def __init__(self, history_file="/app/data/history.json"):
        self.history_file = history_file

    def load_session(self):
        """Reads the filesystem layout state natively to restore past context structures."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"💾 [Persistence] Successfully hydrated state machine memory from history.json.")
                    return {
                        "mode": data.get("mode", "ideate"),
                        "counter": data.get("counter", 0),
                        "history": data.get("history", [])
                    }         
            except Exception as e:
                print(f"⚠️ [Persistence Error] failed to read state save file: {str(e)}")

        # Safe default state fallbacks if no file exists
        return {"mode": "ideate", "counter": 0, "history": []}

    def save_session(self, mode, counter, history):
        """Serialize the live session parameters directly to flat text on the platter"""
        try:
            data = {
                "mode": mode,
                "counter": counter,
                "history": history
            }
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ [Persistence Error] failed to write state save file: {str(e)}")