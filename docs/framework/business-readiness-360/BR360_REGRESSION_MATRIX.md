# BR360 V2 -> V3 Regression Matrix

| Capability | V2 | V3 |
|---|---|---|
| 125 stable controls / 24 domains | yes | preserved |
| 20 project profiles | yes | preserved |
| Applicability golden fixtures | yes | preserved |
| Automated controls | declared | 15/15 executable built-in detectors |
| Control-specific conditions | mostly generic | 125/125 specific conditions |
| Result execution | pre-analysis only | full evaluations/evidence/findings/actions |
| Evidence import | schema only | executable E0..E4 import path |
| Readiness scoring | yes | preserved |
| Confidence/evidence strength | schema dimension | computed |
| Maturity 0..5 | model only | computed with gates |
| Fingerprints/compare | helper | helper + CLI + maturity delta |
| External adapters | 11 candidates | 11 discovered; opt-in execution layer |
| Network safety | explicit intent | preserved; no implicit network execution |
| V2 compatibility | n/a | helper API + V2 snapshot |

V1 remains under `legacy/BR360_V1`. A V2 compatibility snapshot is under `legacy/BR360_V2`.
