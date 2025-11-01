# 2025-10-18 — DARIA Daily Log 🧠🔗

**Author:** Nazere Wright (@daredevtech)  
**Project:** fraud-signal-detector-augmented-producer  
**Branch:** feat/day3-streaming

---

## TL;DR 🚀

Today I focused on wiring infra & CI, and improving dev ergonomics for faster iteration:

- ✨ Added a DDT commit template and made VS Code open the editor for commits.
- ⚙️ Documented CI / Deployment and added a SAM CloudFormation template for the Kinesis ingestor.
- 🧹 Tidied `.gitignore` and `README.md`, and prepared a draft commit message for the current changes.

This is a concise, curious log — written to be copy-paste friendly for Notion and shareable with the team.

---

## Findings & quick notes 🔎

- Fn::Sub / `!Sub` in CloudFormation is great for building names with `${Env}` or `${AWS::Region}`. It reduces boilerplate but sometimes hides explicit `GetAtt` usage — use the mapping form when you need clarity.
- `ubuntu-latest` is chosen in Actions because the runner pool is large, fast, and contains preinstalled tooling (aws-cli, Docker, Python). Use `macos-latest` or `windows-latest` only when necessary (Xcode, Windows-specific builds).
- For Kinesis producers, prefer `PutRecords` batching: up to 500 records / 5 MB per call. Partition keys matter for distributing load across shards.
- Local testing: LocalStack + Docker is the fastest way to emulate Kinesis locally and avoid real AWS calls during development.

---

## Git learnings & workflow tweaks 🧰

- ✅ Commit template: `.gitmessage.txt` added and set as the local commit template (`git config --local commit.template .gitmessage.txt`). VS Code is configured to open the editor for commit messages so the template appears when committing.
  - Benefit: consistent header format `DDT: {type/branch-name} Heading` and a short summary block.
- ⚠️ `.gitignore` only affects untracked files — run `git rm --cached` to stop tracking files already in the repo.
- Reminder: be careful with `git stash pop` — it can reintroduce unstaged changes; double-check `git status` after popping.

---

## Code & repo changes (what I changed, why) 💾

- `.gitmessage.txt` — new: DDT commit template (keeps commits clean and searchable).
- `.vscode/settings.json` — new: `git.openEditorForCommitMessage = true` so the template appears in the editor when committing.
- `.git-commit-draft.txt` — new: draft commit message for the current working tree (handy for pasting into VS Code).
- `README.md` — updated: added CI / Deployment section documenting the workflow and the commit-template.
- `src/daredev_fraud/infra/sam/kinesis_infra.yaml` — SAM template for the Kinesis stream and Lambda roles (added for infra-as-code).
- `src/daredev_fraud/.github/workflows/github-actions-demo.yml` — added: workflow that validates and deploys the SAM template using OIDC.
- `.gitignore` — updated: added `path/` and extra ignore patterns to prevent local artifacts from being tracked.

> Note: There’s a workflow under `src/daredev_fraud/.github/...` — GitHub only runs workflows in the repository root `.github/workflows/`. Consider moving it if you want it to run.

---

## Questions I had / action items for you ❓📝

1. Why was the workflow added under `src/daredev_fraud/.github/workflows/` instead of top-level `.github/workflows/`? If it was accidental, shall I move it and open a PR?

2. `ShardCount: 1` is currently used — do you expect higher throughput during tests or demos? If yes, we should parameterize and document the cost implications.

3. Naming pattern for `Env`: do we standardize on `dev/stage/prod`? I used `${Env}` in `!Sub` for RoleName and ARNs — confirm desired values.

4. Local testing approach: prefer LocalStack (integration) + `moto`/Stubber for unit tests? I can add both and wire a simple test harness.

Reply with short answers and I’ll tighten the infra + docs accordingly.

---

## Optimizations & follow-ups ⚡️

- Implement batched `PutRecords` with partition-key hashing and a bounded thread/async pool for throughput.
- Add retries with exponential backoff for partial `PutRecords` failures and log partial failure metrics.
- Add a `docker-compose.localstack.yml` and a small integration test that starts LocalStack and runs a publish -> consume flow.
- Add a `commit-msg` hook sample that validates the DDT header (prevents missing DDT headers).
- Consolidate workflows into `.github/workflows/` and parametrize region/stack name via workflow inputs or secrets.

---

## Next steps (prioritized) ✅

1. Move workflow to `.github/workflows/` if you want it to run at repo-level (quick).
2. Add `producer.py` batching example + LocalStack compose for local testing (medium).
3. Add `commit-msg` hook and documentation showing how to enable locally (small).
4. Add tests: LocalStack integration + `moto`/Stubber unit tests (medium).

---

## Reflection — in the spirit of web3 ✨🪙

I prefer building small, resilient developer scaffolding: clear commit templates, reproducible local infra, and automated CI. These tiny conveniences especially scale in distributed teams — they free cognitive bandwidth to focus on the hard ML/streaming problems.

I’m not pretending to know everything — I’m here to learn, iterate, and ship small experiments that teach me faster.

If you want, I can now:

- copy this log into Notion via the API (you’ll need to supply a token and a target page/database id),
- add the `commit-msg` hook and document enabling it,
- move the workflow file and open a PR.
