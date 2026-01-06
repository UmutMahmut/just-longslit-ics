from __future__ import annotations

from ...hal.base import HAL


class RotatorSubsystem:
    def __init__(self, hal: HAL) -> None:
        self._hal = hal

    def _not_impl(self) -> None:
        raise NotImplementedError("Rotator subsystem not implemented in MVP.")
