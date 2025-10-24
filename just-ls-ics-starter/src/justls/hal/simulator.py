from __future__ import annotations
import random
from time import time
from .base import HAL, InstrumentState

class SimHAL(HAL):
    def __init__(self) -> None:
        self._state = InstrumentState()

    def get_state(self) -> InstrumentState:
        # Add a tiny jitter to emulate sensor drift
        self._state.temperature_c = 20.0 + random.uniform(-0.2, 0.2)
        return self._state

    def set_slit_width(self, width_um: float) -> InstrumentState:
        if width_um <= 0 or width_um > 5000:
            raise ValueError("slit width out of range (0, 5000] um")
        self._state.slit_width_um = float(width_um)
        return self._state

    def select_grating(self, name: str) -> InstrumentState:
        if name not in {"G1","G2","G3"}:
            raise ValueError("unknown grating")
        self._state.grating = name
        return self._state

    def set_lamp(self, on: bool) -> InstrumentState:
        self._state.lamp_on = bool(on)
        return self._state
