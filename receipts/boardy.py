"""Boardy clone core: schema, boot procedure, Recovery/Invention scoring,
gap routing, and join (candidate introduction) generation.

Implements Boardy's spec (boardy-tools doc 04) and the boot manual (doc 05)
as literally as a minimal system can: edges are derived ONLY from stored
`link` lines in corpus scrolls; weights are copied, never defaulted;
empty families are audited, never filled.
"""

from collections import defaultdict, deque

# --- Schema (doc 04 / manual section 1) -------------------------------------

KIND_ATTRS = {
    "person": {"role", "function", "stage", "current_focus"},
    "org": {"what_it_sells", "stage", "headcount", "traction"},
    "work": {"form", "maturity", "who_uses_it"},
    "claim": {"assertion", "status"},
    "ask": {"purpose", "granularity", "urgency"},
    "blocker": {"kind"},
    "metric": {"value", "as_of", "confidence"},
    "channel": {"medium", "latency"},
    "event": {"what", "when"},
}
FORBIDDEN_CATEGORIES = {"time", "private_context"}
BLOCKER_KINDS = {"no_customer", "no_reference", "technical", "capacity"}
CLAIM_STATUS = {"stated", "inferred"}

EDGE_TYPES = {
    "works_at", "also_at", "made", "asserts", "needs", "blocked_by",
    "supports", "evidences", "enables", "weakens", "measures",
    "reaches_via", "would_fill", "contradicts",
}

# Dense families (manual 1.4): in this schema each dense family is one type.
DENSE_TYPES = {"made", "asserts", "supports", "blocked_by", "weakens"}
DENSE_FAMILY_OF_TYPE = {
    "made": "person->work",
    "asserts": "person->asserts",
    "supports": "work->supports",
    "blocked_by": "ask->blocked_by",
    "weakens": "work->weakens",
}
# Empty families as (source kind, target kind) pairs (manual 1.4).
EMPTY_KIND_PAIRS = {
    ("person", "person"): "person->person",
    ("person", "time"): "person->time",
    ("person", "private_context"): "person->private_context",
    ("work", "work"): "work->work",
    ("org", "claim"): "org->claim",
}


class Graph:
    def __init__(self):
        self.nodes = {}          # id -> {"kind": str|None, "attrs": dict, "coord": tuple}
        self.edges = []          # (src, type, dst, weight)
        self.dropped_attrs = []  # boot discipline log

    def add_node(self, nid, kind, attrs, coord=None):
        self.nodes[nid] = {"kind": kind, "attrs": dict(attrs), "coord": coord}

    def add_edge(self, src, typ, dst, weight):
        assert typ in EDGE_TYPES, typ
        assert 0 <= weight <= 3, weight
        self.edges.append((src, typ, dst, weight))

    def kind(self, nid):
        n = self.nodes.get(nid)
        return n["kind"] if n else None

    def edges_from(self, src, typ=None):
        return [e for e in self.edges if e[0] == src and (typ is None or e[1] == typ)]

    def edges_to(self, dst, typ=None):
        return [e for e in self.edges if e[2] == dst and (typ is None or e[1] == typ)]

    def edge_set(self):
        return set(self.edges)


# --- Boot (manual section 2) --------------------------------------------------
# Corpus scroll text format, one node per scroll:
#   id: N1
#   kind: person            (or "unspecified" -> left unkinded, per manual 1.5)
#   kind-source: <how the corpus determines it>
#   attr <name>: <value>
#   link <type> -> <dst> (<weight>)
#   summary: <corpus text; not a spec attribute>
#   cite: <where this record comes from>

def parse_node_record(text):
    rec = {"attrs": {}, "links": [], "meta": {}}
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("id:"):
            rec["id"] = line[3:].strip()
        elif line.startswith("kind:"):
            rec["kind"] = line[5:].strip()
        elif line.startswith("attr "):
            name, _, value = line[5:].partition(":")
            rec["attrs"][name.strip()] = value.strip()
        elif line.startswith("link "):
            body = line[5:].strip()                     # made -> N6 (3)
            typ, _, rest = body.partition(" -> ")
            dst, _, w = rest.partition(" (")
            rec["links"].append((typ.strip(), dst.strip(), int(w.rstrip(")"))))
        elif ":" in line:
            k, _, v = line.partition(":")
            rec["meta"][k.strip()] = v.strip()
    return rec


