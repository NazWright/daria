# DARIA (2025-10-19)

Author: Nazere Wright (@daredevtech)
Repo: fraud-signal-detector-augmented-producer
Branch: feat/day3-streaming

Summary 🚀
-------
This note captures today's developer-infra work, the errors encountered, commands executed, and precise places to pick up from. Use this as a single reference when handoff or continuing work locally.

What I shipped ✅
--------------
- Local testing assets: `docker-compose.localstack.yml` (local emulation of AWS services used by the project).
- Demo producer: `local_producer.py` — publishes sample transactions to a Kinesis stream (configurable endpoint).
- Cloud infra template: `src/daredev_fraud/infra/sam/kinesis_ingestor.yaml` — SAM/CFN template for production deploy.
- Docs updates: `docs/local-testing.md` (step-by-step run commands), plus this consolidated log and small directory indexes to group docs.

High-level motivation 💡
---------------------
- Speed: catch issues locally, iterate faster without waiting for cloud deploys.
- Safety: avoid accidental charges or changes in shared cloud accounts by verifying flows locally first.
- Onboarding: consistent commit templates and clear docs reduce friction for collaborators.

Errors encountered (root cause & symptoms) ⚠️🐛
-----------------------------------------
- Primary blocking error: LocalStack container repeatedly fails to clear its internal data directory with the message:

  "OSError: [Errno 16] Device or resource busy: '/tmp/localstack'"

  Symptoms observed in the container logs:
  - Supervisor attempts to run `rm -rf "/tmp/localstack"` and fails with "Device or resource busy".
  - The LocalStack supervisor exits with non-zero status and the container loops on restart.

Why that matters ❗
-----------------
- LocalStack cannot start cleanly while it cannot remove or reset its persisted data directory. This prevents the local Kinesis API from becoming healthy and blocks the end-to-end demo (create stream → publish records).

Remediation options tried / recommended 🛠️
-------------------------------------
1. Convert host bind to a Docker named volume (done) and re-run the stack — helps avoid accidental host-file locking, but the busy error persisted.
2. Remove the named LocalStack volume (recommended next step) to flush the stuck state. This will delete LocalStack persisted state.
3. Restart the host container runtime (Docker Desktop / Colima) to clear any kernel-level file locks.
4. Run an ephemeral LocalStack container (no persisted volume) to confirm the compose config is otherwise correct.

Commands run (representative) 🧾
-----------------------------
The exact commands used during the investigation (copy/paste):

```bash
# start LocalStack (detached)
docker compose -f docker-compose.localstack.yml up -d

# stream logs (tail + follow)
docker compose -f docker-compose.localstack.yml logs --follow --tail 100

# stop the stack
docker compose -f docker-compose.localstack.yml down

# list docker volumes and find the localstack one
docker volume ls | grep localstack || true

# remove the named localstack volume (replaces persisted ./ .localstack bind)
docker volume rm <localstack_volume_name>

# create a local Kinesis stream (LocalStack endpoint example)
aws --endpoint-url=http://localhost:4566 kinesis create-stream --stream-name fraud-transactions-stream --shard-count 1

# run the demo producer (example env var usage)
KINESIS_ENDPOINT=http://localhost:4566 STREAM_NAME=fraud-transactions-stream python local_producer.py

# Build and deploy SAM (cloud) when ready
sam build
sam deploy --guided
```

Places to pick up from (concrete next steps) 📌
-------------------------------------------
1. Stop LocalStack (if running):
   - `docker compose -f docker-compose.localstack.yml down`
2. Remove the named LocalStack volume (this is destructive to local state):
   - `docker volume ls` → find the localstack volume name → `docker volume rm <name>`
3. Start LocalStack again and verify logs show healthy startup:
   - `docker compose -f docker-compose.localstack.yml up -d`
   - `docker compose -f docker-compose.localstack.yml logs --follow --tail 100`
4. If LocalStack becomes healthy, create the local stream and run the demo producer (see commands above).
5. If the volume removal does not fix it, try restarting Docker Desktop/Colima and repeat the steps above.

Quick checklist for validation ✅
------------------------------
- [ ] LocalStack container runs without supervisor exit loops.
- [ ] `aws --endpoint-url=http://localhost:4566 kinesis list-streams` returns the expected streams.
- [ ] `local_producer.py` successfully PUTs records and reports success.
- [ ] SAM template builds: `sam build` completes without error.

Notes / context for reviewers
----------------------------
- The working demo script is `local_producer.py` at repo root and uses `boto3` with an optional endpoint override. See `docs/local-testing.md` for more details and full copy/paste run commands.
- The infra template is in `src/daredev_fraud/infra/sam/kinesis_ingestor.yaml`. Use `sam deploy --guided` to push to AWS (you'll need an S3 bucket and appropriate IAM privileges).

Contact / owner
---------------
- Owner: Nazere Wright (@daredevtech)
