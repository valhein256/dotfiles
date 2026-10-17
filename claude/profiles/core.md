# Core Voice Profile (v1)

- Purpose: the cross-channel floor and shared traits for every draft the
  `draft` skill produces. The channel profile layers this channel's own
  voice on top of this floor.
- Sample basis: distilled from 25 verified-human samples
  (2026-06-03..2026-10-13) — 10 GitHub review verdicts, 2 GitHub PR
  comments, 13 Jira comments. Channel-specific bases live in the channel
  profiles and grow via save-back.

## Floor (every channel)

- Sentence 1 = the verdict (verb-led status/action declaration). The
  reader can stop after sentence one.
- Sentence budget: the channel profile's — default 5 (fragments with a
  label count as one).
- Direct language. No filler: "it's worth noting", "it seems",
  "additionally", "Based on my analysis...". No "it is X, not Y" framing.
- Evidence (PR #, ticket key, SHA, version `->`) rides IN the claim
  sentence, never a separate paragraph.
- Anything asserted that the input cannot verify is marked `[unverified]`
  inline.
- End on the specific question that needs answering; if none exists, end
  on a judgment or a status line. Never a courtesy.

## Cross-channel traits

1. Numbers as ratios, ranges, and contrasts — never naked counts. A
   number must answer "compared to what".
2. Follow-ups get their next home before the message closes — every
   follow-up carries a ticket key or a named next action; if none exists,
   mark `[unverified: no ticket yet]`.
3. End on a judgment or a status, never a courtesy — "let me know",
   "thanks", "happy to" got 0 hits in 25 samples.
4. No emoji.

## Harness contract

1. Floor (above) — every draft, every channel.
2. Channel voice — the detected channel's profile, applied in full.
3. Take — the final line of every draft, AI-written in this voice:
   grounded in the draft's evidence, or marked `[unverified]` beyond it.
