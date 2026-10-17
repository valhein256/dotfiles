#!/usr/bin/env bash
# Sync claude/skills-standby mirrors against the installed team plugin.
#
# Per mirror:
#   in sync with the installed plugin        -> silent (nothing to do)
#   upstream moved, mirror unedited (== git HEAD) -> fast-forward, print one line
#   upstream moved, mirror locally edited    -> alert, never touch (promotion signal)
#   .scrubbed marker present                 -> skip (scrubbed mirrors are
#                                                report-only by design)
#   plugin missing                           -> point at skills-activate-standby
#
# Designed to run from the SessionStart hook every session: prints NOTHING
# unless it did something or something needs attention.
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
STANDBY="$ROOT/claude/skills-standby"

# Discover the team plugin dynamically: the INSTALLED plugin whose cache
# provides a standby skill's directory. No plugin or marketplace names
# hardcoded — works regardless of which team plugin provides the skills.
UP_BASE="$(python3 -c "
import json, os, sys
probe = 'team-db-standards'
try:
    d = json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json')))
except OSError:
    sys.exit(0)
for entries in d.get('plugins', {}).values():
    for e in entries:
        base = e.get('installPath', '')
        if os.path.isdir(os.path.join(base, 'skills', probe)):
            print(os.path.join(base, 'skills'))
            sys.exit(0)
" 2>/dev/null || true)"

VER=""
[ -n "${UP_BASE:-}" ] && VER="$(basename "${UP_BASE%/skills}")"

for dir in "$STANDBY"/*/; do
  [ -f "$dir/SKILL.md" ] || continue
  name="$(basename "$dir")"
  [ -f "$dir/.scrubbed" ] && continue

  if [ -z "${UP_BASE:-}" ] || [ ! -f "$UP_BASE/$name/SKILL.md" ]; then
    echo "standby: team plugin not found for '$name' — run: make skills-activate-standby"
    continue
  fi

  if cmp -s "$UP_BASE/$name/SKILL.md" "$dir/SKILL.md"; then
    continue
  fi

  rel="${dir#"$ROOT"/}SKILL.md"
  if git -C "$ROOT" diff --quiet HEAD -- "$rel" 2>/dev/null; then
    # mirror matches HEAD -> zero local divergence -> mechanical fast-forward
    cp "$UP_BASE/$name/SKILL.md" "$dir/SKILL.md"
    echo "standby: fast-forwarded '$name' to plugin $VER — commit the update"
  else
    echo "standby: '$name' has local edits and the plugin changed — promotion signal, resolve manually"
  fi
done

exit 0
