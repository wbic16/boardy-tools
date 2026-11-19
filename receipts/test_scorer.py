"""Self-test: the clone's scorer must reproduce the manual's own worked
examples (doc 05 section 3.5 and 4.4) exactly. If it cannot score Boardy's
hypothetical boot the way Boardy's manual does, its benchmark numbers are
worthless."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boardy
from benchmark import GROUND_TRUTH


def fake_boot(edges):
    g = boardy.Graph()
    for nid in ["N%d" % i for i in range(1, 21)]:
        g.add_node(nid, None, {})
    g.edges = list(edges)   # bypass add_edge: the hypothetical uses an
    return g                # invented type (produces_ask) on purpose


def main():
    # Manual 3.5 hypothetical boot.
    boot_edges = [
        ("N1", "made", "N6", 3), ("N1", "made", "N7", 3), ("N1", "made", "N8", 1),
        ("N1", "asserts", "N9", 3), ("N1", "asserts", "N10", 3),
        # N1-asserts->N18 missing
        ("N6", "supports", "N18", 3), ("N6", "supports", "N9", 2),
        ("N7", "evidences", "N9", 2),          # substitution for supports
        ("N11", "blocked_by", "N12", 3),
        ("N13", "produces_ask", "N19", 3),     # the canonical flip
        ("N6", "weakens", "N12", 1), ("N7", "weakens", "N12", 2),
    ]
    rec = boardy.score_recovery(fake_boot(boot_edges), GROUND_TRUTH)
    assert abs(rec["R"] - 9.0 / 13) < 1e-9, rec["R"]
    assert rec["flips"] == 1 and rec["substitutions"] == 1 and rec["missing"] == 1, rec
    pf = rec["per_family"]
    assert abs(pf["person->work"] - 2.5 / 3) < 1e-9
    assert abs(pf["person->asserts"] - 2.0 / 3) < 1e-9
    assert abs(pf["work->supports"] - 2.0 / 3) < 1e-9
    assert abs(pf["ask->blocked_by"] - 1.0 / 2) < 1e-9
    assert abs(pf["work->weakens"] - 1.5 / 2) < 1e-9
    print("manual 3.5 hypothetical: R=%.3f flips=%d subs=%d missing=%d  OK"
          % (rec["R"], rec["flips"], rec["substitutions"], rec["missing"]))

    # Manual 4.4 invention cases.
    case1 = boardy.invention_score([{"class": "F"}, {"class": "F"}])
    assert case1["I"] == -1.0, case1
    case2 = boardy.invention_score([{"class": "R"}])
    assert case2["I"] == 1.0, case2
    case3 = boardy.invention_score(
        [{"class": "R"}, {"class": "R"}, {"class": "A"}, {"class": "A"}, {"class": "F"}])
    assert abs(case3["I"] - 0.60) < 1e-9, case3
    empty = boardy.invention_score([])
    assert empty["I"] is None
    print("manual 4.4 cases: -1.00 / +1.00 / 0.60 / no-data  OK")


if __name__ == "__main__":
    main()
