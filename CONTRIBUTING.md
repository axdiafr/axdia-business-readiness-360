# Contributing to Business Readiness 360

BR360 favors explicit evidence and deterministic behavior over optimistic scoring. **Until the project-wide license and inbound contribution policy are finalized, please prefer issues, audit-gap reports and documentation feedback over code pull requests.**

## Useful contributions

- new built-in detectors with reproducible fixtures;
- false-positive / false-negative corrections;
- stronger control pass/partial/fail conditions;
- additional project profiles;
- scoring/maturity edge-case tests;
- adapter metadata and safe read-only integrations;
- clearer documentation and examples.

## Requirements

1. Keep built-in execution read-only unless a future design explicitly introduces another mode.
2. Never turn missing evidence into PASS.
3. Add tests for detector or scoring changes.
4. Do not introduce mandatory network access for the default audit path.
5. Do not add copied third-party code/text without a license review and attribution decision.
6. Run:

```bash
python3 -m unittest discover -s tests -v
python3 runtime/br360_engine.py selftest
```

## Pull request evidence

Describe the control/profile affected, the before/after behavior, the fixture used and any limitation that remains.
