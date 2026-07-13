#!/bin/bash
# Redeploy the portfolio site on the VPS.
# Flask runs as the systemd service `myportfolio` (see /etc/systemd/system/myportfolio.service),
# so a redeploy is: sync the repo, install deps, restart the service.

set -e

cd /root/mlh-portfolio-site

BRANCH=$(git branch --show-current)
git fetch origin
git reset "origin/$BRANCH" --hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt

systemctl daemon-reload
systemctl restart myportfolio

sleep 2
if systemctl is-active --quiet myportfolio; then
    echo "Website redeployed successfully."
else
    echo "Service failed to start:" >&2
    journalctl -u myportfolio -n 20 --no-pager >&2
    exit 1
fi
