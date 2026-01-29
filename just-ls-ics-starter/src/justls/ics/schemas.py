from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from ..hal.capabilities import Capabilities

class StateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slit_width_um: float = Field(..., ge=0)
    slit_angle_deg: float = Field(..., ge=-90, le=90)
    lamp_on: bool
    temperature_c: float

class SlitReq(BaseModel):
    width_um: float = Field(..., gt=0, le=5000)
    model_config = ConfigDict(json_schema_extra={"examples": [{"width_um": 200.0}]})

class SlitAngleReq(BaseModel):
    angle_deg: float = Field(..., ge=-90, le=90)
    model_config = ConfigDict(json_schema_extra={"examples": [{"angle_deg": 0.0}]})

class LampReq(BaseModel):
    on: bool = Field(..., strict=True)
    model_config = ConfigDict(json_schema_extra={"examples": [{"on": True}]})

class StatusFullDTO(BaseModel):
    state: StateDTO
    capabilities: Capabilities
    hal: str
    timestamp_utc: datetime
