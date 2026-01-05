from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from ..config import settings
from ..hal.base import HAL
from ..hal.capabilities import Capabilities
from ..hal.simulator import SimHAL
from ..telemetry.influx import write_measurement

logger = logging.getLogger(__name__)

app = FastAPI(title="JUST Long-Slit ICS", version="0.1.0")
hal: HAL = SimHAL()  # 初期版本仅模拟器


class StateDTO(BaseModel):
    # 允许直接从对象属性读取（避免到处写 s.__dict__）
    model_config = ConfigDict(from_attributes=True)

    slit_width_um: float = Field(..., ge=0)
    grating: str
    lamp_on: bool
    temperature_c: float


@app.get("/api/v1/status", response_model=StateDTO)
def status() -> StateDTO:
    s = hal.get_state()

    # 遥测写入（默认关闭；开启后失败也不阻塞主流程）
    if settings.telemetry_enabled:
        try:
            write_measurement(
                "instrument_state",
                {
                    "slit_width_um": s.slit_width_um,
                    "temperature_c": s.temperature_c,
                    "lamp_on": int(s.lamp_on),
                },
                tags={"grating": s.grating},
            )
        except Exception:
            logger.debug("telemetry write failed", exc_info=True)

    return StateDTO.model_validate(s)


class SlitReq(BaseModel):
    width_um: float = Field(..., gt=0, le=5000)

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"width_um": 200.0}]}
    )


@app.post("/api/v1/slit", response_model=StateDTO)
def set_slit(req: SlitReq) -> StateDTO:
    try:
        s = hal.set_slit_width_um(req.width_um)
        return StateDTO.model_validate(s)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class GratingReq(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)

    model_config = ConfigDict(json_schema_extra={"examples": [{"name": "G1"}]})


@app.post("/api/v1/grating", response_model=StateDTO)
def set_grating(req: GratingReq) -> StateDTO:
    try:
        s = hal.set_grating(req.name)
        return StateDTO.model_validate(s)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class LampReq(BaseModel):
    on: bool
    model_config = ConfigDict(json_schema_extra={"examples": [{"on": True}]})


@app.post("/api/v1/lamp", response_model=StateDTO)
def set_lamp(req: LampReq) -> StateDTO:
    try:
        s = hal.set_calib_lamp_on(req.on)
        return StateDTO.model_validate(s)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/capabilities", response_model=Capabilities)
def capabilities() -> Capabilities:
    return hal.get_capabilities()


# UI: 静态托管（html=True 会在目录存在 index.html 时自动加载）
BASE_DIR = Path(__file__).resolve().parents[3]  # -> ...\just-ls-ics-starter
UI_DIR = BASE_DIR / "ui"

_ROOT_REDIRECT = "/docs"
if UI_DIR.is_dir():
    # StaticFiles 会在目录缺失时导致启动失败，因此先检查目录存在
    app.mount("/ui", StaticFiles(directory=str(UI_DIR), html=True), name="ui")
    _ROOT_REDIRECT = "/ui/"
else:
    logger.warning("UI directory not found: %s (skip mounting /ui)", UI_DIR)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url=_ROOT_REDIRECT)
