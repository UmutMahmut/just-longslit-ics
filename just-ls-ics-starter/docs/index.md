# JUST Long-Slit ICS — Docs

This folder contains lightweight documentation for the `just-ls-ics-starter` runtime.

- API contract (v0.1): `docs/api/contract.md`
- ADRs: `docs/adr/*`

---

## Quick links

- Swagger UI (when running locally): `http://127.0.0.1:8000/docs`
- Static UI (served by backend): `http://127.0.0.1:8000/ui/`

---

## Typical local workflow

### Run server
```powershell
cd .\just-ls-ics-starter\
python -m uvicorn justls.ics.api:app --host 127.0.0.1 --port 8000 --reload
```

### Run demo flow
```powershell
cd .\just-ls-ics-starter\
powershell -ExecutionPolicy Bypass -File .\scripts\demo_flow.ps1
```

### Run tests
```powershell
cd .\just-ls-ics-starter\
pytest -q
```

---

## UI camera placeholder

If camera latest-frame endpoints are not available yet, place a placeholder image at:

- `just-ls-ics-starter/ui/assets/latest.jpg`

The UI will use it as a fallback.
