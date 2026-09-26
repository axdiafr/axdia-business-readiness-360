# AXDIA FRAMEWORK — BUSINESS READINESS 360 UNIVERSAL
## UNIVERSAL AUDIT PACK • PRODUCT × BUSINESS × UX × SECURITY × OPERATIONS × COMPLIANCE × GROWTH × RESILIENCE

**Pack ID:** `business-readiness-360`  
**Pack version:** `1.0.0`  
**Audit schema:** `BR360-1`  
**Mode:** `READ_ONLY`  
**Compatibility target:** AXDIA Framework + RECURSIVE V7 evidence/verification model  
**Scope:** tout projet logiciel, numérique ou hybride, commercial ou interne.

---

# 0. BUT DU PACK

Ce pack transforme **Business Readiness 360** en audit générique réutilisable.

Il doit fonctionner sur des projets très différents :

```text
SaaS web
application web
application mobile
application desktop
PWA
API / backend
CLI
outil développeur
SDK / bibliothèque
produit IA
agent / système multi-agent
plateforme d’automatisation
CRM / ERP / business OS
e-commerce
marketplace
site de contenu
service numérique
open source
outil interne
produit hybride
```

L’audit ne doit PAS supposer :

```text
Stripe
Supabase
Vercel
Railway
React
Node
Python
abonnement
multi-tenant
IA
site public
paiement
```

Il doit d’abord détecter ce qui existe réellement.

---

# 1. PHILOSOPHIE

L’objectif n’est pas :

```text
ajouter plus de fonctions
produire une note flatteuse
valider une roadmap
confirmer le discours du créateur
```

L’objectif est :

```text
déterminer ce qui est réellement construit,
ce qui fonctionne,
ce qui apporte de la valeur,
ce qui peut être vendu ou adopté,
ce qui peut être opéré de manière fiable,
ce qui peut grandir,
et quelles preuves manquent encore.
```

Règle centrale :

```text
EVIDENCE > DOCUMENTATION > CLAIM
```

Une grande quantité de code ne signifie pas :

```text
product-market fit
maturité
production readiness
rentabilité
simplicité
sécurité
rétention
```

---

# 2. MODE D’EXÉCUTION

## READ-ONLY PAR DÉFAUT

L’audit ne doit modifier aucun fichier applicatif.

Autorisations :

```text
READ
SEARCH
INSPECT
MEASURE
RUN_EXISTING_NON_DESTRUCTIVE_TESTS
BUILD_IF_NON_DESTRUCTIVE
STATIC_ANALYSIS
LOCAL_BROWSER_QA
PUBLIC_WEB_RESEARCH
TEMPORARY_READ_ONLY_CLONE
CREATE_AUDIT_REPORTS
```

Interdictions par défaut :

```text
APPLICATION_CODE_WRITE
DATABASE_WRITE
REMOTE_MIGRATION
PRODUCTION_DEPLOY
DNS_CHANGE
SECRET_CHANGE
DEPENDENCY_INSTALL_IN_TARGET
PAID_API_ACTION
REAL_CUSTOMER_CONTACT
REAL_MARKETING_SEND
BILLING_ACTION
GIT_COMMIT
GIT_PUSH
DESTRUCTIVE_COMMAND
```

Toute action dépassant le mode lecture doit devenir :

```text
HUMAN_GATE_REQUIRED
```

---

# 3. COMPATIBILITÉ RECURSIVE V7

Si RECURSIVE est présent, utiliser sa logique de preuve et ses outils non destructifs.

Détecter le CLI réel.

Exemples :

```text
recursive
recursive.py
outils/RECURSIVE/recursive.py
tools/recursive.py
```

Utiliser si disponibles :

```text
doctor
capabilities
inspect
audit
plan
compare
contracts
data-check
security-full
full-scan
verify
report
selftest
license inventory
SBOM
secret scan
web-check
supabase-check
performance/observability checks
```

IMPORTANT :

un Framework Pack RECURSIVE est **data-only**.

Il sert à :

```text
détection
checks candidats
risques
commandes candidates
```

Il ne donne jamais une autorisation d’exécution.

L’audit Business Readiness 360 reste un **Audit Pack AXDIA Framework** plus riche.

---

# 4. PHASE 1 — CLASSIFIER LE PROJET AVANT DE L’AUDITER

Créer :

```text
PROJECT_PROFILE
```

Ne jamais auditer tous les projets avec les mêmes critères obligatoires.

## 4.1 Type principal

Choisir un ou plusieurs :

```text
SAAS_WEB
WEB_APP
STATIC_SITE
MOBILE_APP
DESKTOP_APP
PWA
API_BACKEND
CLI_TOOL
SDK_LIBRARY
AI_PRODUCT
AI_AGENT_PLATFORM
AUTOMATION_PLATFORM
CRM_ERP_BUSINESS_OS
ECOMMERCE
MARKETPLACE
CONTENT_PLATFORM
OPEN_SOURCE_PROJECT
INTERNAL_TOOL
SERVICE_BUSINESS
HYBRID
OTHER
```

## 4.2 Modèle de distribution

```text
CLOUD_HOSTED
SELF_HOSTED
LOCAL_FIRST
OFFLINE
MOBILE_STORE
DESKTOP_DISTRIBUTION
PACKAGE_REGISTRY
SOURCE_DISTRIBUTION
API_ONLY
HYBRID
```

## 4.3 Modèle business

```text
SUBSCRIPTION
USAGE_BASED
ONE_TIME_LICENSE
FREEMIUM
OPEN_CORE
SERVICES
MARKETPLACE_COMMISSION
ECOMMERCE_MARGIN
AD_SUPPORTED
SPONSORSHIP
INTERNAL_VALUE
OPEN_SOURCE_NON_COMMERCIAL
UNKNOWN
```

## 4.4 Cible

```text
B2B
B2C
B2B2C
DEVELOPER
ENTERPRISE
SMB
PUBLIC_SECTOR
INTERNAL_EMPLOYEES
COMMUNITY
MIXED
UNKNOWN
```

## 4.5 Architecture

Détecter au minimum :

