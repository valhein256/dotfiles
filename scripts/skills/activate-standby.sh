#!/usr/bin/env bash
# Flip claude/skills-standby mirrors into live personal skills
# (~/.claude/skills/<name> -> repo mirror). For use when the team plugin
# is gone: a new personal machine, or after leaving the team.
#
# Usage: activate-standby.sh [--all]
#   default: skip .scrubbed mirrors (company identifiers were replaced with
#            placeholders — review manually before activating)
#   --all:   activate everything, including .scrubbed mirrors
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
STANDBY="$ROOT/claude/skills-standby"
SKILLS_DIR="$HOME/.claude/skills"

for dir in "$STANDBY"/*/; do
  [ -f "$dir/SKILL.md" ] || continue
  name="$(basename "$dir")"
  if [ -f "$dir/.scrubbed" ] && [ "${1:-}" != "--all" ]; then
    echo "skip: $name (scrubbed mirror — review, then rerun with --all)"
    continue
  fi
  rm -rf "$SKILLS_DIR/$name"
  ln -s "$dir" "$SKILLS_DIR/$name"
  echo "activated: $name"
done

echo "standby skills now live under $SKILLS_DIR"
