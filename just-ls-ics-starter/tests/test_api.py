import os
import time

import pytest
from fastapi.testclient import TestClient

from justls.ics.api import app
from justls.ics.runtime import get_runtime


@pytest.fixture(autouse=True)
def _fresh_runtime():
    # runtime 用了 lru_cache：每个测试都清掉，避免状态污染
    get_runtime.cache_clear()
    yield
    get_runtime.cache_clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_status_ok(client: TestClient):
    r = client.get("/api/v1/status")
    assert r.status_code == 200
    j = r.json()
    assert "slit_width_um" in j
    assert "grating" in j
    assert "lamp_on" in j
    assert "temperature_c" in j


@pytest.mark.parametrize("width_um,expected", [
    (200, 200.0),
    (1, 1.0),
    (4999, 4999.0),
])
def test_set_slit_changes_state(client: TestClient, width_um, expected):
    r = client.post("/api/v1/slit", json={"width_um": width_um})
    assert r.status_code == 200
    assert r.json()["slit_width_um"] == expected

    r2 = client.get("/api/v1/status")
    assert r2.status_code == 200
    assert r2.json()["slit_width_um"] == expected


@pytest.mark.parametrize("bad_width_um", [0, -1, 5001, 1e9])
def test_invalid_slit_returns_400_or_422(client: TestClient, bad_width_um):
    r = client.post("/api/v1/slit", json={"width_um": bad_width_um})
    assert r.status_code in (400, 422)


def test_set_lamp_changes_state(client: TestClient):
    r = client.post("/api/v1/lamp", json={"on": True})
    assert r.status_code == 200
    assert r.json()["lamp_on"] is True

    r2 = client.get("/api/v1/status")
    assert r2.status_code == 200
    assert r2.json()["lamp_on"] is True


def test_invalid_lamp_payload_returns_422(client: TestClient):
    # 缺字段/类型错误，FastAPI/Pydantic 通常是 422
    r = client.post("/api/v1/lamp", json={})
    assert r.status_code == 422
    r2 = client.post("/api/v1/lamp", json={"on": "yes"})
    assert r2.status_code == 422


def test_set_grating_accepts_G1(client: TestClient):
    r = client.post("/api/v1/grating", json={"name": "G1"})
    assert r.status_code == 200
    assert r.json()["grating"] == "G1"


def test_invalid_grating_payload_returns_422(client: TestClient):
    r = client.post("/api/v1/grating", json={"name": ""})
    assert r.status_code == 422


def test_status_full_ok(client: TestClient):
    # 这里能直接锁死你这次遇到的 500
    r = client.get("/api/v1/status/full")
    assert r.status_code == 200
    data = r.json()
    assert "state" in data
    assert "capabilities" in data
    assert "slit_width_um" in data["state"]


def test_capabilities_endpoint_ok(client: TestClient):
    r = client.get("/api/v1/capabilities")
    assert r.status_code == 200
    caps = r.json()
    assert "slit" in caps
    assert "grating" in caps
    assert "calib_lamps" in caps


def test_quick_stress_2min_optional(client: TestClient):
    # 默认不跑：避免 CI/本地每次都等 2 分钟
    # 想跑时：JUSTLS_STRESS=1 pytest -q
    if os.getenv("JUSTLS_STRESS") != "1":
        pytest.skip("set JUSTLS_STRESS=1 to run stress test")

    t0 = time.time()
    i = 0
    while time.time() - t0 < 120:
        width = 100 + (i % 100)  # 100..199
        r1 = client.post("/api/v1/slit", json={"width_um": width})
        assert r1.status_code == 200

        r2 = client.post("/api/v1/lamp", json={"on": (i % 2 == 0)})
        assert r2.status_code == 200

        r3 = client.post("/api/v1/grating", json={"name": "G1"})
        assert r3.status_code == 200

        r4 = client.get("/api/v1/status")
        assert r4.status_code == 200
        i += 1
