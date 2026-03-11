from __future__ import annotations

import socket
import sys
import threading
import time
import urllib.request
from pathlib import Path

import uvicorn
import webview
from fastapi.staticfiles import StaticFiles
import justls.ics.api as ics_api

app = ics_api.app

HOST = "127.0.0.1"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"
UI_URL = f"{BASE_URL}/ui/?desktop=1"

backend_server = None
backend_thread = None


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def bundle_dir() -> Path:
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def ensure_ui_mount() -> None:
    existing_paths = {getattr(route, "path", None) for route in app.routes}
    if "/ui" in existing_paths:
        return

    ui_dir = bundle_dir() / "ui"
    if ui_dir.is_dir() and (ui_dir / "index.html").is_file():
        app.mount("/ui", StaticFiles(directory=str(ui_dir), html=True), name="ui-desktop")
    else:
        raise RuntimeError(f"UI directory missing for desktop runtime: {ui_dir}")


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


class ThreadedUvicornServer(uvicorn.Server):
    def install_signal_handlers(self) -> None:
        return


def start_backend() -> None:
    global backend_server, backend_thread

    if backend_thread is not None and backend_thread.is_alive():
        return

    ensure_ui_mount()

    config = uvicorn.Config(
        app=app,
        host=HOST,
        port=PORT,
        log_level="info",
        access_log=True,
        reload=False,
    )

    backend_server = ThreadedUvicornServer(config=config)
    backend_thread = threading.Thread(
        target=backend_server.run,
        name="uvicorn-backend",
        daemon=True,
    )
    backend_thread.start()


def stop_backend() -> None:
    global backend_server, backend_thread

    if backend_server is not None:
        backend_server.should_exit = True

    if backend_thread is not None and backend_thread.is_alive():
        backend_thread.join(timeout=5)

    backend_server = None
    backend_thread = None


def main() -> None:
    if not is_port_open(HOST, PORT):
        start_backend()

    if not wait_http(UI_URL, timeout=30.0):
        stop_backend()
        raise RuntimeError(f"Backend/UI did not become ready: {UI_URL}")

    webview.settings["REMOTE_DEBUGGING_PORT"] = 9222
    webview.settings["OPEN_DEVTOOLS_IN_DEBUG"] = False

    webview.create_window(
        title="JUST 长缝光谱仪控制",
        url=UI_URL,
        width=1440,
        height=960,
        min_size=(1200, 800),
    )

    try:
        webview.start(gui="edgechromium", debug=True)
    finally:
        stop_backend()


if __name__ == "__main__":
    main()