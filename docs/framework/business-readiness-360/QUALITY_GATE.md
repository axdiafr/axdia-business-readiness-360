# BR360 V3 Quality Gate — 2026-09-26

A build is acceptable only when all conditions below hold:

- all JSON assets parse;
- >=100 stable/unique control IDs remain;
- golden applicability behavior remains deterministic;
- all 15 AUTOMATED controls have executable built-in detector wiring;
- automated control conditions are specific, not the V2 generic template;
- scoring N/A and real-world gates remain intact;
- fingerprint/compare behavior remains deterministic;
- external adapters remain opt-in with explicit network intent;
- selftest passes;
- unit/regression suite passes.

A project audit itself can still return PARTIAL/FAIL; that is an audit result, not a framework regression.
