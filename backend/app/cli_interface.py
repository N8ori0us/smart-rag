import sys
import json
from app.rag_engine import RagEngine
from app.diagnostics import DiagnosticEngine

class TerminalInterface:
    def __init__(self):
        print("[SmartRAG System Init] Starting localized loop...")
        print("Type '/exit' to close, '/diagnose' for a raw readout, or '/audit' for AI health analysis.")
        
        self.engine = RagEngine()
        self.diag_client = DiagnosticEngine()
        print(f"[Active State] Session hydrated. Current Mode: {self.engine.mode.upper()}")

    def launch(self):
        """Runs the continuous command-line transaction loop until an exit token is caught."""
        BOLD_START = "\033[1m"
        BOLD_END = "\033[0m"

        while True:
            try:
                user_input = input(f"\n{BOLD_START}User Prompt > {BOLD_END}").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() == "/exit":
                    print("Exiting runtime test loop. Progress saved cleanly.")
                    sys.exit(0)
                    
                # COMMAND 1: Raw technical data readout (AI is bypassed)
                if user_input.lower() == "/diagnose":
                    print("\n[System Self-Audit] Initializing structural diagnostics...")
                    report = self.diag_client.execute_self_diagnosis()
                    print("\n[Live RAM Diagnostic Data Package Received]")
                    print(json.dumps(report, indent=2, ensure_ascii=False))
                    continue
                
                # COMMAND 2: Full pipeline ingestion (Data is generated and passed to the agent)
                if user_input.lower() == "/audit":
                    print("\n[System Self-Audit] Running hardware and network infrastructure diagnostics...")
                    report = self.diag_client.execute_self_diagnosis()
                    
                    print("\n[Live RAM Diagnostic Data Package Generated]")
                    print(json.dumps(report, indent=2, ensure_ascii=False))
                    
                    print("\nFeeding telemetry matrix to the RAG Engine for analysis...")
                    # Intercept user input and transform it into a direct instruction payload
                    user_input = (
                        f"SYSTEM DIAGNOSTIC COMMAND EXECUTED. Analyze this exact telemetry log "
                        f"and provide an evaluation of my current health status, network latency, "
                        f"and multi-node infrastructure metrics:\n\n{json.dumps(report)}"
                    )
                    
                print(f"Dispatching query to upstream pipeline ({self.engine.mode})...")
                
                # Execute the standard orchestrator conversation path
                output_packet = self.engine.submit_query(user_input, use_rag=False)
                
                if isinstance(output_packet, dict) and "response" in output_packet:
                    print("-" * 50)
                    print(f"Agent Response:\n{output_packet['response']['content']}")
                    print("-" * 50)
                    
                    metrics = output_packet.get("metrics", {})
                    latency = metrics.get("api_latency_seconds", 0.0)
                    runtime = metrics.get("total_runtime_seconds", 0.0)
                    print(f"  [Metrics | API Latency: {latency:.2f}s | Total Script Runtime: {runtime:.2f}s]")
                else:
                    print(f"\n[Pipeline Error]: {output_packet}")
                    
            except KeyboardInterrupt:
                print("\nExecution interrupted by command. Session saved safely.")
                sys.exit(0)
            except Exception as e:
                print(f"\n[Runtime Interface Failure]: {str(e)}")
