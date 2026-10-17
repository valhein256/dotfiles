---
name: draft
description: Draft any external-facing message (ticket comment, PR review comment, status update, email, chat message, report) in the user's own voice — verdict first, max 5 sentences, evidence in the same sentence, ending with an AI-simulated take marked [unverified] beyond the evidence. Every draft goes through an English + Chinese review pass with the user before it is final, and the user's edits are saved back to the channel profile. Use when the user says "draft", asks for a message/comment/email/status/report write-up, or wants to tighten text they pasted.
---

# Draft (personal drafting harness)

Turn the user's rough input into a tight draft in their own voice — floor
rules, channel voice, and an AI-simulated take. Every draft goes through an
English + Chinese review pass with the user before it is final; the user's
final wording is saved back to the channel profile, so the voice keeps
learning from real edits.

## Input & channel detection

- Input: rough thoughts / bullet notes / a pasted text to tighten (in
  `args`, or the user pastes it next).
- Detect the channel from context (the tool the message goes to, the
  audience, the register). Channels: `message`, `reporting`,
  `tickets-comments-pr`, `docs`, plus anything email-like or unlisted —
  treat unlisted channels with `tickets-comments-pr` by default and say so.
- If audience OR channel is unclear, ask ONE merged question:
  "Who reads this, and where does it go (chat message / report /
  ticket-comment-PR / docs / email)?"
- Then load the profiles (Rule 1) and draft.

## Rules (in order)

1. **Load the profiles**: read `~/.claude/profiles/core.md` in full, then
   the detected channel's profile (`~/.claude/profiles/<channel>.md`) in
   full. Core holds the floor rules and the cross-channel traits; the
   channel profile holds that channel's traits, its Do/Don't table, and its
   Verified samples. If a channel profile is missing or empty, fall back to
   core plus the `tickets-comments-pr` profile and say so.

2. **Floor (manager rules)** — every draft, no exceptions:
   - Sentence 1 = the verdict (verb-led status/action declaration). The
     reader can stop after sentence one.
   - Sentence budget: the channel profile's — default 5 (fragments with a
     label count as one).
   - Direct language. No filler: "it's worth noting", "it seems",
     "additionally", "Based on my analysis...". No "it is X, not Y" framing.
   - Evidence (PR #, ticket key, SHA, version `->`) rides IN the verdict
     sentence. Mark anything asserted that the input cannot verify as
     `[unverified]` inline.
   - End with the specific question that needs answering — if one exists.
     If none exists, end on a judgment or a status line.

3. **Voice layer**: the loaded channel profile's traits, applied in full.
   Do not excerpt or restate them here — the profile is the single source;
   when the profile changes, this skill does not.

4. **The take**: the final line of the draft is the take, written by the AI
   in the user's voice. Ground it only in what the draft's own evidence
   supports — that is the judgment or status ending the floor requires.
   When the take must state intent, stance, or preference beyond that
   evidence, still write it, but mark it `[unverified]` inline, same as the
   floor's marking rule. If a specific question needs answering, put it on
   the line just before the take. Nothing follows the take.

## Workflow: review gate + save-back

After the rules produce the draft, it is not final yet:

1. **Review gate**: show the user an English + Chinese review pass — the
   English draft, then its Chinese translation. Wait for the user. The
   draft is final only when the user confirms it.

2. **Apply edits**: if the user changes anything, apply the edits and show
   the updated draft the same way, and wait again. The user's last
   confirmed text is the final version.

3. **Save-back**: after confirmation, append to the channel profile's
   "Verified samples" section — but only when the user edited the draft.
   Scrub before saving: keep the sentence structures, phrasing habits, and
   word choices; replace company identifiers (ticket keys, handles,
   internal system names) with fictional substitutes, or remove them.
   Record with each sample: date, channel, and the edit delta — what the
   AI version got wrong.

## Output format

Show ONLY the draft (no preamble, no explanation, no "here's your draft"),
then its Chinese translation — the review gate. If the input was pasted
text to tighten, show the tightened draft. The take is the last line;
nothing follows it.

## Example

Input: "logs point to crawler retry loop as the main latency source, same
thing we hit with the indexer last year, thinking cap retries at 2"

Draft (channel `tickets-comments-pr`, detected from the log/ticket context):

> Latency is the crawler retry loop. Same pattern we hit in the indexer
> last year — retry storms spike p99 by ~4x `[unverified: exact multiple]`.
> Cap retries at 2 and re-measure. Any reason not to? Capping at 2 is the
> right call.

Then its Chinese translation, then wait for the user's review. If the user
edits, apply the edits and save back per the workflow.
