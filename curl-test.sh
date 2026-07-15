#!/bin/bash
# Tests the /api/timeline_post endpoints with curl:
#   1. POST a timeline post with random content
#   2. GET all posts and verify the new post is there
#   3. DELETE the test post (bonus endpoint) and verify it's gone
# Requires the flask app to be running: flask run
# Uses 127.0.0.1 rather than localhost: on macOS, localhost can resolve to
# IPv6 (::1) where Apple's AirPlay Receiver squats on port 5000.

URL="${URL:-http://127.0.0.1:5000}/api/timeline_post"

RANDOM_ID=$RANDOM
NAME="Test User $RANDOM_ID"
EMAIL="test$RANDOM_ID@example.com"
CONTENT="random test post $RANDOM_ID"

echo "==> POST $URL"
post_response=$(curl -s -X POST "$URL" \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")
echo "$post_response"

post_id=$(echo "$post_response" | sed -n 's/.*"id": *\([0-9]*\).*/\1/p')
if [ -z "$post_id" ]; then
  echo "FAIL: POST did not return a post id"
  exit 1
fi
echo "created test post id=$post_id"

echo
echo "==> GET $URL"
get_response=$(curl -s "$URL")
echo "$get_response"

if echo "$get_response" | grep -q "$CONTENT"; then
  echo "PASS: test post found in GET response"
else
  echo "FAIL: test post not found in GET response"
  exit 1
fi

echo
echo "==> DELETE $URL/$post_id"
curl -s -X DELETE "$URL/$post_id"
echo

if curl -s "$URL" | grep -q "$CONTENT"; then
  echo "FAIL: test post still present after DELETE"
  exit 1
else
  echo "PASS: test post deleted"
fi

echo
echo "All tests passed!"
