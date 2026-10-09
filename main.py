import os
import sys

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.cli_interface import TerminalInterface

def main():

    try:
        app = TerminalInterface()
        app.launch()
    except Exception as startup_error:
        print(f"[Fatal Boot Error] System failed to initialize: {str(startup_error)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
