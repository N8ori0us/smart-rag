class IntentClassifier:
    @staticmethod
    def is_live_query(user_prompt: str) -> bool:
        """Programmatically checks if user prompt tokens flag an active internet sourcing requirement."""
        live_tokens = ["latest", "current", "news", "status", "who is", "benchmark", "update"]
        return any(token in user_prompt.lower() for token in live_tokens)
