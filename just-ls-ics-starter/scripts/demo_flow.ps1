param(
  [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"

function Invoke-Json {
  param(
    [Parameter(Mandatory=$true)][string]$Method,
    [Parameter(Mandatory=$true)][string]$Path,
    [object]$Body = $null
  )

  $uri = "$BaseUrl$Path"
  Write-Host ""
  Write-Host "==> $Method $uri" -ForegroundColor Cyan

  if ($null -ne $Body) {
    $json = $Body | ConvertTo-Json -Depth 10
    Write-Host "Body: $json"
    return Invoke-RestMethod -Method $Method -Uri $uri -ContentType "application/json" -Body $json
  } else {
    return Invoke-RestMethod -Method $Method -Uri $uri
  }
}

Write-Host "JUST Long-Slit ICS demo flow (v0.1)" -ForegroundColor Green
Write-Host "BaseUrl: $BaseUrl"

# 1) GET status
$status1 = Invoke-Json -Method "GET" -Path "/api/v1/status"
Write-Host "Status (initial):" -ForegroundColor Yellow
$status1 | ConvertTo-Json -Depth 10

# 2) POST slit
$slit = Invoke-Json -Method "POST" -Path "/api/v1/slit" -Body @{ width_um = 200 }
Write-Host "After slit:" -ForegroundColor Yellow
$slit | ConvertTo-Json -Depth 10

# 3) POST slit_angle
$angle = Invoke-Json -Method "POST" -Path "/api/v1/slit_angle" -Body @{ angle_deg = 0 }
Write-Host "After slit_angle:" -ForegroundColor Yellow
$angle | ConvertTo-Json -Depth 10

# 4) POST lamp
$lamp = Invoke-Json -Method "POST" -Path "/api/v1/lamp" -Body @{ on = $true }
Write-Host "After lamp:" -ForegroundColor Yellow
$lamp | ConvertTo-Json -Depth 10

# 5) GET status (final)
$status2 = Invoke-Json -Method "GET" -Path "/api/v1/status"
Write-Host "Status (final):" -ForegroundColor Yellow
$status2 | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "Done." -ForegroundColor Green