```text
frontend
backend
database
auth
billing
email
storage
queues
workers
AI providers
third-party APIs
mobile wrapper
desktop shell
browser extension
webhooks
CI/CD
hosting
observability
analytics
```

---

# 5. APPLICABILITY ENGINE

Pour chaque domaine d’audit, produire :

```text
REQUIRED
RECOMMENDED
OPTIONAL
NOT_APPLICABLE
UNKNOWN
```

Exemples :

```text
Pricing
→ REQUIRED pour produit commercial
→ NOT_APPLICABLE pour outil interne sans refacturation

Multi-tenant
→ REQUIRED pour SaaS multi-organisation
→ NOT_APPLICABLE pour CLI mono-utilisateur

App-store readiness
→ REQUIRED pour app distribuée en store
→ NOT_APPLICABLE pour API backend

SEO
→ REQUIRED si acquisition organique publique importante
→ OPTIONAL pour console interne

Accessibility
→ REQUIRED pour interfaces humaines
→ NOT_APPLICABLE à une bibliothèque sans UI
```

Ne jamais pénaliser une dimension réellement :

```text
NOT_APPLICABLE
```

---

# 6. MODÈLE DE PREUVE UNIVERSEL

Pour chaque constat :

```text
DOCUMENTED
CODE_PRESENT
CONNECTED
CONFIGURED
TESTED_HISTORICALLY
TESTED_NOW
USER_VISIBLE
USABLE
REAL_WORLD_PROVEN
PRODUCTION_READY
UNKNOWN
```

Ajouter :

```text
confidence = 0–100
```

et une ou plusieurs preuves :

```text
FILE
LINE/RANGE
ROUTE
COMPONENT
TEST
BUILD
LOG
SCREEN
DATABASE_POLICY
CONFIG
PUBLIC_URL
OFFICIAL_EXTERNAL_SOURCE
USER_EVIDENCE
BUSINESS_METRIC
```

Interdit :

```text
mock → REAL_WORLD_PROVEN
fixture → PRODUCTION_READY
README → TESTED_NOW
marketing copy → IMPLEMENTED
```

---

# 7. NORMALISATION DES STATUTS

Utiliser :

```text
PASS
PASS_WITH_WARNINGS
PARTIAL
FAIL
BLOCKED_EXTERNAL
NOT_TESTED
NOT_AVAILABLE
NOT_APPLICABLE
UNKNOWN
```

Jamais :

```text
PASS
```

sans preuve correspondant au niveau de claim.

---

# 8. SCORE MODEL

Notes :

```text
0–2 = absent / cassé
3–4 = prototype faible
5 = utilisable mais insuffisant
6 = MVP crédible
7 = bon niveau pré-commercial
8 = solide
9 = très fort et largement démontré
10 = exceptionnel et fortement prouvé
```

Chaque note doit inclure :

```text
score
confidence
why_this_score
why_not_plus_one
why_not_minus_one
evidence
```

## 8.1 N/A

Une dimension `NOT_APPLICABLE` est exclue du calcul.

Ne jamais convertir `N/A` en zéro.

## 8.2 Absence de preuve

Une absence de données réelles peut limiter la note même si le code est excellent.

Exemple :

```text
retention code = strong
retention evidence = none
→ retention score cannot be treated as proven 9/10
```

---

# 9. PROFILS DE PONDÉRATION

L’audit doit adapter les poids au type de projet.

## SaaS / produit commercial

Priorité forte :

```text
production
security
UX
conversion
retention
pricing
analytics
unit economics
support
scalability
```

## Open source / SDK

Priorité forte :

```text
API quality
documentation
developer experience
compatibility
security
maintenance
community
release discipline
license
adoption
```

## Outil interne

Priorité forte :

```text
business value
adoption
workflow efficiency
reliability
security
integration
support burden
maintainability
```

## Mobile/Desktop

Priorité forte :

```text
device compatibility
distribution
updates
offline
crash resilience
privacy
performance
accessibility
```

## AI product

Priorité forte :

```text
evaluation
hallucination/failure modes
cost
latency
privacy
provider resilience
human oversight
model governance
prompt/tool security
```

---

# 10. AUDIT 360 — DOMAINES COMMUNS

Les sections suivantes constituent le noyau universel.

Chaque section est évaluée uniquement si applicable.

---

# 11. PRODUCT MAP

Reconstruire le produit réel :

```text
modules
features
routes
entry points
services
APIs
jobs
data stores
external dependencies
roles
plans
```

Pour chaque feature :

```text
name
purpose
target user
status
value
dependencies
evidence
```

Statuts feature :

```text
IMPLEMENTED
PARTIAL
MOCK
DOCUMENTATION_ONLY
LEGACY
BROKEN
UNKNOWN
```

---

# 12. PROBLÈME / POSITIONNEMENT

Répondre :

```text
Pour qui ?
Quel problème ?
Quel résultat ?
Pourquoi ce produit ?
Pourquoi maintenant ?
Quelle alternative remplace-t-il ?
```

Pour produit interne :

```text
Quel processus améliore-t-il ?
Quel coût/temps/risque réduit-il ?
```

Score :

```text
POSITIONING_CLARITY
```

---

# 13. VALUE PROPOSITION

Pour chaque promesse :

```text
claim
target
pain
outcome
proof
quantitative proof
credibility
```

Classer :

```text
PROVEN
SUPPORTED
PLAUSIBLE
UNPROVEN
OVERCLAIM
```

Score :

```text
VALUE_PROPOSITION
```

---

# 14. TARGET USERS / SEGMENTS

Identifier les segments réellement supportés.

Pour chaque :

```text
pain
job
fit
time_to_value
support_burden
willingness_to_pay_or_adopt
retention_potential
```

Ne pas multiplier les personas sans preuve.

---

# 15. JOBS TO BE DONE

Format :

```text
Quand...
Je veux...
Afin de...
```

Puis vérifier :

```text
CAN_COMPLETE
PARTIAL
MANUAL
CANNOT_COMPLETE
UNKNOWN
```

---

# 16. PRODUCT SIMPLICITY

