from __future__ import annotations

from typing import Any

from ...hal.base import HAL


class SlitSubsystem:
    """Slit mechanics / width control façade."""

    def __init__(self, hal: HAL) -> None:
        self._hal = hal

    def set_width_um(self, width_um: float) -> Any:
        # HAL 已定义新接口：set_slit_width_um
        return self._hal.set_slit_width_um(width_um)


    def set_angle_deg(self, angle_deg: float) -> Any:
        # HAL 新增接口：set_slit_angle_deg
        return self._hal.set_slit_angle_deg(angle_deg)
    def get_width_um(self) -> float:
        s = self._hal.get_state()
        return float(s.slit_width_um)

    def get_angle_deg(self) -> float:
        s = self._hal.get_state()
        return float(s.slit_angle_deg)
