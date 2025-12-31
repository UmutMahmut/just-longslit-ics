param(
  [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"

function Invoke-JsonGet([string]$Path) {
  return Invoke-RestMethod -Method Get -Uri "$BaseUrl$Path"
}

function Invoke-JsonPost([string]$Path, [hashtable]$Body) {
  $json = ($Body | ConvertTo-Json -Compress)
  return Invoke-RestMethod -Method Post -Uri "$BaseUrl$Path" -ContentType "application/json" -Body $json
}

Write-Host "== JUST Long-Slit ICS Demo Flow =="
Write-Host "BaseUrl: $BaseUrl"
Write-Host ""

# 1) GET status
Write-Host "[1] GET /api/v1/status"
$st0 = Invoke-JsonGet "/api/v1/status"
$st0 | ConvertTo-Json -Depth 5
Write-Host ""

# 2) POST slit
$targetSlit = 200
if ($st0.slit_width_um -lt 4900) { $targetSlit = [double]$st0.slit_width_um + 100 }

Write-Host "[2] POST /api/v1/slit  (width_um=$targetSlit)"
$st1 = Invoke-JsonPost "/api/v1/slit" @{ width_um = $targetSlit }
$st1 | ConvertTo-Json -Depth 5
Write-Host ""

# 3) POST lamp (toggle)
$targetLamp = -not [bool]$st1.lamp_on
Write-Host "[3] POST /api/v1/lamp  (on=$targetLamp)"
$st2 = Invoke-JsonPost "/api/v1/lamp" @{ on = $targetLamp }
$st2 | ConvertTo-Json -Depth 5
Write-Host ""

# 4) POST grating (G1)
Write-Host "[4] POST /api/v1/grating (name=G1)"
$st3 = Invoke-JsonPost "/api/v1/grating" @{ name = "G1" }
$st3 | ConvertTo-Json -Depth 5
Write-Host ""

# 5) GET status again
Write-Host "[5] GET /api/v1/status (final)"
$st4 = Invoke-JsonGet "/api/v1/status"
$st4 | ConvertTo-Json -Depth 5
Write-Host ""

# Simple checks (non-fatal, just human-readable)
Write-Host "== Checks =="
Write-Host ("slit_width_um: {0} -> {1}" -f $st0.slit_width_um, $st4.slit_width_um)
Write-Host ("lamp_on      : {0} -> {1}" -f $st0.lamp_on, $st4.lamp_on)
Write-Host ("grating      : {0} -> {1}" -f $st0.grating, $st4.grating)
Write-Host ""
Write-Host "Done."
