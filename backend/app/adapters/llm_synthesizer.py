from app.core.config import MODEL_TIERS

class LlmSynthesizer:
    @staticmethod
    def synthesize(user_prompt: str, chat_history: list, active_mode: str, system_prompt: str, local_context: str, web_context: str, model_client) -> tuple:
        """Assembles prompt wrappers, sets rules, and generates the final OpenRouter completion."""
        model_target = MODEL_TIERS.get(active_mode, "nvidia/nemotron-3.5-lightning:free")

        assembled_context = ""
        if local_context:
            assembled_context += f"--- LOCAL SYSTEMS INSIGHTS ---\n{local_context}\n\n"
        if web_context:
            assembled_context += f"--- GLOBAL WEB CONSENSUS CLUSTERS ---\n{web_context}\n\n"

        final_prompt_payload = user_prompt
        if assembled_context:
            final_prompt_payload = f"{assembled_context}User Direct Question: {user_prompt}"

        llm_response = model_client.generate_completion(
            prompt_content=final_prompt_payload,
            system_instruction=system_prompt,
            model_target=model_target
        )
        return llm_response, model_target
