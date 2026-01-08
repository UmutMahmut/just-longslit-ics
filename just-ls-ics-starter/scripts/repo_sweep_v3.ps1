param(
  [string]$RepoRoot = "",
  [switch]$Strict
)

$ErrorActionPreference = "Stop"

function Resolve-RepoRoot([string]$Hint) {
  if ($Hint -and (Test-Path $Hint)) { return (Resolve-Path $Hint).Path }
  try {
    $top = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -eq 0 -and $top) { return (Resolve-Path $top).Path }
  } catch {}
  return (Get-Location).Path
}

function Ensure-Dir([string]$Path) {
  if (-not (Test-Path $Path)) { New-Item -ItemType Directory -Force -Path $Path | Out-Null }
}

function Tier-Of([string]$Path) {
  $p = $Path -replace '/', '\'
  if ($p -match "\\just-ls-ics-starter\\(src|ui|tests)\\") { return "T1" }
  if ($p -match "\\just-ls-ics-starter\\scripts\\(demo_flow\.ps1|run_.*\.ps1|.*\.ps1)$") { return "T1" }
  if ($p -match "\\docs\\") { return "T2" }
  if ($p -match "\\README\.md$") { return "T2" }
  return "T3"
}

function Filter-Files([string[]]$Paths, [string[]]$IncludeRegex, [string[]]$ExcludeRegex) {
  $out = New-Object System.Collections.Generic.List[string]
  foreach ($f in $Paths) {
    $ok = $true
    if ($IncludeRegex -and $IncludeRegex.Count -gt 0) {
      $ok = $false
      foreach ($r in $IncludeRegex) { if ($f -match $r) { $ok = $true; break } }
    }
    if ($ok -and $ExcludeRegex -and $ExcludeRegex.Count -gt 0) {
      foreach ($r in $ExcludeRegex) { if ($f -match $r) { $ok = $false; break } }
    }
    if ($ok) { $out.Add($f) | Out-Null }
  }
  return $out.ToArray()
}

$RepoRoot = Resolve-RepoRoot $RepoRoot

$Ts = Get-Date -Format "yyyyMMdd_HHmmss"
$OutDir = Join-Path $RepoRoot "just-ls-ics-starter\scripts\sweep_out"
Ensure-Dir $OutDir

$LogPath  = Join-Path $OutDir ("repo_sweep_{0}.log" -f $Ts)
$JsonPath = Join-Path $OutDir ("repo_sweep_{0}.summary.json" -f $Ts)

function Log([string]$s) {
  $s | Tee-Object -FilePath $LogPath -Append
}

Log ("== repo_sweep_v3 ==")
Log ("timestamp : {0}" -f $Ts)
Log ("repo_root : {0}" -f $RepoRoot)

# --- collect files ---
$includeExt = @(".py",".md",".html",".js",".ts",".css",".ps1",".yml",".yaml",".toml",".json",".txt")
$excludeDirNames = @(".git","__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv", "node_modules", "dist", "build", ".idea", ".vscode", "sweep_out")

$allFiles = Get-ChildItem -Path $RepoRoot -Recurse -File -Force |
  Where-Object { $includeExt -contains $_.Extension.ToLower() } |
  Where-Object {
    $p = $_.FullName
    foreach ($d in $excludeDirNames) {
      if ($p -match ("\\{0}\\" -f [regex]::Escape($d))) { return $false }
    }
    return $true
  } |
  ForEach-Object { $_.FullName }

# avoid scanning sweep scripts themselves to reduce noise
$allFiles = Filter-Files $allFiles @() @("\\just-ls-ics-starter\\scripts\\repo_sweep_v[0-9]+\.ps1$")

Log ("target_files : {0}" -f $allFiles.Count)
Log ""

