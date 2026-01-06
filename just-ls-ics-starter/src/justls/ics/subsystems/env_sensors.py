from __future__ import annotations

from ...hal.base import HAL


class EnvSensorsSubsystem:
    """Environmental sensors façade (temperature etc.)."""

    def __init__(self, hal: HAL) -> None:
        self._hal = hal

    def temperature_c(self) -> float:
        s = self._hal.get_state()
        return float(s.temperature_c)
