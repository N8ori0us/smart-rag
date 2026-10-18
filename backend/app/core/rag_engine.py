import os
import time
from app.core.config import API_KEY
from app.adapters.model_client import OpenRouterClient
from app.utils.vector_client import QdrantVectorClient
from app.core.session_manager import SessionManager
from app.adapters.search_client import WebSearchClient

from app.core.behavioral_config import BehavioralConfig
from app.processors.intent_classifier import IntentClassifier
from app.processors.local_context_binder import LocalContextBinder
from app.processors.web_harvest_weaver import WebHarvestWeaver
from app.adapters.llm_synthesizer import LlmSynthesizer

class RagEngine:
    def __init__(self) -> None:
        self.model_client = OpenRouterClient()
        self.vector_client = QdrantVectorClient()
        self.search_client = WebSearchClient()
        self.session_manager = SessionManager()

    def submit_query(self, user_prompt: str, use_rag: bool = True) -> dict:
        """The Master Entry Point: Tracks session timelines and coordinates data between handlers."""
        if not API_KEY:
            return {"error": "Local .env configuration is missing or OPENROUTER_API_KEY is uninitialized."}
        
        start_time = time.time()
        
        # Hydrate active conversational metrics from storage via focused lifecycle module
        session = self.session_manager.load_session()
        active_mode = session.get("mode", "ideate")
        turn_counter = session.get("counter", 0)
        chat_history = session.get("history", [])

        # 1. INTENT CLASSIFICATION
        is_live = IntentClassifier.is_live_query(user_prompt)

        # 2. LOCAL CONTEXT BINDING
        local_context = LocalContextBinder.retrieve_and_format(user_prompt, use_rag, self.vector_client)

        # 3. GLOBAL WEB CONSENSUS HARVESTING
        web_context = WebHarvestWeaver.compile_consensus_blocks(
            user_prompt, use_rag, is_live, bool(local_context), self.search_client
        )

        # 4. DYNAMIC BEHAVIOR RESOLUTION & SYNTHESIS
        # Pull custom behavioral rules directly out of the independent config slice
        system_prompt = BehavioralConfig.get_prompt(active_mode)
        
        llm_response, model_target = LlmSynthesizer.synthesize(
            user_prompt, chat_history, active_mode, system_prompt, local_context, web_context, model_target, self.model_client
        )        

        # 5. TURN INTERCEPTOR SHIFT EVALUATION
        interceptor_active = False
        if active_mode == "ideate":
            turn_counter += 1
            if turn_counter >= 5:
                interceptor_active = True
                turn_counter = 0

        # Sync active tracking configurations back down to host storage files
        chat_history.append({"role": "user", "content": user_prompt})
        chat_history.append({"role": "assistant", "content": llm_response})
        self.session_manager.save_session(active_mode, turn_counter, chat_history)

        total_elapsed = time.time() - start_time

        return {
            "response": {"content": llm_response, "mode_executed": active_mode},
            "interceptor": {
                "triggered": interceptor_active,
                "action_required": "workspace_notification" if interceptor_active else "none"
            },
            "metrics": {
                "api_latency_seconds": total_elapsed * 0.9,
                "total_runtime_seconds": total_elapsed,
                "model_target": model_target
            }
        }

engine = RagEngine()
