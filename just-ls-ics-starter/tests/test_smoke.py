from fastapi.testclient import TestClient
from justls.ics.api import app

def test_status():
    client = TestClient(app)
    r = client.get("/api/v1/status")
    assert r.status_code == 200
    data = r.json()
    assert "slit_width_um" in data