def boot(scrolls):
    """scrolls: {coord: text} merged from the problem+solution phexts.
    Returns (graph, inventory) following manual steps 1-7 (audit in step 7
    is performed by audit_empties; the dense check is dense_counts)."""
    g = Graph()
    inventory = []
    records = []
    # Step 1 - freeze and inventory.
    for coord in sorted(scrolls):
        text = scrolls[coord]
        if not text.strip():
            continue
        rec = parse_node_record(text)
        rec["coord"] = coord
        records.append(rec)
        inventory.append(rec["id"])
    # Steps 2-3 - kind assignment and attribute fill (fixed sets only).
    for rec in records:
        kind = rec.get("kind")
        if kind in (None, "", "unspecified"):
            kind = None                      # flagged, left unkinded
        assert kind is None or kind in KIND_ATTRS, (rec["id"], kind)
        assert kind not in FORBIDDEN_CATEGORIES
        attrs = {}
        if kind is not None:
            for name, value in rec["attrs"].items():
                if name in KIND_ATTRS[kind]:
                    attrs[name] = value
                else:
                    g.dropped_attrs.append((rec["id"], name))
            # Enumerated values are validated when present; absence stays
            # absent (manual step 3: missing stays missing).
            if kind == "blocker" and "kind" in attrs and attrs["kind"] not in BLOCKER_KINDS:
                raise ValueError("bad blocker kind %r" % attrs["kind"])
            if kind == "claim" and "status" in attrs and attrs["status"] not in CLAIM_STATUS:
                raise ValueError("bad claim status %r" % attrs["status"])
        g.add_node(rec["id"], kind, attrs, rec["coord"])
    # Steps 4-5 - edge derivation from stored links only; weights copied.
    for rec in records:
        for typ, dst, weight in rec["links"]:
            g.add_edge(rec["id"], typ, dst, weight)
    return g, inventory


def dense_counts(g):
    counts = defaultdict(int)
    for (_, typ, _, _) in g.edges:
        if typ in DENSE_TYPES:
            counts[DENSE_FAMILY_OF_TYPE[typ]] += 1
    return dict(counts)


def empty_family_edges(g):
    """Every boot edge landing in an empty kind-pair family (manual step 7)."""
    bad = []
    for (src, typ, dst, w) in g.edges:
        pair = (g.kind(src), g.kind(dst))
        if pair in EMPTY_KIND_PAIRS:
            bad.append((src, typ, dst, w, EMPTY_KIND_PAIRS[pair]))
    return bad


def forbidden_nodes(g):
    return [nid for nid, n in g.nodes.items() if n["kind"] in FORBIDDEN_CATEGORIES]


# --- Recovery scoring (manual section 3) --------------------------------------

def score_recovery(boot_g, gt_edges):
    """gt_edges: list of (src, type, dst, weight) ground truth.
    Returns dict with R, per-family R, precision, flips, substitutions,
    missing, nondense recall (secondary), per-edge detail."""
    boot_set = boot_g.edge_set()
    boot_pairs = defaultdict(list)
    for e in boot_g.edges:
        boot_pairs[(e[0], e[2])].append(e)
    detail = []
    total = 0.0
    flips = subs = missing = 0
    fam_scores = defaultdict(float)
    fam_counts = defaultdict(int)
    nondense_hit = nondense_total = 0
    for (src, typ, dst, w) in gt_edges:
        if typ not in DENSE_TYPES:
            nondense_total += 1
            if (src, typ, dst, w) in boot_set or any(
                    e[1] == typ for e in boot_pairs.get((src, dst), [])):
                nondense_hit += 1
            continue
        fam = DENSE_FAMILY_OF_TYPE[typ]
        fam_counts[fam] += 1
        same_pair = boot_pairs.get((src, dst), [])
        exact = [e for e in same_pair if e[1] == typ]
        if exact:
            bw = exact[0][3]
            if bw == w:
                s = 1.0
            elif abs(bw - w) == 1:
                s = 0.5
            else:
                s = 0.0
            note = "exact" if s == 1.0 else "weight off by %d" % abs(bw - w)
        elif same_pair:
            s, note = 0.0, "substitution (boot has %s)" % same_pair[0][1]
            subs += 1
        elif boot_pairs.get((dst, src)):
            s, note = 0.0, "flip (boot has the reversed pair)"
            flips += 1
        else:
            s, note = 0.0, "missing"
            missing += 1
        fam_scores[fam] += s
        total += s
        detail.append((src, typ, dst, w, s, note))
    n_dense = sum(fam_counts.values())
    boot_dense = [e for e in boot_g.edges if e[1] in DENSE_TYPES]
    gt_dense_set = {(s, t, d) for (s, t, d, w) in gt_edges if t in DENSE_TYPES}
    correct_dense = sum(1 for e in boot_dense if (e[0], e[1], e[2]) in gt_dense_set)
    precision = (correct_dense / len(boot_dense)) if boot_dense else 1.0
    return {
        "R": total / n_dense if n_dense else 0.0,
        "per_family": {f: fam_scores[f] / fam_counts[f] for f in fam_counts},
        "precision": precision,
        "flips": flips,
        "substitutions": subs,
        "missing": missing,
        "nondense_recall": (nondense_hit / nondense_total) if nondense_total else None,
        "detail": detail,
    }


