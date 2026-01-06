from __future__ import annotations

from ...hal.base import HAL, State


class CalibLampsSubsystem:
    def __init__(self, hal: HAL) -> None:
        self._hal = hal

    def set_on(self, on: bool) -> State:
        # 对齐 HAL 新接口：set_calib_lamp_on
        return self._hal.set_calib_lamp_on(on)
