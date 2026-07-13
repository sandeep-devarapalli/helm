#!/bin/sh
set -eu

mkdir -p /target/skills /target/cron
cp /profile/config.yaml /target/config.yaml
cp /profile/SOUL.md /target/SOUL.md
cp /profile/mcp.json /target/mcp.json

for skill in /profile/skills/*; do
  name=$(basename "$skill")
  rm -rf "/target/skills/$name"
  cp -R "$skill" "/target/skills/$name"
done

cp -R /profile/cron/. /target/cron/
chown -R 10000:10000 /target
