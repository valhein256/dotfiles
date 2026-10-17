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
PLUGIN_JSON="$HOME/.claude/plugins/installed_plugins.json"
PLUGIN_KEY="<TEAM_PLUGIN>@<TEAM_MARKETPLACE>"

VER="$(python3 -c "import json; d=json.load(open('$PLUGIN_JSON')); print(d['plugins']['$PLUGIN_KEY'][0]['version'])" 2>/dev/null || true)"
UP_BASE="$HOME/.claude/plugins/cache/<TEAM_MARKETPLACE>/<TEAM_PLUGIN>/${VER:-}/skills"

for dir in "$STANDBY"/*/; do
  [ -f "$dir/SKILL.md" ] || continue
  name="$(basename "$dir")"
  [ -f "$dir/.scrubbed" ] && continue

  if [ -z "${VER:-}" ] || [ ! -f "$UP_BASE/$name/SKILL.md" ]; then
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
