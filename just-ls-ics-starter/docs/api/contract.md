# JUST Long-Slit ICS 鈥?API Contract (v0.1)

Base URL (local):
- http://127.0.0.1:8000

Interactive docs (auto-generated from OpenAPI):
- /docs (Swagger UI)
- /openapi.json (OpenAPI schema)

UI (static, served by backend):
- /ui/  (served via StaticFiles mount; not part of OpenAPI) :contentReference[oaicite:1]{index=1}

---

## 1. Versioned API (Contract)

### 1.1 GET /api/v1/api/v1/status
Return current instrument state.

Response 200 (application/json):
```json
{
  "slit_width_um": 100.0,
  "grating": "G1",
  "lamp_on": false,
  "temperature_c": 20.0
}
