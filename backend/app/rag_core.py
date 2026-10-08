import os
from app.config import API_KEY, MODEL_TIERS
from app.model_client import send_prompt_to_server
from app.session_manager import SessionManager
from app.vector_client import VectorClient

class ConversationEngine:
    def __init__(self):
        self.vector_client = VectorClient()
        
        # Path routing: check if running locally on Mac or inside server container        
        if os.getenv("RUNNING_LOCAL_MAC") == "true":
            self.session_manager = SessionManager(history_file="./data/history.json")
        else:
            self.session_manager = SessionManager(history_file="/app/data/history.json")
                   
        # Hydrate session parameters cleanly from the dedicated storage manager module
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
        
        if self.mode == "ideate":
            self.counter += 1

        system_rules = self.get_system_prompt()
        
        local_context = ""
        if use_rag:
            local_context = self.vector_client.search_similarity(user_prompt)

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

        interceptor_active = False
        if self.mode == "ideate" and self.counter >= 5:
            interceptor_active = True
            self.counter = 0

        ai_response = send_prompt_to_server(payload)
        
        if not ai_response.startswith("Error") and not ai_response.startswith("An HTTP error"):
            self.history.append({"role": "user", "content": user_prompt})
            self.history.append({"role": "assistant", "content": ai_response})
            
            # Delegate tracking states out to the session module writer
            self.session_manager.save_session(self.mode, self.counter, self.history)

        if interceptor_active:
            alert_prefix = "\n\n🚨 [This line of inquiry has been logged.]" 
            # add to alert_prefix and implement <"Continue now or return to execution mode?">  during interactive build out. 
            return ai_response + alert_prefix

        return ai_response

engine = ConversationEngine()
