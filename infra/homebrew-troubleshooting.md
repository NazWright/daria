## Homebrew download failure: m4 bottle (diagnosis and recovery)

This note explains the `m4` download failure you saw when running `brew install pyenv`, why it happens, and the exact Homebrew commands we ran (or suggested) along with why each one helps resolve the problem.

Context / use case
- You're using the SAM CLI to build Lambda functions targeting `python3.12`.
- SAM's Python builder needs a matching Python interpreter on your PATH (or it will build inside a Docker container).
- We attempted to install `pyenv` via Homebrew so you could install Python 3.12 locally. That flow failed early because Homebrew couldn't download the `m4` bottle (a build dependency).

Observed error (example)

```
Error: pyenv: Failed to download resource "m4"
Download failed: https://ghcr.io/v2/homebrew/core/m4/blobs/sha256:...
```

Why this can happen (root causes)
- Transient network or GitHub Container Registry (GHCR) outage. The Homebrew bottles are hosted on GHCR and occasionally a blob download will fail.
- GHCR / GitHub rate-limiting on anonymous pulls. If many anonymous pulls occur from the same IP, GHCR may throttle or reject requests.
- Local Homebrew cache corruption or partial download. A stale or partial file in `$(brew --cache)` can cause repeated failures.
- Corporate VPN / proxy / firewall blocking direct downloads from GHCR.

Commands we run and why they help

- `brew update`
  - What it does: refreshes Homebrew itself (formulae and taps). This ensures Homebrew uses the latest metadata and updated download URLs.
  - Why it helps: a stale tap can point to outdated bottle digests or locations. Refreshing metadata is the first troubleshooting step.

- `brew cleanup`
  - What it does: removes old versions of installed formulae and clears stale cache items.
  - Why it helps: frees disk space and may remove corrupted cached downloads that could block new installs.

- `brew doctor`
  - What it does: runs Homebrew's built-in diagnostics and surface local environment issues.
  - Why it helps: it prints common problems (out-of-date Xcode, PATH issues, permission problems) that can indirectly block installs.

- `brew install m4` (try to install the failing resource directly)
  - What it does: attempts to download and install `m4` alone.
  - Why it helps: isolates the failing resource; the error message is often more explicit when installing the single package.

- `rm -rf "$(brew --cache)/m4*"` then retry `brew install m4`
  - What it does: removes any partially downloaded or corrupted cached files for `m4` and forces a fresh download.
  - Why it helps: clears local cache corruption which is a frequent cause of repeated download failures.

- `brew install python@3.12`
  - What it does: installs the Homebrew `python@3.12` formula which provides a Python 3.12 binary on PATH.
  - Why it helps: if `pyenv` installation is blocked by bottle issues, installing Python directly can be faster and is sufficient for SAM builds (SAM only needs a matching interpreter on PATH), bypassing pyenv entirely.

- `sam build --use-container --template-file <template>`
  - What it does: runs the SAM build inside Docker using images that match your target runtime.
  - Why it helps: avoids local Python requirements entirely — useful when installing Python locally is blocked or you want exact runtime parity.

How to pick the right recovery path
- If the error looks transient (most are), try `brew update` → `brew cleanup` → `brew install m4` once or twice.
- If you're behind a corporate proxy/VPN, test from a home network or confirm the proxy allows GHCR pulls.
- For a quick unblock when you only need Python 3.12 for SAM, prefer `brew install python@3.12` over troubleshooting pyenv bottles.
- If you want deterministic builds and don't want to touch local Python, use `sam build --use-container` (requires Docker running).

Exact recovery steps I recommend (zsh-ready)

1) Quick retry + cleanup

```zsh
brew update
brew cleanup
brew doctor   # read any reported issues and fix if necessary
brew install m4
# if install fails with the same blob error, remove cache and retry
rm -rf "$(brew --cache)/m4*"
brew install m4
```

2) If still failing, install Python 3.12 directly (fast unblock)

```zsh
brew install python@3.12
echo 'export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
python3.12 --version
sam build --template-file '/Users/xaymunyun/Documents/projects 2025/daria/infra/sam/kinesis_infra.yaml'
```

3) Or: use Docker for SAM build (no local Python required)

```zsh
# Start Docker Desktop first, then
sam build --use-container --template-file '/Users/xaymunyun/Documents/projects 2025/daria/infra/sam/kinesis_infra.yaml'
```

Other useful diagnostics
- Check `brew config` and `brew doctor` output for system-level problems.
- Inspect Homebrew cache logs: `ls -la "$(brew --cache)"` and `tail -n 200 $(brew --cache)/logs/*` for clues.
- If GHCR/GitHub rate-limiting is suspected, wait a short while or authenticate (for Docker/GHCR pulls; for Homebrew formula downloads you can set `HOMEBREW_GITHUB_API_TOKEN` to a personal access token to increase API rate limits for some operations).

Notes about security / tokens
- Avoid embedding tokens into checked-in files. If you need a `HOMEBREW_GITHUB_API_TOKEN`, set it in your shell session when running brew (export only in your shell or use a local secret manager like aws-vault).

Summary
- The `m4` failure is usually a transient download or cache issue rather than a logic error in your repo. The `brew update` / `brew cleanup` / cache removal sequence is a safe first step. If you need a fast workaround, installing `python@3.12` via Homebrew or using `sam build --use-container` are reliable alternatives.

If you'd like, I can add a short `infra/README.md` entry linking to this note and include the exact commands we ran in the session for traceability. Want me to commit that as well?
