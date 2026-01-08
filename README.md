# JUST Long-Slit ICS

[![CI](https://github.com/UmutMahmut/just-longslit-ics/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/UmutMahmut/just-longslit-ics/actions/workflows/ci.yml)

Instrument Control System (ICS) prototype for the JUST Telescope **Long-Slit Spectrograph**.

This repository currently provides:
- A versioned **FastAPI** backend with a stable v0.1 contract (`/api/v1/*`)
- A **SimHAL** simulator enabling end-to-end operation without hardware
- Static UI served by the backend at `/ui/` for zero-CORS local integration
- A reproducible engineering pipeline: **demo script + pytest regression + GitHub Actions CI**
- A maintenance sweep script (optional) to detect legacy endpoint references in docs

---

## Project status

### Completed
- **Sprint 0 (Baseline runnable skeleton)**
  - API v0.1 available at `/api/v1/*`
  - Static UI served by backend at `/ui/`
  - Telemetry is configurable and **disabled by default** (`telemetry_enabled=false`)
- **Sprint 1 (Reproducible + regression-safe)**
  - One-click demo script (`just-ls-ics-starter/scripts/demo_flow.ps1`) for E2E flow
  - Pytest regression suite + GitHub Actions CI on push/PR
- **Sprint 2 (UI + simulator hardening + contract alignment)**
  - UI upgraded for stable local integration (status polling, request feedback, operation logs)
  - `/api/v1/status/full` stabilized; capabilities surfaced for UI/clients
  - SimHAL + subsystem boundary cleaned up for predictable behavior
  - Docs/contract endpoint references unified to `/api/v1/*`

### Next
- **Sprint 3**: Packaging & distribution (training-friendly “double-click run” first; `.exe` later if needed)

---

## Repository layout

- `just-ls-ics-starter/` — main Python package and runtime
  - `src/justls/ics/api.py` — FastAPI entry (serves API + UI)
  - `ui/` — static UI assets (served at `/ui/`)
  - `scripts/demo_flow.ps1` — one-click demo flow (PowerShell)
  - `tests/` — regression + optional stress tests
  - `docs/api/contract.md` — API contract (human-readable)
- `.github/workflows/ci.yml` — GitHub Actions CI (pytest)

---

## Quickstart (Windows)

### 0) Recommended Python version
CI is pinned to Python 3.12.x. For best consistency, use Python 3.12.x locally as well.

If you use conda:
```powershell
conda activate dino

### 1) Install (editable)
From repository root:
```powershell
cd .\just-ls-ics-starter\
python -m pip install -U pip
pip install -e .
pip install -U pytest httpx
```

### 2) Run server
```powershell
cd .\just-ls-ics-starter\
python -m uvicorn justls.ics.api:app --host 127.0.0.1 --port 8000 --reload
```

### 3) Open in browser
- Swagger UI: http://127.0.0.1:8000/docs
- Static UI:  http://127.0.0.1:8000/ui/

---

## API (v0.1)

The v0.1 contract is described in:
- `just-ls-ics-starter/docs/api/contract.md`

Canonical endpoints:
- `GET /api/v1/status`  
- `GET /api/v1/status/full`   
- `GET /api/v1/capabilities` 
- `POST /api/v1/slit body`   
- `POST /api/v1/grating body`    
- `POST /api/v1/lamp body`    

## Demo (one-click)

Run the E2E demo flow:
```powershell
cd .\just-ls-ics-starter\
powershell -ExecutionPolicy Bypass -File .\scripts\demo_flow.ps1
```

The script performs:
1) GET status  
2) POST slit  
3) POST lamp  
4) POST grating  
5) GET status (final)

---

## Tests

Run locally:
```powershell
cd .\just-ls-ics-starter\
pytest -q
```

Notes:
- Tests use `fastapi.testclient.TestClient`, which requires `httpx` installed.
- CI runs pytest on every push/PR.

---

## Telemetry (optional)

Telemetry is intentionally **off by default** to keep the minimal closed-loop independent of external services.

Configuration is read from `.env` (optional). Example:
```env
telemetry_enabled=false
influx_url=http://localhost:8181
influx_token=
influx_org=just-lab
influx_bucket=ics
log_level=INFO
```

When `telemetry_enabled=true`, the backend attempts to write instrument state telemetry; any telemetry write failure must not block API responses.

---

## Roadmap (Sprint 2 focus)

Sprint 2 will prioritize usability and realism, without introducing external simulators yet:
- UI: connection status + request feedback + readable errors + operation log + refresh strategy
- SimHAL: tighter parameter constraints + clearer grating selection behavior + (optional) fault injection hooks

---

## Contributing workflow (internal)

- `main` is protected: merges require the GitHub Actions status check `test` to pass.
- Prefer PR-based changes so CI gates all merges.

---

## License

If `LICENSE` is not yet added, treat this repository as internal until a license is chosen.
