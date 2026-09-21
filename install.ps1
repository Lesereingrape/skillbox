# Install skills from this repo into $HOME\.qoder\skills\.
# Usage: .\install.ps1 [skill-name ...]   (default: all)
param([string[]]$Names)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$Dest = Join-Path $HOME ".qoder\skills"
New-Item -ItemType Directory -Force -Path $Dest | Out-Null

if (-not $Names) {
  $Names = Get-ChildItem "skills" -Directory | Select-Object -ExpandProperty Name
}
foreach ($n in $Names) {
  $src = Join-Path "skills" $n
  if (-not (Test-Path (Join-Path $src "SKILL.md"))) { Write-Host "SKIP $n (no SKILL.md)"; continue }
  $target = Join-Path $Dest $n
  if (Test-Path $target) { Remove-Item -Recurse -Force $target }
  Copy-Item -Recurse $src $target
  Write-Host "INSTALLED $n -> $target"
}
Write-Host "Done. Restart the session or run /skills reload."
