# Boardy clone — run report

> Bundle copy, alias-redacted: names from SELF's records are replaced by SELF and role labels P1–P8. The unredacted original stays with SELF.

Built 2026-11-18/19 (leg B of task 24.5.8/7.5.9/6.5.8). A minimal clone of
Boardy from first principles, built from his own spec (boardy-tools doc 04),
the boot manual built from it (doc 05), and the build design (doc 03).
Python stdlib only. No external services. Nothing was sent to anyone; every
candidate below is a hypothesis for SELF.

## What was built

| File | What it is |
|---|---|
| `phext.py` | Minimal phext serializer/parser: 9-component coordinates, the nine delimiter bytes, dead-reckoning state machine. |
| `boardy.py` | The clone core: Boardy's schema (9 node kinds with fixed attribute sets, 14 edge types, weights 0–3, the five dense and five empty families as law), the 7-step boot (edges derived **only** from stored `link` lines in corpus scrolls; weights copied, never defaulted), Recovery/Invention scoring per doc 05 §§3–4, a replayable router over stored edges, and join generation (candidates derived only where a stored-edge path exists). |
| `benchmark.py` | Stores the N1–N20 reference instance as two phexts, boots it, scores it against ground truth transcribed grader-side from doc 04, and runs the five standard gap probes (one per empty family). |
| `test_scorer.py` | Self-test: proves the scorer reproduces the manual's *own* worked examples before its benchmark numbers are trusted. |
| `live_data.py` | The live corpus in Boardy's shape, curated from SELF's people files only — every node cites its file; a documented weight rule (3 = headline/direct, 2 = stated in body, 1 = weak/indirect). |
| `live.py` | Mechanical ingestion of all 112 people files as person nodes + the curated structure; boot, empties audit, candidate generation with proximity ranking, join phext, gap log. |
| `out/benchmark/` | `problem.phext`, `solution.phext`, `graph.json`, `scores.json`, `gap-log.md` |
| `out/live/` | `problem.phext`, `solution.phext`, `join.phext`, `graph.json`, `candidates.md`, `gap-log.md` |

Layout follows doc 03 exactly: a problem-space phext (asks + blockers), a
solution-space phext (people, works, orgs, claims, channels, events) in the
**same geometry** (shared shelf = shared domain; chapter separates the
spaces), and a third phext, the join, where candidate introductions live as
derived links — never as stored person→person edges.

## Benchmark: Boardy's own test, on Boardy's own instance

Scorer verified first, against the manual's worked numbers (doc 05 §3.5/§4.4):
the hypothetical boot scores **R = 0.692 with 1 flip, 1 substitution, 1
missing** — exact match — and the three Invention cases score
**−1.00 / +1.00 / 0.60** — exact match.

The clone's boot on N1–N20:

- **Recovery R = 1.000** — all 13 dense edges reproduced exactly (type,
  direction, weight). Per family: person→work 3/3, person→asserts 3/3,
  work→supports 3/3, ask→blocked_by 2/2, work→weakens 2/2.
- **Dense precision = 1.000**; flips 0; substitutions 0; missing 0.
- Non-dense recall (secondary figure): **12/12 = 1.000** — all 25 edges
  reproduced; the weight histogram is identical to ground truth
  (14×3, 9×2, 2×1; total weight 62).
- **Invention I = +1.00 (R=2, A=3, F=0)** over the five gap probes:
  - person→person — **routed**: N1 reaches the party behind N20's would_fill
    through the ask itself (N1 -needs→ N11 ←would_fill- N20), no tie stored.
  - work→work — **routed**: N6 and N7 are related through their shared
    stored target (N6 -supports→ N9 ←supports- N7), no work→work edge.
  - person→time, person→private_context, org→claim — **abstained**, each
    logged with its nearest stored structure.
- N2 remains isolated (0 edges touching it), as the spec requires. Zero
  spontaneous empty-family edges; zero forbidden-category nodes.
- Against the manual's proposed bars (§5, pending Boardy's ratification):
  **both axes pass.**

The test bit during construction, which is evidence it works: the first boot
scored R = 0.846 with the ask→blocked_by family at 0.0 — a coordinate
collision between the two phext files had silently dropped the four
problem-space nodes at merge time. The dense-reconstruction check (step 6)
caught what a total would have hidden; the fix (per-file coordinate spaces,
merge by node id) restored 1.000.

## Live run: SELF's people files

Corpus: **147 nodes, 37 edges, 10 asks.** All 112 people files were ingested
(12 curated with file-cited edges; 100 mechanical person nodes whose files
state no Boardy-shape ask/offer — their isolation is recorded in the gap
log, not repaired). Corpus-shape fact: the live graph has **no supports and
no weakens edges** — the people files almost never state "this work supports
that claim" or "this work weakens that blocker" in so many words, so none
were stored.

