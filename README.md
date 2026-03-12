# JUST Long-Slit ICS

[![CI](https://github.com/UmutMahmut/just-longslit-ics/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/UmutMahmut/just-longslit-ics/actions/workflows/ci.yml)

Instrument Control System (ICS) prototype for the JUST Telescope **Long-Slit Spectrograph**.

This repository currently provides:
- A versioned **FastAPI** backend with a stable v0.1 contract (`/api/v1/*`)
- A **SimHAL** simulator enabling end-to-end operation without hardware
- Static UI served by the backend at `/ui/` for zero-CORS local integration
- A validated Windows desktop host path using **pywebview** + local backend embedding
- A reproducible engineering pipeline: **demo script + pytest regression + GitHub Actions CI**
- A maintenance sweep script (optional) to detect legacy endpoint references in code/docs

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
- **Sprint 2 (Contract alignment + simulator hardening)**
  - `/api/v1/status/full` stabilized; capabilities surfaced for UI/clients
  - SimHAL + subsystem boundary cleaned up for predictable behavior
  - Deprecated/legacy references removed; contracts unified to `/api/v1/*`
- **Sprint 3 (UI overview refresh + camera placeholder integration)**
  - UI upgraded for stable local operation (polling, request feedback, operation logs)
  - Overview reworked into a “quad” layout (Quick control + SlitCam + B/G/R + Status)
  - Camera panels support a **static placeholder** image at `ui/assets/latest.jpg`
    - Used automatically when camera API is not available
- **Sprint 4 (Desktop packaging baseline)**
  - A Windows desktop launcher is now available at `desktop_webview/main.py`
  - The desktop host starts or reuses the local backend, then opens the ICS UI in an embedded window
  - Desktop runtime behavior has been validated for the current training/demo workflow
  - A first working **PyInstaller onedir** packaging path has been verified for internal testing

### Next
- **Sprint 5**: packaging hardening and release workflow
  - Freeze build settings into a reusable spec/config
  - Add release-oriented packaging notes (what to copy, how to test on another machine)
  - Decide whether to publish internal zip packages / GitHub Releases
- **Sprint 6**: functional upgrades on top of the current desktop-capable baseline

---

## Repository layout

- `just-ls-ics-starter/` — main Python package and runtime
  - `src/justls/ics/api.py` — FastAPI entry (serves API + UI)
  - `ui/` — static UI assets (served at `/ui/`)
    - `assets/latest.jpg` — placeholder used by UI when camera endpoints are not implemented
  - `scripts/demo_flow.ps1` — one-click demo flow (PowerShell)
  - `tests/` — regression + optional stress tests
  - `docs/api/contract.md` — API contract (human-readable)
- `desktop_webview/`
  - `main.py` — Windows desktop launcher for the current UI/backend stack
- `.github/workflows/ci.yml` — GitHub Actions CI (pytest)

---

## Quickstart (Windows)

### 0) Recommended Python version
CI is pinned to Python 3.12.x. For best consistency, use Python 3.12.x locally as well.

If you use conda:
```powershell
conda activate dino
```

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

### 4) Optional desktop host (Windows, internal baseline)
From repository root, run the desktop launcher:
```powershell
python .\desktop_webview\main.py
```

Notes:
- The desktop host is intended for local/internal use during the current packaging stage.
- For packaged desktop testing, distribute/copy the whole generated application folder rather than only a single `.exe`.

---

## API (v0.1)

The v0.1 contract is described in:
- `just-ls-ics-starter/docs/api/contract.md`

Canonical endpoints:
- `GET /api/v1/status`
- `GET /api/v1/status/full`
- `GET /api/v1/capabilities`
- `POST /api/v1/slit` (body: `{"width_um": ...}`)
- `POST /api/v1/slit_angle` (body: `{"angle_deg": ...}`)
- `POST /api/v1/lamp` (body: `{"on": true|false}`)

Notes:
- The UI includes camera panels. If camera latest-frame endpoints are not implemented/available, the UI falls back to `/ui/assets/latest.jpg`.

---

## Demo (one-click)

Run the E2E demo flow:
```powershell
cd .\just-ls-ics-starter\
powershell -ExecutionPolicy Bypass -File .\scripts\demo_flow.ps1
```

The script performs:
1) GET status
2) POST slit
3) POST slit_angle
4) POST lamp
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

## Desktop packaging notes (internal)

Current validated direction:
- Desktop host: `desktop_webview/main.py`
- Backend model: local FastAPI/uvicorn runtime embedded in the desktop workflow
- Packaging baseline: internal **onedir** build for Windows testing/training use

At the current stage:
- Browser mode remains the reference development mode
- Desktop mode is the validated internal “double-click friendly” path
- Packaging/release hardening is still in progress

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

## Contributing workflow (internal)

- `main` is protected: merges require the GitHub Actions status check `test` to pass.
- Prefer PR-based changes so CI gates all merges.
- For desktop-related changes, validate both:
  - browser mode (`/ui/`)
  - desktop launcher mode (`desktop_webview/main.py`)

---

## License

If `LICENSE` is not yet added, treat this repository as internal until a license is chosen.
