#!/bin/sh
set -eu

mkdir -p /home/vibe/.vibe-trading /home/vibe/runs
chown -R vibe:vibe /home/vibe/.vibe-trading /home/vibe/runs

exec setpriv --reuid=10001 --regid=10001 --init-groups "$@"
