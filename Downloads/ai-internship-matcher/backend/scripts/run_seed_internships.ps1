<#
PowerShell helper to run the RapidAPI-backed seeder only if RapidAPI keys are configured.
Usage (run from repo root):
  .\backend\scripts\run_seed_internships.ps1
#>
$envFile = Join-Path (Get-Location) "backend" ".env"
if (Test-Path $envFile) {
    Write-Host "Loading .env from backend/.env"
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^\s*([^#=]+)=\s*(.*)\s*$") {
            $k=$matches[1].Trim(); $v=$matches[2].Trim();
            if ($k -and $v) {
                Write-Host "Setting env var $k"
                Set-Item -Path env:$k -Value $v
            }
        }
    }
}

if (-not $env:RAPID_API_KEY) {
    Write-Error "RAPID_API_KEY not set. Aborting seeder. Set RAPID_API_KEY in backend/.env or environment."
    exit 1
}

Write-Host "Running seed_internships.py (Philippines-focused)..."
cd .\backend
python .\scripts\seed_internships.py
Write-Host "Seeder finished."
