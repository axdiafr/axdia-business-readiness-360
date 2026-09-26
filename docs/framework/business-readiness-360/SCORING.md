# BR360 V3 Scoring

BR360 keeps separate dimensions for implementation, verification, real-world evidence and readiness. `NOT_APPLICABLE` is excluded from scoring. `NOT_TESTED` never counts as PASS and reduces coverage.

## Core readiness

- `implementation`: PASS=1, PARTIAL=0.5, FAIL=0 over all applicable controls.
- `verification`: share of applicable controls backed by E2/E3/E4 evidence.
- `real_world_evidence`: share of applicable `REAL_WORLD_REQUIRED` controls backed by E4 and at least PARTIAL.
- `readiness`: weighted aggregate with the V2 gates preserved.

When real-world controls apply:

`0.45 * implementation + 0.30 * verification + 0.25 * real_world_evidence`

When no real-world control applies, implementation/verification weights are renormalized to 0.60/0.40.

## Readiness caps

- real-world controls apply but E4 score is 0 -> readiness capped at 6.5;
- verification < 5 -> readiness capped at 7.5;
- evaluated coverage < 70% -> readiness capped at 8.0.

## V3 additional dimensions

- `confidence`: coverage weighted by confidence of collected evidence;
- `evidence_strength`: average E0..E4 strength normalized to 0..10;
- `maturity`: separate 0..5 level constrained by readiness, verification, coverage and real-world evidence.

A high implementation score cannot compensate for missing runtime or real-world proof.
