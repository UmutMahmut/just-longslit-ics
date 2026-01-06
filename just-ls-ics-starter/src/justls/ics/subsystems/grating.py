from __future__ import annotations

from typing import Any

from ...hal.base import HAL


class GratingSubsystem:
    def __init__(self, hal: HAL) -> None:
        self._hal = hal

    def select(self, name: str) -> Any:
        # 对齐当前 HAL 新接口：set_grating(name)
        return self._hal.set_grating(name)