Mesurer :

```text
number_of_primary_sections
number_of_visible_concepts
technical_jargon
duplicate_features
dead_ends
configuration_before_value
```

Classer chaque surface :

```text
KEEP_VISIBLE
SIMPLIFY
MERGE
HIDE_ADVANCED
DEPRECATE
REMOVE_CANDIDATE
```

Score :

```text
PRODUCT_SIMPLICITY
```

---

# 17. ONBOARDING

Cartographier :

```text
first_open
signup_or_install
setup
configuration
first_action
first_result
saved_value
return_path
```

Mesurer :

```text
TTFMA = Time To First Meaningful Action
TTFR = Time To First Result
TTFSV = Time To First Saved Value
```

Si inconnu :

```text
NOT_MEASURED
```

Score :

```text
ONBOARDING
```

---

# 18. TIME TO VALUE

Définir la première vraie valeur selon le projet.

Exemples :

```text
SaaS → premier résultat exploitable
SDK → premier appel API réussi
CLI → première tâche terminée
outil interne → premier workflow terminé plus vite
AI → première réponse/action acceptable
automation → premier workflow exécuté avec succès
```

Score :

```text
TIME_TO_VALUE
```

---

# 19. UX / DEVELOPER EXPERIENCE

Selon projet :

```text
end-user UX
admin UX
developer experience
CLI ergonomics
API ergonomics
SDK ergonomics
configuration ergonomics
```

Examiner :

```text
terminology
navigation
defaults
errors
feedback
empty states
examples
discoverability
help
```

Score :

```text
UX_OR_DX
```

---

# 20. ACCESSIBILITY

Si UI humaine :

référence de base :

```text
WCAG 2.2
```

Tester selon environnement :

```text
keyboard
focus
labels
aria
contrast
zoom
reflow
touch targets
motion
form errors
screen reader
```

Séparer :

```text
AUTOMATED
MANUAL
NOT_TESTED
```

Score :

```text
ACCESSIBILITY
```

---

# 21. PERFORMANCE

Selon type :

## Web

```text
LCP
INP
CLS
TTFB
bundle
JS errors
cache
image/font weight
API latency
```

Pour les Core Web Vitals, revalider les seuils officiels au moment de l’audit.

## API

```text
p50
p95
p99
throughput
error rate
cold start
```

## CLI/Desktop/Mobile

```text
startup
memory
CPU
battery
package size
crash rate
```

Score :

```text
PERFORMANCE
```

---

# 22. CROSS-PLATFORM / COMPATIBILITY

Selon applicable :

```text
Chrome
Safari
Firefox
Edge
iOS
Android
Windows
macOS
Linux
Node versions
Python versions
API versions
SDK versions
```

Score :

```text
COMPATIBILITY
```

---

# 23. RELIABILITY

Auditer :

```text
error handling
timeouts
retry
idempotency
cancellation
backpressure
graceful degradation
dependency outage
data corruption
recovery
```

Score :

```text
RELIABILITY
```

---

# 24. SECURITY

Utiliser une approche adaptée au projet.

Pour application web/API, considérer les contrôles OWASP pertinents et, si utile, ASVS.

Examiner :

```text
auth
authorization
tenant isolation
secret storage
input validation
XSS
CSRF
SSRF
injection
CORS
CSP
rate limiting
uploads
webhooks
admin endpoints
logging
egress
dependency security
supply chain
```

Score :

```text
SECURITY_READINESS
```

---

# 25. SECURE DEVELOPMENT / SUPPLY CHAIN

Auditer :

```text
dependency pinning
lockfiles
SBOM
licenses
provenance
CI checks
secret scan
release integrity
vulnerability process
dependency update process
```

Utiliser un référentiel type NIST SSDF lorsqu’il est pertinent.

Ne pas supposer qu’une version draft est une obligation.

Score :

```text
SOFTWARE_SUPPLY_CHAIN
```

---

# 26. PRIVACY / DATA PROTECTION

Selon juridiction et données :

```text
data inventory
purpose
minimization
consent
retention
access
export
delete
processors
subprocessors
international transfer
sensitive data
tracking
```

Ne pas donner un avis juridique définitif.

Classer :

```text
SUPPORTED
PARTIAL
MISSING
LEGAL_REVIEW_REQUIRED
NOT_APPLICABLE
```

Score :

```text
PRIVACY_READINESS
```

---

# 27. AI-SPECIFIC AUDIT

Activer si :

```text
AI_PRODUCT
LLM
agent
classification
generation
AI automation
AI decision support
```

Auditer :

```text
model/provider inventory
prompt injection
tool permissions
egress
hallucination handling
evals
golden datasets
confidence
human oversight
fallback
provider outage
cost
latency
PII handling
model change regression
AI disclosure
```

Créer :

```text
AI_RISK_MATRIX
AI_EVAL_COVERAGE
AI_PROVIDER_DEPENDENCY
```

Score :

```text
AI_READINESS
```

Sinon :

```text
NOT_APPLICABLE
```

---

# 28. DATA ARCHITECTURE / GOVERNANCE

Auditer :

```text
source of truth
data ownership
provenance
lineage
duplicate data
merge
conflicts
schema evolution
history
retention
deletion
orphan data
export
```

Score :

```text
DATA_GOVERNANCE
```

---

# 29. MULTI-TENANT / PERMISSIONS

Activer si multi-user/workspace/org.

Créer matrice :

```text
Resource | Role | Read | Create | Update | Delete | Export | Admin
```

Tester :

```text
direct routes
API
search
deep links
exports
background jobs
shared files
```

Score :

```text
TENANT_ISOLATION
```

Sinon :

```text
NOT_APPLICABLE
```

---

# 30. AUTH / IDENTITY

Si applicable :

```text
signup
login
logout
password reset
email verification
MFA
session expiration
revocation
account deletion
SSO
role provisioning
```

Score :

```text
IDENTITY_READINESS
```

---

# 31. PRODUCTION READINESS

Auditer :

```text
build
runtime config
hosting
database
migrations
health
readiness
logging
monitoring
email
storage
backup
support
deployment
rollback
```

