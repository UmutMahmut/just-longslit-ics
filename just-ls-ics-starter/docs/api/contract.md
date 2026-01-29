# JUST Long-Slit ICS — API Contract (v0.1)

This document is the **human-readable contract** for the current stable API surface.

- Base path: `/api/v1`
- Content type: JSON (`application/json`) unless otherwise noted

---

## Data model (v0.1)

### Instrument state (Status)

`GET /api/v1/status` returns the current instrument state:

```json
{
  "slit_width_um": 100.0,
  "slit_angle_deg": 0.0,
  "lamp_on": false,
  "temperature_c": 20.0
}
```

Field notes:
- `slit_width_um`: float, **0 < x ≤ 5000**
- `slit_angle_deg`: float, **-90 ≤ x ≤ 90**
- `lamp_on`: boolean
- `temperature_c`: float (simulated in SimHAL)

---

## Endpoints

### 1) Status

#### `GET /api/v1/status`
Returns the current instrument state (see “Instrument state”).

#### `GET /api/v1/status/full`
Returns a richer payload used by the UI and clients:

```json
{
  "state": {
    "slit_width_um": 100.0,
    "slit_angle_deg": 0.0,
    "lamp_on": false,
    "temperature_c": 20.0
  },
  "capabilities": {
    "slit": true,
    "slit_angle": true,
    "calib_lamps": true,
    "guider": false,
    "science_channels_bgr": false,
    "env_sensors": false
  },
  "hal": "sim",
  "run_mode": "sim",
  "timestamp_utc": "2026-01-27T00:00:00Z"
}
```

Notes:
- `timestamp_utc` is an ISO-8601 UTC timestamp string.
- `capabilities` is intended to be a **forward-compatible** map; clients should ignore unknown keys.

---

### 2) Capabilities

#### `GET /api/v1/capabilities`
Returns the current capabilities map (same structure as `status/full.capabilities`).

---

### 3) Control

#### `POST /api/v1/slit`
Set slit width (μm).

Request body:
```json
{ "width_um": 200.0 }
```

Success response: returns updated instrument state (same schema as `GET /api/v1/status`).

Validation:
- invalid payload returns **422**
- out-of-range `width_um` returns **422**

#### `POST /api/v1/slit_angle`
Set slit angle (degrees).

Request body:
```json
{ "angle_deg": 0.0 }
```

Success response: returns updated instrument state.

Validation:
- invalid payload returns **422**
- out-of-range `angle_deg` returns **422**

#### `POST /api/v1/lamp`
Set master calibration lamp state.

Request body:
```json
{ "on": true }
```

Success response: returns updated instrument state.

---

## Errors

- Validation errors: **422** with a FastAPI/Pydantic error payload (`detail: [...]`).
- Server errors: **500** (should be treated as retryable by clients).

---

## Camera panels (UI placeholder)

The UI contains camera panels (“SlitCam” and “B/G/R”). In the current baseline:
- If camera latest-frame APIs are **not** implemented/available, the UI falls back to a static placeholder image:
  - `/ui/assets/latest.jpg`

Future work may introduce optional endpoints like:
- `/api/v1/camera/slit/latest.jpg`
- `/api/v1/camera/{b|g|r}/latest.jpg`

These are **not** required for v0.1 test/demo flow unless explicitly implemented.
