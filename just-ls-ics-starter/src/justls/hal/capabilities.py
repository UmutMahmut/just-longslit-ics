from __future__ import annotations

from pydantic import BaseModel


class Capabilities(BaseModel):
    # Core subsystems
    slit: bool = True
    grating: bool = True
    calib_lamps: bool = True

    # Optional / future subsystems
    rotator: bool = False
    slit_monitor_camera: bool = False
    guider: bool = False
    env_sensors: bool = True
    science_channels_bgr: bool = False
    fast_photometry: bool = False
