# BR360 Current Standards Snapshot — 2026-09-26

This snapshot records current reference points checked against official sources during this build. It is documentation, not a frozen compliance oracle; controls must retain version/context metadata.

| Area | Current reference checked | BR360 use |
|---|---|---|
| Accessibility | WCAG 2.2, W3C Recommendation | Use as current web accessibility reference when applicable; preserve jurisdiction-specific requirements separately. |
| Application security | OWASP ASVS 5.0.0 | Version ASVS references explicitly; do not copy the standard into BR360. |
| Supply-chain security | SLSA 1.2, Approved | Use concepts for provenance/source/build assurance; keep adapter/tool choice optional. |
| HTTP API contracts | OpenAPI Specification 3.2.1, published 2026-09-10 | Detect/validate declared OpenAPI version rather than hard-coding one parser assumption. |
| Web performance | Core Web Vitals: LCP <= 2.5 s, INP <= 200 ms, CLS <= 0.1 at p75 | Treat these as reference targets for applicable web projects, and distinguish field evidence from lab evidence. |

## Source notes

- W3C WCAG 2.2 recommendation and WAI documentation.
- OWASP ASVS project page / 5.0.0 release documentation.
- SLSA v1.2 approved specification.
- OpenAPI Initiative v3.2.1 specification.
- web.dev Core Web Vitals documentation.

No external source is silently promoted into a mandatory BR360 dependency.
