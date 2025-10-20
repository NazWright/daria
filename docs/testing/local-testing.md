Local testing & deploy commands

This document collects the exact shell commands used to run LocalStack for local testing and to deploy the SAM/CloudFormation stack to AWS. Copy-paste the blocks below into your terminal (zsh) and adjust values where indicated.

1) Prerequisites

- macOS with Homebrew
- Docker Desktop (or Colima + docker)
- AWS CLI v2 and AWS SAM CLI (installed via Homebrew)
- Python 3.10+ (venv recommended)

Install tools (Homebrew):

    # Homebrew (if needed)
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Docker Desktop (GUI) or Colima (headless)
    brew install --cask docker        # installs Docker Desktop (macOS GUI)
    # OR headless option:
    brew install colima docker
    colima start

    # AWS CLI + SAM CLI
    brew install awscli
    brew tap aws/tap
    brew install aws-sam-cli

2) Local Kinesis testing with LocalStack

Create the LocalStack compose file (already provided in this repo as docker-compose.localstack.yml). Start LocalStack:

    # from repo root
    docker compose -f docker-compose.localstack.yml up -d

Create a local Kinesis stream and run the example local producer:

    export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_REGION=us-east-1
    aws --endpoint-url=http://localhost:4566 kinesis create-stream --stream-name fraud-stream --shard-count 1

    # point the demo producer at LocalStack
    export KINESIS_ENDPOINT=http://localhost:4566
    python local_producer.py

Notes:
- LocalStack Edge API listens on port 4566 in the compose file.
- local_producer.py sends demo rows in batches using PutRecords.

To stop LocalStack:

    docker compose -f docker-compose.localstack.yml down

3) Build & deploy SAM to AWS (interactive / guided)

Create an S3 bucket for artifacts (one-time):

    export AWS_PROFILE=default
    export AWS_REGION=us-east-1
    BUCKET=daria-deploy-artifacts-$(date +%s)
    aws s3 mb s3://$BUCKET --region $AWS_REGION

Build the SAM application (from repo root):

    sam build

Guided deploy (recommended first time):

    sam deploy --guided

When prompted, give values such as:
- Stack Name: daria-kinesis-ingestor
- S3 bucket: the bucket you created above
- StreamName: fraud-transactions-stream-dev
- Env: dev
- Capabilities: accept CAPABILITY_IAM and CAPABILITY_NAMED_IAM if requested

4) Build & deploy SAM to AWS (non-interactive)

    # package
    sam package --s3-bucket $BUCKET --output-template-file packaged.yaml

    # deploy
    sam deploy \
      --template-file packaged.yaml \
      --stack-name daria-kinesis-ingestor \
      --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
      --parameter-overrides StreamName=fraud-transactions-stream-dev Env=dev \
      --region $AWS_REGION

Verify stack status and events:

    aws cloudformation describe-stacks --stack-name daria-kinesis-ingestor --region $AWS_REGION
    aws cloudformation describe-stack-events --stack-name daria-kinesis-ingestor --region $AWS_REGION | less

Tail Lambda logs (SAM helper):

    sam logs -n IngestFn --stack-name daria-kinesis-ingestor --tail

5) Clean up (optional)

To delete the stack:

    aws cloudformation delete-stack --stack-name daria-kinesis-ingestor --region $AWS_REGION
    aws cloudformation wait stack-delete-complete --stack-name daria-kinesis-ingestor --region $AWS_REGION

To remove the S3 bucket (if empty):

    aws s3 rb s3://$BUCKET --force

If you'd like, I can:
- Add a Makefile or script that wraps the common commands (start-local, stop-local, create-stream, deploy-dev).
- Add automated tests that run against LocalStack in CI (optional).
