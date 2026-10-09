import os
import time
from app.config import API_KEY, MODEL_TIERS
from app.model_client import send_prompt_to_server
from app.session_manager import SessionManager
from app.vector_client import VectorClient


class RagEngine:
    def __init__(self):
        self.vector_client = VectorClient()

        # Dynamic path topography: check if executing locally on a Mac, inside Docker, or bare Linux host
        if os.getenv("RUNNING_LOCAL_MAC") == "true":
            self.session_manager = SessionManager(history_file="./data/history.json")
        elif os.path.exists("/.dockerenv") or os.path.exists("/app"):
            self.session_manager = SessionManager(history_file="/app/data/history.json")
        else:
            self.session_manager = SessionManager(history_file="./data/history.json")

        session = self.session_manager.load_session()
        self.mode = session["mode"]
        self.counter = session["counter"]
        self.history = session["history"]

    def get_system_prompt(self):
        if self.mode == "ideate":
            return (
                "You are an empathetic, highly analytical, creative ideation assistant,"
                "engineering collaborator, and teacher.Provide innovative and out-of-the-box"
                "ideas to help define nebulous and ambiguous thoughts. Propose actionable" 
                "potential design and development solutions. Keep their pace do not"
                "rush ahead and ask clarifying questions to ensure you understand the"
                "needs, goals, and intention and offer to provide step by step guidance."
            )
        else:
            return (
                "You are a pragmatic, straight-forward coding engineer and logic-based auditor. "
                "Answer queries strictly using only verified technical data, context, or"
                "historical relevance/precedent. Directly challenge malformed premises. Maintain"
                "professional demeanor and uphold integrity to the facts and the truth without"
                "compromising accuracy or objectivity or otherwise succumbing to customer"
                "service sycophantic acquiescence. Provide set by step guidance, do not rush"
                "ahead, and ask clarifying quetions to verify comprehension and confirm the"
                "status of the tasks progress to ensure and maintain project alignment."
            )
        
    def submit_query(self, user_prompt, use_rag=True):
        if not API_KEY:
            return "Error: Local .env is missing or OPENROUTER_API_KEY is uninitialized."
        
        model_target = MODEL_TIERS[self.mode]
        system_rules = self.get_system_prompt()
        
        local_context = ""
        if use_rag:
            # Catch the list of dictionaries from the database client utility
            raw_chunks = self.vector_client.search_similarity(user_prompt)
            
            # Map the text layout here, inside the Orchestration/RAG domain layer
            formatted_segments = []
            for chunk in raw_chunks:
                formatted_segments.append(
                    f"[{chunk['source']} (Database Semantic Score: {chunk['score']:.4f})]:\n{chunk['content']}\n---"
                )
            
            if formatted_segments:
                local_context = "\n\n".join(formatted_segments)

        if local_context:
            final_content = f"Context Data:\n{local_context}\n\nUser Query: {user_prompt}"
        else:
            final_content = user_prompt

        messages = [{"role": "system", "content": system_rules}]
        for past_turn in self.history:
            messages.append(past_turn)
            
        messages.append({"role": "user", "content": final_content})
        
        payload = {
            "model": model_target,
            "messages": messages
        }

        # Track total script runtime start point
        start_time = time.time()

        # Fire request and receive the live data packet dictionary
        network_result = send_prompt_to_server(payload)

        # Drop out safely if the underlying network client handles a hard connection drop
        if isinstance(network_result, str) and network_result.startswith("Error"):
            return {"error": network_result}
        
        # Evaluate the Turn Interceptor state change
        interceptor_active = False
        if self.mode == "ideate":
            self.counter += 1
            if self.counter >= 5:
                interceptor_active = True
                self.counter = 0

        total_elapsed = time.time() - start_time

        # THE DATA CONTRACT: Pack fields into predictable dictionary keys for the UI layer
        unified_output = {
            "response": {
                "content": network_result["content"],
                "mode_executed": self.mode
            },
            "interceptor": {
                "triggered": interceptor_active,
                "action_required": "workspace_notification" if interceptor_active else "none"
            },
            "metrics": {
                "api_latency_seconds": network_result["latency"],
                "total_runtime_seconds": total_elapsed,
                "model_target": model_target
            }
        }

        # Commit transaction history and state parameters to local storage disk file
        self.history.append({"role": "user", "content": user_prompt})
        self.history.append({"role": "assistant", "content": network_result["content"]})
        self.session_manager.save_session(self.mode, self.counter, self.history)

        return unified_output

engine = RagEngine()
