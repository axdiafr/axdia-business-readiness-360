# BR360 GitHub Research Final

## Executive Summary

The 2026-09-26 corpus contains **54/54 successful repositories and 0 failed downloads**. Research was static-first; no repository script, install, binary or test suite was executed. Exact commit and license-file paths come from the corpus manifest.

The main conclusion is architectural: BR360 V1 already had unusually broad audit coverage, but most intelligence lived in one large prose pack. V2 therefore preserves that content and adds a control/evidence/applicability runtime around it rather than replacing it with scanner integrations.

## Corpus Inventory
See `BR360_GITHUB_CORPUS_INVENTORY.md`.

## License Matrix
See `BR360_LICENSE_MATRIX.md`. Restrictive or mixed-license references remain inspiration/review sources, not code sources.

## Repository Value Matrix
See `BR360_REPOSITORY_VALUE_MATRIX.md`.

## Concepts Extracted
- stable control IDs and test categories;
- normalized finding schema with severity, confidence, location, fingerprint and suppression;
- SBOM/provenance/license inventory;
- performance budgets and regression gates;
- automated vs manual accessibility states;
- API schema/conformance/breaking-change testing;
- subject/resource/relation authorization tests;
- SLI/SLO/error-budget and telemetry evidence;
- activation/funnel/retention/product-event capabilities;
- experiment/feature-release governance;
- survey/feedback lifecycle;
- architecture decision traceability;
- workflow/records/views/permission concepts from reference products only.

## Concepts Rejected
- Wholesale code copying from Twenty/n8n/Grafana/Sentry
- Mandatory embedding of scanners or observability stacks
- Treating scanner count as audit quality
- Using GitHub stars as quality score
- Using lab performance as equivalent to real-user evidence
- Turning legal/compliance uncertainty into PASS

## Audit Gaps Found
- Controls were primarily prose, without stable machine IDs
- Result schema was intentionally minimal and permissive
- No machine-readable project detector registry
- No adapter contract or explicit network intent
- No baseline compare/finding fingerprint contract
- Evidence strength/coverage were not first-class result dimensions
- No golden fixtures or deterministic applicability tests
- No corpus license/value inventory attached to the pack

## Architecture Improvements

V2 adds 125 stable controls, 20 profiles, machine project facts, applicability reasons, optional adapters, evidence graph, four-score model, finding deduplication, baseline comparison, strict schemas and audit-of-the-audit fields.

## Evidence Improvements
Every score can be traced through the evidence graph. Conflicting evidence is represented, not silently resolved.

## Scoring Improvements
Implementation, verification and real-world evidence are independent inputs. Evidence/coverage gates prevent unsupported perfect readiness.

## Adapters
11 adapters are defined as optional `CANDIDATE` contracts. The core has no new mandatory external dependency.

## UX Improvements
`AUTO` is the beginner default; Simple mode can explain selected controls and missing access while Expert mode exposes controls, evidence, adapters and network intent.

## Implementation Decisions
The V1 audit pack is preserved unchanged under `legacy/BR360_V1`; the V2 runtime is additive and local-first.

## Regression Risks
The supplied archive does not include the live AXDIA Framework repository or the current `outils/recursive` / `outils/formation` directories. Therefore integration-level RECURSIVE/AXDIA verification is not claimed by this standalone pack build.
