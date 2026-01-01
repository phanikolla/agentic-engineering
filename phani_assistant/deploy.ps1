# One-Click Deployment Script for Phani Assistant
# Prerequisites: AWS CLI configured, SAM CLI installed, Docker running

param(
    [string]$Region = "us-east-1"
)

$ErrorActionPreference = "Stop"

Write-Host "========================================"
Write-Host "  Phani Assistant - AWS Deployment"
Write-Host "========================================"
Write-Host ""

# Check prerequisites
Write-Host "[1/6] Checking prerequisites..." -ForegroundColor Yellow

# Check AWS CLI
try {
    $null = aws --version 2>&1
    Write-Host "  AWS CLI installed" -ForegroundColor Green
} catch {
    Write-Host "  AWS CLI not found. Install from: https://aws.amazon.com/cli/" -ForegroundColor Red
    exit 1
}

# Check SAM CLI
try {
    $null = sam --version 2>&1
    Write-Host "  SAM CLI installed" -ForegroundColor Green
} catch {
    Write-Host "  SAM CLI not found. Install from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html" -ForegroundColor Red
    exit 1
}

# Check Docker
try {
    $null = docker info 2>&1
    Write-Host "  Docker running" -ForegroundColor Green
} catch {
    Write-Host "  Docker not running. Please start Docker Desktop" -ForegroundColor Red
    exit 1
}

# Load environment variables from .env file
Write-Host ""
Write-Host "[2/6] Loading secrets from .env file..." -ForegroundColor Yellow

$envFile = Join-Path $PSScriptRoot ".." ".env"
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile
    foreach ($line in $envContent) {
        if ($line -and (-not $line.StartsWith("#"))) {
            $parts = $line.Split("=", 2)
            if ($parts.Length -eq 2) {
                $key = $parts[0].Trim()
                $value = $parts[1].Trim()
                [Environment]::SetEnvironmentVariable($key, $value, "Process")
            }
        }
    }
    Write-Host "  Environment variables loaded" -ForegroundColor Green
} else {
    Write-Host "  .env file not found at $envFile" -ForegroundColor Red
    exit 1
}

# Validate required secrets
$requiredVars = @("PERPLEXITY_API_KEY", "PUSHOVER_USER", "PUSHOVER_TOKEN")
foreach ($var in $requiredVars) {
    $val = [Environment]::GetEnvironmentVariable($var)
    if (-not $val) {
        Write-Host "  Missing required variable: $var" -ForegroundColor Red
        exit 1
    }
}
Write-Host "  All required secrets present" -ForegroundColor Green

# Build the application
Write-Host ""
Write-Host "[3/6] Building Docker image..." -ForegroundColor Yellow
Push-Location $PSScriptRoot
sam build
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Build failed" -ForegroundColor Red
    Pop-Location
    exit 1
}
Write-Host "  Build successful" -ForegroundColor Green

# Deploy to AWS
Write-Host ""
Write-Host "[4/6] Deploying to AWS Lambda..." -ForegroundColor Yellow

$perplexityKey = [Environment]::GetEnvironmentVariable("PERPLEXITY_API_KEY")
$pushoverUser = [Environment]::GetEnvironmentVariable("PUSHOVER_USER")
$pushoverToken = [Environment]::GetEnvironmentVariable("PUSHOVER_TOKEN")

sam deploy --region $Region --parameter-overrides "PerplexityApiKey=$perplexityKey" "PushoverUser=$pushoverUser" "PushoverToken=$pushoverToken" --no-confirm-changeset --no-fail-on-empty-changeset

if ($LASTEXITCODE -ne 0) {
    Write-Host "  Deployment failed" -ForegroundColor Red
    Pop-Location
    exit 1
}
Write-Host "  Deployment successful" -ForegroundColor Green

# Get outputs
Write-Host ""
Write-Host "[5/6] Retrieving deployment URLs..." -ForegroundColor Yellow

$stackInfo = aws cloudformation describe-stacks --stack-name phani-assistant --region $Region --query "Stacks[0].Outputs" 2>&1 | ConvertFrom-Json

Write-Host ""
Write-Host "========================================"
Write-Host "  Deployment Complete!"
Write-Host "========================================"
Write-Host ""

if ($stackInfo) {
    foreach ($output in $stackInfo) {
        Write-Host "$($output.Description):" -ForegroundColor Yellow
        Write-Host "  $($output.OutputValue)"
        Write-Host ""
    }
}

Write-Host "[6/6] Your Phani Assistant is now live!" -ForegroundColor Green
Pop-Location
