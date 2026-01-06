from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .routers.capabilities import router as capabilities_router
from .routers.control import router as control_router
from .routers.status import router as status_router

logger = logging.getLogger(__name__)

app = FastAPI(title="JUST Long-Slit ICS", version="0.1.0")

# 路由拆分：推荐做法是 include_router
app.include_router(status_router)
app.include_router(control_router)
app.include_router(capabilities_router)

# UI: 静态托管
BASE_DIR = Path(__file__).resolve().parents[3]  # -> ...\just-ls-ics-starter
UI_DIR = BASE_DIR / "ui"

if UI_DIR.is_dir():
    app.mount("/ui", StaticFiles(directory=str(UI_DIR), html=True), name="ui")
else:
    logger.warning("UI directory not found: %s (skip mounting /ui)", UI_DIR)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/ui/")
