# Fraud Signal Detector — Augmented Producer

Real-time fraud demo using **Kinesis Data Streams**. We pull a Kaggle dataset via **KaggleHub**, serialize transactions, and publish them into a sharded stream for downstream analytics (rules + ML).

## Why this exists
- Show **streaming-first** fraud detection (not batch).
- Demonstrate **ordered, replayable** shards + horizontal throughput.
- Provide a clean producer that anyone can point at their own stream.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # update region/stream
bash infra/create_stream.sh fraud-transactions-stream 2 us-east-1

python -m src.producer   # publishes Kaggle transactions
python -m src.consumer_demo  # quick reader
