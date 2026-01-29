from __future__ import annotations

from dataclasses import replace

from .base import HAL, State
from .capabilities import Capabilities


class SimHAL(HAL):
    """Pure software simulator HAL (MVP)."""

    def __init__(
        self,
        *,
        slit_width_um: float = 100.0,
        lamp_on: bool = False,
        temperature_c: float = 20.0,
        slit_angle_deg: float = 0.0,
        capabilities: Capabilities | None = None,
    ) -> None:
        self._state = State(
            slit_width_um=float(slit_width_um),
            lamp_on=bool(lamp_on),
            temperature_c=float(temperature_c),
            slit_angle_deg=float(slit_angle_deg),
        )
        self._cap = capabilities or Capabilities()

    def get_state(self) -> State:
        return self._state

    def get_capabilities(self) -> Capabilities:
        return self._cap

    def set_slit_width_um(self, width_um: float) -> State:
        width_um = float(width_um)
        if width_um < 0:
            raise ValueError("slit width must be >= 0")
        self._state = replace(self._state, slit_width_um=width_um)
        return self._state




    def set_slit_angle_deg(self, angle_deg: float) -> State:
        angle_deg = float(angle_deg)
        if angle_deg < -90 or angle_deg > 90:
            raise ValueError("slit angle must be in [-90, 90]")
        self._state = replace(self._state, slit_angle_deg=angle_deg)
        return self._state
    def set_calib_lamp_on(self, on: bool) -> State:
        self._state = replace(self._state, lamp_on=bool(on))
        return self._state
