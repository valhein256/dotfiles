# Channel Profile: tickets-comments-pr (v1)

- Scope: tickets and comments, PR descriptions and review comments — the
  recorded, evidence-anchored work communication, one exchange at a time.
- Sample basis: 25 verified-human samples (2026-06-03..2026-10-13) —
  10 GitHub review verdicts, 2 GitHub PR comments, 13 Jira comments.
  AI-contaminated samples were excluded by pattern and confirmed excluded
  by the user 2026-10-14.
- Sentence budget: 5 (fragments with a label count as one). Corpus:
  median 2 sentences, max 9.

## Traits

1. **Mechanism gets exactly one compact sentence** — identifiers
   backticked, dependency relations named the way build tools name them
   (transitive via / BOM-managed / dependencyManagement override). One
   parenthetical at most. Corpus: ~8 backticked spans per technical
   comment.
2. **Fragments for compression** — "Result:", "Full data:", "Delivered:",
   "Note on X:" — label, then payload. Full sentences are reserved for
   verdicts and mechanism.
3. **Pre-empt the next obvious question** with a "Note on <the thing
   they'll ask>:" line, answered in one or two sentences.
4. **Negative-elimination endings** — close by naming what no longer
   exists. Sparingly, only when an elimination genuinely happened.
5. **Punctuation habits** — `+` as a conjunction, `->` for version/state
   transitions, parentheses carry scope or refs, a period even on a
   three-word verdict ("Ready for reviewing."). No bold in short
   messages, no `##` headings in comments.
6. **Addressing people: handle embedded mid-sentence, no greeting lines**
   — no "Hi X" opener; `@handle` + verb-led sentence ("@rchen fixed in
   fa242d3c.").

## Do / Don't

| Do | Don't |
|---|---|
| "Closing as complete — v0.5 -> v1.1 is live." | "Based on my analysis, it appears that the release was successful." |
| "Result: 16-way fan-out against 2 cores — ~8x oversubscription." | "It's worth noting that there seems to be an oversubscription issue." |
| "no more `{env}` hardcoding." | "This change will help improve the configuration situation." |
| One sentence, one mechanism, backticked IDs | Multi-level bullet trees, `##` sections in comments |
| Ends with judgment or ticket ref | Ends with "Happy to discuss!" |

## Verified samples

Saved by the `draft` skill's save-back: user-edited final versions only,
scrubbed (sentence structures and word habits kept; company identifiers
replaced with fictional substitutes or removed). Each entry records date
and the edit delta — what the AI version got wrong.

- (none yet — grows via save-back)
