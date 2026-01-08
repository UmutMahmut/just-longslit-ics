from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from ...config import settings
from ...telemetry.influx import write_measurement
from ..runtime import get_runtime

logger = logging.getLogger(__name__)
router = APIRouter()


class StateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slit_width_um: float = Field(..., ge=0)
    grating: str
    lamp_on: bool
    temperature_c: float


@router.get("/api/v1/status", response_model=StateDTO)
@router.get("/status", response_model=StateDTO, include_in_schema=False)
def status() -> StateDTO:
    rt = get_runtime()
    s = rt.system.get_state()

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


@router.get("/api/v1/status/full")
@router.get("/status/full", include_in_schema=False)
def status_full() -> dict:
    rt = get_runtime()
    s = rt.system.get_state()
    return {
        "state": StateDTO.model_validate(s).model_dump(),
        "capabilities": rt.system.get_capabilities_dict(),
        "hal": type(rt.hal).__name__,
        "run_mode": settings.run_mode,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
