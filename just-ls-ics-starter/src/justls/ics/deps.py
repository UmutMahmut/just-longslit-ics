from __future__ import annotations

from ..hal.base import HAL
from ..hal.simulator import SimHAL

# 单例 HAL：测试与 demo_flow 都依赖“状态能持续”
_hal: HAL = SimHAL()


def get_hal() -> HAL:
    return _hal
