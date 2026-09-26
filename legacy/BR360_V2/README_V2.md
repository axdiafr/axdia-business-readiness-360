# AXDIA Business Readiness 360 V2

This package upgrades BR360 1.0.0 into a structured, local-first audit engine while retaining the original V1 under `legacy/BR360_V1`.

- Corpus analyzed: **54 repositories / 54 successful / 0 failed**.
- Machine-readable controls: **125** across **24 domains**.
- Audit profiles: **20**.
- Optional adapters: **11**.
- New mandatory external dependencies: **0**.
- Third-party code copied from research corpus: **0**.

Run local pack tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Run a read-only project pre-analysis:

```bash
python3 runtime/br360_engine.py --project /path/to/project --profile AUTO --out br360-preanalysis.json
```
