#!/bin/bash
# Redeploy the portfolio site on the VPS with Docker Compose.
# Flow: sync the repo from GitHub, spin containers down first (prevents
# out-of-memory on the small droplet while building), then rebuild + start.

set -e

cd /root/mlh-portfolio-site

git fetch && git reset origin/main --hard

docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml up -d --build

# Wait for the site to come up through nginx (mysql init + first-run cert
# issuance can take a couple of minutes; -k because the cert is for the
# duckdns domain, not localhost)
for i in $(seq 1 60); do
    if curl -skf https://localhost/ >/dev/null; then
        echo "Website redeployed successfully."
        exit 0
    fi
    sleep 5
done

echo "Site did not respond after redeploy:" >&2
docker compose -f docker-compose.prod.yml logs --tail 30 >&2
exit 1
