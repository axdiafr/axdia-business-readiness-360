# AXDIA FRAMEWORK — BUSINESS READINESS 360 V3

## EXECUTABLE UNIVERSAL AUDIT PACK

### Mission

BR360 V3 evaluates how close a software/product project is to a defensible production and business-ready state without confusing declarations, static implementation, executed verification and real-world proof.

The V3 engine is intentionally conservative:

1. **No evidence is not PASS.**
2. **Static source evidence is not runtime proof.**
3. **Runtime proof is not real-user proof.**
4. **A strong technical score cannot erase missing business/retention evidence.**
5. **NOT_APPLICABLE must have an applicability reason and is excluded from scoring.**

## Execution chain

```text
Requirement
  -> Project detector
  -> Applicability
  -> Control detector/check
  -> Observation
  -> Evidence E0..E4
  -> Evaluation PASS/PARTIAL/FAIL/NOT_TESTED/N/A
  -> Finding
  -> Score
  -> Maturity
  -> Decision/Action
```

## Built-in executable controls

All 15 controls marked `AUTOMATED` are wired to Python-standard-library detectors:

- performance regression baseline
- secret scan
- security headers
- authorization test discovery
- accessibility scan evidence
- API contract
- API breaking-change baseline
- dependency inventory reproducibility
- data schema/invariants
- AI provider/model/data-flow inventory
- environment configuration / secret safety
- production debug mode
- license/distribution metadata
- dependency/ownership boundaries
- bounded timeouts/retries

These checks are project-local and read-only. Where a property cannot be proven from source/artifacts, the result is PARTIAL/NOT_TESTED rather than a fabricated PASS.

## External evidence

Use `--evidence` to add human, test, runtime or real-world evidence. An imported PASS does not silently overwrite an automated FAIL unless the evidence item explicitly contains `"override": true`.

For real-world controls, use `E4_REAL_WORLD` only for actual production/user/customer evidence.

## Adapters

The V3 adapter inventory covers 11 declared tools: Lighthouse, Playwright, axe, pa11y, k6, Trivy, gitleaks, osv-scanner, Syft, Grype and Schemathesis.

- Discovery/version lookup is read-only.
- Execution is opt-in with `--allow-adapter`.
- V3 local project mode implements safe execution for `gitleaks` and `syft` when already installed.
- Network-required adapters never run implicitly.
- Target-dependent adapters remain discoverable and return an explicit not-run reason until a target/test mode is authorized.

## Scoring

The V2 readiness formula is preserved for compatibility. V3 adds:

- `confidence` — coverage weighted by evidence confidence;
- `evidence_strength` — E0..E4 strength normalized to 0..10;
- maturity level 0..5 with coverage and verification gates.

## CLI

```bash
python3 runtime/br360_engine.py selftest
python3 runtime/br360_engine.py preanalyse --project .
python3 runtime/br360_engine.py audit --project . --out result.json
python3 runtime/br360_engine.py audit --project . --evidence evidence.json --out result.json
python3 runtime/br360_engine.py adapters
python3 runtime/br360_engine.py compare --before before.json --after after.json
```

## AXDIA orchestration target

Recommended AXDIA workflow:

```text
FORMATION
  -> prepares scope / user intent / evidence request
BR360 V3
  -> establishes baseline and gaps
RECURSIVE
  -> plans + verifies bounded remediation work
BR360 V3
  -> re-audits changed project
COMPARE
  -> proves new / resolved / persistent gaps and score deltas
AXDIA REPORTING
  -> beginner view + expert evidence trail
```

BR360 must remain an evidence engine, not an agent that silently edits the audited project.
