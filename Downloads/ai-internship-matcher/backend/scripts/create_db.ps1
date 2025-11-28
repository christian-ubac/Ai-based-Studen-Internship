<#
PowerShell helper to create a PostgreSQL user and database using psql.
Usage (PowerShell):
  # set postgres superuser password for this session (if required)
  $env:PGPASSWORD = Read-Host -Prompt "Postgres superuser password" -AsSecureString | ConvertFrom-SecureString
  # easier: set plain text for the session (less secure):
  $env:PGPASSWORD = 'your_postgres_password'

  # run script with defaults
  .\create_db.ps1

Optional parameters:
  -DbUser, -DbPass, -DbName, -Host, -Port, -SuperUser

This script requires `psql` to be installed and available in PATH.
#>
param(
    [string]$DbUser = "internship_user",
    [string]$DbPass = "Internship@2025",
    [string]$DbName = "internshipdb",
    [string]$Host = "localhost",
    [int]$Port = 5432,
    [string]$SuperUser = "postgres"
)

# Helper to run a psql command
function Run-Sql($sql) {
    $cmd = "psql -U $SuperUser -h $Host -p $Port -d postgres -c \"$sql\""
    Write-Host "Running: $cmd"
    $proc = Start-Process -FilePath psql -ArgumentList "-U", $SuperUser, "-h", $Host, "-p", $Port.ToString(), "-d", "postgres", "-c", $sql -NoNewWindow -Wait -PassThru -RedirectStandardOutput stdout.txt -RedirectStandardError stderr.txt
    if ($proc.ExitCode -ne 0) {
        Write-Host "psql returned exit code $($proc.ExitCode). Check stderr.txt"
        Get-Content stderr.txt | Write-Host
    } else {
        Get-Content stdout.txt | Write-Host
    }
}

# Compose SQL statements
$createUser = "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DbUser') THEN CREATE ROLE \"$DbUser\" WITH LOGIN PASSWORD '$DbPass'; END IF; END $$;"
$createDb = "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DbName') THEN CREATE DATABASE \"$DbName\" OWNER \"$DbUser\"; END IF; END $$;"

Write-Host "Creating user (if not exists)..."
Run-Sql $createUser
Write-Host "Creating database (if not exists)..."
Run-Sql $createDb

Write-Host "Done. Suggested DATABASE_URL:"
Write-Host "postgresql://$DbUser:$DbPass@$Host:$Port/$DbName"