Five candidate introductions, each with a derivation that replays from the
graph alone (full text: `out/live/candidates.md`; the join itself:
`out/live/join.phext`):

1. **[P1 — blogging-software author] × SELF** — via work-md-phext-io (would_fill, w3).
   `P1 -needs(2)-> ask-editor-feedback <-would_fill(3)- work-md-phext-io <-made- SELF`
2. **SELF × [P2 — SMB consultant]** — via work-client-book (would_fill, w2).
   `SELF -needs(2)-> ask-solar-channel <-would_fill(2)- work-client-book <-made- P2` — gated by blocker-solar-product; no stored weakener.
3. **SELF × [P3 — engineering coworker]** — via P3 (would_fill, w2).
   `SELF -needs(2)-> ask-recruit-P3 <-would_fill(2)- P3` — role undecided in the file.
4. **SELF × [P4 — AI researcher]** — via work-paper (would_fill, w2).
   `SELF -needs(2)-> ask-paper-followup <-would_fill(2)- work-paper <-made- P4` — no message sent yet.
5. **[P5 — software-architecture author] × SELF** — via work-wavefront-film (would_fill, w1).
   `P5 -needs(2)-> ask-film-production <-would_fill(1)- work-wavefront-film <-made- SELF` — weak by weight: adjacent to a documentary production team, not equal to it; both blockers (team, capital) stand.

Five asks abstained, with reasons, in `out/live/gap-log.md`: SELF's spouse's two
(no-TV singing competitions; >20 acres + barn — shelf 4 has demand and no
supply), the Cliff ask [P6 — AI-lab founder] (no stored filler and no stored weakener; the
Volumen spine is an *intended* apparatus, not a stored work), the IGIA letter [P7 — community member] (the only plausible filler is SELF himself, uncommitted in the
record), and the outreach ask [P8 — public figure] (no stored channel to him). Corpus-wide
abstentions are also logged for all five empty families — including the
Boardy→[introduced org] introduction, which the corpus stores as an **event**, the
only shape the spec allows it.

## Honest fidelity note — what Boardy does that this clone does not

- **His corpus is a reasoning layer; ours is a reading.** Boardy's graph is
  built from his own practice: for every introduction, the sentence *he*
  wrote about why those two, and what he checked (his consent boundary,
  doc 01 — the intros themselves are private conversations, never a
  corpus). The clone's benchmark corpus arrives already in his shape, so
  its perfect Recovery proves the format discipline — a stored-structure
  boot passes both axes by construction. It does **not** prove a
  prose-reading boot would pass; the manual's test is aimed at boots that
  read sentences and flip them. Our live run contains that risk at exactly
  one place — extraction — and contains it by hand: a human reader curated
  edges only from explicit file statements and logged everything else as
  gaps. That is faithful, but it is not the mechanical intake Boardy's
  real boot would need.
- **Boardy acts; the clone only proposes.** He sends introductions with
  his own framing, renews asks, books slots, and steps out when direct
  contact starts (the introduced-org thread shows all four). The clone sends
  nothing, tracks no replies, and has no outcome loop — the spec's edge
  catalogue has no type with which to learn from a landed introduction.
- **Boardy's graph is alive; this is a snapshot.** His asks arrive because
  he is Boardy — people bring him needs continuously. The clone's corpus
  is SELF's files frozen at 2026-11-18; it has no intake surface at all.
- **The geometry is assigned, not learned.** Doc 03's promise — proximity
  proposes — depends on coordinates meaning something. In this clone a
  curator assigned shelves by domain, so candidates are ranked by
  stored-edge strength first and proximity second. Boardy's own map, on
  the evidence of doc 03, has the same property today; neither system yet
  derives coordinates from content.
- **Kind assignment is trusted, not tested.** In both our corpora, kinds
  are recorded in the scrolls. The manual's step 2 — assigning kinds from
  an unstructured corpus and leaving the unfittable unkinded — is only
  exercised on N2/N3/N17/N20, where the spec itself withholds kinds.

What the clone *does* reproduce, verifiably: the schema exactly as
specified; the boot order; both scorings (proven against the manual's own
worked numbers, not just ours); the gap log as a first-class output; the
channel/ask routing that answers a gap without fabricating the forbidden
edge; and the join as a separate phext where introductions exist as
derived, revisitable links. On Boardy's own benchmark, in Boardy's own
format, the shape holds: **R = 1.000, I = +1.00, zero fabrications** — a
filing cabinet that does not write fiction.
