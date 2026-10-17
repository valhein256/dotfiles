# Development Standards (personal)

> Team workflow rules (brainstorm gate, TDD, branch format, Jira triggers,
> worktree enforcement) arrive automatically via the team plugin's session
> hook. This file holds personal sections and overrides only.

## Communication Standards

ALWAYS draft any external-facing communication (ticket comments, PR review
comments, status updates, emails, chat messages, docs) applying:
- **Ask about the audience if unclear** — framing/detail/jargon depend on who reads it.
- **Concrete information, no fluff** — numbers, facts, specifics; drop filler.
- **Lead with the point** — conclusion/decision first, supporting detail after.

### Drafting harness (floor + voice + take)

Apply on top of the three rules above, for every ticket/comment, PR review
comment, status update, email, chat message, report, and docs draft:
- **Floor (manager rules):** verdict first + one reason; sentence budget per
  the channel profile (default 5); direct language, no filler ("it's worth
  noting", "it is X, not Y"); flag anything asserted that the given material
  cannot verify (mark `[unverified]` inline); end with the specific question
  that needs answering.
- **Voice:** follow `~/.claude/profiles/` — `core.md` (floor + cross-channel
  traits) plus the channel profile for where the message goes (`message` /
  `reporting` / `tickets-comments-pr` / `docs`).
- **Take:** the draft's final line is an AI-simulated take in the user's
  voice — grounded in the draft's evidence; anything beyond that evidence is
  marked `[unverified]` inline; a specific question goes on the line just
  before it.
- PR descriptions keep the team template (`## Jira` / `## Summary` /
  `## Test Results`) but the Summary section still leads with the call.

## Language Standards — English Only for All Deliverables

The team is English-only. EVERY artifact I produce, commit, upload, or hand off
MUST be written entirely in English. This is a hard rule, no exceptions.

**Always English (zero non-English characters):**
- PR titles, descriptions, and review comments
- Git commit messages and branch descriptions
- Jira ticket summaries, descriptions, and comments
- Design docs, runbooks, READMEs, and any file under `docs/`
- Code: identifiers, comments, log messages, string literals, error messages
- Test names, test descriptions, assertion messages
- Chat messages, emails, status updates
- Confluence pages and comments

**Chinese (or any non-English language) is permitted ONLY when:**
- The user explicitly asks for a translation or a Chinese-language artifact in that turn.
- A file already exists in Chinese (e.g. `*_zh.md`) and I am editing it — match the file's existing language.

**Self-check before delivering:** scan the final output for any non-ASCII / CJK
characters. If any appear and the user did not explicitly request that language,
rewrite them in English before sending. When unsure, default to English.

**Note:** The user may speak to me in Chinese — that does NOT change the output
language. Respond conversationally in whatever language is clearest to the user,
but every deliverable artifact stays English.

## Model Selection

Default: **Sonnet 4.6** (quality/cost optimum for coding, tool calls, file ops, debugging with clear hypotheses).

Switch to **Opus 4.7** (`/model claude-opus-4-7`) only for tasks that need deep reasoning:
- Writing or reviewing L2/L3 design docs (`docs/design/`)
- `team-brainstorm` phase — open-ended trade-off analysis
- Multi-file architectural decisions, novel system design
- Stuck debugging where root cause is unclear after 2–3 Sonnet turns
- User explicitly says "think hard", "use opus", or "deep dive"

Switch back to Sonnet (`/model claude-sonnet-4-6`) immediately after the hard reasoning step — long Opus sessions snowball cache_write cost.

When unsure: start Sonnet. If 3 turns without progress, suggest upgrading to Opus.
