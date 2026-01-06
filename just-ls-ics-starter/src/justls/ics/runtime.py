from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..config import settings
from ..hal.base import HAL
from ..hal.factory import build_hal

from .subsystems.calib_lamps import CalibLampsSubsystem
from .subsystems.env_sensors import EnvSensorsSubsystem
from .subsystems.grating import GratingSubsystem
from .subsystems.slit import SlitSubsystem
from .subsystems.system import SystemSubsystem


@dataclass(frozen=True)
class Runtime:
    """Process-wide singletons: one HAL instance + thin subsystem facades."""
    hal: HAL
    system: SystemSubsystem
    slit: SlitSubsystem
    grating: GratingSubsystem
    calib_lamps: CalibLampsSubsystem
    env_sensors: EnvSensorsSubsystem


@lru_cache
def get_runtime() -> Runtime:
    """
    Build exactly once per process.

    We use lru_cache for 'create once' semantics (same idea as FastAPI settings caching).
    """
    hal = build_hal(settings.run_mode)
    return Runtime(
        hal=hal,
        system=SystemSubsystem(hal),
        slit=SlitSubsystem(hal),
        grating=GratingSubsystem(hal),
        calib_lamps=CalibLampsSubsystem(hal),
        env_sensors=EnvSensorsSubsystem(hal),
    )
