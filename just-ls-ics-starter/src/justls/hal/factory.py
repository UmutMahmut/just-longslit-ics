from __future__ import annotations

from functools import lru_cache

from ..config import settings
from .base import HAL
from .simulator import SimHAL


def build_hal(run_mode: str | None) -> HAL:
    """
    Build a HAL instance according to run_mode.

    run_mode:
      - "sim": simulator HAL
      - "hw" : hardware HAL (not implemented yet)
    """
    mode = (run_mode or "sim").lower().strip()

    if mode == "sim":
        return SimHAL()

    if mode == "hw":
        raise NotImplementedError("HW HAL not implemented yet")

    raise ValueError(f"Unknown run_mode: {run_mode!r}")


@lru_cache
def get_hal() -> HAL:
    """
    Cached singleton HAL for FastAPI dependency injection.

    Important: keep a single HAL instance so state persists across requests.
    """
    return build_hal(getattr(settings, "run_mode", None))
