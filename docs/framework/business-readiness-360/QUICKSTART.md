# BR360 V3 Quickstart

## 1. Validate the pack

```bash
python3 runtime/br360_engine.py selftest
python3 -m unittest discover -s tests -v
```

## 2. Pre-analyse a project

```bash
python3 runtime/br360_engine.py preanalyse --project /path/to/project --out preanalysis.json
```

This detects project facts and applicability only. It intentionally does not claim PASS.

## 3. Run the executable audit

```bash
python3 runtime/br360_engine.py audit --project /path/to/project --out br360.json
```

The result includes evaluations, normalized evidence, findings, prioritized actions, readiness/confidence/evidence-strength scores and maturity.

## 4. Add evidence BR360 cannot infer locally

Copy `examples/evidence-input.example.json`, replace the examples with genuine evidence, then:

```bash
python3 runtime/br360_engine.py audit --project /path/to/project --evidence my-evidence.json --out br360-with-evidence.json
```

Use E4 only for actual real-world/user/customer evidence.

## 5. Compare before/after

```bash
python3 runtime/br360_engine.py compare --before baseline.json --after after-fixes.json --out delta.json
```

## 6. Optional adapters

```bash
python3 runtime/br360_engine.py adapters
```

Nothing external is run by this command. To opt in to a supported local read-only adapter:

```bash
python3 runtime/br360_engine.py audit --project /path/to/project --allow-adapter gitleaks --allow-adapter syft --out br360.json
```
