from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from ..runtime import get_runtime
from .status import StateDTO

router = APIRouter()


class SlitReq(BaseModel):
    width_um: float = Field(..., gt=0, le=5000)
    model_config = ConfigDict(json_schema_extra={"examples": [{"width_um": 200.0}]})


class SlitAngleReq(BaseModel):
    angle_deg: float = Field(..., ge=-90, le=90)
    model_config = ConfigDict(json_schema_extra={"examples": [{"angle_deg": 0.0}]})


@router.post("/api/v1/slit", response_model=StateDTO)
@router.post("/slit", response_model=StateDTO, include_in_schema=False)
def set_slit(req: SlitReq) -> StateDTO:
    try:
        s = get_runtime().slit.set_width_um(req.width_um)
        return StateDTO.model_validate(s)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/api/v1/slit_angle", response_model=StateDTO)
@router.post("/slit_angle", response_model=StateDTO, include_in_schema=False)
def set_slit_angle(req: SlitAngleReq) -> StateDTO:
    try:
        s = get_runtime().slit.set_angle_deg(req.angle_deg)
        return StateDTO.model_validate(s)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class LampReq(BaseModel):
    on: bool = Field(..., strict=True)
    model_config = ConfigDict(json_schema_extra={"examples": [{"on": True}]})


@router.post("/api/v1/lamp", response_model=StateDTO)
@router.post("/lamp", response_model=StateDTO, include_in_schema=False)
def set_lamp(req: LampReq) -> StateDTO:
    try:
        s = get_runtime().calib_lamps.set_on(req.on)
        return StateDTO.model_validate(s)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
