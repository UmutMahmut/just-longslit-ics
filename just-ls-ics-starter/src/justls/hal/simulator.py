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
        grating: str = "G300",
        lamp_on: bool = False,
        temperature_c: float = 20.0,
        capabilities: Capabilities | None = None,
    ) -> None:
        self._state = State(
            slit_width_um=float(slit_width_um),
            grating=str(grating),
            lamp_on=bool(lamp_on),
            temperature_c=float(temperature_c),
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

    def set_grating(self, name: str) -> State:
        name = str(name).strip()
        if not name:
            raise ValueError("grating name must be non-empty")
        # MVP: 不做枚举收紧，先宽松接受（避免你现在 test_set_grating_accepts_G1 失败）
        self._state = replace(self._state, grating=name)
        return self._state

    def set_calib_lamp_on(self, on: bool) -> State:
        self._state = replace(self._state, lamp_on=bool(on))
        return self._state
