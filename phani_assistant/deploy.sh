#!/bin/bash
# One-Click Deployment Script for Phani Assistant
# Prerequisites: AWS CLI configured, SAM CLI installed, Docker running

set -e

REGION="${1:-us-east-1}"

echo "========================================"
echo "  Phani Assistant - AWS Deployment"
echo "========================================"
echo ""

# Check prerequisites
echo "[1/6] Checking prerequisites..."

if ! command -v aws &> /dev/null; then
    echo "  ✗ AWS CLI not found. Install from: https://aws.amazon.com/cli/"
    exit 1
fi
echo "  ✓ AWS CLI installed"

if ! command -v sam &> /dev/null; then
    echo "  ✗ SAM CLI not found. Install from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html"
    exit 1
fi
echo "  ✓ SAM CLI installed"

if ! docker info &> /dev/null; then
    echo "  ✗ Docker not running. Please start Docker"
    exit 1
fi
echo "  ✓ Docker running"

# Load environment variables
echo ""
echo "[2/6] Loading secrets from .env file..."

ENV_FILE="$(dirname "$0")/../../.env"
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
    echo "  ✓ Environment variables loaded"
else
    echo "  ✗ .env file not found at $ENV_FILE"
    exit 1
fi

# Validate required secrets
for var in PERPLEXITY_API_KEY PUSHOVER_USER PUSHOVER_TOKEN; do
    if [ -z "${!var}" ]; then
        echo "  ✗ Missing required variable: $var"
        exit 1
    fi
done
echo "  ✓ All required secrets present"

# Build
echo ""
echo "[3/6] Building Docker image..."
sam build
echo "  ✓ Build successful"

# Deploy
echo ""
echo "[4/6] Deploying to AWS Lambda..."
sam deploy \
    --region "$REGION" \
    --parameter-overrides \
        "PerplexityApiKey=$PERPLEXITY_API_KEY" \
        "PushoverUser=$PUSHOVER_USER" \
        "PushoverToken=$PUSHOVER_TOKEN" \
    --no-confirm-changeset \
    --no-fail-on-empty-changeset

echo "  ✓ Deployment successful"

# Get outputs
echo ""
echo "[5/6] Retrieving deployment URLs..."
echo ""
echo "========================================"
echo "  Deployment Complete!"
echo "========================================"
echo ""

aws cloudformation describe-stacks \
    --stack-name phani-assistant \
    --region "$REGION" \
    --query "Stacks[0].Outputs[*].[Description,OutputValue]" \
    --output table

echo ""
echo "[6/6] Your Phani Assistant is now live!"
