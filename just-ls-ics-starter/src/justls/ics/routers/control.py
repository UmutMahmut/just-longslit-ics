from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from ..runtime import get_runtime
from .status import StateDTO

router = APIRouter()


class SlitReq(BaseModel):
    width_um: float = Field(..., gt=0, le=5000)
    model_config = ConfigDict(json_schema_extra={"examples": [{"width_um": 200.0}]})


@router.post("/api/v1/slit", response_model=StateDTO)
@router.post("/slit", response_model=StateDTO, include_in_schema=False)
def set_slit(req: SlitReq) -> StateDTO:
    try:
        s = get_runtime().slit.set_width_um(req.width_um)
        return StateDTO.model_validate(s)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class LampReq(BaseModel):
    on: bool
    model_config = ConfigDict(json_schema_extra={"examples": [{"on": True}]})


@router.post("/api/v1/lamp", response_model=StateDTO)
@router.post("/lamp", response_model=StateDTO, include_in_schema=False)
def set_lamp(req: LampReq) -> StateDTO:
    try:
        s = get_runtime().calib_lamps.set_on(req.on)
        return StateDTO.model_validate(s)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class GratingReq(BaseModel):
    name: str = Field(..., min_length=1)
    model_config = ConfigDict(json_schema_extra={"examples": [{"name": "G1"}]})


@router.post("/api/v1/grating", response_model=StateDTO)
@router.post("/grating", response_model=StateDTO, include_in_schema=False)
def set_grating(req: GratingReq) -> StateDTO:
    try:
        s = get_runtime().grating.select(req.name)
        return StateDTO.model_validate(s)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
