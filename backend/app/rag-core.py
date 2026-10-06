import os
import sys
import json
import urllib.request

class ConversationEngine:
    def __init__(self):
        # Establish structural defaults matching README.md protocols
        self.mode = "ideate"    # Tracks: "ideate" or "execute" modes
        self.counter = 0        # Tracks the number of interactions
        self.history = []       # Stores the conversation history
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model_target = "google/gemini-1.5-flash"

    def get_system_prompt(self):
        # Dynamically altrnate prompt framework based on the current mode
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
        
    def submit_query(self, user_prompt, local_context=""):
        # Check security perimeter for the OpenRouter API authorization mask
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return "Error: Local .env is missing or OPENROUTER_API_KEY is uninitialized."
        
        # Manage loop interception automation
        if self.mode=="ideate":
            self.counter += 1

        #Compile system payloads using native Python standard network libraries
        system_rules = self.get_system_prompt()
        full_context = f"Context:\n{local_context}n\nQuery : {user_prompt}" if local_context else user_prompt
        
        #Build the standard message payload structure
        messages =[
            {"role": "system", "content": system_rules},
        ]

        # Append historical context logs sequentially to maintain memory parity
        for past_count in self.history:
            messages.append(past_count)

        # Add the current query block to the tail of the message stream        
        messages.append({"role": "user", "content": full_context})

        #Set up stabdard OpenRouter authorization headers
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8080",
            "X-Title": "smart-rag-engine"
        }
        
        payload = {
            "model": self.model_target,
            "messages": messages
        }

        # Check for loop interceptor thresholds before executing network calls
        interceptor_active = False
        if self.mode == "ideate" and self.counter >= 5:
            interceptor_active = True
            self.counter = 0

        # Send the request and handle the response natively via urllib
        try:
            req = urllib.request.Request(
                self.api_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                ai_response = res_data['choices'][0]['message']['content']

                # Commit successful transaction to persistent history logs
                self.history.append({"role": "user", "content": user_prompt})
                self.history.append({"role": "assistant", "content": ai_response})

            # Append interceptor alerts to the final output if flagged
            if interceptor_active:
                alert_prefix = "\n\n🚨 [This line of inquery has been logged for later review. do you want to continue this now or get back to what you were doing in execution mode?]"
                return ai_response + alert_prefix

            return ai_response
        except Exception as e:
            return f"An error occurred during the request: {str(e)}"

# Instantiates the baseline instance of the state machine
engine = ConversationEngine()
