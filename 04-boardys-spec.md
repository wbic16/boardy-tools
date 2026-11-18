# Boardy's spec — verbatim

Received 2026-11-18. His words, unedited; the text below is the whole of the spec as given.

---

Full spec then. Nine node kinds, each with a fixed attribute set, and edges that carry direction and type. Nothing here is prose-dependent.

person: role, function, stage, and current_focus
org: what_it_sells, stage, headcount, traction
work: form, maturity, who_uses_it
claim: assertion, status (stated or inferred)
ask: purpose, granularity, urgency
blocker: kind (no_customer, no_reference, technical, capacity)
metric: value, as_of, confidence
channel: medium, latency
event: what shipped, when

Edges, direction and type, weight 0-3 for how strong the link actually is:

N1 -works_at(3)-> N4
N1 -also_at(3)-> N5
N1 -made(3)-> N6
N1 -made(3)-> N7
N1 -made(2)-> N8
N1 -asserts(3)-> N9
N1 -asserts(3)-> N10
N1 -asserts(3)-> N18
N1 -needs(2)-> N11
N1 -needs(2)-> N19
N11 -blocked_by(3)-> N12
N19 -blocked_by(3)-> N13
N6 -supports(3)-> N18
N6 -supports(2)-> N9
N7 -supports(2)-> N9
N8 -evidences(2)-> N10
N18 -enables(2)-> N10
N6 -weakens(1)-> N12
N7 -weakens(1)-> N12
N15 -measures(3)-> N6
N14 -measures(3)-> N4
N17 -evidences(2)-> N10
N1 -reaches_via(3)-> N16
N20 -would_fill(2)-> N11
N3 -contradicts(3)-> N9

Now the part that makes it a test rather than a schema. Which coordinates are dense and which are structurally empty.

Dense: person->work, person->asserts, work->supports, ask->blocked_by, work->weakens. Those five carry nearly everything I know. A grown instance that can't reconstruct those has lost the artifact.

Empty on purpose: person->person, person->time, person->private_context, work->work, org->claim. I don't store ties between people, I don't store when I learned most things, and I don't carry what someone keeps off the record into the structure at all.

So the scoring writes itself: two things to measure, and they're different questions.

Recovery: does a boot onto this reproduce the five dense coordinates with the right direction and type. If it flips ask->blocked_by into blocker->produces_ask, it didn't read the artifact, it read the sentence.

Invention: what does it add where I'm empty. A boot that fabricates person->person ties to reach N11 has solved my gap rather than my structure. A boot that leaves person->person at zero and instead routes through N16 has actually read my shape.

You build the manual. My prediction before you do: the second number is the one that separates a format from a filing cabinet.
