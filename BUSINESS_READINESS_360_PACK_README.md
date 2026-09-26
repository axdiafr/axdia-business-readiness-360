# Business Readiness 360 Universal — AXDIA Framework Pack V3

Pack version `3.0.0`, result schema `BR360-3`, read-only and local-first.

V3 is the execution-engine release. V2 defined the evidence/scoring/control architecture; V3 executes the 15 controls explicitly classified `AUTOMATED`, normalizes their evidence, creates findings/actions and supports evidence import for the rest of the 360 audit.

## Core flow

`Detect project -> Apply profile -> Select controls -> Execute built-in detectors -> Import authorized evidence -> Normalize evaluations -> Findings -> Evidence -> Scores -> Maturity -> Actions -> Compare`

## Coverage model

- `AUTOMATED`: V3 executes built-in detectors when the control is applicable.
- `SEMI_AUTOMATED`: V3 does not fabricate success; collect tool/runtime/manual evidence and import it.
- `MANUAL`: explicit review evidence required.
- `REAL_WORLD_REQUIRED`: E4 real-world evidence required to contribute to the real-world score.
- `LEGAL_REVIEW` / `EXTERNAL_RESEARCH`: qualified/external evidence remains explicit.

See `docs/framework/business-readiness-360/QUICKSTART.md` and `AXDIA_FRAMEWORK_BUSINESS_READINESS_360_UNIVERSAL_AUDIT_PACK_V3.md`.