# --- Gap decisions (manual section 4) ------------------------------------------

def find_route(g, src, dst):
    """Replayable route over stored edges only (traversed in either direction,
    each step logged with its true direction and type). None if no stored path."""
    adj = defaultdict(list)
    for (s, t, d, w) in g.edges:
        adj[s].append((d, "%s -%s(%d)-> %s" % (s, t, w, d)))
        adj[d].append((s, "%s -%s(%d)-> %s  [traversed in reverse]" % (s, t, w, d)))
    prev = {src: None}
    queue = deque([src])
    while queue:
        cur = queue.popleft()
        if cur == dst:
            break
        for nxt, step in adj[cur]:
            if nxt not in prev:
                prev[nxt] = (cur, step)
                queue.append(nxt)
    if dst not in prev:
        return None
    steps = []
    cur = dst
    while prev[cur] is not None:
        cur_prev, step = prev[cur]
        steps.append(step)
        cur = cur_prev
    return list(reversed(steps))


def invention_score(decisions):
    """decisions: list of dicts with classification in {R, A, F}."""
    R = sum(1 for d in decisions if d["class"] == "R")
    A = sum(1 for d in decisions if d["class"] == "A")
    F = sum(1 for d in decisions if d["class"] == "F")
    total = R + A + F
    I = None if total == 0 else (R + A - F) / total
    return {"I": I, "R": R, "A": A, "F": F}


# --- Join: candidate introductions (doc 03) -------------------------------------
# Candidates live in the JOIN, never as graph edges (person->person stays empty).
# A candidate exists only where a derivation path over stored edges exists:
#   holder -needs-> ask <-would_fill- filler        (filler = node or its maker)
#   holder -needs-> ask -blocked_by-> blocker <-weakens- work <-made- maker
# Proximity (shared phext geometry) ranks candidates; it never creates one.

def generate_candidates(g):
    candidates = []
    for (holder, typ, ask, nw) in list(g.edges):
        if typ != "needs":
            continue
        blockers = [d for (_, t, d, _) in g.edges_from(ask, "blocked_by")]
        # Direct fill. (would_fill points filler -> ask, so the filler is the
        # edge's source.)
        for (filler, _, _, fw) in g.edges_to(ask, "would_fill"):
            if g.kind(filler) == "person":
                party, via = filler, filler
                path = ["%s -needs(%d)-> %s" % (holder, nw, ask),
                        "%s -would_fill(%d)-> %s" % (filler, fw, ask)]
            else:
                makers = [s for (s, _, _, _) in g.edges_to(filler, "made")]
                party = makers[0] if makers else None
                via = filler
                path = ["%s -needs(%d)-> %s" % (holder, nw, ask),
                        "%s -would_fill(%d)-> %s" % (filler, fw, ask)]
                if party:
                    path.append("%s -made-> %s" % (party, filler))
            candidates.append({
                "holder": holder, "party": party, "ask": ask, "via": via,
                "kind": "would_fill", "strength": fw, "path": path,
                "blockers": list(blockers),
            })
        # Weakener route through a blocker.
        for b in blockers:
            for (wsrc, _, _, ww) in g.edges_to(b, "weakens"):
                makers = [s for (s, _, _, _) in g.edges_to(wsrc, "made")]
                for maker in makers:
                    candidates.append({
                        "holder": holder, "party": maker, "ask": ask, "via": wsrc,
                        "kind": "weakens_blocker", "strength": ww,
                        "path": ["%s -needs(%d)-> %s" % (holder, nw, ask),
                                 "%s -blocked_by-> %s" % (ask, b),
                                 "%s -weakens(%d)-> %s" % (wsrc, ww, b),
                                 "%s -made-> %s" % (maker, wsrc)],
                        "blockers": [x for x in blockers if x != b],
                    })
    return candidates
