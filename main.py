import os
import sys

# THE PATH ANCHOR: Point Python directly to backend application directory
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# FIX: Import the updated class name from your new file name
from app.rag_engine import RagEngine

def run_test_loop():
    print("[SmartRAG System Init] Starting localized loop...")
    print("Type '/exit' to close. Current mode dictates your agent.")
    
    # FIX: Instantiate the newly named RagEngine class
    engine = RagEngine()
    print(f"[Active State] Session hydrated. Current Mode: {engine.mode.upper()}")
    
    while True:
        try:
            user_input = input("\nUser Prompt > ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == "/exit":
                print("Exiting runtime test loop. Progress saved cleanly.")
                sys.exit(0)
                
            print(f"Dispatching query to upstream pipeline ({engine.mode})...")
            
            # Execute the orchestrator
            output_packet = engine.submit_query(user_input, use_rag=False)

            if isinstance(output_packet, dict) and "response" in output_packet:
                # CLEAN HUMAN PARSING: Extract and print only the text content response stream
                print(f"\n Agent Response:\n{output_packet['response']['content']}\n")
                
                # Print clean, scannable processing metrics rows below the text block
                metrics = output_packet.get("metrics", {})
                latency = metrics.get("api_latency_seconds", 0.0)
                runtime = metrics.get("total_runtime_seconds", 0.0)
                print(f"  [Metrics | API Latency: {latency:.2f}s | Total Script Runtime: {runtime:.2f}s]")
            else:
                print(f"\n [Pipeline Error]: {output_packet}")
      
        except KeyboardInterrupt:
            print("\nExecution interrupted by command. Session saved safely.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[Runtime Failure]: {str(e)}")

if __name__ == "__main__":
    run_test_loop()
