# Business Readiness 360 Universal — AXDIA Framework Pack

Ce paquet contient :

- `AXDIA_FRAMEWORK_BUSINESS_READINESS_360_UNIVERSAL_AUDIT_PACK.md` : audit universel principal.
- `business-readiness-360.framework.json` : manifeste compatible avec le schéma `FRAMEWORK_PACK` de RECURSIVE V7 observé.
- `BUSINESS_READINESS_360_RESULT.schema.json` : contrat JSON minimal pour les résultats.

Le manifeste RECURSIVE ne contient volontairement pas toute la logique d'audit : les Framework Packs V7 sont data-only et limités à la détection, checks/risques et commandes candidates. La logique complète reste dans l'Audit Pack AXDIA Framework.

Mode par défaut : READ_ONLY.