Distinguer :

```text
LOCAL
TEST
STAGING
PRODUCTION
```

Score :

```text
PRODUCTION_READINESS
```

---

# 32. SRE / OPERATIONS

Auditer :

```text
SLI
SLO
SLA
health endpoints
alerts
5xx
latency
queue depth
worker health
provider health
incident process
postmortem
on-call/ownership
runbooks
```

Score :

```text
OPERATIONS_READINESS
```

---

# 33. BACKUP / DISASTER RECOVERY

Examiner :

```text
backup
restore
restore test
RPO
RTO
file recovery
database recovery
provider outage
region outage
accidental deletion
```

Un backup non restauré ne prouve pas la restauration.

Score :

```text
DISASTER_RECOVERY
```

---

# 34. OBSERVABILITY

Examiner :

```text
logs
metrics
traces
error aggregation
audit logs
business telemetry
correlation IDs
privacy-safe logging
```

Score :

```text
OBSERVABILITY
```

---

# 35. ABUSE / FRAUD / COST EXPOSURE

Auditer selon projet :

```text
account spam
credential abuse
API abuse
scraping
AI credit abuse
upload abuse
automation loops
webhook abuse
referral fraud
marketplace fraud
payment abuse
resource exhaustion
```

Score :

```text
ABUSE_RESILIENCE
```

---

# 36. THIRD-PARTY / VENDOR RISK

Pour chaque dépendance critique :

```text
name
purpose
criticality
replaceability
switching_cost
pricing_risk
API_risk
data_lock_in
outage_fallback
```

Score :

```text
VENDOR_RISK
```

---

# 37. PORTABILITY / LOCK-IN

Auditer :

```text
data export
config export
project export
provider switch
hosting switch
identity migration
automation export
model/provider switch
self-host possibility if relevant
```

Score :

```text
PORTABILITY
```

---

# 38. MAINTAINABILITY

Pour chaque composant majeur :

```text
complexity
dependencies
test burden
external APIs
legacy code
duplication
ownership
documentation
breakage frequency
```

Créer :

```text
MAINTENANCE_COST_MATRIX
```

Score :

```text
MAINTAINABILITY
```

---

# 39. TECHNICAL SCALABILITY

Évaluer :

```text
10 users/projects
100
1000
10000 if relevant
```

Examiner :

```text
concurrency
database
queues
storage
rate limits
provider limits
background jobs
large files
large reports
caching
```

Score :

```text
TECHNICAL_SCALABILITY
```

---

# 40. OPERATIONAL SCALABILITY

Mesurer ce qui reste humain :

```text
onboarding
support
configuration
deployment
review
billing
incident
content
data cleanup
customer success
```

Créer :

```text
PROCESS | AUTO | SEMI_MANUAL | MANUAL | COST/TIME
```

Score :

```text
OPERATIONAL_SCALABILITY
```

---

# 41. DOCUMENTATION

Selon projet :

```text
end-user docs
admin docs
developer docs
API docs
deployment docs
troubleshooting
examples
migration guides
release notes
```

Score :

```text
DOCUMENTATION
```

---

# 42. SUPPORT / RECOVERY UX

Examiner :

```text
support entry point
FAQ
knowledge base
error recovery
ticketing
status
self-service
diagnostics
```

Score :

```text
SUPPORT_READINESS
```

---

# 43. RELEASE / UPDATE DISCIPLINE

Selon distribution :

```text
versioning
changelog
migration
rollback
release notes
staging
canary
auto-update
store release
package publishing
compatibility policy
```

Score :

```text
RELEASE_READINESS
```

---

# 44. LICENSE / IP

Auditer :

```text
dependencies
source licenses
copied code
assets
fonts
icons
datasets
models
workflow templates
commercial SDKs
AGPL/GPL/LGPL
third-party notices
```

Créer :

```text
LICENSE_RISK_MATRIX
```

Score :

```text
LICENSE_READINESS
```

---

# 45. BUSINESS MODEL

Activer pour projet commercial.

Identifier :

```text
who_pays
why_pay
what_is_metered
recurring_or_one_time
upsell
expansion
services
cost_to_serve
```

Score :

```text
BUSINESS_MODEL_READINESS
```

Pour projet non commercial :

```text
NOT_APPLICABLE
```

et utiliser `VALUE_MODEL_READINESS`.

---

# 46. OFFER ARCHITECTURE

Si offres/plans :

créer :

```text
Offer | Target | Problem | Features | Price | Limits | Upgrade | Status
```

Détecter :

```text
overlap
cannibalization
confusion
feature mismatch
```

Score :

```text
OFFER_ARCHITECTURE
```

---

# 47. PRICING

Si monétisé :

auditer :

```text
price source of truth
monthly
annual
trial
free
usage
seats
credits
support
enterprise
discounts
```

Classer :

```text
TOO_LOW_RISK
TOO_HIGH_RISK
UNCLEAR
UNTESTED
COHERENT
```

Score :

```text
PRICING_READINESS
```

---

# 48. FREEMIUM / TRIAL

Si présent :

```text
free value
activation
cost exposure
upgrade trigger
cannibalization
abuse
limits
conversion path
```

Score :

```text
FREEMIUM_OR_TRIAL_READINESS
```

---

# 49. BILLING

Si paiement intégré :

```text
checkout
subscription
invoice
tax
failure
retry
portal
upgrade
downgrade
cancel
refund
webhooks
idempotency
```

Distinguer :

```text
TEST
SANDBOX
LIVE
```

Score :

```text
BILLING_READINESS
```

---

# 50. CONVERSION

Si acquisition publique :

cartographier :

```text
Visit
→ Understand
→ Explore
→ Trust
→ Signup/Install
→ Activate
→ Upgrade/Buy
→ Retain
```

Pour chaque étape :

```text
friction
CTA
proof
drop-off risk
measurement
```

Score :

```text
CONVERSION_READINESS
```

---

# 51. ACQUISITION

Identifier les canaux adaptés :

```text
SEO
content
community
GitHub
app stores
marketplaces
outbound
partners
referrals
paid ads
sales
events
integrations
```

