from __future__ import annotations

from typing import Any

from ...hal.base import HAL


class SystemSubsystem:
    """
    Cross-cutting system façade.
    Owns the canonical 'get_state' and 'capabilities' readouts.
    """

    def __init__(self, hal: HAL) -> None:
        self._hal = hal

    def get_state(self) -> Any:
        return self._hal.get_state()

    def get_capabilities_dict(self) -> dict:
        caps = self._hal.capabilities()
        # 你的 capabilities 对象已实现 to_dict()
        return caps.to_dict()

    def get_status_full(self) -> dict:
        return {
            "state": self.get_state(),
            "capabilities": self.get_capabilities_dict(),
        }
