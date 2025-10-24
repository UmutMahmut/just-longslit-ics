from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from ..config import settings
from ..hal.simulator import SimHAL
from ..hal.base import HAL
from ..telemetry.influx import write_measurement

app = FastAPI(title="JUST Long-Slit ICS", version="0.1.0")

hal: HAL = SimHAL()  # 初期版本仅模拟器

class StateDTO(BaseModel):
    slit_width_um: float = Field(..., ge=0)
    grating: str
    lamp_on: bool
    temperature_c: float

@app.get("/api/v1/status", response_model=StateDTO)
def status() -> StateDTO:
    s = hal.get_state()
    # 遥测写入（可选，无 token 会报错，故 try/except）
    try:
        write_measurement("instrument_state", {
            "slit_width_um": s.slit_width_um,
            "temperature_c": s.temperature_c,
            "lamp_on": int(s.lamp_on),
        }, tags={"grating": s.grating})
    except Exception:
        pass
    return StateDTO.model_validate(s.__dict__)

class SlitReq(BaseModel):
    width_um: float = Field(..., gt=0, le=5000)

@app.post("/api/v1/slit", response_model=StateDTO)
def set_slit(req: SlitReq) -> StateDTO:
    try:
        s = hal.set_slit_width(req.width_um)
        return StateDTO.model_validate(s.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

class GratingReq(BaseModel):
    name: str

@app.post("/api/v1/grating", response_model=StateDTO)
def set_grating(req: GratingReq) -> StateDTO:
    try:
        s = hal.select_grating(req.name)
        return StateDTO.model_validate(s.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

class LampReq(BaseModel):
    on: bool

@app.post("/api/v1/lamp", response_model=StateDTO)
def set_lamp(req: LampReq) -> StateDTO:
    s = hal.set_lamp(req.on)
    return StateDTO.model_validate(s.__dict__)
