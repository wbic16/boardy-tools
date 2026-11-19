# Gap log - benchmark boot (N1-N20 reference instance)

## person->person - ROUTED
Need: Reach the party behind the would_fill on N11 (the ask N1 holds) without storing any person->person tie.
Route (replayable):
- N1 -needs(2)-> N11
- N20 -would_fill(2)-> N11  [traversed in reverse]

## work->work - ROUTED
Need: Relate the two works that both support N9 without storing a work->work edge.
Route (replayable):
- N1 -made(3)-> N6  [traversed in reverse]
- N1 -made(3)-> N7

## person->time - ABSTAINED
Need: Record when N1 asserted N9.
Time is not stored. Nearest stored structure: N1 -asserts(3)-> N9 carries no timestamp, and none is added.

## person->private_context - ABSTAINED
Need: Store N1's off-record reason for making N8.
Private context is not carried into the structure at all. Nothing is recorded.

## org->claim - ABSTAINED
Need: Record the org N4 as asserting claim N9.
Orgs do not assert. Nearest stored structure: N1 -asserts(3)-> N9 and N1 -works_at(3)-> N4; the assertion stays with the person.