Classer :

```text
READY
TESTABLE
EARLY
UNPROVEN
NOT_APPLICABLE
```

Score :

```text
ACQUISITION_READINESS
```

---

# 52. SEO / DISCOVERABILITY

Si public web :

```text
title
meta
canonical
robots
sitemap
schema
internal links
404
redirect
indexability
content
```

Pour app stores/package registries :

auditer la discoverability correspondante.

Score générique :

```text
DISCOVERABILITY
```

---

# 53. SOCIAL PROOF / TRUST PROOF

Chercher :

```text
testimonials
case studies
usage stats
customer logos
benchmarks
public adoption
GitHub adoption
before/after
measurable outcomes
```

Classer :

```text
REAL
INTERNAL
DEMO
MOCK
UNKNOWN
```

Score :

```text
SOCIAL_PROOF
```

---

# 54. RETENTION

Répondre :

```text
Pourquoi revenir ?
Pourquoi garder le produit ?
Qu’est-ce qui s’accumule ?
Qu’est-ce qui devient coûteux à remplacer ?
```

Distinguer :

```text
one-shot
recurring
stored value
network/team
automation
monitoring
data history
workflow habit
```

Score :

```text
RETENTION_POTENTIAL
```

---

# 55. ANALYTICS PRODUIT

Vérifier :

```text
activation
feature usage
errors
sessions
funnels
retention
cohorts
performance
```

Score :

```text
PRODUCT_ANALYTICS
```

---

# 56. BUSINESS / VALUE ANALYTICS

Commercial :

```text
MRR
ARR
ARPU
CAC
LTV
churn
gross margin
support cost
conversion
expansion
```

Interne :

```text
time saved
cost avoided
error reduction
throughput
adoption
completion rate
```

Score :

```text
VALUE_ANALYTICS
```

---

# 57. UNIT ECONOMICS / COST MODEL

Si commercial :

```text
infra
AI
email
storage
bandwidth
support
payments
manual work
third-party APIs
```

Créer :

```text
KNOWN_COSTS
UNKNOWN_COSTS
MISSING_MEASUREMENTS
```

Score :

```text
UNIT_ECONOMICS
```

Pour interne :

évaluer :

```text
COST_BENEFIT_READINESS
```

---

# 58. COMPETITIVE LANDSCAPE

Si pertinent et web disponible :

rechercher :

```text
direct competitors
partial competitors
alternatives
DIY stack
status quo
```

Comparer :

```text
target
price
capabilities
simplicity
trust
distribution
switching cost
```

Score :

```text
COMPETITIVE_POSITION
```

---

# 59. DIFFERENTIATION

Pour chaque différenciateur :

```text
exists?
works?
user-visible?
valuable?
hard_to_copy?
evidence?
```

Classer :

```text
COMMODITY
EXPECTED
USEFUL_DIFFERENTIATOR
STRONG_DIFFERENTIATOR
CORE_ADVANTAGE
UNPROVEN
```

Score :

```text
DIFFERENTIATION
```

---

# 60. MOAT / DEFENSIBILITY

Chercher :

```text
data
network effects
workflows
history
customer configuration
distribution
brand
community
integrations
proprietary evaluation
operational know-how
switching cost
```

Classer :

```text
NO_MOAT
WEAK
EMERGING
STRONG
```

Score :

```text
MOAT
```

---

# 61. GROWTH LOOPS

Si pertinent :

```text
sharing
invite
public artifacts
templates
referrals
marketplace
embeds
collaboration
user-generated content
```

Distinguer :

```text
REAL_LOOP
WEAK_LOOP
GIMMICK
NONE
```

Score :

```text
GROWTH_LOOPS
```

---

# 62. OPEN-SOURCE SPECIFIC

Activer pour open source.

Auditer :

```text
license
README
install
quickstart
examples
contribution guide
issue templates
release cadence
maintainer bus factor
security policy
community
governance
adoption
compatibility
```

Score :

```text
OPEN_SOURCE_READINESS
```

---

# 63. SDK / LIBRARY SPECIFIC

Activer pour SDK/library.

Auditer :

```text
API stability
semantic versioning
types
documentation
examples
error model
compatibility
package size
dependency footprint
migration
test matrix
```

Score :

```text
SDK_READINESS
```

---

# 64. CLI SPECIFIC

Activer pour CLI.

Auditer :

```text
install
help
commands
exit codes
stdin/stdout
JSON mode
config
secrets
non-interactive mode
automation compatibility
errors
cross-platform
```

Score :

```text
CLI_READINESS
```

---

# 65. MOBILE SPECIFIC

Activer pour mobile.

Auditer :

```text
permissions
privacy manifests
offline
background tasks
deep links
push
crashes
store metadata
updates
device matrix
battery/network
```

Score :

```text
MOBILE_READINESS
```

---

# 66. DESKTOP SPECIFIC

Activer pour desktop.

Auditer :

```text
installer
signing
updates
permissions
filesystem
local storage
crash recovery
OS compatibility
uninstall
```

Score :

```text
DESKTOP_READINESS
```

---

# 67. E-COMMERCE / MARKETPLACE SPECIFIC

Si applicable :

```text
catalog
inventory
checkout
payment
refund
fraud
seller/buyer roles
disputes
tax
fulfillment
reviews
trust
```

Score :

```text
COMMERCE_READINESS
```

---

# 68. AUTOMATION PLATFORM SPECIFIC

Si workflows/automations :

```text
trigger
action
condition
branch
delay
loop
retry
error handler
human approval
secrets
idempotency
run history
debugging
export/import
provider compatibility
```

Mesurer :

```text
WORKFLOW_TOTAL
STATIC_VALID_RATE
IMPORT_TESTED_RATE
RUNTIME_TESTED_RATE
LICENSE_CLEAR_RATE
DUPLICATE_RATE
FAILURE_HANDLING_RATE
```

Score :

```text
AUTOMATION_READINESS
```

---

# 69. CATALOG / FEATURE QUALITY

Pour chaque module/tool/template :

