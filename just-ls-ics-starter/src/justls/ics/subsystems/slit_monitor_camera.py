from __future__ import annotations

from ...hal.base import HAL


class SlitMonitorCameraSubsystem:
    def __init__(self, hal: HAL) -> None:
        self._hal = hal

    def _not_impl(self) -> None:
        raise NotImplementedError("Slit monitor camera not implemented in MVP.")
