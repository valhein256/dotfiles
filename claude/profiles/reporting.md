# Channel Profile: reporting (v1)

- Scope: weekly work reports and progress updates — reporting upward or
  summarizing a body of work.
- Sample basis: ~40 weekly reports by the author (2026, Jan–Oct), genre
  cross-checked against three teammates' reports (39 + 33 + 41 weekly
  entries) to separate team convention from personal voice.
- Sentence budget: no fixed cap — structure-appropriate (see traits).

## Team conventions (every report in this genre)

1. Top-level grouping by project-area label, ticket-led items under it,
   a catch-all Misc section closes.
2. Every substantive item leads with its ticket key (as a link); PRs as
   "PR #NNN"; only narrative glue goes un-ticketed.
3. Verb-led, past tense for done work; status vocabulary trailing the
   item: Done / Ongoing / Todo / Pending / Blocked.
4. Blockers name the owning system or person and carry a ticket
   ("Blocked by {system}: {TICKET}", "Pending {owner}'s completion").
5. Every entry closes with a forward line — "Next:", "Follow-up:", or
   "Once done, ..." — a pending tail, never a trailing list.

## Personal voice (evidence-derived)

6. Verification sentence when declaring done: "verified end-to-end on
   the live {env} pod", "all passed, no issues", "No regressions vs
   the {date} recorded results".
7. Numbers come as fractions, pairs, arrows, or ranges — never one
   bare figure: "95/95 pass", "92% instruction / 90% branch",
   "v0.1 -> v1.2", "1.6x-3.6x per-pod" — each answers "compared to
   what".
8. Scoped-change qualifiers in parentheses: "(config-only change)",
   "(test-only change, no product behavior change)".
9. Problem->fix narration: "The X used to require manually filling Y.
   They are now derived from Z." — "now" as the state-change marker.
10. "Root Cause:" labeled line, causal chain with backticked systems.
11. Semicolon joins two related claims in one line.
12. Negative-elimination closers: "no remaining issues", "zero impact
    on our system", "Completely got rid of X".

## Do / Don't

| Do | Don't |
|---|---|
| "Cleared 13 open defect tickets (5 PRs merged + 1 obsolete closed)." | "Made good progress on defect cleanup." |
| "Gates are now bound to commit SHAs, so a pass means that commit was really checked." | "We improved the CI gates significantly." |
| "verified end-to-end on the live {env} pod — all passed, no issues" | "testing went well overall" |
| "(test-only change, no product behavior change)" | unscoped change descriptions |
| Ends with "Next: {TICKET} — {action}" | Ends with a bare trailing list |

## Verified samples

The ~40 weekly reports that ground these traits live in the team's
weekly-report document, not here (too large, team-specific). This
section receives scrubbed samples via the `draft` skill's save-back:
user-edited final versions only; sentence structures and word habits
kept; company identifiers replaced with fictional substitutes or
removed; date and edit delta recorded with each.

- (none yet — the first edited report starts this file)
