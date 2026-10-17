---
name: weekly-report
description: Generate the user's personal weekly work report — what was done in the past week, in the user's own weekly-report voice (the reporting channel profile), matching the shape of their entries in the team weekly-report document. Derives the week's repos and task narrative from the Claude Code session history (~/.claude/projects/), corroborates with git commits and Jira tickets, then drafts via the `draft` skill (channel reporting), so the review gate and save-back apply. Triggers on "weekly report", "summarize my week", "generate my weekly report", "report last week's progress".
---

# Weekly Report

Personal workflow: turn the past week's work into a report in the user's
own weekly-report voice — the same shape as their real weekly entries —
drafted through the `draft` skill's reporting channel.

## The report shape

Single source: the `reporting` channel profile (`~/.claude/profiles/
reporting.md`) — project-area grouping, ticket-led items, trailing
status vocabulary, verification sentences, numbers as pairs, closing
forward line. Do not restate its traits here.

## Workflow

1. **Establish the window**: default = Monday of the current week to
   today; the user may name any range in their own words (e.g. the
   previous Mon–Sun).

2. **Gather the facts** — raw material only, never invent work:
   - **Agent sessions (the entry point)**: list
     `~/.claude/projects/*/*.jsonl` modified in the window
     (`find ~/.claude/projects -name '*.jsonl' -newermt <start>`).
     Group by project directory — the directory name is the working
     repo (path slug; convert `-` back to `/` under `$HOME`). Skip the
     `subagents` directory (harness-internal, no user messages). For each
     session read only the FIRST user message (the task) and its
     date. This yields the week's repo list AND each repo's task
     narrative — including debugging and investigation that never
     landed in git.
   - **git (the evidence)**: for each repo discovered above, run
     `git log --since=<start> --until=<end> --author=<user> --oneline`
     — what actually landed (commits, PR anchors). Do not scan for
     repos beyond the session-derived list.
   - **Jira (the anchors)**: via the Atlassian MCP, the tickets the
     user updated or resolved in the window. Resolve the cloudId via
     `getAccessibleAtlassianResources` first — the hostname alone
     returns 403.
   - **Ask once what none of them can see**: meetings, offline
     reviews, docs — one closing question before drafting.

3. **Group by project area**: the session-derived repo (or ticket
   project) is the area label. Ticket-led items only; ad-hoc help and
   reviews go under a Misc group, if any.

4. **Draft via the `draft` skill**: invoke `draft` with channel
   `reporting` and the grouped facts as rough input. The full pipeline
   applies — floor, reporting voice, AI-simulated take, the English +
   Chinese review gate, save-back of the user's edits.

5. The user-confirmed text is final: ready to paste into the weekly
   report document as-is.

## Notes

- If the Atlassian MCP is unavailable (no Jira access), fall back to
  session + git facts and say so — never skip the Jira section
  silently.
- If a week has no session, git, or Jira activity at all, say so and
  ask what to include instead of padding the report.
- The facts stay machine-local (the user's sessions, git, and Jira);
  this skill's text stays portable — it names no repo, cluster, or
  ticket.
