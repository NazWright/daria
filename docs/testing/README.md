# docs/testing — Local testing and quickstart

This directory indexes testing-first docs and commands.

- `local-testing.md` — step-by-step instructions to run LocalStack locally and exercise the demo producer.

Key commands (see `docs/local-testing.md` for the full flow):

```bash
docker compose -f docker-compose.localstack.yml up -d
docker compose -f docker-compose.localstack.yml logs --follow --tail 100
aws --endpoint-url=http://localhost:4566 kinesis create-stream --stream-name fraud-transactions-stream --shard-count 1
KINESIS_ENDPOINT=http://localhost:4566 STREAM_NAME=fraud-transactions-stream python local_producer.py
```