```text
USED
VALUABLE
REDUNDANT
CONFUSING
HIGH_MAINTENANCE
REMOVE_CANDIDATE
UNKNOWN
```

Si usage non instrumenté :

```text
USAGE_UNKNOWN
```

Créer :

```text
CATALOG_VALUE_MATRIX
```

---

# 70. KILL CRITERIA

Pour les features majeures :

```text
CONTINUE_IF
IMPROVE_IF
MERGE_IF
HIDE_IF
KILL_IF
```

Critères :

```text
usage
value
retention
revenue
adoption
support burden
maintenance cost
strategic differentiation
```

---

# 71. USER / CUSTOMER EVIDENCE

Chercher :

```text
real users
active users
paying customers
renewals
case studies
support tickets
feedback
NPS/CSAT if relevant
usage cohorts
```

Classer :

```text
REAL
LIMITED
INTERNAL
DEMO
NONE
UNKNOWN
```

---

# 72. REAL-WORLD VALIDATION PLAN

Si preuves insuffisantes, créer des expériences.

Exemples :

```text
5 beginner users
5 target prospects
3 pilot customers
5–10 paying customers
30-day retention
pricing/willingness-to-pay
support burden
cost measurement
```

Pour projet interne :

```text
5 target employees
before/after time study
error-rate comparison
adoption after 30 days
```

Pour SDK/open-source :

```text
5 external developers
cold install test
first-success time
issue/support burden
repeat usage
```

---

# 73. STANDARD USER TEST GRID

Créer une grille applicable selon projet :

```text
understood_in_10_seconds
goal_selected
time_to_first_action
time_to_first_value
blockers
help_requests
feature_used_spontaneously
perceived_value
willingness_to_pay_or_keep
return_intent
return_reason
abandon_reason
```

---

# 74. NORTH STAR / SUCCESS METRIC

Déterminer :

```text
PRIMARY_CANDIDATE
SECONDARY_CANDIDATE
```

Exemples :

```text
successful workflows
completed business outcomes
active projects
verified releases
successful API calls by active integrations
weekly active workspaces
time saved
```

Ne pas imposer une North Star si le projet ne s’y prête pas.

---

# 75. ACTIVATION METRIC

Identifier l’événement qui signifie :

```text
“l’utilisateur a compris et obtenu la première valeur”
```

Peut être :

```text
GLOBAL
SEGMENT_SPECIFIC
NOT_DEFINED
```

---

# 76. HEALTH METRICS

Proposer seulement les métriques pertinentes :

```text
activation
D1/D7/D30
WAU/MAU
successful tasks
failure rate
support burden
cost per active user/project
latency
uptime
conversion
churn
gross margin
renewal
```

---

# 77. BLOCKERS TO STRONG READINESS

Créer :

```text
BLOCKERS_TO_8
BLOCKERS_TO_9
BLOCKERS_TO_10
```

Maximum :

```text
10
15
15
```

Pour chaque :

```text
problem
domain
evidence
impact
effort
risk
dependency
```

---

# 78. TOP LEVERAGE ACTIONS

Créer :

```text
TOP_25_ACTIONS
```

Colonnes :

```text
ID
Action
Domain
Priority
Impact
Effort
Risk
Evidence
Expected outcome
```

Priorités :

```text
P0
P1
P2
P3
RESEARCH
LEGAL_REVIEW
REAL_USER_TEST
SKIP
```

---

# 79. WHAT NOT TO BUILD

Créer :

```text
TOP_15_THINGS_NOT_TO_BUILD_NOW
```

Exemples :

```text
feature without usage proof
new framework
new provider without demand
marketplace too early
enterprise feature without customer
UI rewrite without evidence
generic workflow engine duplication
premature plugin ecosystem
```

---

# 80. RESEARCH EXTERNE

Utiliser le web uniquement lorsque nécessaire pour :

```text
competitors
pricing
standards
laws/regulation
security standards
accessibility standards
performance standards
platform requirements
public market context
```

Priorité :

```text
official documentation
standards bodies
regulators
vendor official docs
primary repositories
```

Toujours distinguer :

```text
LOCAL_PROJECT_EVIDENCE
EXTERNAL_RESEARCH
ANALYST_INFERENCE
```

---

# 81. RÉFÉRENCES TECHNIQUES PAR DÉFAUT

Ces références sont des points de départ, à revalider au moment de l’audit :

```text
W3C WCAG 2.2
OWASP ASVS — latest stable/current published version
NIST SSDF — latest final version; drafts identified as drafts
Google Core Web Vitals — current official thresholds
```

Ne pas transformer une bonne pratique en obligation légale.

---

# 82. LEGAL / COMPLIANCE CONTEXT ENGINE

Détecter si possible :

```text
jurisdiction
customer type
data types
regulated sector
children/minors
health
finance
public sector
employment
biometrics
AI decisions
payments
```

Puis activer seulement les contrôles pertinents.

Toujours produire :

```text
LEGAL_REVIEW_REQUIRED
```

lorsqu’une conclusion nécessite un professionnel.

---

# 83. SCORECARD UNIVERSELLE

Créer notes applicables parmi :

```text
Technical Asset
Product Depth
Product Maturity
Positioning
Value Proposition
Product Simplicity
UX/DX
Onboarding
Time To Value
Accessibility
Performance
Compatibility
Reliability
Security
Supply Chain
Privacy
AI Readiness
Data Governance
Tenant Isolation
Identity
Production Readiness
Operations/SRE
Disaster Recovery
Observability
Abuse Resilience
Vendor Risk
Portability
Maintainability
Technical Scalability
Operational Scalability
Documentation
Support
Release Readiness
License Readiness
Business Model
Offer Architecture
Pricing
Freemium/Trial
Billing
Conversion
Acquisition
Discoverability
Social Proof
Retention
Product Analytics
Value Analytics
Unit Economics / Cost Benefit
Competitive Position
Differentiation
Moat
Growth Loops
Catalog Quality
Open Source Readiness
SDK Readiness
CLI Readiness
Mobile Readiness
Desktop Readiness
Commerce Readiness
Automation Readiness
```

Pour chaque :

