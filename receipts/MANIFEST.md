# Boardy receipts bundle — manifest

Artifacts from the 2026-11-18 boardy-clone work. Every claim below is checkable
with the commands in the Verify section. Nothing here needs to be taken on trust.

## Index

- `boardy.phext` — your spec instance (N1–N20, 25 edges) as a phext: 46 scrolls.
- `boardy_mcp.py` + `MCP-README.md` — MCP server (stdio, Python stdlib only) that loads a phext and serves `load` / `toc` / `fetch` / `search`. `test_client.py` play-tests it; `PLAYTEST.md` is a real transcript.
- `boardy.py`, `phext.py`, `benchmark.py`, `test_scorer.py`, `out/benchmark/` — the clone and its run on your instance.
- `RUN-REPORT.md` — what the clone does and does not reproduce.
- `wbic16-boardy.phext` + `BUILD-NOTES.md` — the worked example: one person's full Twitter archive (2008–2025) mapped with your methodology. Aliases only.
- `RESEARCH.md` — your public architecture and operating-cost model, sourced.

## Files

| file | bytes | sha-256 |
|---|---|---|
| `BUILD-NOTES.md` | 5589 | `a889797077160fc58309fcc22f82a564685410b72105166da263ffc7adac9faf` |
| `MCP-README.md` | 1042 | `44ab4e023de653527b06fdcaa8b829096fd515ae0cd8753c7653a30746ce25e3` |
| `PLAYTEST.md` | 6558 | `72a3f44d34056f865a1f30a4f346df72c1e0662e222987bbfb0d2b5932cb2468` |
| `RESEARCH.md` | 17213 | `663fffde541fd12bc0897edb2b3d9037da9b779ca36eee7436c31e712db26671` |
| `RUN-REPORT.md` | 9658 | `6840fae3bbf23898ee6afd36a6fc01741de62e07840f0771b3049111b1d0653e` |
| `benchmark.py` | 10119 | `a580171069f0e89194056f77893683f22d618fb9fc35e65e38056d7b6848e2fb` |
| `boardy.phext` | 8594 | `4330d18c0d3b49e481bd238db20e5dfbbf165632a839456ee5c299bc28234122` |
| `boardy.py` | 13218 | `bb56c39ef8e47b796ae145f3ecdbd62d792596871d87454a60c363aa0b48b0ac` |
| `boardy_mcp.py` | 6342 | `c272ba5206fb005464494526f13f04c5bc897238b7ae4c9dc865aa5289952db8` |
| `phext.py` | 2020 | `27878b226d6024283498c99807b229b99e43f9a9e265b128d2d05e56bbd2add9` |
| `test_client.py` | 4195 | `88e8a6467ed02c8a5fe9635dffd53487f8170363000d9c4217aa48edf8e9d457` |
| `test_scorer.py` | 2454 | `bb99f384bba0af39a2c49f65039d04880b163c7fc8a17f9599de8ca4113dffc8` |
| `wbic16-boardy.phext` | 72054 | `c3ff3dc24cc1d580897a88ff7eb869ef6dd91fe30191c43834c726df169ccdf2` |
| `out/benchmark/gap-log.md` | 1016 | `b5466b05faa553a16a296dd5ac8b5b0c4b66642803acc32ffada6b47a9be28ac` |
| `out/benchmark/graph.json` | 2214 | `bc7c650809a004fbdd545bea49bb6aa1d2394cbf8809c8174c89798ecccb4622` |
| `out/benchmark/problem.phext` | 289 | `1ec64800ae938250bcdb4700e0986cf59fab8d890b19247e915c970444006eb1` |
| `out/benchmark/scores.json` | 933 | `1644475718479f1b7888700be6423c0db77d97add720df38dab3ab9f043e0418` |
| `out/benchmark/solution.phext` | 1613 | `dbe253de926311fee1144498ad2226ac12bd68f06fc34407184f4f9ccf1cff90` |

Total: 18 files, 165121 bytes (this manifest excluded).

## Verify

Hashes: `sha256sum <file>` against the table above.

Scorer, against the boot manual's own worked examples:
`python3 test_scorer.py` → `manual 3.5 hypothetical: R=0.692 flips=1 subs=1 missing=1 OK` and `manual 4.4 cases: -1.00 / +1.00 / 0.60 / no-data OK`.

Benchmark, on your N1–N20 instance:
`python3 benchmark.py` → `out/benchmark/scores.json` reports `recovery_R: 1.0`, `dense_precision: 1.0`, `invention.I: 1.0` (R=2, A=3, F=0). The regenerated `out/benchmark/` files are byte-identical to the copies in this bundle.

MCP play-test:
`python3 test_client.py` → ends `PLAYTEST: ALL GREEN` (9 checks) and rewrites `PLAYTEST.md` with the run's transcript (the copy in this bundle is the transcript of a re-run against the bundle itself; path lines reflect that).

Worked example, through the same server (client config in `MCP-README.md`):
`load` `wbic16-boardy.phext` → `134 scrolls, 72054 bytes`; `fetch` `1.1.1/1.6.1/1.1.1` → the verdict scroll; `fetch` `1.1.1/1.4.1/1.1.12` → edge E12.

## Bundle changes and exclusions

- `RUN-REPORT.md` is alias-redacted in this bundle: names from SELF's records are replaced by SELF and role labels P1–P8. Every other file is byte-identical to its original in `boardy-clone/`.
- Excluded by design: `wbic16-alias-key.txt` (private; maps the worked example's aliases) and `out/live/` (candidate derivations that name SELF's contacts). The clone's live-run summary is in `RUN-REPORT.md`, redacted as above.
