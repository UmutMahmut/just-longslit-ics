from __future__ import annotations

from ...hal.base import HAL


class ScienceChannelsSubsystem:
    def __init__(self, hal: HAL) -> None:
        self._hal = hal

    def _not_impl(self) -> None:
        raise NotImplementedError("Science channels not implemented in MVP.")
