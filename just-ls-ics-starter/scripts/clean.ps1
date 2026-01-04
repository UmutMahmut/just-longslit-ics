[CmdletBinding()]
param(
    [switch]$DryRun,
    [ValidateSet("starter", "repo")]
    [string]$Scope = "starter",

    # 是否连 repo_tree*.txt 这类“沟通输出物”也清掉（默认不动）
    [switch]$IncludeTreeOutputs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-RepoRoot([string]$fromDir) {
    $root = ""
    try {
        $root = (git -C $fromDir rev-parse --show-toplevel 2>$null).Trim()
    } catch {
        $root = ""
    }
    if (-not $root) {
        throw "Not inside a Git repository (git rev-parse --show-toplevel failed)."
    }
    return $root
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot  = Get-RepoRoot $scriptDir

$starterRoot = Join-Path $repoRoot "just-ls-ics-starter"
if (-not (Test-Path $starterRoot)) {
    throw "Expected starter root not found: $starterRoot"
}

$targetRoot = if ($Scope -eq "repo") { $repoRoot } else { $starterRoot }

# 目录类垃圾（按“目录名”匹配）
$dirNames = @(
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    "dist",
    "build",
    "site"
)

# 文件类垃圾（按通配符匹配）
$filePatterns = @("*.pyc", "*.pyo", "*.pyd")

# 固定路径（相对 targetRoot）
$fixedPaths = @(
    (Join-Path $targetRoot "docs\site")
)

if ($IncludeTreeOutputs -and $Scope -eq "repo") {
    $fixedPaths += @(
        (Join-Path $repoRoot "repo_tree.txt"),
        (Join-Path $repoRoot "repo_tree_brief.txt"),
        (Join-Path $repoRoot "temp_tree.txt")
    )
}

# 收集候选项
$items = @()

# 1) 固定路径（存在才加入）
foreach ($p in $fixedPaths) {
    if (Test-Path $p) { $items += Get-Item -Force $p }
}

# 2) 按目录名扫描（包含 *.egg-info）
$items += Get-ChildItem -Path $targetRoot -Recurse -Directory -Force -ErrorAction SilentlyContinue |
    Where-Object { ($dirNames -contains $_.Name) -or ($_.Name -like "*.egg-info") }

# 3) 按文件模式扫描
$items += Get-ChildItem -Path $targetRoot -Recurse -File -Force -ErrorAction SilentlyContinue -Include $filePatterns

# 去重
$items = $items | Sort-Object FullName -Unique

Write-Host ("Target root : {0}" -f $targetRoot)
Write-Host ("Scope       : {0}" -f $Scope)
Write-Host ("DryRun      : {0}" -f $DryRun)
Write-Host ("Candidates  : {0}" -f $items.Count)

if ($items.Count -eq 0) {
    Write-Host "Nothing to clean."
    Write-Host "Done."
    exit 0
}

# DryRun：列出清理清单但不删除
if ($DryRun) {
    Write-Host ""
    Write-Host "---- Would remove ----"
    foreach ($it in $items) {
        # 打印相对路径更易读
        $rel = $it.FullName.Replace($targetRoot.TrimEnd('\') + "\", "")
        Write-Host $rel
    }
    Write-Host "----------------------"
    Write-Host "Done."
    exit 0
}

# 实删：先删文件，再删目录（避免目录非空）
$files = $items | Where-Object { -not $_.PSIsContainer }
$dirs  = $items | Where-Object { $_.PSIsContainer } | Sort-Object FullName -Descending

foreach ($f in $files) {
    Remove-Item -Force $f.FullName
}
foreach ($d in $dirs) {
    Remove-Item -Recurse -Force $d.FullName
}

Write-Host "Removed: $($items.Count) items."
Write-Host "Done."
