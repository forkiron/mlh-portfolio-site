---
name: upd-port
description: Deploy this MLH portfolio to the DigitalOcean VPS that serves the DuckDNS site. Commits + pushes the current branch, SSHes into the droplet, syncs the branch, and restarts Flask in tmux. Use when the user says "/upd-port", "update my portfolio", "deploy the site", "push to the vps/duckdns", or "redeploy". Scoped to the mlh-portfolio-site repo only.
---

# upd-port — deploy the portfolio to the VPS

One command to ship local changes to the live DuckDNS site. The heavy lifting is in
`scripts/deploy.sh`; this skill just runs it and reports the result.

## What it does
1. Commits any uncommitted changes on the **current branch**.
2. Pushes that branch to `origin` (keeps `main` clean for friends to fork).
3. SSHes into the VPS, `git reset --hard origin/<branch>`, reinstalls deps.
4. Restarts Flask in a detached `tmux` session (`flask run --host=0.0.0.0`).

## Config
All settings live in `.deploy.env` at the repo root (gitignored — never committed,
since this repo gets forked). Template: `scripts/deploy.example.env`.
Keys: `VPS_HOST`, `REMOTE_DIR`, `TMUX_SESSION`, `APP_PORT`, `DUCKDNS_URL`, `VPS_PASS`.

## How to run it
From the repo root:

```bash
bash scripts/deploy.sh "short commit message describing the change"
```

When invoking this skill, craft a concise commit message from the actual pending
diff instead of the generic default. If the tree is clean it just redeploys.

## Auth (important — do the one-time setup once)
The droplet uses **SSH key auth**. The deploy uses plain `ssh`, so the key must be
usable without an interactive prompt. Run this **once** to cache the key passphrase
in the macOS keychain (enter the passphrase when asked):

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

After that, `/upd-port` runs passwordless every time.

Alternative (password auth): install `sshpass`
(`brew install hudochenkov/sshpass/sshpass`) and set `VPS_PASS` in `.deploy.env`;
the script will use it automatically.

## Notes / guardrails
- Deploys the branch you're currently on. Be on your personal branch, not `main`.
- `git reset --hard origin/<branch>` on the server discards any local edits there
  (the box only serves; it shouldn't have any).
- This is an outward-facing action (pushes to GitHub + restarts the live server).
  Confirm with the user before running if there's any doubt about the branch.
- If `ssh` hangs, the key passphrase isn't cached — do the `ssh-add` step above.
