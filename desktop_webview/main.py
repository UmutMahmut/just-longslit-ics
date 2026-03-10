import os
import sys
import time
import signal
import socket
import pathlib
import subprocess
import urllib.request
import webview

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "just-ls-ics-starter"
LOG_DIR = REPO_ROOT / "desktop_webview" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

HOST = "127.0.0.1"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"
UI_URL = f"{BASE_URL}/ui/?desktop=1"

backend_proc = None

def wait_http(url: str, timeout: float = 30.0) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2.0) as resp:
                if 200 <= resp.status < 500:
                    return True
        except Exception:
            time.sleep(0.5)
    return False

def is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0

def start_backend():
    global backend_proc

    stdout_log = LOG_DIR / "backend_stdout.log"
    stderr_log = LOG_DIR / "backend_stderr.log"

    stdout_f = open(stdout_log, "w", encoding="utf-8")
    stderr_f = open(stderr_log, "w", encoding="utf-8")

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "justls.ics.api:app",
        "--app-dir",
        str(BACKEND_ROOT / "src"),
        "--host",
        HOST,
        "--port",
        str(PORT),
    ]
    backend_proc = subprocess.Popen(
        cmd,
        cwd=str(BACKEND_ROOT),
        stdout=stdout_f,
        stderr=stderr_f,
        env=env,
    )

def stop_backend():
    global backend_proc
    if backend_proc is None:
        return

    try:
        backend_proc.terminate()
        backend_proc.wait(timeout=5)
    except Exception:
        try:
            backend_proc.kill()
        except Exception:
            pass
    finally:
        backend_proc = None

def main():
    if not is_port_open(HOST, PORT):
        start_backend()

    if not wait_http(UI_URL, timeout=30.0):
        stop_backend()
        raise RuntimeError(f"Backend/UI did not become ready: {UI_URL}")

    window = webview.create_window(
        title="JUST 长缝光谱仪控制",
        url=UI_URL,
        width=1440,
        height=960,
        min_size=(1200, 800),
    )

    webview.settings["REMOTE_DEBUGGING_PORT"] = 9222
    webview.settings["OPEN_DEVTOOLS_IN_DEBUG"] = False

    try:
        webview.start(gui="edgechromium", debug=True)
    finally:
        stop_backend()

if __name__ == "__main__":
    main()