```text
APPLICABILITY
SCORE
CONFIDENCE
WHY
WHY_NOT_PLUS_ONE
WHY_NOT_MINUS_ONE
EVIDENCE
```

---

# 84. SCORES FINAUX ADAPTATIFS

Toujours calculer :

```text
PRODUCT_READINESS
TECHNICAL_READINESS
OPERATIONAL_READINESS
TRUST_READINESS
ADOPTION_READINESS
SCALABILITY_READINESS
EVIDENCE_STRENGTH
```

Si projet commercial :

```text
COMMERCIAL_READINESS
BUSINESS_MODEL_READINESS
MARKET_EVIDENCE
OVERALL_BUSINESS_POTENTIAL
```

Si projet interne/non commercial :

```text
ORGANIZATIONAL_VALUE_READINESS
ADOPTION_VALUE
COST_BENEFIT_READINESS
OVERALL_VALUE_POTENTIAL
```

Ne jamais forcer un score commercial à un outil non commercial.

---

# 85. MATURITY STAGE

Commercial :

```text
EXPERIMENT
PROTOTYPE
MVP
BETA
ADVANCED_BETA
PRE_COMMERCIAL
EARLY_COMMERCIAL
VALIDATED_NICHE
SCALING
MATURE
```

Open source :

```text
EXPERIMENTAL
EARLY
USABLE
STABLE
ESTABLISHED
ECOSYSTEM
```

Interne :

```text
PROTOTYPE
PILOT
TEAM_READY
DEPARTMENT_READY
ORG_READY
MISSION_CRITICAL
```

---

# 86. LIVRABLES STANDARD

Créer dans un dossier d’audit dédié :

```text
BUSINESS_READINESS_360_REPORT.md
BUSINESS_READINESS_360_DATA.json
BUSINESS_READINESS_360_BACKLOG.md
BUSINESS_READINESS_360_METRICS.md
BUSINESS_READINESS_360_VALIDATION_PLAN.md
BUSINESS_READINESS_360_OPERATIONS_RESILIENCE.md
BUSINESS_READINESS_360_PRUNING.md
```

Optionnel :

```text
BUSINESS_READINESS_360_EVIDENCE.json
BUSINESS_READINESS_360.html
```

---

# 87. REPORT STRUCTURE

`BUSINESS_READINESS_360_REPORT.md` doit contenir :

```text
1 Executive Summary
2 Project Profile
3 Applicability Matrix
4 Evidence Quality
5 Product Map
6 Target Users
7 JTBD
8 Positioning
9 Value Proposition
10 Simplicity
11 UX/DX
12 Onboarding
13 Time To Value
14 Accessibility
15 Performance
16 Compatibility
17 Reliability
18 Security
19 Supply Chain
20 Privacy
21 AI
22 Data Governance
23 Multi-tenant / Permissions
24 Identity
25 Production
26 SRE / Operations
27 Disaster Recovery
28 Observability
29 Abuse / Fraud
30 Vendor Risk
31 Portability
32 Maintainability
33 Technical Scalability
34 Operational Scalability
35 Documentation
36 Support
37 Release
38 Licenses/IP
39 Business Model
40 Offers
41 Pricing
42 Freemium/Trial
43 Billing
44 Conversion
45 Acquisition
46 Discoverability
47 Social Proof
48 Retention
49 Product Analytics
50 Business/Value Analytics
51 Unit Economics / Cost Benefit
52 Competition
53 Differentiation
54 Moat
55 Growth Loops
56 Catalog Quality
57 Specialized Project-Type Audits
58 Kill Criteria
59 Missing Evidence
60 Real-World Validation
61 Metrics
62 Blockers 8/9/10
63 Top 25 Actions
64 What Not To Build
65 Scorecard
66 Maturity
67 Final Readiness
68 Final Verdict
```

---

# 88. JSON OUTPUT CONTRACT

`BUSINESS_READINESS_360_DATA.json` :

```json
{
  "schema": "BR360-1",
  "audit": {
    "date": "",
    "project": "",
    "version": "",
    "commit": "",
    "mode": "READ_ONLY"
  },
  "project_profile": {},
  "applicability": {},
  "evidence_summary": {},
  "scores": {},
  "modules": [],
  "risks": [],
  "business": {},
  "operations": {},
  "security": {},
  "privacy": {},
  "ai": {},
  "data": {},
  "analytics": {},
  "competition": [],
  "blockers_to_8": [],
  "blockers_to_9": [],
  "blockers_to_10": [],
  "actions": [],
  "not_to_build": [],
  "experiments": [],
  "missing_evidence": [],
  "final": {
    "product_readiness": null,
    "technical_readiness": null,
    "operational_readiness": null,
    "trust_readiness": null,
    "adoption_readiness": null,
    "scalability_readiness": null,
    "evidence_strength": null,
    "commercial_readiness": null,
    "overall_business_potential": null,
    "overall_value_potential": null,
    "confidence": null,
    "maturity_stage": ""
  }
}
```

JSON strictement valide.

---

# 89. PRIORITY BACKLOG

Créer :

```text
ID
Domain
Finding
Priority
Impact
Effort
Risk
Evidence strength
Dependency
Recommended action
```

---

# 90. METRICS PLAN

Pour chaque métrique :

```text
name
definition
event/source
frequency
segment
decision_enabled
status
```

Ne pas inventer une instrumentation existante.

---

# 91. VALIDATION PLAN

Pour chaque expérience :

```text
hypothesis
target
sample
procedure
metric
success threshold
failure meaning
next action
```

Ne pas contacter d’utilisateur.

---

# 92. OPERATIONS / RESILIENCE PLAN

Inclure si applicable :

```text
SLI/SLO
alerts
runbooks
backup
restore
RPO
RTO
incident response
dependency outage
provider outage
rollback
ownership
```

---

# 93. PRUNING PLAN

Pour chaque feature :

```text
feature
usage evidence
value
maintenance cost
support burden
strategic value
decision
```

Décisions :

```text
KEEP
IMPROVE
MERGE
HIDE
DEPRECATE
REMOVE
RESEARCH
```

