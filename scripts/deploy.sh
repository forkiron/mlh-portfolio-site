#!/usr/bin/env bash
# Deploy this portfolio to the DigitalOcean VPS that serves the DuckDNS site.
#
# Flow: commit + push the CURRENT branch -> SSH into the VPS -> sync that branch
# -> restart Flask inside a detached tmux session. Run from anywhere:
#   scripts/deploy.sh ["optional commit message"]
#
# Config + secrets live in .deploy.env (gitignored). See scripts/deploy.example.env.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ENV_FILE="$ROOT/.deploy.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: $ENV_FILE not found." >&2
  echo "       cp scripts/deploy.example.env .deploy.env  then edit it." >&2
  exit 1
fi
set -a; source "$ENV_FILE"; set +a

: "${VPS_HOST:?set VPS_HOST in .deploy.env (e.g. root@147.182.144.24)}"
REMOTE_DIR="${REMOTE_DIR:-~/mlh-portfolio-site}"
TMUX_SESSION="${TMUX_SESSION:-portfolio}"
APP_PORT="${APP_PORT:-5000}"
DUCKDNS_URL="${DUCKDNS_URL:-}"

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
COMMIT_MSG="${1:-chore: redeploy portfolio}"

echo "==> Deploying branch '$BRANCH' to $VPS_HOST"

# 1) commit local changes (if any)
if [[ -n "$(git status --porcelain)" ]]; then
  echo "==> Committing local changes"
  git add -A
  git commit -m "$COMMIT_MSG"
else
  echo "==> Working tree clean, nothing to commit"
fi

# 2) push current branch
echo "==> Pushing to origin/$BRANCH"
git push -u origin "$BRANCH"

# 3) remote: sync the branch + restart Flask in tmux
echo "==> Updating server + restarting Flask"
SSH_OPTS=(-o StrictHostKeyChecking=accept-new -o ConnectTimeout=15)

run_remote() {
  if [[ -n "${VPS_PASS:-}" ]] && command -v sshpass >/dev/null 2>&1; then
    sshpass -p "$VPS_PASS" ssh "${SSH_OPTS[@]}" "$VPS_HOST" \
      bash -s -- "$BRANCH" "$REMOTE_DIR" "$TMUX_SESSION" "$APP_PORT"
  else
    ssh "${SSH_OPTS[@]}" "$VPS_HOST" \
      bash -s -- "$BRANCH" "$REMOTE_DIR" "$TMUX_SESSION" "$APP_PORT"
  fi
}

run_remote <<'REMOTE'
set -e
BR="$1"; RD="$2"; SESS="$3"; PORT="$4"
# Resolve RD to an absolute path on THIS (remote) machine.
case "$RD" in
  "~")    RD="$HOME" ;;
  "~/"*)  RD="$HOME/${RD#~/}" ;;
  /*)     : ;;
  *)      RD="$HOME/$RD" ;;
esac
cd "$RD"
echo "   - fetching origin"
git fetch origin
git switch "$BR" 2>/dev/null || git switch -c "$BR" --track "origin/$BR"
echo "   - hard-reset to origin/$BR"
git reset --hard "origin/$BR"
source python3-virtualenv/bin/activate
echo "   - installing requirements"
pip install -q -r requirements.txt || true
echo "   - restarting tmux session '$SESS'"
tmux kill-session -t "$SESS" 2>/dev/null || true
tmux new-session -d -s "$SESS" -c "$RD" \
  "source python3-virtualenv/bin/activate && exec flask run --host=0.0.0.0 --port $PORT"
sleep 1
if tmux has-session -t "$SESS" 2>/dev/null; then
  echo "   - flask is running in tmux '$SESS'"
else
  echo "   ! tmux session failed to start" >&2
  exit 1
fi
REMOTE

echo ""
echo "==> Done. Deployed branch '$BRANCH'."
if [[ -n "$DUCKDNS_URL" ]]; then
  echo "    Live at: $DUCKDNS_URL"
else
  echo "    Live at: http://${VPS_HOST#*@}:$APP_PORT"
fi
