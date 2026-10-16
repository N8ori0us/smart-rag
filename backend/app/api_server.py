import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app.rag_engine import engine
from document_manager import DocumentManager 

doc_manager = DocumentManager(data_dir="/app/data" if os.path.exists("/app") else "./data")

class FastApiAdapter(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/query":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    self.send_error_packet(400, "Empty payload context received.")
                    return

                raw_body = self.rfile.read(content_length).decode('utf-8')
                body_data = json.loads(raw_body)

                user_prompt = body_data.get("prompt", "").strip()
                use_rag = body_data.get("use_rag", True)

                if not user_prompt:
                    self.send_error_packet(400, "Missing string token field: 'prompt'")
                    return
                
                output_packet = engine.submit_query(user_prompt, use_rag=use_rag)

                response_bytes = json.dumps(output_packet, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(response_bytes)))
                self.end_headers()
                self.wfile.write(response_bytes)

            except json.JSONDecodeError:
                self.send_error_packet(400, "Malformed request payload: Invalid JSON structure.")
            except Exception as e:
                self.send_error_packet(500, f"Internal Pipeline Server Failure: {str(e)}")
        elif self.path == "/sync":
            try:
                print("\n [Headless Ingestion Activated]: Scanning filesystem directories...")

                chunks = doc_manager.read_local_documents()

                sync_success = engine.vector_client.sync_documents(chunks)

                if sync_success:
                    sync_response = {
                        "status": "success",
                        "message": "Local knowledge base successfully indexed into vector storage.",
                        "indexed_chunks_count": len(chunks)
                    }
                    status_code = 200
                else:
                    sync_response = {
                        "status": "failed",
                        "message": "Ingestion loop failed to establish network contact with database container.",
                    }
                    status_code = 500

                response_bytes = json.dumps(sync_response, ensure_ascii=False).encode('utf-8')
                self.send_response(status_code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(response_bytes)))
                self.end_headers()
                self.wfile.write(response_bytes)    

            except Exception as e:
                self.send_error_packet(500, f"Headless Ingestion Failure: {str(e)}")
        else:
            self.send_error_packet(404, f"Port slot endpoint route '{self.path}' not found.")

    def send_error_packet(self, status_code, error_message):
        error_payload = {
            "error": error_message,
            "status_code": status_code
        }
        response_bytes = json.dumps(error_payload).encode('utf-8')
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

def run_api_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FastApiAdapter)
    print(f"[REST API Gateway Active]: Serving endpoints natively on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nAPI Gateway shutting down cleanly.")
        httpd.server_close()

if __name__ == "__main__":
    run_api_server()