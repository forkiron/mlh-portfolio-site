#!/bin/bash
# Redeploy the portfolio site on the VPS with Docker Compose.
# Flow: sync the repo from GitHub, spin containers down first (prevents
# out-of-memory on the small droplet while building), then rebuild + start.

set -e

cd /root/mlh-portfolio-site

git fetch && git reset origin/main --hard

docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml up -d --build

# Wait for Flask to come up (the mysql container needs a moment to initialize)
for i in $(seq 1 30); do
    if curl -sf http://localhost:5000/ >/dev/null; then
        echo "Website redeployed successfully."
        exit 0
    fi
    sleep 2
done

echo "Site did not respond after redeploy:" >&2
docker compose -f docker-compose.prod.yml logs --tail 30 >&2
exit 1
