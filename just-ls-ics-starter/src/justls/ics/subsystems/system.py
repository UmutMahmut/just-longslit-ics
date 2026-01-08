from __future__ import annotations

from dataclasses import asdict

from ...hal.base import HAL, State
from ...hal.capabilities import Capabilities


class SystemSubsystem:
    def __init__(self, hal: HAL) -> None:
        self._hal = hal

    def get_state(self) -> State:
        return self._hal.get_state()

    def get_state_dict(self) -> dict:
        return asdict(self.get_state())

    def get_capabilities(self) -> Capabilities:
        return self._hal.get_capabilities()

    def get_capabilities_dict(self) -> dict:
        return self.get_capabilities().model_dump()

    def get_status_full(self) -> dict:
        return {
            "state": self.get_state_dict(),
            "capabilities": self.get_capabilities_dict(),
        }
