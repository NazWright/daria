
# 🧱 Contributing to DareDevTech — Fraud Detection Pipeline

Welcome to **DareDevTech Ventures** — where myth meets machine.
This repo powers our **Hybrid AWS + Solana Fraud Detection Pipeline**, combining machine learning, cloud-scale streaming, and verifiable trust on-chain.

We keep our codebase clean, auditable, and boldly branded — every commit carries our signature: **DDT**.
If you’re contributing (even solo), please follow these conventions for clarity and continuity.

---

## ⚡️ Branch Naming Convention

Use short, descriptive branch names — one feature or fix per branch.

| Type           | Format                           | Example                      | Purpose                 |
| -------------- | -------------------------------- | ---------------------------- | ----------------------- |
| **Feature**    | feature/<short-descriptive-name> | feature/kinesis-streaming    | New feature or module   |
| **Fix**        | fix/<bug-or-issue>               | fix/lambda-timeout           | Patch or bug fix        |
| **Refactor**   | refactor/<component>             | refactor/onchain-proof-logic | Code structure cleanup  |
| **Docs**       | docs/<topic>                     | docs/architecture-overview   | Documentation updates   |
| **Experiment** | experiment/<idea>                | experiment/zk-proof-poc      | Prototyping new concept |

### 🧭 Rules

* Use **kebab-case** (lowercase with hyphens).
* Each branch corresponds to a **GitHub Issue**.
* Keep names concise (3–5 words).
* Start branches from `main` unless otherwise stated.
* Prefix your branch properly (`feature/`, `fix/`, etc.).

---

## 💬 Commit Message Convention (DDT Signature)

All commits must start with `DDT` — the **DareDevTech signature**.
This builds brand consistency and searchable history across repos.

### Format

```
DDT <type>(<scope>): <short description>

[optional longer explanation]
[optional issue reference: #<issue-number>]
```

### Examples

```
DDT feat(streaming): add kinesis producer for fraud data (#2)
DDT fix(lambda): resolve consumer timeout issue
DDT refactor(onchain): simplify submit_proof instruction
DDT docs(architecture): update AWS → Solana diagram
```

**Commit Types**

| Type     | Purpose                              |
| -------- | ------------------------------------ |
| feat     | New feature or capability            |
| fix      | Bug fix                              |
| refactor | Code cleanup without behavior change |
| docs     | Documentation updates                |
| chore    | Repo maintenance tasks               |
| test     | New or updated tests                 |

---

## 🧱 Pull Request Guidelines

Before opening a PR:

1. **Sync main**

   ```
   git checkout main
   git pull origin main
   ```
2. **Branch from main**

   ```
   git checkout -b feature/<name>
   ```
3. **Commit using DDT format**

   ```
   git add .
   git commit -m "DDT feat(streaming): implement producer → consumer flow (#2)"
   ```
4. **Push and open PR**

   ```
   git push -u origin feature/<name>
   ```
5. **PR Title Example:**

   ```
   DDT Feature: Add Kinesis Streaming Pipeline (#2)
   ```

### PR Description Template

```
### What Changed
- Implemented streaming from AWS Kinesis to Lambda to S3.

### Why
Enables real-time fraud data ingestion for hybrid AWS + Solana system.

### Linked Issue
Closes #2
```

---

## 🧠 Workflow Recap

| Stage             | Branch                             | Example Commit                                             | Status |
| ----------------- | ---------------------------------- | ---------------------------------------------------------- | ------ |
| EDA               | feature/eda-initial-analysis       | DDT feat(eda): complete exploratory data review            | ✅      |
| Data Augmentation | feature/data-augmentation          | DDT feat(augmentation): balance dataset with SMOTE + Faker | ✅      |
| Streaming         | feature/kinesis-streaming          | DDT feat(streaming): connect Kinesis → Lambda → S3         | 🚧     |
| Proof Logic       | feature/proof-logic-design         | DDT feat(proof): define on-chain fraud schema              | ⏳      |
| Smart Contract    | feature/solana-fraudproof-registry | DDT feat(onchain): implement FraudProofRegistry            | ⏳      |
| Integration       | feature/aws-to-solana-integration  | DDT feat(integration): connect Lambda with Solana SDK      | ⏳      |
| Dashboard         | feature/fraud-dashboard-ui         | DDT feat(ui): create fraud proof dashboard                 | ⏳      |

---

## 🏷️ Version Tags

Use DareDevTech-styled tags for releases:

```
git tag -a DDT-v0.1.0 -m "EDA + Data Augmentation complete"
git push origin DDT-v0.1.0
```

---

## ⚙️ Optional Git Alias (Shortcut)

Add a global Git alias to simplify commits:

```
git config --global alias.ddt '!f() { git commit -m "DDT $1"; }; f'
```

Usage:

```
git add .
git ddt "feat(augmentation): finalize SMOTE + Faker pipeline"
```

---

## 🧩 Code Style

* **Python:** PEP8 + Black formatting
* **JavaScript/React:** Prettier + ESLint
* **Rust (Solana):** Cargo fmt + Clippy
* Always include docstrings/comments for all key functions

---

## 🌟 DareDevTech Ethos

> “We don’t just write code — we write proof.”
> Every function, commit, and contract in this repo should reinforce the **trust layer** we’re building for modern finance.

---

**Built by:**
🧠 **Naz Wright — DareDevTech Ventures**
📍 *Hybrid Cloud + Web3 Engineering*
