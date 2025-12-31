import pytest
from fastapi.testclient import TestClient

import justls.ics.api as api
from justls.hal.simulator import SimHAL


client = TestClient(api.app)


@pytest.fixture(autouse=True)
def _fresh_hal():
    # 每个测试前重置模拟器状态，避免测试间污染
    api.hal = SimHAL()
    yield


def test_status_ok():
    r = client.get("/api/v1/status")
    assert r.status_code == 200
    j = r.json()
    assert "slit_width_um" in j
    assert "grating" in j
    assert "lamp_on" in j
    assert "temperature_c" in j


def test_set_slit_changes_state():
    r = client.post("/api/v1/slit", json={"width_um": 200})
    assert r.status_code == 200
    assert r.json()["slit_width_um"] == 200.0

    r2 = client.get("/api/v1/status")
    assert r2.status_code == 200
    assert r2.json()["slit_width_um"] == 200.0


def test_invalid_slit_returns_400_or_422():
    # width_um: gt=0, le=5000；通常会触发 422（校验错误）
    r = client.post("/api/v1/slit", json={"width_um": 0})
    assert r.status_code in (400, 422)


def test_set_lamp_changes_state():
    r = client.post("/api/v1/lamp", json={"on": True})
    assert r.status_code == 200
    assert r.json()["lamp_on"] is True

    r2 = client.get("/api/v1/status")
    assert r2.status_code == 200
    assert r2.json()["lamp_on"] is True


def test_set_grating_accepts_G1():
    r = client.post("/api/v1/grating", json={"name": "G1"})
    assert r.status_code == 200
    assert r.json()["grating"] == "G1"