---

# 94. AXDIA FRAMEWORK INTEGRATION CONTRACT

AXDIA Framework doit pouvoir présenter ce pack comme :

```text
Name: Business Readiness 360
Category: Audit
Scope: Universal
Mode: Read-only
Difficulty: Advanced
Outputs: Markdown + JSON + Backlog + Metrics + Validation + Operations + Pruning
Requires AI: optional/recommended for qualitative analysis
Requires Web: optional, only for external research
Requires Credentials: no by default
Can Modify Project: no
```

## 94.1 Inputs UI

Minimum :

```text
Project path
Audit profile = Auto / Commercial / Internal / Open Source / Technical
External research = On/Off
Run existing tests = On/Off
Browser QA = On/Off
Recursive integration = Auto/Off
Target jurisdiction = Auto/Manual/Unknown
```

Optional :

```text
Known target users
Known business model
Known pricing
Known production URL
Known staging URL
Known constraints
```

## 94.2 Outputs UI

Afficher :

```text
Overall readiness
Evidence strength
Top P0
Top blockers
Missing real-world evidence
Scorecard
Maturity stage
Download reports
```

---

# 95. AXDIA FRAMEWORK EXECUTION PIPELINE

```text
DETECT
↓
CLASSIFY PROJECT
↓
APPLICABILITY MATRIX
↓
LOCAL EVIDENCE
↓
NON-DESTRUCTIVE TESTS
↓
OPTIONAL EXTERNAL RESEARCH
↓
DOMAIN AUDITS
↓
EVIDENCE GRAPH
↓
SCORECARD
↓
BLOCKERS
↓
BACKLOG
↓
VALIDATION PLAN
↓
REPORT
```

---

# 96. FRAMEWORK SAFETY CONTRACT

AXDIA Framework doit appliquer :

```text
READ_ONLY = TRUE
REMOTE_MUTATION = FALSE
PRODUCTION_ACTION = FALSE
SECRET_OUTPUT = FALSE
PAID_ACTION = FALSE
USER_CONTACT = FALSE
```

Tout dépassement :

```text
HUMAN_GATE_REQUIRED
```

---

# 97. GENERIC DETECTION HINTS

Le pack peut considérer comme projet valide s’il trouve au moins un marqueur :

```text
package.json
pyproject.toml
requirements.txt
setup.py
go.mod
Cargo.toml
pom.xml
build.gradle
composer.json
Gemfile
*.csproj
*.sln
index.html
Dockerfile
docker-compose.yml
README.md
src/
app/
```

L’absence de ces marqueurs ne signifie pas automatiquement :

```text
NOT_A_PROJECT
```

Le Framework peut accepter un dossier sélectionné manuellement.

---

# 98. EXTERNAL STANDARDS RULE

Les versions de standards changent.

Au lancement d’un audit connecté au web :

```text
revalidate current standard versions
```

Sans web :

```text
use bundled baseline
mark VERSION_NOT_REVALIDATED
```

Ne jamais inventer une version.

---

# 99. FINAL EXECUTIVE BLOCK

Le rapport doit commencer par :

```text
BUSINESS_READINESS_360 = COMPLETE / PARTIAL / BLOCKED

PROJECT_TYPE =
BUSINESS_MODEL =
TARGET_USER =
DISTRIBUTION_MODEL =

PRODUCT_READINESS =
TECHNICAL_READINESS =
OPERATIONAL_READINESS =
TRUST_READINESS =
ADOPTION_READINESS =
SCALABILITY_READINESS =
EVIDENCE_STRENGTH =

COMMERCIAL_READINESS =
OVERALL_BUSINESS_POTENTIAL =
OVERALL_VALUE_POTENTIAL =
CONFIDENCE =

MATURITY_STAGE =

TOP_STRENGTH =
TOP_WEAKNESS =
TOP_TECHNICAL_RISK =
TOP_PRODUCT_RISK =
TOP_OPERATIONS_RISK =
TOP_SECURITY_RISK =
TOP_BUSINESS_OR_VALUE_RISK =

BLOCKERS_TO_8 =
BLOCKERS_TO_9 =
BLOCKERS_TO_10 =
P0_ACTIONS =
MISSING_REAL_WORLD_EVIDENCE =
```

Les champs non applicables :

```text
NOT_APPLICABLE
```

---

# 100. FINAL VERDICT

Finir par :

```text
PROJECT_READY_FOR_TARGET_USE = YES / PARTIAL / NO

IF_COMMERCIAL:
READY_TO_CHARGE = YES / PARTIAL / NO
READY_TO_SCALE = YES / PARTIAL / NO
BUSINESS_POTENTIAL_NOW = X/10 or NOT_APPLICABLE
BUSINESS_POTENTIAL_AFTER_P0 = X/10 or NOT_APPLICABLE
BUSINESS_POTENTIAL_AFTER_REAL_VALIDATION = X/10 or NOT_APPLICABLE

IF_INTERNAL_OR_NON_COMMERCIAL:
VALUE_POTENTIAL_NOW = X/10
VALUE_POTENTIAL_AFTER_P0 = X/10
ORGANIZATIONAL_ADOPTION_READINESS = X/10

MOST_IMPORTANT_MISSING_PROOF =
MOST_IMPORTANT_MISSING_METRIC =
RECOMMENDED_NEXT_STEP =
```

---

# 101. GARDE-FOU

Ne pas recommander automatiquement :

```text
plus de fonctionnalités
plus d’IA
plus de modules
plus d’intégrations
plus de providers
nouvelle architecture
réécriture
```

Favoriser d’abord :

```text
preuve
simplicité
activation
reliability
security
retention
adoption
conversion
support
observability
maintainability
economics/value
```

---

# 102. RÈGLE ULTIME

Le rôle de Business Readiness 360 n’est pas de dire :

> « le projet est impressionnant ».

Il doit répondre :

> **« Est-ce que ce projet crée une valeur réelle, pour qui, avec quel niveau de preuve, à quel coût, avec quels risques, et qu’est-ce qui l’empêche d’atteindre son prochain niveau de maturité ? »**

