from fastapi import FastAPI, HTTPException
import boto3
import os
from dotenv import load_dotenv
import json

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

client = boto3.client(
    'stepfunctions',
    region_name=os.getenv('AWS_DEFAULT_REGION', 'ca-central-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)


@app.post("/orchestrate")
async def orchestrate(payload: dict):
    """
    Docstring for orchestrate
    
    :param input: Description
    """
    try:
        # Business Logic: Ensure Policy ID exist
        if not payload["claim_details"]["policy_number"]:
            raise HTTPException(
                status_code=400, detail="policy number missing")

        response = client.start_execution(
            stateMachineArn=os.getenv("STATE_MACHINE_ARN"),
            input=json.dumps(payload)
        )
        return (f"Execution started: {response['executionArn']}")
    except Exception as e:
        return {"status": "error", "msg": str(e)}


@app.get("/health")
async def read_root():
    return {"status": "health check"}
