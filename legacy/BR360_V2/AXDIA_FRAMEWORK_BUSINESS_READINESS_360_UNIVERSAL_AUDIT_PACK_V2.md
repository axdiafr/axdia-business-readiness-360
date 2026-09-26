# AXDIA FRAMEWORK — BUSINESS READINESS 360 V2
## Structured audit engine • local-first • evidence-first • adapter-extensible

**Pack ID:** `business-readiness-360`  
**Pack version:** `2.0.0`  
**Result schema:** `BR360-2`  
**Mode:** `READ_ONLY`  
**Mandatory external dependencies:** none

## Purpose

V2 preserves the coverage of the V1 universal audit while moving the operational contract into machine-readable controls, profiles, detectors, evidence, scoring and result schemas. The V1 text is preserved byte-for-byte under `legacy/BR360_V1/` for regression comparison.

## Core execution chain

`project facts → applicability → selected controls → observations → findings → evidence graph → scores → decisions → actions`

No control is silently treated as applicable. No missing evidence becomes PASS. No `NOT_APPLICABLE` becomes zero.

## Four independent scores

- `IMPLEMENTATION_SCORE`: what exists.
- `VERIFICATION_SCORE`: what was actually tested/verified.
- `REAL_WORLD_EVIDENCE_SCORE`: what real users, customers or operations demonstrate.
- `READINESS_SCORE`: combined decision signal subject to evidence gates.

A technically excellent project with no required real-world evidence is capped by the scoring policy and cannot become a business `10/10` by code quality alone.

## Evidence states

`E0_CLAIM_ONLY → E1_STATIC → E2_TESTED → E3_RUNTIME → E4_REAL_WORLD`

Conflicts are represented as `EVIDENCE_CONFLICT`; the engine never chooses silently between contradictory sources.

## Automation levels

`AUTOMATED`, `SEMI_AUTOMATED`, `MANUAL`, `REAL_WORLD_REQUIRED`, `EXTERNAL_RESEARCH`, `LEGAL_REVIEW`.

## Control library

125 controls across 24 domains. IDs are stable and semantic (`BR360-SEC-001`, `BR360-API-001`, etc.) and never depend on row order.

## Adapters

Adapters are optional. `CORE AUDIT` has no new external dependency. Tool commands are `CANDIDATE`, never `AUTHORIZED`, and every network-capable adapter declares its intent.

## Safety

- corpus repositories remain untrusted research input;
- no third-party install/test/script is executed automatically;
- no commit, push or deployment is part of this pack;
- read-only is the default and expected mode;
- code copied from corpus: **false**;
- license matrix is included before any possible reuse decision.

## UX contract for AXDIA

Simple flow: `Audit → Business Readiness 360 → Project → AUTO → Pre-analysis → Detected domains → Run → Progress → Results`.

Simple mode explains what will be checked, what will not be modified, required access and expected outputs. Expert mode exposes profiles, controls, evidence, detectors, standards, command candidates and network intent.

## Current external references checked 2026-09-26

- OWASP ASVS stable line: 5.0.0 (corpus also contains current bleeding-edge commit for research only).
- WCAG 2.2 remains the W3C Recommendation baseline for web accessibility.
- SLSA 1.2 is the current approved specification.
- OpenAPI 3.2.1 is the current patch release listed by the OpenAPI specification site.
- Core Web Vitals reference targets remain LCP ≤2.5 s, INP ≤200 ms and CLS ≤0.1 at the 75th percentile; thresholds must be revalidated before hard-coding future releases.