function Run-Check {
  param(
    [string]$Id,
    [string]$Title,
    [string[]]$Patterns,
    [ValidateSet("regex","simple")] [string]$Mode = "regex",
    [string[]]$IncludeRegex = @(),
    [string[]]$ExcludeRegex = @(),
    [int]$SampleMax = 20
  )

  $scope = Filter-Files $allFiles $IncludeRegex $ExcludeRegex
  $hits = @()

  if ($scope.Count -gt 0) {
    if ($Mode -eq "simple") {
      $hits = Select-String -Path $scope -Pattern $Patterns -SimpleMatch -AllMatches -ErrorAction SilentlyContinue
    } else {
      $hits = Select-String -Path $scope -Pattern $Patterns -AllMatches -ErrorAction SilentlyContinue
    }
  }

  $byFile = @{}
  foreach ($h in $hits) {
    if (-not $byFile.ContainsKey($h.Path)) { $byFile[$h.Path] = New-Object System.Collections.Generic.List[object] }
    $byFile[$h.Path].Add($h) | Out-Null
  }

  $files = $byFile.Keys | Sort-Object
  $matchCount = ($hits | Measure-Object).Count

  $tierCount = @{ T1 = 0; T2 = 0; T3 = 0 }
  foreach ($fp in $files) { $tierCount[(Tier-Of $fp)]++ }

  Log ("== [{0}] {1}" -f $Id, $Title)
  Log ("patterns : {0}" -f ($Patterns -join " | "))
  Log ("scope    : {0} files" -f $scope.Count)
  Log ("matches  : {0} (files: {1})  [T1={2}, T2={3}, T3={4}]" -f $matchCount, $files.Count, $tierCount.T1, $tierCount.T2, $tierCount.T3)

  $samples = New-Object System.Collections.Generic.List[string]
  foreach ($fp in $files) {
    foreach ($m in $byFile[$fp]) {
      if ($samples.Count -ge $SampleMax) { break }
      $line = $m.Line.Trim()
      $samples.Add(("{0}:{1}: {2}" -f $fp, $m.LineNumber, $line)) | Out-Null
    }
    if ($samples.Count -ge $SampleMax) { break }
  }

  if ($samples.Count -gt 0) {
    Log ("sample   :")
    foreach ($s in $samples) { Log ("  " + $s) }
  }
  Log ""

  return [pscustomobject]@{
    id = $Id
    title = $Title
    patterns = $Patterns
    scope_files = $scope.Count
    matches = $matchCount
    files = $files
    tiers = $tierCount
    sample = $samples
  }
}

$results = New-Object System.Collections.Generic.List[object]

# --- Endpoint drift: unversioned usage (avoid matching /api/v1/* by negative lookbehind) ---
$results.Add((Run-Check -Id "E1" -Title "Unversioned endpoint usage (runtime-facing)" -Mode "regex" `
  -Patterns @('(?<!/api/v1)/status(\b|")','(?<!/api/v1)/slit(\b|")','(?<!/api/v1)/lamp(\b|")','(?<!/api/v1)/grating(\b|")','(?<!/api/v1)/capabilities(\b|")','(?<!/api/v1)/status/full(\b|")') `
  -IncludeRegex @("\\just-ls-ics-starter\\(ui|scripts|tests)\\") `
  -ExcludeRegex @("\\just-ls-ics-starter\\src\\justls\\ics\\routers\\") )) | Out-Null

$results.Add((Run-Check -Id "E2" -Title "Unversioned endpoint mentions (docs/README)" -Mode "regex" `
  -Patterns @('(?<!/api/v1)/status(\b|")','(?<!/api/v1)/slit(\b|")','(?<!/api/v1)/lamp(\b|")','(?<!/api/v1)/grating(\b|")','(?<!/api/v1)/capabilities(\b|")','(?<!/api/v1)/status/full(\b|")') `
  -IncludeRegex @("\\docs\\","\\README\.md$") )) | Out-Null

# --- Payload drift: legacy request keys that should NOT appear in runtime UI/scripts/tests ---
$results.Add((Run-Check -Id "P1" -Title "Legacy request keys in UI/scripts/tests (width/mode/center_wavelength/active/state)" -Mode "regex" `
  -Patterns @('"width"\s*:','\bwidth\s*:','"mode"\s*:','\bmode\s*:','"center_wavelength"\s*:','\bcenter_wavelength\b','"active"\s*:','\bactive\s*:','"state"\s*:','\bstate\s*:') `
  -IncludeRegex @("\\just-ls-ics-starter\\(ui|scripts|tests)\\") `
  -ExcludeRegex @("\\just-ls-ics-starter\\ui\\.*\.bak$") )) | Out-Null

