# Phani Assistant - One-Click AWS Deployment

## Prerequisites

1. **AWS CLI** - [Install Guide](https://aws.amazon.com/cli/)
2. **SAM CLI** - [Install Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
3. **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
4. **AWS Credentials** configured (`aws configure`)

## One-Click Deploy

### Windows (PowerShell)
```powershell
cd phani_assistant
.\deploy.ps1
```

### Linux/Mac
```bash
cd phani_assistant
chmod +x deploy.sh
./deploy.sh
```

## What Gets Deployed

- **AWS Lambda** with Function URL (serverless, pay-per-use)
- **API Gateway** HTTP API (low latency)
- **Docker container** with Lambda Web Adapter

## Cost Estimate

| Resource | Free Tier | After Free Tier |
|----------|-----------|-----------------|
| Lambda | 1M requests/month | ~$0.20/1M requests |
| API Gateway | 1M requests/month | ~$1.00/1M requests |
| ECR Storage | 500MB | ~$0.10/GB/month |

**Estimated monthly cost for light usage: $0 - $5**

## Manual Deployment (Alternative)

```bash
cd phani_assistant

# Build
sam build

# Deploy (will prompt for parameters)
sam deploy --guided
```

## Cleanup

To delete all resources:
```bash
sam delete --stack-name phani-assistant --region us-east-1
```

## Troubleshooting

**Docker not running**: Start Docker Desktop before deploying

**AWS credentials**: Run `aws configure` to set up credentials

**Build fails**: Ensure Docker has enough memory (4GB+ recommended)
