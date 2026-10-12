import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from app.rag_engine import RagEngine

engine = RagEngine()

class FastApiAdapter(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/query":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    self.send_error(400, "Empty payload context recieved.")
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
                self.send_header("Content-Type", str(len(response_bytes)))
                self.end_headers()
                self.wfile.write(response_bytes)

            except json.JSONDecodeError:
                self.send_error_packet(400, "Malformed request payload: Invalid JSON structure.")
            except Exception as e:
                self.send_error_packet(500, f"Internal Pipeline Server Failure: {str(e)}")
        else:
                self.send_error_packet(500, f"Port slot endpoint route '{self.path}' not found.")

    def send_error_packet(self, status_code, error_message):
        error_payload = {
            "error": error_message,
            "status_code": status_code
        }
        response_bytes = json.dumps(error_payload).encode('utf-8')
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Type", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

def run_api_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FastApiAdapter)
    print(f"[REST API Gateway Active]: Serving endpoints natively on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nAPI Gatewat shutting down cleanly.")
        httpd.server_close()

if __name__ == "__main__":
    run_api_server()