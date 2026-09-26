# Migrating BR360 V2 consumers to V3

The V2 Python helpers remain available, so existing integrations using `detect_project`, `select_controls`, `score`, `fingerprint` or `compare` can migrate incrementally.

## CLI compatibility

The old form remains a pre-analysis call:

```bash
python3 runtime/br360_engine.py --project . --profile AUTO
```

Use the V3 executable audit explicitly:

```bash
python3 runtime/br360_engine.py audit --project . --out result.json
```

## Result changes

V3 changes `schema` from `BR360-2` to `BR360-3` and `pack_version` from `2.0.0` to `3.0.0`. It adds top-level `evaluations` and `evidence`. Consumers should read findings by `fingerprint`, not array position.

## Recommended integration

Keep V2 parsing available during transition, then switch consumers to:

`project_profile -> applicability -> evaluations -> findings/actions -> scores/maturity -> final`
