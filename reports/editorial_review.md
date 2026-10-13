# Editorial review — *The Redacted Crisis*

Reviewer stance: investigative editor. The factual corrections are already applied
(see `corrections_log.md`). Everything below is **proposed, not applied**. These
changes are about framing, structure or new findings, so they're the author's call.
Each one comes as a ready-to-apply text block.

## Verdict

The piece earns its ambition. Its method discipline is unusual for data journalism:
two vintages kept apart, every proxy labelled, and an explicit "what we cannot claim"
section. Its voice is controlled and unsensational. The main editorial weaknesses:

1. **The original contribution arrives late.** The piece's strongest material is §4,
   §6b and the version audit. It shows *that redaction exists, varies 7× between states,
   and moves in administrative batches*. A reader meets it only after ~1,400 words
   about registry growth and homicides (§1–§3), which is context, not discovery.
2. **§2 had become the piece's weakest reasoning**, and I've fixed it (B-1). Even
   corrected, it's a long detour. Its honest conclusion is now "mostly not, can't
   exclude some", which doesn't advance the redaction thesis.
3. **§6b is the longest section and does three jobs**: the version audit, the 2023
   censo, and the 2026 reclassification. The censo case studies are powerful, but they
   make §6b a second article.
4. **The ending works.** §9's "absence of an account" is the right note, and the
   handoff to Stage 2 is earned.

## Strongest original contribution — state it in the standfirst

What no other outlet has published (per the project's own source review) is the
**version audit**. Across ten monthly snapshots, confidentiality grew by 5,101 records
(77% of net registry growth) in state-level batches. Alongside it sits the
filing-authority finding proposed below. Data Cívica (2026) independently confirms the
38%-scale redaction and the state ranking; the *movement over time* is this piece's.

### Proposal E-1 — standfirst — **APPLIED 2026-10-12** (two unsupported phrases removed; see `corrections_log.md` A-07)

```diff
- On 15 August 2026 Mexico's official registry counted 134,268 people still missing.
- That live registry publishes only totals, so field-level detail comes from the last
- record-level snapshot, dated 2 December 2025. In it, 63.2% of unresolved records were
- open to inspection, with fields such as date, age, sex, municipality and case status
- — not always complete. The other 36.8% revealed only the state and the authority that
- filed the report. This is the story of how publication decisions shape what the
- public can see.
+ On 15 August 2026 Mexico's official registry counted 134,268 people still missing.
+ For more than a third of the unresolved records it publishes, the public can learn
+ only two things: the state, and which office filed the report. Ten monthly snapshots
+ of the registry show that this blackout is not set one family at a time. It moves in
+ batches — 2,500 records in one state in two months — and which office files a case
+ matters more than where the family lives.
```

(The last clause depends on adopting E-3. Without E-3, end at "two months".)

## Structure

### Proposal E-2 — compress §2 and move the forensic backlog

Keep Fig I and the two-series divergence (≈250 words). Move the Fig J discussion and
the 72,172 forensic backlog into a boxed "Did deaths become disappearances?" sidebar
after §2, or into the methods note. The corrected answer, "mostly not; cannot
exclude some", is honest but deflating in the main line. The 72,172 figure is
important, but it belongs to Stage 2 (find-events), where it can be engaged properly.

### Proposal E-3 — add the filing-authority finding to §6 — **APPLIED 2026-10-12** (with corrections; see `corrections_log.md` A-06)

Insert after the paragraph ending "…did not speak." in §6. Every number is reproduced by
`src/audit_sensitivity.py` §4 from the 2025-12-02 snapshot.

> The one field the registry leaves on a confidential record makes a test possible.
> It names the office that filed the report. If redaction reflected what families
> chose, it should not depend much on which office happened to take the case. It
> depends on it enormously. In Estado de México, 3% of the unresolved records filed by
> the state prosecutor are confidential, against 36% of those filed by the state's
> search commission. In Nuevo León the figures are 32% and 91%. In Jalisco, 64% and 84%.
> Meanwhile families who report directly through the national commission's online
> portal end up confidential at a similar rate almost everywhere — between 35% and
> 41% in half of the states with enough cases to measure. The families do not change
> at the state line or the office door. The offices do.

Caveat to keep in the text or a footnote: *case mix differs by channel* (the portal
skews to family self-reports and recent years), so this is descriptive. It's
consistent with the oficio's account of capturing authorities, and with Data Cívica's
"concentrated in certain agencies".

A chart: a dot plot, one row per state, two dots (prosecutor vs commission) plus a
portal tick. It would carry this better than prose. If added, generate it from the
freeze and pin it in the manifest like the others.

### Proposal E-4 — split §6b

- **6b — "The totals move in batches"**: version audit plus the CDMX reversal. Keep.
- **6c — "Located is a status the register asserts"**: censo, Quinto Elemento cases,
  and the 2026 reclassification. That last item is new and was the missing link
  between 2023 and the article's present.

Each half then gets its own heading, so a reader can find it again.

### Proposal E-5 — headline

Of the working titles, *The Redacted Crisis* is the strongest: short, accurate, not
sensational. The subtitle "What Mexico's public registry leaves unseen" is good.
Avoid #3 ("disappear twice"). It's a phrase Data Cívica's own project uses ("volver a
desaparecer"), so it would read as borrowed.

## Clarity for a non-statistical reader

- §2 now says "a correlation coefficient adds little here". Good. Consider dropping
  the r values from the body altogether and keeping them in the methods note.
- §5: "Pearson r = −0.38" could become "if anything, the more violent states redact
  *less*". The figure carries the number.
- "Unresolved records" vs "still missing" vs "disappeared or not located". The piece
  uses all three. Add one sentence in §1: *"This piece calls a record 'unresolved' or
  'still missing' when the registry lists the person as disappeared or not located."*

## Repetition to cut

- The "these are current statuses, not dates anyone was found" caveat appears five
  times (status bar, §1 twice, Fig A subtitle, Fig A caption). Keep it in the status
  bar and once in §1.
- "Different denominators" appears in §4 and the methods note. One is enough.

## Captions

Captions are long because they double as provenance. Consider splitting each into a
one-sentence takeaway and a smaller source line. Fig B's caption mixes the 2025
snapshot with the 2026 CDMX update. Move the CDMX note into §6b, where it's discussed.

## Ethics and representation

- Named families (Solís, Guzmán, Sandoval Zúñiga) are quoted from investigations
  published with their participation. That's appropriate. The Solís quote is now
  accurate (C-18).
- The killings of González Murillo and Morales are now dated, cited and kept clear of
  motive (C-24). The paragraph serves the argument (risk borne by civil society) and
  doesn't linger. Keep it short.
- §9's final paragraph centres families without using them as rhetoric. Keep it.

## Language

The draft notes the natural readership is Spanish-speaking. The sources, quotes and
policy audience are all in Spanish. A Spanish edition should be a publication
requirement, not an afterthought. At minimum, publish EN and ES together with
cross-links.
