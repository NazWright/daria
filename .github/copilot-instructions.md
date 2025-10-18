# Copilot Instructions — Fraud Signal Detector (producer)

This repository is a small streaming-first demo that publishes Kaggle transaction records into an Amazon Kinesis Data Stream. The codebase is intentionally minimal; the important files and workflows are documented below so an AI coding agent can be productive immediately.

Overview
- Purpose: publish ordered, replayable transaction events to a Kinesis stream for downstream rules/ML.
- Main components: a lightweight producer (`src`), a consumer demo (`src.consumer_demo`), and infrastructure helpers (`infra/*.sh`).
- Data source: Kaggle dataset loaded via `kagglehub` and serialized per-record before publishing.

Key files
- `README.md`: bootstrapping, virtualenv, and example run commands.
- `src/daredev-fraud/__init__.py`: example KaggleHub usage and hint about required extras (`kagglehub[pandas-datasets]`).
- `infra/create_stream.sh`: stream creation helper (region and shard inputs).

Developer workflows & commands
- Setup virtualenv and install deps:
  - `python -m venv .venv && source .venv/bin/activate`
  - `pip install -r requirements.txt`
- Create stream (example):
  - `bash infra/create_stream.sh fraud-transactions-stream 2 us-east-1`
- Run producer (publishes Kaggle transactions):
  - `python -m src.producer`
- Quick consumer reader:
  - `python -m src.consumer_demo`

Project-specific patterns and conventions
- Streaming-first: code focuses on per-record serialization and immediate publish. Prefer clear, small functions that transform a single record.
- External-data adapter: Kaggle datasets are loaded via `kagglehub.dataset_load(KaggleDatasetAdapter.PANDAS, ...)`. The project expects `kagglehub[pandas-datasets]` extras (see `src/daredev-fraud/__init__.py`). If you see ImportError referencing `pandas-datasets`, install extras with: `pip install kagglehub[pandas-datasets]`.
- Config via environment: the project uses a `.env` example. Prefer reading configuration from environment variables rather than hardcoding AWS region/stream names.

Integration points and dependencies
- AWS Kinesis Data Streams: publishing uses the AWS SDK (boto3) — be mindful of region and credentials in the environment.
- KaggleHub: dataset retrieval. Use the `KaggleDatasetAdapter.PANDAS` path when downstream code expects a Pandas DataFrame.

Examples to copy/paste
- KaggleHub load snippet (from `src/daredev-fraud/__init__.py`):
  ```py
  import kagglehub
  from kagglehub import KaggleDatasetAdapter

  df = kagglehub.dataset_load(
    KaggleDatasetAdapter.PANDAS,
    "vipin20/transaction-data",
    "",
  )
  ```

What to avoid / common pitfalls
- Missing `kagglehub` extras: you'll get an ImportError if the `pandas-datasets` extras are not installed — message: "The 'dataset_load' function requires the 'pandas-datasets' extras. Install them with 'pip install kagglehub[pandas-datasets]'".
- Hardcoding stream names or AWS region in code — prefer `.env` or environment variables.

If you change code that reads or writes streams
- Update `README.md` with new example commands.
- Add small unit or integration test (script) that can run locally with a mocked Kinesis client or AWS credentials.

When to ask the repo owner
- If you need AWS credentials or a specific Kinesis stream name for integration tests.
- Clarify whether the producer should support multiple dataset sources or different Kaggle datasets.

Feedback
- Ask for clarification if any runtime steps are unclear, or if you want me to add examples for mocking AWS or using localstack for offline development.
