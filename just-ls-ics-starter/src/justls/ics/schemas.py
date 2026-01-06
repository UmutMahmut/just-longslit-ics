from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from ..hal.capabilities import Capabilities


class StateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slit_width_um: float = Field(..., ge=0)
    grating: str
    lamp_on: bool
    temperature_c: float


class SlitReq(BaseModel):
    width_um: float = Field(..., gt=0, le=5000)
    model_config = ConfigDict(json_schema_extra={"examples": [{"width_um": 200.0}]})


class GratingReq(BaseModel):
    name: str = Field(..., min_length=1)
    model_config = ConfigDict(json_schema_extra={"examples": [{"name": "G1"}]})


class LampReq(BaseModel):
    on: bool
    model_config = ConfigDict(json_schema_extra={"examples": [{"on": True}]})


class StatusFullDTO(BaseModel):
    state: StateDTO
    capabilities: Capabilities
    hal: str
    timestamp_utc: datetime
