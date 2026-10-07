import os
from app.config import API_KEY, MODEL_TIERS
from app.document_manager import DocumentManager
from app.model_client import send_prompt_to_server

class ConversationEngine:
    def __init__(self):
        self.mode = "ideate"    # Tracks: "ideate" or "execute" modes
        self.counter = 0        # Tracks interaction thresholds
        self.history = []       # Stores conversation turns
        self.doc_manager = DocumentManager()

    def get_system_prompt(self):
        if self.mode == "ideate":
            return (
                "You are an empathetic, highly analytical, creative ideation assistant, "
                "engineering collaborator, and teacher. Provide innovative and out-of-the-box "
                "ideas to help define nebulous thoughts. Ask clarifying questions."
            )
        else:
            return (
                "You are a pragmatic, straight-forward coding engineer and logic-based auditor. "
                "Answer queries strictly using verified data. Challenge malformed premises. "
                "Maintain professional demeanor without customer service sycophancy."
            )
        
    def submit_query(self, user_prompt, use_rag=True):
        if not API_KEY:
            return "Error: Local .env is missing or OPENROUTER_API_KEY is uninitialized."
        
        # Pull model assignment dynamically from config map
        model_target = MODEL_TIERS[self.mode]
        
        if self.mode == "ideate":
            self.counter += 1

        system_rules = self.get_system_prompt()
        
        local_context = ""
        if use_rag:
            local_context = self.doc_manager.retrieve_context(user_prompt)

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

        # Pass payload safely over to the model client transport loop
        ai_response = send_prompt_to_server(payload)
        
        if not ai_response.startswith("Error") and not ai_response.startswith("An HTTP error"):
            self.history.append({"role": "user", "content": user_prompt})
            self.history.append({"role": "assistant", "content": ai_response})

        if interceptor_active:
            alert_prefix = "\n\n🚨 [This line of inquiry has been logged. Continue now or return to execution mode?]"
            return ai_response + alert_prefix

        return ai_response

engine = ConversationEngine()
