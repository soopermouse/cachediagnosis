# Cachemed Infrastructure

This directory contains AWS CloudFormation templates for deploying Cachemed infrastructure.

## Files

| File | Description |
|------|-------------|
| `database.yaml` | DynamoDB tables for patients, biometrics, files, predictions |
| `auth.yaml` | Cognito user pools and identity pools |
| `storage.yaml` | S3 buckets for file storage |
| `api.yaml` | API Gateway and Lambda functions |
| `monitoring.yaml` | CloudWatch dashboards and alarms |
| `networking.yaml` | VPC, subnets, and networking |

## Deployment Order

Deploy in this order:

1. `networking.yaml` - VPC and networking
2. `database.yaml` - DynamoDB tables
3. `storage.yaml` - S3 buckets
4. `auth.yaml` - Cognito authentication
5. `api.yaml` - API Gateway and Lambda
6. `monitoring.yaml` - Monitoring and alerts

## Deployment Commands

```bash
# Deploy networking
aws cloudformation deploy \
  --template-file infrastructure/networking.yaml \
  --stack-name cachemed-dev-networking \
  --parameter-overrides Environment=dev

# Deploy database
aws cloudformation deploy \
  --template-file infrastructure/database.yaml \
  --stack-name cachemed-dev-database \
  --parameter-overrides Environment=dev

# Deploy storage
aws cloudformation deploy \
  --template-file infrastructure/storage.yaml \
  --stack-name cachemed-dev-storage \
  --parameter-overrides Environment=dev

# Deploy auth
aws cloudformation deploy \
  --template-file infrastructure/auth.yaml \
  --stack-name cachemed-dev-auth \
  --parameter-overrides Environment=dev DomainPrefix=cachemed

# Deploy API
aws cloudformation deploy \
  --template-file infrastructure/api.yaml \
  --stack-name cachemed-dev-api \
  --parameter-overrides Environment=dev LambdaCodeBucket=your-bucket

# Deploy monitoring
aws cloudformation deploy \
  --template-file infrastructure/monitoring.yaml \
  --stack-name cachemed-dev-monitoring \
  --parameter-overrides Environment=dev AlarmEmail=your-email@example.com