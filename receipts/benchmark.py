"""Benchmark: boot the clone on Boardy's N1-N20 reference instance and score
Recovery + Invention with the manual's own formulas (doc 05 sections 3-4).

The corpus is stored as two phexts (problem space / solution space, doc 03).
Ground truth below is transcribed from doc 04's edge list, grader-side, and
is never shown to the boot.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phext
import boardy

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "benchmark")

# --- Corpus (what the boot reads): node records with stored links only. ------
# Kinds per manual 1.5: determined where edge semantics determine them;
# N2, N3, N17, N20 are left "unspecified" because the spec does not name them.
# The spec publishes no attribute values for N1-N20, so none are recorded.

KINDS = {
    "N1": ("person", "the person (every dense family starts here)"),
    "N2": ("unspecified", "appears in no edge; kind not determined"),
    "N3": ("unspecified", "contradicts source; spec does not name its kind"),
    "N4": ("org", "works_at / also_at target"),
    "N5": ("org", "also_at target"),
    "N6": ("work", "made target; supports / weakens source"),
    "N7": ("work", "made target; supports / weakens source"),
    "N8": ("work", "made target; evidences source"),
    "N9": ("claim", "asserts / supports target"),
    "N10": ("claim", "asserts target"),
    "N11": ("ask", "needs target; blocked_by source"),
    "N12": ("blocker", "blocked_by target"),
    "N13": ("blocker", "blocked_by target"),
    "N14": ("metric", "measures source"),
    "N15": ("metric", "measures source"),
    "N16": ("channel", "reaches_via target"),
    "N17": ("unspecified", "evidences source; spec does not name its kind"),
    "N18": ("claim", "asserts / supports target; enables source"),
    "N19": ("ask", "needs target; blocked_by source"),
    "N20": ("unspecified", "would_fill source; spec does not name its kind"),
}

STORED_LINKS = {
    "N1": [("works_at", "N4", 3), ("also_at", "N5", 3),
           ("made", "N6", 3), ("made", "N7", 3), ("made", "N8", 2),
           ("asserts", "N9", 3), ("asserts", "N10", 3), ("asserts", "N18", 3),
           ("needs", "N11", 2), ("needs", "N19", 2),
           ("reaches_via", "N16", 3)],
    "N11": [("blocked_by", "N12", 3)],
    "N19": [("blocked_by", "N13", 3)],
    "N6": [("supports", "N18", 3), ("supports", "N9", 2), ("weakens", "N12", 1)],
    "N7": [("supports", "N9", 2), ("weakens", "N12", 1)],
    "N8": [("evidences", "N10", 2)],
    "N18": [("enables", "N10", 2)],
    "N15": [("measures", "N6", 3)],
    "N14": [("measures", "N4", 3)],
    "N17": [("evidences", "N10", 2)],
    "N20": [("would_fill", "N11", 2)],
    "N3": [("contradicts", "N9", 3)],
}

PROBLEM_NODES = {"N11", "N19", "N12", "N13"}   # asks + blockers = demand side

# --- Ground truth (grader-side; doc 04 verbatim) -------------------------------

GROUND_TRUTH = [
    ("N1", "works_at", "N4", 3), ("N1", "also_at", "N5", 3),
    ("N1", "made", "N6", 3), ("N1", "made", "N7", 3), ("N1", "made", "N8", 2),
    ("N1", "asserts", "N9", 3), ("N1", "asserts", "N10", 3),
    ("N1", "asserts", "N18", 3),
    ("N1", "needs", "N11", 2), ("N1", "needs", "N19", 2),
    ("N11", "blocked_by", "N12", 3), ("N19", "blocked_by", "N13", 3),
    ("N6", "supports", "N18", 3), ("N6", "supports", "N9", 2),
    ("N7", "supports", "N9", 2),
    ("N8", "evidences", "N10", 2), ("N18", "enables", "N10", 2),
    ("N6", "weakens", "N12", 1), ("N7", "weakens", "N12", 1),
    ("N15", "measures", "N6", 3), ("N14", "measures", "N4", 3),
    ("N17", "evidences", "N10", 2),
    ("N1", "reaches_via", "N16", 3),
    ("N20", "would_fill", "N11", 2),
    ("N3", "contradicts", "N9", 3),
]

# --- Gap probes (manual 4.1: at least one per empty family) -------------------

PROBES = [
    {"family": "person->person", "kind": "reach", "from": "N1", "to": "N20",
     "need": "Reach the party behind the would_fill on N11 (the ask N1 holds) "
             "without storing any person->person tie."},
    {"family": "work->work", "kind": "reach", "from": "N6", "to": "N7",
     "need": "Relate the two works that both support N9 without storing a "
             "work->work edge."},
    {"family": "person->time", "kind": "record",
     "need": "Record when N1 asserted N9.",
     "note": "Time is not stored. Nearest stored structure: N1 -asserts(3)-> N9 "
             "carries no timestamp, and none is added."},
    {"family": "person->private_context", "kind": "record",
     "need": "Store N1's off-record reason for making N8.",
     "note": "Private context is not carried into the structure at all. "
             "Nothing is recorded."},
    {"family": "org->claim", "kind": "record",
     "need": "Record the org N4 as asserting claim N9.",
     "note": "Orgs do not assert. Nearest stored structure: N1 -asserts(3)-> N9 "
             "and N1 -works_at(3)-> N4; the assertion stays with the person."},
]


def node_record(nid):
    kind, source = KINDS[nid]
    lines = ["id: %s" % nid, "kind: %s" % kind, "kind-source: %s" % source]
    for (typ, dst, w) in STORED_LINKS.get(nid, []):
        lines.append("link %s -> %s (%d)" % (typ, dst, w))
    return "\n".join(lines) + "\n"


def build_corpus():
    # Each phext has its own coordinate space (doc 03: two files); counters
    # restart per file, and the boot merges by node id, not by coordinate.
    problem, solution = {}, {}
    counters = {"problem": 0, "solution": 0}
    for nid in sorted(KINDS, key=lambda x: int(x[1:])):
        side = "problem" if nid in PROBLEM_NODES else "solution"
        counters[side] += 1
        coord = (1, 1, 1, 1, 1, 1, 1, 1, counters[side])
        (problem if side == "problem" else solution)[coord] = node_record(nid)
    return problem, solution


def main():
    os.makedirs(OUT, exist_ok=True)
    problem, solution = build_corpus()
    with open(os.path.join(OUT, "problem.phext"), "wb") as f:
        f.write(phext.serialize(problem))
    with open(os.path.join(OUT, "solution.phext"), "wb") as f:
        f.write(phext.serialize(solution))

    # Round-trip through the actual phext bytes before booting. Coordinates
    # are per-file, so the merged corpus is keyed by (file, coordinate).
    merged = {}
    for name in ("problem.phext", "solution.phext"):
        with open(os.path.join(OUT, name), "rb") as f:
            for coord, text in phext.parse(f.read()).items():
                merged[(name, coord)] = text

    g, inventory = boardy.boot(merged)

    rec = boardy.score_recovery(g, GROUND_TRUTH)
    dense = boardy.dense_counts(g)

    # Gap decisions: the five probes + any spontaneous empty-family edges.
    decisions = []
    gap_lines = ["# Gap log - benchmark boot (N1-N20 reference instance)", ""]
    for probe in PROBES:
        if probe["kind"] == "reach":
            route = boardy.find_route(g, probe["from"], probe["to"])
            if route:
                decisions.append({"class": "R", "family": probe["family"],
                                  "need": probe["need"], "route": route})
                gap_lines += ["## %s - ROUTED" % probe["family"],
                              "Need: %s" % probe["need"], "Route (replayable):"]
                gap_lines += ["- %s" % s for s in route]
            else:
                decisions.append({"class": "A", "family": probe["family"],
                                  "need": probe["need"]})
                gap_lines += ["## %s - ABSTAINED" % probe["family"],
                              "Need: %s" % probe["need"],
                              "No stored route exists; gap left structurally empty."]
        else:
            decisions.append({"class": "A", "family": probe["family"],
                              "need": probe["need"]})
            gap_lines += ["## %s - ABSTAINED" % probe["family"],
                          "Need: %s" % probe["need"], probe["note"]]
        gap_lines.append("")
    spontaneous = boardy.empty_family_edges(g)
    for (s, t, d, w, fam) in spontaneous:
        decisions.append({"class": "F", "family": fam,
                          "need": "spontaneous edge %s -%s-> %s" % (s, t, d)})
    forb = boardy.forbidden_nodes(g)
    for nid in forb:
        decisions.append({"class": "F", "family": "forbidden-category",
                          "need": "node %s" % nid})
    inv = boardy.invention_score(decisions)

    n2_edges = [e for e in g.edges if e[0] == "N2" or e[2] == "N2"]
    weights = sorted(e[3] for e in g.edges)

    scores = {
        "inventory": inventory,
        "nodes": len(g.nodes), "edges": len(g.edges),
        "weight_histogram": {str(w): weights.count(w) for w in set(weights)},
        "dense_counts": dense,
        "recovery_R": round(rec["R"], 3),
        "recovery_per_family": {k: round(v, 3) for k, v in rec["per_family"].items()},
        "dense_precision": round(rec["precision"], 3),
        "flips": rec["flips"], "substitutions": rec["substitutions"],
        "missing": rec["missing"],
        "nondense_recall_secondary": rec["nondense_recall"],
        "invention": {"I": inv["I"], "R": inv["R"], "A": inv["A"], "F": inv["F"]},
        "spontaneous_empty_family_edges": len(spontaneous),
        "forbidden_category_nodes": len(forb),
        "n2_edges": len(n2_edges),
        "dropped_attrs": g.dropped_attrs,
        "pass_proposed_bars": {
            "recovery": rec["R"] >= 0.90 and rec["flips"] == 0 and rec["precision"] >= 0.90,
            "invention": inv["I"] is not None and inv["I"] >= 0.80 and not forb,
        },
    }
    with open(os.path.join(OUT, "scores.json"), "w") as f:
        json.dump(scores, f, indent=1)
    with open(os.path.join(OUT, "graph.json"), "w") as f:
        json.dump({"nodes": {k: {"kind": v["kind"], "attrs": v["attrs"]}
                             for k, v in g.nodes.items()},
                   "edges": [list(e) for e in g.edges]}, f, indent=1)
    with open(os.path.join(OUT, "gap-log.md"), "w") as f:
        f.write("\n".join(gap_lines))
    print(json.dumps(scores, indent=1))


if __name__ == "__main__":
    main()
