<#
PowerShell helper to stage and commit removal of a file from git.
Usage (run from repo root):

  .\backend\scripts\git_remove_file.ps1 -PathToRemove "backend/scripts/seed_data.py" -Message "Remove deprecated seed_data"

This script runs `git rm` and `git commit`. It does not push — run `git push` after verifying the commit.
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$PathToRemove,
    [string]$Message = "Remove file"
)

if (-not (Test-Path $PathToRemove)) {
    Write-Host "File not found: $PathToRemove" -ForegroundColor Yellow
    exit 1
}

Write-Host "Staging removal of $PathToRemove..."
git rm --cached --force $PathToRemove 2>&1 | Write-Host

Write-Host "Committing..."
git commit -m $Message 2>&1 | Write-Host

Write-Host "Done. If you want to push, run: git push origin HEAD" -ForegroundColor Green
