# BR360 V3 — RECURSIVE / FORMATION Integration Contract

BR360 V3 is designed as the evidence/readiness boundary between FORMATION and RECURSIVE.

## Recommended orchestration

```text
FORMATION
  -> collect beginner-friendly mission/context/evidence inputs
  -> emit BR360 evidence-input JSON when the user supplies verifiable facts

BR360 V3 audit
  -> project facts
  -> applicability
  -> built-in automated checks
  -> evidence normalization
  -> findings/actions/scores/maturity

RECURSIVE
  -> consume selected BR360 findings/actions as bounded remediation objectives
  -> execute its own verification/quality gates
  -> must not rewrite BR360 evidence history

BR360 V3 re-audit
  -> produce after.json

BR360 compare
  -> new/resolved/persistent fingerprints
  -> score delta
  -> maturity delta
```

## Stable fields for consumers

Use these fields as the primary integration contract:

- `schema`, `pack_version`
- `project_profile.facts`
- `applicability.controls[]`
- `evaluations[]`
- `evidence[]`
- `findings[].fingerprint`
- `actions[]`
- `coverage`
- `scores`
- `maturity`
- `audit_self_evaluation`
- `final`

## Safety boundary

FORMATION may collect claims, but BR360 labels them by evidence level. RECURSIVE may remediate findings, but BR360 independently re-checks the result. No component should silently convert user claims to E2/E3/E4 proof.
