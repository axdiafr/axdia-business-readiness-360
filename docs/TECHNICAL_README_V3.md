# AXDIA Business Readiness 360 V3

**Version:** `3.0.0`  
**Result schema:** `BR360-3`  
**Runtime:** Python standard library only  
**Default mode:** `READ_ONLY`, local-first, network disabled unless an external adapter is explicitly authorized.

BR360 V3 turns the V2 decision framework into an executable audit engine. It keeps the 125 controls / 24 domains / 20 profiles and adds deterministic project-local execution for every control marked `AUTOMATED`.

## What changed in V3

- 15/15 `AUTOMATED` controls now have executable built-in detectors.
- Built-in detectors are conservative: missing evidence never becomes a PASS.
- Control-specific PASS / PARTIAL / FAIL conditions replace the generic V2 template for automated controls.
- Full audit output now contains `evaluations`, normalized `evidence`, `findings`, prioritized `actions`, `blockers`, scores, confidence, evidence strength and maturity.
- Manual, runtime and real-world evidence can be imported without weakening automated failures.
- Maturity 0..5 is computed separately from readiness and gated by coverage / verification / real-world evidence.
- All 11 external adapters are discovered; supported local read-only adapters can be explicitly opted into. Network-required adapters are never auto-run.
- CLI comparison is now exposed for audit N -> audit N+1 regression tracking.
- V2 public helpers remain available: `detect_project`, `select_controls`, `score`, `fingerprint`, `compare`.
- A compatibility snapshot of the V2 runtime/schema/manifest is kept in `legacy/BR360_V2/`.

## Quick start

```bash
python3 runtime/br360_engine.py selftest
python3 runtime/br360_engine.py audit --project /path/to/project --out br360-result.json
python3 runtime/br360_engine.py adapters
```

Add human/runtime/real-world evidence:

```bash
python3 runtime/br360_engine.py audit \
  --project /path/to/project \
  --evidence examples/evidence-input.example.json \
  --out br360-result-with-evidence.json
```

Compare two audits:

```bash
python3 runtime/br360_engine.py compare \
  --before audit-before.json \
  --after audit-after.json \
  --out audit-delta.json
```

The old V2 CLI form remains a pre-analysis mode:

```bash
python3 runtime/br360_engine.py --project /path/to/project --profile AUTO
```

## Safety model

BR360 does not install dependencies, change project files, commit, push or deploy. Built-in detectors only inspect the supplied project tree. External adapters are opt-in. Network-required adapters return an authorization requirement instead of executing in local-safe mode.

## Important interpretation rule

`PASS` means the evidence required by that specific control and detector was found. It does **not** mean the whole project is production-ready. Semi-automated, manual, runtime, legal and real-world controls remain `NOT_TESTED` until suitable evidence is supplied.
