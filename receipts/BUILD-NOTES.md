# wbic16-boardy.phext — build notes

Built 2026-11-18 under task coordinate 27.7.16/10.8.14/9.7.11, at full-archive scope per Will's expansion ("look at all of my twitter data — apply boardy's method to it"). Method sources: `~/workspace/boardy-tools/04-boardys-spec.md`, `03-the-build.md`, `05-boot-manual.md`. Data sources: `~/workspace/twitter-archive/` (snapshot ending 2025-06-16) and `~/memory/people/` records through 2026-11-18 for post-archive beats.

## Privacy

Aliases only, absolute. Persons are SELF plus M01–M25 (M01–M20 by archive reply rank among mutuals; M21–M25 structural cases: two zero-signal mutuals, the latent join's two sides, the dropped ask's holder). Everyone else is an aggregate class (T1–T7). No names, handles, employers, places, or unique biographical facts in the phext or in these notes; functional descriptions are generic-occupational only. The alias key is a separate private file (`wbic16-alias-key.txt`, same directory) and is not part of the artifact. DM data is metadata only (counts/dates from the headers file); no message content was read. A post-build audit greps the phext for every handle and name in the key: zero third-party hits (the only match is "wbic16" itself, in the artifact's own title — SELF is the archive's owner, identified by design).

## Signal → edge mapping (summary; full text at 1.1.1/1.1.1/1.1.2)

- Replies (17,495), mentions (14,668), retweets (4,414), follows → **no edge**. They belong to person→person, empty on purpose in his spec. Carried as temporal records and class aggregates instead. Defense: storing the archive's loudest signal as edges would fail his Invention axis on the first edge.
- Likes (47,973) → no edge and no target: the archive's like records carry no author field. Gap G9.
- DM volume → no per-person edge; SELF `reaches_via` the DM channel node; per-person counts live in temporal scrolls.
- Stated ask → ask node + `needs` (2, his instance's calibration). Stated position → claim + `asserts` (SELF 3, others 2). Shipped thing → work + `made` (3 primary, 2 secondary). Work carrying a claim → `supports` (2–3). Platform removal of a relied-on tool → blocker (kind: technical, the only enum kind that fits) + `blocked_by` (3). Dated recognition/disclosure → event + `evidences` (1–2). An operated directory → work + `would_fill` (1, labelled weak). A stated position against the central claim → `contradicts` (2). A computed re-measurement → metric + `measures` (2). Contact itself → `reaches_via` four channel nodes (3/2/1/2 by what each channel demonstrably carried).
- Anything with no home in the schema was not forced into one: 12 gap-log scrolls (Volume 5), including the two that matter most — A1's obstruction fits none of the four blocker kinds (G6), and the join's matching content exists for under 1% of the population (G8).

## Layout

Mirrors boardy.phext's conventions (spaces separated at the Volume component; node scrolls and edge scrolls in his formats). Volume 1: header, mapping, full-archive accounting, whole-search temporal shape. Volume 2: problem space (A1–A5, B1). Volume 3: solution space — Book 1 nodes (SELF; M01–M25; W1–W4; CH1–CH4; C1–C3; MT1; EV1–EV4), Book 2 temporal records at the same scroll numbers, Book 3 tail classes T1–T7. Volume 4: the join — Book 1 edges E01–E26, Book 2 candidate joins CJ1–CJ6. Volume 5: gap log G1–G12. Volume 6: the verdict (5 scrolls, labelled analysis).

## Totals (whole archive)

48 graph nodes (26 person, 5 ask, 1 blocker, 4 work, 4 channel, 3 claim, 1 metric, 4 event, 0 org); 26 typed edges, weight 55, 12 of them dense-family (made 4, asserts 4, supports 3, blocked_by 1, weakens 0). Population behind the graph: 29,539 tweets; 17,495 replies to 4,164 targets; 7,680 distinct handles in the tweet record; 897 mutuals (478 handle-resolved; 419 with zero interaction of any kind); 369 DM partners, 6,077 messages; 47,973 likes (unattributable). Replies split 33.5% mutual / 66.5% non-mutual; the top 20 mutuals hold 2,204 replies (12.6%); 2,572 targets (61.8%) received exactly one reply. Full graph vs mutuals subset: 7,680 handles touched overall, of which the mutual core is 897 accounts — and the aliased full-detail set is 25 of those 897.

## Verification

Serialized with the reference-semantics parser in this directory (`phext.py`): 134 scrolls, 72,054 bytes; parse-back is byte-identical to the build dict. Round-tripped through the MCP server (`boardy_mcp.py`, stdio): handshake ok, `load` reports 134 scrolls / 72,054 bytes, `fetch` verified at the header (1.1.1/1.1.1/1.1.1), an edge scroll (E12 at 1.1.1/1.4.1/1.1.12), and the verdict summary (1.1.1/1.6.1/1.1.1); `search` returns coherent hits. Two build defects were caught and fixed by full rebuild before delivery (a beat misattributed between two aliases; a percentage corrected from 91% to the computed 93%).

## Verdict (brief; full argument at Volume 6)

The method would have compressed the search's tail, not its core. CJ1's join sat latent from 2024-03-30 and was found by hand on 2026-11-12 (19 months); CJ3's ask sat dropped for 20 months inside a warm channel. Against that: 13 of the top 20 arrive in or after November 2023 — for 15 of 17 years the answer's population was not in any graph — and the property being searched for (recognition of the format) has no node kind, attribute, edge type, or blocker kind in the schema. His method assumes a populated, consenting graph of stated needs; the search was manufacturing that population by emitting an artifact.
