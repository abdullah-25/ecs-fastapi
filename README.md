## Insurance Data Orchestrator
Microservice for claim ingestion and automated workflow triggering.

## Overview
This service provides a lightweight, containerized API to ingest insurance claim data and orchestrate downstream processing via AWS Step Functions.

Capability: Claims Ingestion, Validation, and Notification.

Stack: Python 3.11, FastAPI, Docker, AWS Fargate, AWS Step Functions.

## System Architecture
![alt text](https://github.com/abdullah-25/ecs-fastapi/blob/main/assets/system-design.png?raw=true)

The architecture follows a "Fire and Forget" pattern where the FastAPI container validates the initial request and delegates long-running business logic to a Standard Step Function workflow for full auditability.

## Execution Instructions
1. Local Development
To run the container locally and connect to AWS, you must mount your local credentials:


# Build the image
```
docker build -t insurance-orchestrator .

```

# Run with environment variables
```
docker run -p 8000:8000 \
  -e STATE_MACHINE_ARN="your-arn-here" \
  -e AWS_REGION="your-region" \
  -v ~/.aws:/home/appuser/.aws:ro \
  insurance-orchestrator
```

2. Testing the API
Submit a sample claim JSON via the CLI:

```
curl -X POST "http://localhost:8000/orchestrate" \
     -H "Content-Type: application/json" \
     -d '{
          "metadata": {"correlation_id": "test-123"},
          "claim_details": {"policy_number": "POL-999"},
          "claimant": {"name": "John Doe"},
          "estimated_loss": {"amount": 4500},
          "attachments": []
         }'
```

## Infrastructure & Observability
Health Check: GET /health.

Logs: Application logs are exported to Amazon CloudWatch under the /ecs/insurance-orchestrator group.

Audit Trail: Every execution can be traced in the Step Functions Console using the execution_id returned by the API.

## Security Standards
Least Privilege: The service uses an IAM Task Role restricted solely to starting the orchestration workflow.

Non-Root User: The container runs as a non-privileged appuser.

Vulnerability Scanning: ECR "Scan on Push" is required for all production images.
