import subprocess
import sys
import os
import webbrowser
import time


# ----------------------------
# Paths (adjust if needed)
# ----------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
BACKEND_MAIN = os.path.join(PROJECT_ROOT, "backend", "main.py")

# ----------------------------
# Start backend function
# ----------------------------
def start_backend():
    print("Starting FastAPI backend on http://localhost:8000 ...")
    subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--reload"], cwd=PROJECT_ROOT)

# ----------------------------
# Start frontend function
# ----------------------------
def start_frontend():
    print("Starting frontend HTTP server on http://localhost:5500 ...")
    os.chdir(FRONTEND_DIR)
    subprocess.Popen([sys.executable, "-m", "http.server", "5500"])

# ----------------------------
# Open browser
# ----------------------------
def open_browser():
    time.sleep(2)  # wait a moment for servers to start
    webbrowser.open("http://localhost:5500/index.html")

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    start_backend()
    start_frontend()
    open_browser()
    print("Backend + Frontend running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
