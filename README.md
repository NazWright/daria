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

---

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

## 🖋️ Author

**Nazere Wright (@daredevtech)**
*Full-Stack + AWS Machine Learning Engineer*
Building myth-driven, cloud-native intelligence systems.

---

