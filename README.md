# 🧠 DARIA — Fraud Signal Detector ( Augmented Producer )

**DARIA** — *Detection And Risk-Intelligence Agent* — begins here.  
This system powers real-time fraud simulation and streaming analysis across AWS + Web3 systems.

---

## ⚡️ Overview

`DARIA` is a **real-time fraud detection architecture** built on  
**Amazon Kinesis Data Streams** + **KaggleHub** + **Python**.

It ingests a Kaggle credit-card dataset, serializes each transaction,  
and publishes them into **sharded Kinesis streams** for downstream analytics,  
risk scoring, and eventually blockchain-backed audit trails.

> 🧩 *This is where DARIA learns to “see” — synthetic data, real signals.*

---

## 🎯 Why This Exists

- Showcase a **streaming-first** fraud detection architecture (not batch).  
- Demonstrate **ordered, replayable shards** and horizontal throughput.  
- Provide a clean, reproducible **producer pipeline** anyone can point at their own stream.  
- Bridge **AWS ML + Web3**, enabling on-chain logging and smart-contract-based rule enforcement.

---

## 🧱 Core Concepts

| Layer | Purpose |
|-------|----------|
| **Kinesis Data Streams** | Real-time event ingestion (ordered shards). |
| **KaggleHub** | Pulls public Kaggle datasets directly into the pipeline. |
| **Augmented Transactions** | Synthetic + SMOTE-balanced data from Tranche I. |
| **Smart Contracts (future)** | Run fraud-rule logic and immutable logging on-chain. |
| **DARIA** | The AI Agent orchestrating detection and risk intelligence. |

---

## 🚀 Quick Start

```bash
# 1.  Create and activate virtual environment
python -m venv .venv && source .venv/bin/activate

# 2.  Install dependencies
pip install -r requirements.txt

# 3.  Configure environment
cp .env.example .env      # update region / stream / creds

# 4.  Provision the stream
bash infra/create_stream.sh fraud-transactions-stream 2 us-east-1

# 5.  Run the producer
python -m src.producer      # publishes Kaggle (or augmented) transactions

# 6.  Optional: test a consumer
python -m src.consumer_demo # quick reader
````
 
## 🐍 Python virtualenv & Jupyter kernel (zsh / macOS)

If you want a repeatable Python environment for the notebooks and to select a dedicated Jupyter kernel, run these commands from the repository root (zsh):

```bash
# Create and activate a venv in the repo (creates `./.venv`)
python3 -m venv .venv
source .venv/bin/activate

# Upgrade packaging tools and install dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install the package in editable mode for development
pip install -e .

# Ensure Jupyter + ipykernel are available and register a kernel
pip install jupyter ipykernel
python -m ipykernel install --user --name daria-venv --display-name "daria (.venv)"

# Quick check (should print OK messages)
python -c "import daredev_fraud; print('daredev_fraud import OK')"
python -c "from daredev_fraud.data_ingestion import load_fraud_dataset; print('load_fraud_dataset imported:', callable(load_fraud_dataset))"
```

Once the kernel is installed, open Jupyter Notebook or Lab and choose the kernel named "daria (.venv)" from the Kernel menu.





## 🧬 Data Lineage

**Input → Augmentation → Stream**

1. `creditcard.csv` from Kaggle
2. Augmented via SMOTE + Faker (see `02_data_augmentation_with_faker.ipynb`)
3. Serialized into JSON payloads
4. Pushed into `fraud-transactions-stream` shards
5. Read downstream for analytics, rule evaluation, and ML training

---

## 🌐 Web3 Integration (Upcoming)

DARIA’s risk events will soon publish to **smart contracts** that:

* Verify fraud-rule outcomes on-chain
* Append immutable audit logs
* Enable decentralized compliance tracing

> *AWS streams meet blockchain state — transparency by design.*

---

## 🧠 Roadmap

| Phase           | Focus                                                     |
| --------------- | --------------------------------------------------------- |
| **Tranche I**   | Data Augmentation (SMOTE + Faker) ✅                       |
| **Tranche II**  | Real-time Streaming Producer (AWS Kinesis) ✅              |
| **Tranche III** | Fraud-Rule Engine + Smart Contract Logging 🧩             |
| **Tranche IV**  | Model Serving + SageMaker Integration 🚀                  |
| **Tranche V**   | DARIA as an Autonomous Risk Agent (AWS Bedrock + Web3) 🌌 |

---

## 🪞 Vision

> “DARIA doesn’t guess — she *knows* when something feels off.”
> — Naz Wright, DareDevTech

The goal isn’t just to detect fraud — it’s to teach machines the intuition of trust.

---

## 🧰 CI / Deployment

This repository includes a GitHub Actions workflow that validates and deploys the
SAM/CloudFormation template located at `src/daredev_fraud/infra/sam/kinesis_infra.yaml`.

- Workflow path: `.github/workflows/github-actions-demo.yml`.
- The workflow validates the CloudFormation template and applies a change set (using OIDC).
- Set `AWS_ROLE_ARN` in repository secrets to allow the workflow to assume a deploy role in your account.

For local development, a commit template is provided at the repository root as
`.gitmessage.txt`. VS Code is configured (via `.vscode/settings.json`) to open
the editor for commit messages so the template appears automatically when
you run `git commit` without `-m`. Edit the template and remove comment lines
before saving the final commit message.

## � Local testing (LocalStack)

If you want to run and test the Kinesis producer locally without touching AWS, use LocalStack.

1. Start LocalStack (from repo root):

```bash
docker compose -f docker-compose.localstack.yml up -d
```

2. Create a Kinesis stream in LocalStack:

```bash
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_REGION=us-east-1
aws --endpoint-url=http://localhost:4566 kinesis create-stream --stream-name fraud-stream --shard-count 1
```

3. Run the local producer (sends demo rows):

```bash
export KINESIS_ENDPOINT=http://localhost:4566
python local_producer.py
```

Notes:
- LocalStack listens on the edge port 4566 by default in this compose file.
- The demo producer uses `KINESIS_ENDPOINT` environment variable to point at LocalStack.


## �🖋️ Author

**Nazere Wright (@daredevtech)**
*Full-Stack + AWS Machine Learning Engineer*
Building myth-driven, cloud-native intelligence systems.

---

