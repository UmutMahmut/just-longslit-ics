param(
  [string]$Message = "",
  [switch]$AllowMain
)

$ErrorActionPreference = "Stop"
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

# 必须在 Git 仓库内
git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) { Write-Error "Not a git repository."; exit 1 }

# 当前分支 & 保护 main
$branch = (git rev-parse --abbrev-ref HEAD).Trim()
if ($branch -eq "HEAD") { Write-Error "Detached HEAD; checkout a branch."; exit 1 }
if ($branch -eq "main" -and -not $AllowMain) {
  Write-Host "You are on 'main'. Use -AllowMain to push to main, or create a feature branch."
  exit 2
}

# 预览状态并暂存
git status -sb
git add -A

# 没有暂存内容就退出
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) { Write-Host "Nothing to commit."; exit 0 }

# 防止 .env 被误提交
$staged = (git diff --cached --name-only).Split([Environment]::NewLine) | Where-Object { $_ }
$hasEnv = $false
foreach ($f in $staged) { if ($f -match '(^|[\\/])\.env($|[\\/\.])') { $hasEnv = $true } }
if ($hasEnv) { Write-Error ".env is staged; aborting to protect secrets."; exit 3 }

# 默认提交信息
if (-not $Message) { $Message = "chore(sync): " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") }

Write-Host "About to commit the following files:"
$staged | ForEach-Object { Write-Host "  $_" }
$ans = Read-Host 'Commit and push now? (y/N)'
if ($ans -notin @('y','Y')) { Write-Host 'Aborted.'; exit 0 }

git commit -m $Message

# 推送：若无 upstream 则建立
$up = (git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>$null)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($up)) {
  git push -u origin $branch
} else {
  git push
}
Write-Host 'Sync complete.'
