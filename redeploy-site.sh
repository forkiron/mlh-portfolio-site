#!/bin/bash

set -e

cd /root/mlh-portfolio-site

BRANCH=$(git branch --show-current)
git pull origin "$BRANCH"

source python3-virtualenv/bin/activate
pip install -r requirements.txt

tmux kill-session -t portfolio 2>/dev/null || true

tmux new-session -d -s portfolio "bash -lc 'cd /root/mlh-portfolio-site && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0'"

echo "Website redeployed successfully."