# --- Response drift: legacy field names in UI ---
$results.Add((Run-Check -Id "R1" -Title "Legacy response fields in UI/scripts (slit_width/lamp/grating variants)" -Mode "regex" `
  -Patterns @('\bslit_width\b','\blamp_state\b','\bgrating_mode\b','\bslit_state\b') `
  -IncludeRegex @("\\just-ls-ics-starter\\(ui|scripts|tests)\\") )) | Out-Null

# --- Hard-coded base URL ---
$results.Add((Run-Check -Id "U1" -Title "Hard-coded API base URL / localhost / port in runtime UI/scripts" -Mode "simple" `
  -Patterns @("http://127.0.0.1:8000","http://localhost:8000","127.0.0.1:8000","localhost:8000") `
  -IncludeRegex @("\\just-ls-ics-starter\\(ui|scripts|tests)\\") )) | Out-Null

# --- HAL capability naming drift ---
$results.Add((Run-Check -Id "H1" -Title "HAL capability naming drift (.capabilities vs get_capabilities)" -Mode "regex" `
  -Patterns @('\.capabilities\(\)','get_capabilities\(\)') `
  -IncludeRegex @("\\just-ls-ics-starter\\src\\") )) | Out-Null

# --- Legacy test injection / direct api.hal override patterns ---
$results.Add((Run-Check -Id "T1" -Title "Legacy test injection patterns (api.hal = SimHAL / etc.)" -Mode "regex" `
  -Patterns @('\bapi\.hal\s*=\s*SimHAL\(','\bapi\.hal\s*=\s*') `
  -IncludeRegex @("\\just-ls-ics-starter\\tests\\") )) | Out-Null

# --- Doc/UI copy drift (hash) ---
Log "== [UIHASH] UI copies hash check"
$uiPaths = @(
  (Join-Path $RepoRoot "just-ls-ics-starter\ui\index.html"),
  (Join-Path $RepoRoot "just-ls-ics-starter\ui\longslit_ui_static.html"),
  (Join-Path $RepoRoot "just-ls-ics-starter\ui\longslit_ui_static.bak"),
  (Join-Path $RepoRoot "docs\ui\longslit_ui_static.html")
) | Where-Object { Test-Path $_ }

$uiHashes = @()
foreach ($p in $uiPaths) {
  $h = (Get-FileHash -Path $p -Algorithm SHA256).Hash
  $uiHashes += [pscustomobject]@{ path = $p; sha256 = $h }
  Log ("  {0}  {1}" -f $h, $p)
}
Log ""

# classify actionable findings
$actionableT1 = 0
foreach ($r in $results) { $actionableT1 += [int]$r.tiers.T1 }

$summary = [pscustomobject]@{
  timestamp = $Ts
  repo_root = $RepoRoot
  target_files = $allFiles.Count
  checks = $results
  ui_hashes = $uiHashes
  actionable_t1_files = $actionableT1
  strict = [bool]$Strict
  log_path = $LogPath
  json_path = $JsonPath
}

($summary | ConvertTo-Json -Depth 12) | Set-Content -Path $JsonPath -Encoding UTF8

Log ("== DONE ==")
Log ("log  : {0}" -f $LogPath)
Log ("json : {0}" -f $JsonPath)
Log ("actionable(T1 files count sum): {0}" -f $actionableT1)

if ($Strict -and $actionableT1 -gt 0) {
  Log "Strict mode: FAIL (actionable Tier1 findings exist)."
  exit 2
}

exit 0
