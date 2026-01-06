from __future__ import annotations

from fastapi import APIRouter

from ..runtime import get_runtime

router = APIRouter()


@router.get("/api/v1/capabilities")
def capabilities() -> dict:
    return get_runtime().system.get_capabilities_dict()
