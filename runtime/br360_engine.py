#!/usr/bin/env python3
"""AXDIA Business Readiness 360 V3 execution engine.

Design goals:
- dependency-free Python standard library runtime;
- read-only by default;
- conservative evidence handling (no evidence == no PASS);
- backward-compatible public helpers from V2;
- deterministic built-in checks for controls marked AUTOMATED;
- explicit human/real-world evidence import for the rest;
- optional, opt-in adapter discovery/execution.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
PACK_VERSION = "3.0.0"
SCHEMA_VERSION = "BR360-3"

SKIP_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "vendor", ".venv", "venv", "env",
    "dist", "build", "coverage", ".next", ".nuxt", ".svelte-kit", "target",
    "Pods", "DerivedData", ".gradle", ".idea", ".vscode-test", "__pycache__",
}
TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".jsonc", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".py", ".go", ".rs", ".java", ".kt", ".kts", ".cs", ".php", ".rb", ".swift",
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".xml", ".yaml", ".yml",
    ".toml", ".ini", ".conf", ".cfg", ".env", ".example", ".sh", ".bash", ".zsh",
    ".sql", ".graphql", ".gql", ".properties",
}
SEVERITY_RANK = {"CRITICAL": 5, "HIGH": 4, "MEDIUM": 3, "LOW": 2, "INFO": 1}
EVIDENCE_RANK = {
    "E0_CLAIM_ONLY": 0,
    "E1_STATIC": 1,
    "E2_TESTED": 2,
    "E3_RUNTIME": 3,
    "E4_REAL_WORLD": 4,
}
VALID_EVAL_STATUSES = {"PASS", "PARTIAL", "FAIL", "NOT_TESTED", "NOT_APPLICABLE"}


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def _load_json(path: Path | str) -> Any:
    with Path(path).open(encoding="utf-8") as fh:
        return json.load(fh)


def _json_digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return path.name


def _read_text(path: Path, limit: int = 1_000_000) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _iter_project_files(project: Path, max_files: int = 6000) -> Iterable[Path]:
    seen = 0
    if not project.exists() or not project.is_dir():
        return
    for base, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".cache")]
        for name in files:
            if seen >= max_files:
                return
            p = Path(base) / name
            try:
                if p.is_symlink() or not p.is_file():
                    continue
            except OSError:
                continue
            seen += 1
            yield p


def _text_files(project: Path, max_files: int = 3500) -> Iterable[Path]:
    count = 0
    special = {"Dockerfile", "Makefile", "Procfile", "Gemfile", "LICENSE", "NOTICE", "CODEOWNERS"}
    for p in _iter_project_files(project):
        if count >= max_files:
            return
        if p.suffix.lower() in TEXT_EXTENSIONS or p.name in special or p.name.startswith(".env"):
            count += 1
            yield p


def load_controls() -> List[dict]:
    out: List[dict] = []
    for p in sorted((ROOT / "business-readiness-360" / "controls").glob("*.json")):
        out.extend(_load_json(p)["controls"])
    return out


def load_profiles() -> Dict[str, dict]:
    return {p["id"]: p for p in _load_json(ROOT / "business-readiness-360" / "profiles" / "PROFILES.json")["profiles"]}


def load_adapters() -> List[dict]:
    return _load_json(ROOT / "business-readiness-360" / "adapters" / "ADAPTERS.json")["adapters"]


def load_detector_catalog() -> Dict[str, dict]:
    p = ROOT / "business-readiness-360" / "detectors" / "CONTROL_DETECTORS.json"
    if not p.exists():
        return {}
    return {x["id"]: x for x in _load_json(p).get("detectors", [])}


def detect_project(path: Path | str) -> dict:
    """Conservative project fact detector. Kept API-compatible with V2."""
    p = Path(path)
    facts: set[str] = set()
    evidence: List[dict] = []

    def hit(f: str, reason: str, location: Optional[str] = None) -> None:
        facts.add(f)
        row = {"fact": f, "reason": reason}
        if location:
            row["location"] = location
        evidence.append(row)

    if not p.exists() or not p.is_dir():
        return {"facts": [], "evidence": [], "warnings": ["Project path is missing or is not a directory."]}

    names = {x.name for x in p.iterdir()}
    package: dict = {}
    deps: Dict[str, str] = {}
    if "package.json" in names:
        hit("language.javascript", "package.json", "package.json")
        try:
            package = _load_json(p / "package.json")
            deps = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
            if any(x in deps for x in ["react", "next", "vue", "svelte", "@angular/core", "astro"]):
                hit("has_web_ui", "JS UI framework dependency", "package.json")
            if "electron" in deps:
                hit("has_desktop", "electron dependency", "package.json")
            if "@capacitor/core" in deps:
                hit("has_mobile", "Capacitor dependency", "package.json")
            if any(x in deps for x in ["openai", "@anthropic-ai/sdk", "anthropic", "@google/generative-ai", "ollama"]):
                hit("uses_ai", "AI provider dependency", "package.json")
            if any(x in deps for x in ["stripe", "@stripe/stripe-js", "paddle", "lemonsqueezy"]):
                hit("has_billing", "billing dependency", "package.json")
            if package.get("bin"):
                hit("has_cli", "package.json bin", "package.json")
            if package.get("license"):
                hit("has_license_metadata", "package.json license metadata", "package.json")
        except Exception as exc:
            evidence.append({"fact": "warning.package_json", "reason": f"Could not parse package.json: {exc}"})

    if {"pyproject.toml", "requirements.txt", "setup.py"} & names:
        hit("language.python", "python manifest")
    if "go.mod" in names:
        hit("language.go", "go.mod", "go.mod")
    if "Cargo.toml" in names:
        hit("language.rust", "Cargo.toml", "Cargo.toml")
    if {"pom.xml", "build.gradle", "build.gradle.kts"} & names:
        hit("language.jvm", "JVM build manifest")
    if "composer.json" in names:
        hit("language.php", "composer.json", "composer.json")
    if "Gemfile" in names:
        hit("language.ruby", "Gemfile", "Gemfile")

    if "index.html" in names or (p / "public").exists() or (p / "app").exists() or (p / "src").exists() and "has_web_ui" in facts:
        hit("has_human_ui", "UI surface")
    if any((p / x).exists() for x in ["openapi.yaml", "openapi.yml", "openapi.json", "swagger.json", "swagger.yaml"]):
        hit("has_api", "OpenAPI contract")
    if any((p / x).exists() for x in ["asyncapi.yaml", "asyncapi.yml", "asyncapi.json"]):
        hit("has_event_api", "AsyncAPI contract")
    if (p / ".github" / "workflows").exists():
        hit("has_ci", ".github/workflows")
    if any((p / x).exists() for x in ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yaml", "compose.yml"]):
        hit("has_containers", "container config")
    if any((p / x).exists() for x in ["vercel.json", "railway.json", "render.yaml", "fly.toml", "netlify.toml"]):
        hit("production_service", "hosting config")
    if (p / "android").exists() or (p / "ios").exists():
        hit("has_mobile", "native mobile directory")
    if (p / "src-tauri").exists():
        hit("has_desktop", "Tauri directory")
    if any((p / x).exists() for x in ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"]):
        hit("open_source", "license file")
        hit("has_license_metadata", "license file")
    if any((p / x).exists() for x in ["prisma/schema.prisma", "supabase", "migrations", "db", "database"]):
        hit("has_persistent_data", "database schema/migration surface")

    # Conservative content facts. Limit to high-value configuration/documentation files.
    text = ""
    locations = []
    candidate_docs = ["README.md", "package.json", "pyproject.toml", "Cargo.toml", "go.mod", "vercel.json"]
    for fn in candidate_docs:
        q = p / fn
        if q.exists():
            t = _read_text(q, 250_000)
            if t:
                text += "\n" + t
                locations.append(fn)
    low = text.lower()
    if any(k in low for k in ["tenant_id", "organization_id", "workspace_id", "multi-tenant", "multitenant"]):
        hit("multi_tenant", "tenant identifier pattern")
    if any(k in low for k in ["supabase", "firebase", "next-auth", "auth.js", "authentication", "oauth", "clerk"]):
        hit("has_auth", "auth pattern")
    if any(k in low for k in ["entitlement", "subscription", "plan_id", "pricing tier"]):
        hit("has_entitlements", "entitlement pattern")
    if any(k in low for k in ["api/", "fastapi", "express", "nestjs", "hono", "flask", "django rest"]):
        hit("has_api", "API pattern")
    if any(k in low for k in ["analytics", "posthog", "plausible", "segment", "mixpanel", "amplitude"]):
        hit("has_analytics", "analytics pattern")
    if any(k in low for k in ["stripe", "checkout", "billing", "payment"]):
        facts.add("commercial_product")
    if "uses_ai" in facts:
        hit("commercial_product", "AI product candidate")
    if "has_human_ui" in facts:
        facts.add("has_web_ui")
    if "production_service" in facts or "has_api" in facts:
        facts.add("has_backend")

    return {"facts": sorted(facts), "evidence": evidence, "warnings": []}


def control_applicability(c: dict, facts: Iterable[str]) -> Tuple[str, str]:
    r = c.get("applicability", {})
    f = set(facts)
    anyf = r.get("facts_any", [])
    allf = r.get("facts_all", [])
    notf = r.get("not_facts", [])
    if notf and any(x in f for x in notf):
        return "NOT_APPLICABLE", "negative fact matched"
    if allf and not all(x in f for x in allf):
        return r.get("default", "NOT_APPLICABLE"), "required facts absent"
    if anyf and not any(x in f for x in anyf):
        return r.get("default", "NOT_APPLICABLE"), "no applicability fact matched"
    return ("REQUIRED" if anyf or allf else r.get("default", "RECOMMENDED"),
            "applicability facts matched" if anyf or allf else "default policy")


def select_controls(facts: Iterable[str], profile: str = "AUTO") -> List[dict]:
    profs = load_profiles()
    p = profs.get(profile, profs["AUTO"])
    out: List[dict] = []
    by_domain: Dict[str, List[dict]] = {}
    for c in load_controls():
        by_domain.setdefault(c["domain"], []).append(c)
    for domain in p["included_domains"]:
        for c in by_domain.get(domain, []):
            status, reason = control_applicability(c, facts)
            out.append({
                "control_id": c["id"], "domain": c["domain"], "applicability": status,
                "reason": reason, "automation": c["automation"], "detectors": c.get("detectors", []),
            })
    return out


def score(evaluations: List[dict]) -> dict:
    """V2-compatible scoring with V3 confidence/evidence additions calculated elsewhere."""
    vals = {"PASS": 1.0, "PARTIAL": 0.5, "FAIL": 0.0}
    applicable = [e for e in evaluations if e.get("applicability") != "NOT_APPLICABLE"]
    scored = [e for e in applicable if e.get("status") in vals]
    impl = 10 * sum(vals[e["status"]] for e in scored) / len(applicable) if applicable else 0
    verified = [e for e in applicable if e.get("evidence_level") in ["E2_TESTED", "E3_RUNTIME", "E4_REAL_WORLD"]]
    verification = 10 * len(verified) / len(applicable) if applicable else 0
    rw = [e for e in applicable if e.get("automation") == "REAL_WORLD_REQUIRED"]
    rw_ok = [e for e in rw if e.get("evidence_level") == "E4_REAL_WORLD" and e.get("status") in ["PASS", "PARTIAL"]]
    real = 10 * len(rw_ok) / len(rw) if rw else 10
    coverage = len(scored) / len(applicable) if applicable else 0
    readiness = (.45 * impl + .30 * verification + .25 * real) if rw else (.60 * impl + .40 * verification)
    if rw and real == 0:
        readiness = min(readiness, 6.5)
    if verification < 5:
        readiness = min(readiness, 7.5)
    if coverage < .70:
        readiness = min(readiness, 8.0)
    return {
        "implementation": round(impl, 2), "verification": round(verification, 2),
        "real_world_evidence": round(real, 2), "readiness": round(readiness, 2),
        "coverage": round(coverage, 4),
    }


def fingerprint(f: dict) -> str:
    s = "|".join(str(f.get(k, "")) for k in [
        "audit_domain", "affected_asset", "control_id", "package_or_resource",
        "issue_identifier", "location",
    ])
    return hashlib.sha256(s.encode()).hexdigest()[:24]


def compare(a: dict, b: dict) -> dict:
    A = {x["fingerprint"]: x for x in a.get("findings", []) if x.get("fingerprint")}
    B = {x["fingerprint"]: x for x in b.get("findings", []) if x.get("fingerprint")}
    return {
        "new_findings": sorted(set(B) - set(A)),
        "resolved_findings": sorted(set(A) - set(B)),
        "persistent_findings": sorted(set(A) & set(B)),
        "score_delta": {
            k: round(b.get("scores", {}).get(k, 0) - a.get("scores", {}).get(k, 0), 2)
            for k in ["implementation", "verification", "real_world_evidence", "readiness"]
        },
        "maturity_delta": b.get("maturity", {}).get("level", 0) - a.get("maturity", {}).get("level", 0),
    }


# ------------------------- evidence helpers -------------------------

def make_evidence(ev_type: str, level: str, source: str, summary: str, *,
                  location: Optional[str] = None, digest_payload: Any = None,
                  authority: float = .75, confidence: float = .8) -> dict:
    return {
        "id": "EV-" + hashlib.sha256(f"{ev_type}|{level}|{source}|{summary}|{location}".encode()).hexdigest()[:16],
        "type": ev_type,
        "level": level,
        "source": source,
        "summary": summary,
        "digest": _json_digest(digest_payload) if digest_payload is not None else None,
        "freshness": _now(),
        "authority": round(float(authority), 3),
        "confidence": round(float(confidence), 3),
        "location": location,
    }


def _eval(control: dict, applicability: str, status: str, level: str, evidence: List[dict],
          summary: str, source_method: str = "builtin") -> dict:
    return {
        "control_id": control["id"], "domain": control["domain"], "title": control["title"],
        "applicability": applicability, "automation": control["automation"], "status": status,
        "evidence_level": level, "evidence": evidence, "summary": summary,
        "source_method": source_method,
    }


def _find_named(project: Path, names: Iterable[str]) -> List[Path]:
    wanted = {x.lower() for x in names}
    return [p for p in _iter_project_files(project) if p.name.lower() in wanted]


def _find_patterns(project: Path, patterns: Iterable[str], max_matches: int = 30) -> List[str]:
    regexes = [re.compile(x, re.I) for x in patterns]
    matches: List[str] = []
    for p in _text_files(project):
        rel = _safe_rel(p, project)
        txt = _read_text(p, 500_000)
        if not txt:
            continue
        if any(r.search(txt) for r in regexes):
            matches.append(rel)
            if len(matches) >= max_matches:
                break
    return matches


def _all_relative(project: Path) -> set[str]:
    return {_safe_rel(p, project).lower() for p in _iter_project_files(project)}


def _manifest_and_lock(project: Path) -> Tuple[List[str], List[str]]:
    manifests = ["package.json", "pyproject.toml", "requirements.txt", "go.mod", "cargo.toml", "pom.xml", "build.gradle", "composer.json", "gemfile"]
    locks = ["package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "bun.lock", "poetry.lock", "uv.lock", "pdm.lock", "pipfile.lock", "cargo.lock", "go.sum", "composer.lock", "gemfile.lock", "gradle.lockfile"]
    rels = _all_relative(project)
    m = [x for x in manifests if any(r.endswith("/" + x) or r == x for r in rels)]
    l = [x for x in locks if any(r.endswith("/" + x) or r == x for r in rels)]
    return m, l


# ------------------------- built-in detectors -------------------------

def check_secret_scan(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    secret_patterns = [
        ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
        ("GitHub classic token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
        ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b")),
        ("OpenAI-like secret", re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b")),
        ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
        ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ]
    findings: List[dict] = []
    scanned = 0
    for p in _text_files(project):
        rel = _safe_rel(p, project)
        lowrel = rel.lower()
        # Ignore fixtures/examples and generated audit output to reduce false positives.
        if any(x in lowrel for x in ["fixture", "example", "sample", "golden", "testdata", "node_modules"]):
            continue
        txt = _read_text(p, 800_000)
        if not txt:
            continue
        scanned += 1
        for label, rx in secret_patterns:
            for m in rx.finditer(txt):
                line = txt.count("\n", 0, m.start()) + 1
                findings.append({"type": label, "location": f"{rel}:{line}"})
                if len(findings) >= 25:
                    break
            if len(findings) >= 25:
                break
        if len(findings) >= 25:
            break
    evidence = [make_evidence("TEST_RESULT", "E2_TESTED", "builtin.secret_scan",
                              f"Scanned {scanned} text files; high-confidence secret hits: {len(findings)}.",
                              digest_payload=findings, authority=.9, confidence=.9)]
    if findings:
        evidence.append(make_evidence("OBSERVATION", "E2_TESTED", "builtin.secret_scan",
                                      "Potential secret locations were detected; values are intentionally redacted.",
                                      location=findings[0]["location"], digest_payload=findings, authority=.9, confidence=.92))
        return _eval(control, applicability, "FAIL", "E2_TESTED", evidence,
                     f"Detected {len(findings)} high-confidence secret candidate(s).")
    if scanned == 0:
        return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No scannable text files were found.")
    return _eval(control, applicability, "PASS", "E2_TESTED", evidence,
                 "Built-in high-confidence secret scan found no matches in the scanned source surface.")


def check_api_contract(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    names = ["openapi.json", "openapi.yaml", "openapi.yml", "swagger.json", "swagger.yaml", "swagger.yml", "asyncapi.json", "asyncapi.yaml", "asyncapi.yml"]
    found = _find_named(project, names)
    valid: List[str] = []
    for p in found:
        txt = _read_text(p, 1_000_000)
        if p.suffix.lower() == ".json":
            try:
                d = json.loads(txt)
                if any(k in d for k in ["openapi", "swagger", "asyncapi"]):
                    valid.append(_safe_rel(p, project))
            except Exception:
                pass
        elif re.search(r"(?m)^\s*(openapi|swagger|asyncapi)\s*:", txt):
            valid.append(_safe_rel(p, project))
    if valid:
        ev = [make_evidence("CONTRACT", "E1_STATIC", "builtin.api_contract", f"Machine-readable API contract(s): {', '.join(valid[:8])}.", digest_payload=valid, authority=.9, confidence=.95)]
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "A recognizable machine-readable API contract exists.")
    if "has_api" in facts:
        ev = [make_evidence("OBSERVATION", "E1_STATIC", "builtin.api_contract", "API surface detected, but no recognizable OpenAPI/Swagger/AsyncAPI contract was found.", authority=.8, confidence=.85)]
        return _eval(control, applicability, "FAIL", "E1_STATIC", ev, "API detected without a machine-readable contract.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No API fact was detected and no contract was found.")


def check_license(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    license_files = _find_named(project, ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "NOTICE"])
    pkg_license = None
    if (project / "package.json").exists():
        try:
            pkg_license = _load_json(project / "package.json").get("license")
        except Exception:
            pass
    sources = [_safe_rel(p, project) for p in license_files]
    if pkg_license:
        sources.append(f"package.json:license={pkg_license}")
    if sources:
        ev = [make_evidence("DOCUMENTATION", "E1_STATIC", "builtin.license", f"Distribution/license metadata found: {', '.join(sources[:8])}.", digest_payload=sources, authority=.9, confidence=.95)]
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "Project license/distribution terms are explicitly represented in source metadata.")
    ev = [make_evidence("OBSERVATION", "E1_STATIC", "builtin.license", "No LICENSE/COPYING/NOTICE file or package license metadata was found.", authority=.8, confidence=.9)]
    return _eval(control, applicability, "FAIL", "E1_STATIC", ev, "Project distribution/license terms are not explicit in the inspected source tree.")


def check_supply_inventory(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    manifests, locks = _manifest_and_lock(project)
    if manifests and locks:
        ev = [make_evidence("CONFIG", "E1_STATIC", "builtin.dependency_inventory", f"Dependency manifests {manifests} and lock/integrity files {locks} found.", digest_payload={"manifests": manifests, "locks": locks}, authority=.9, confidence=.95)]
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "Dependency inventory is reproducible from manifest plus lock/integrity metadata.")
    if manifests:
        ev = [make_evidence("CONFIG", "E1_STATIC", "builtin.dependency_inventory", f"Dependency manifest(s) found without a recognized lock/integrity file: {manifests}.", digest_payload=manifests, authority=.8, confidence=.9)]
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "Dependency inventory exists but deterministic resolution evidence is incomplete.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No recognized dependency manifest was found.")


def check_env_secret_safe(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    rels = _all_relative(project)
    env_examples = [r for r in rels if r.endswith((".env.example", ".env.sample", ".env.template", "example.env", "sample.env"))]
    config_files = [r for r in rels if r.endswith(("vercel.json", "railway.json", "render.yaml", "fly.toml", "docker-compose.yml", "compose.yaml", "config.toml"))]
    committed_env = [r for r in rels if r.endswith(".env") and not any(x in r for x in ["example", "sample", "template"])]
    # do not expose values; only recognize suspicious non-placeholder assignment in committed .env files
    suspicious_env: List[str] = []
    for rel in committed_env[:20]:
        p = project / rel
        txt = _read_text(p, 200_000)
        for line in txt.splitlines():
            if re.match(r"\s*(?:SECRET|TOKEN|PASSWORD|API_KEY|PRIVATE_KEY)[A-Z0-9_]*\s*=\s*[^\s#]{8,}\s*$", line, re.I):
                val = line.split("=", 1)[1].strip().lower()
                if not any(x in val for x in ["example", "changeme", "placeholder", "your_", "<", "${"]):
                    suspicious_env.append(rel)
                    break
    ev: List[dict] = []
    if env_examples:
        ev.append(make_evidence("CONFIG", "E1_STATIC", "builtin.env_config", f"Environment template(s) found: {env_examples[:8]}.", digest_payload=env_examples, authority=.85, confidence=.9))
    if config_files:
        ev.append(make_evidence("CONFIG", "E1_STATIC", "builtin.env_config", f"Deployment/config files found: {config_files[:8]}.", digest_payload=config_files, authority=.8, confidence=.85))
    if suspicious_env:
        ev.append(make_evidence("OBSERVATION", "E2_TESTED", "builtin.env_config", f"Potential committed secret-bearing .env file(s): {sorted(set(suspicious_env))[:8]}.", digest_payload=suspicious_env, authority=.9, confidence=.88))
        return _eval(control, applicability, "FAIL", "E2_TESTED", ev, "Potential secret-bearing environment configuration is committed in the inspected source tree.")
    if env_examples and (config_files or "production_service" in facts or "has_backend" in facts):
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "Explicit environment configuration template exists and no suspicious committed secret assignment was detected.")
    if env_examples or config_files:
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "Some explicit environment configuration exists, but the production boundary is not fully evidenced.")
    return _eval(control, applicability, "FAIL", "E1_STATIC", [make_evidence("OBSERVATION", "E1_STATIC", "builtin.env_config", "No recognized environment template or production configuration file was found.", authority=.75, confidence=.8)], "Production environment configuration is not explicit in the inspected tree.")


def check_debug_disabled(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    bad: List[str] = []
    good: List[str] = []
    patterns_bad = [re.compile(r"\bdebug\s*[:=]\s*(?:true|1)\b", re.I), re.compile(r"FLASK_DEBUG\s*=\s*1", re.I), re.compile(r"APP_DEBUG\s*=\s*true", re.I)]
    patterns_good = [re.compile(r"NODE_ENV\s*[:=]\s*[\"']?production", re.I), re.compile(r"\bdebug\s*[:=]\s*(?:false|0)\b", re.I), re.compile(r"APP_ENV\s*=\s*production", re.I)]
    for p in _text_files(project):
        rel = _safe_rel(p, project)
        if not any(k in rel.lower() for k in ["config", "vercel", "railway", "render", "docker", ".env", "settings", "main", "app"]):
            continue
        txt = _read_text(p, 300_000)
        if any(rx.search(txt) for rx in patterns_bad):
            bad.append(rel)
        if any(rx.search(txt) for rx in patterns_good):
            good.append(rel)
    if bad:
        ev = [make_evidence("CONFIG", "E2_TESTED", "builtin.production_debug", f"Development/debug enablement pattern detected in: {sorted(set(bad))[:10]}.", digest_payload=bad, authority=.85, confidence=.86)]
        return _eval(control, applicability, "FAIL", "E2_TESTED", ev, "Debug/development behavior appears enabled in a production-relevant configuration surface.")
    if good:
        ev = [make_evidence("CONFIG", "E1_STATIC", "builtin.production_debug", f"Explicit production/debug-off configuration detected in: {sorted(set(good))[:10]}.", digest_payload=good, authority=.85, confidence=.9)]
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "Production or debug-off configuration is explicit and no obvious debug-on pattern was detected.")
    if "production_service" in facts:
        ev = [make_evidence("OBSERVATION", "E1_STATIC", "builtin.production_debug", "Production hosting configuration exists, but no explicit debug-off/production-mode assertion was located.", authority=.7, confidence=.75)]
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "No debug-on pattern was found, but an explicit production-mode assertion is missing.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No production service fact was detected.")


def check_ai_inventory(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    provider_patterns = [r"openai", r"anthropic", r"claude", r"gemini", r"ollama", r"mistral", r"groq", r"bedrock", r"azure openai"]
    flow_patterns = [r"data flow", r"dataflow", r"prompt.*data", r"model.*provider", r"ai.*privacy", r"llm.*privacy", r"retention.*ai"]
    provider_files = _find_patterns(project, provider_patterns, 20)
    flow_files = _find_patterns(project, flow_patterns, 20)
    ev: List[dict] = []
    if provider_files:
        ev.append(make_evidence("CONFIG", "E1_STATIC", "builtin.ai_inventory", f"AI provider/model references found in {provider_files[:10]}.", digest_payload=provider_files, authority=.8, confidence=.9))
    if flow_files:
        ev.append(make_evidence("DOCUMENTATION", "E1_STATIC", "builtin.ai_inventory", f"AI data-flow/privacy documentation signals found in {flow_files[:10]}.", digest_payload=flow_files, authority=.75, confidence=.8))
    if provider_files and flow_files:
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "AI provider/model references and data-flow documentation signals are both present.")
    if provider_files or "uses_ai" in facts:
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "AI usage is evident, but provider/model/data-flow inventory evidence is incomplete.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No AI usage was detected.")


def check_authz_tests(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    tests: List[str] = []
    authz_impl: List[str] = []
    auth_rx = re.compile(r"\b(authori[sz]e|permission|role|rbac|acl|forbidden|unauthori[sz]ed|403)\b", re.I)
    for p in _text_files(project):
        rel = _safe_rel(p, project)
        txt = _read_text(p, 500_000)
        if not txt or not auth_rx.search(txt):
            continue
        if re.search(r"(^|/)(test|tests|__tests__|spec)(/|_)|\.(test|spec)\.", rel, re.I):
            tests.append(rel)
        else:
            authz_impl.append(rel)
        if len(tests) >= 20 and len(authz_impl) >= 20:
            break
    ev: List[dict] = []
    if tests:
        ev.append(make_evidence("TEST_RESULT", "E1_STATIC", "builtin.authz_test_discovery", f"Authorization-related deterministic test source found in {tests[:10]}.", digest_payload=tests, authority=.8, confidence=.88))
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "Authorization decision tests are present in the source tree. This proves test presence, not runtime success.")
    if authz_impl or "has_auth" in facts:
        ev.append(make_evidence("OBSERVATION", "E1_STATIC", "builtin.authz_test_discovery", f"Authorization/authentication implementation signals exist but no authorization test source was found. Implementation files: {authz_impl[:8]}.", digest_payload=authz_impl, authority=.75, confidence=.8))
        return _eval(control, applicability, "FAIL", "E1_STATIC", ev, "Authorization behavior is present but deterministic authorization tests were not located.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No authorization/authentication surface was detected.")


def check_accessibility_scan(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    tooling = _find_patterns(project, [r"@axe-core", r"axe-core", r"pa11y", r"lighthouse", r"toHaveNoViolations", r"accessibility.*test"], 25)
    reports = [p for p in _iter_project_files(project) if re.search(r"(axe|pa11y|lighthouse|accessibility|a11y).*(report|result).*\.(json|html)$", p.name, re.I)]
    unresolved = 0
    inspected_reports: List[str] = []
    for p in reports[:15]:
        rel = _safe_rel(p, project)
        inspected_reports.append(rel)
        txt = _read_text(p, 2_000_000)
        if re.search(r'"impact"\s*:\s*"(?:serious|critical)"', txt, re.I):
            unresolved += 1
        if re.search(r'"violations"\s*:\s*\[\s*\]', txt):
            continue
    ev: List[dict] = []
    if tooling:
        ev.append(make_evidence("CONFIG", "E1_STATIC", "builtin.a11y_scan", f"Accessibility automation tooling/config detected in {tooling[:10]}.", digest_payload=tooling, authority=.8, confidence=.85))
    if inspected_reports:
        ev.append(make_evidence("TEST_RESULT", "E2_TESTED", "builtin.a11y_scan", f"Accessibility report artifact(s) inspected: {inspected_reports[:10]}; reports with serious/critical tokens: {unresolved}.", digest_payload={"reports": inspected_reports, "unresolved": unresolved}, authority=.85, confidence=.82))
        if unresolved:
            return _eval(control, applicability, "FAIL", "E2_TESTED", ev, "Accessibility result artifacts contain serious/critical violation signals.")
        return _eval(control, applicability, "PASS", "E2_TESTED", ev, "Accessibility result artifacts were found without serious/critical violation signals.")
    if tooling:
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "Accessibility tooling is configured, but no result artifact was available to verify unresolved high-impact issues.")
    if "has_web_ui" in facts or "has_human_ui" in facts:
        return _eval(control, applicability, "FAIL", "E1_STATIC", [make_evidence("OBSERVATION", "E1_STATIC", "builtin.a11y_scan", "Web/human UI detected without recognizable automated accessibility tooling or result artifact.", authority=.7, confidence=.75)], "No automated accessibility scan evidence was found for the detected UI surface.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No web/human UI fact was detected.")


def check_api_breaking(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    tools = _find_patterns(project, [r"oasdiff", r"openapi-diff", r"optic", r"breaking.*openapi", r"api.*breaking.*change"], 20)
    baseline = [p for p in _iter_project_files(project) if re.search(r"(openapi|swagger|asyncapi).*(baseline|previous|golden)|baseline.*(openapi|swagger|asyncapi)", _safe_rel(p, project), re.I)]
    ev: List[dict] = []
    if tools:
        ev.append(make_evidence("CONFIG", "E1_STATIC", "builtin.api_breaking", f"API breaking-change tooling/config detected in {tools[:10]}.", digest_payload=tools, authority=.8, confidence=.85))
    if baseline:
        rels = [_safe_rel(p, project) for p in baseline[:10]]
        ev.append(make_evidence("BASELINE", "E1_STATIC", "builtin.api_breaking", f"API baseline artifact(s) detected: {rels}.", digest_payload=rels, authority=.8, confidence=.85))
    if tools and baseline:
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "API contract breaking-change comparison has both tooling/config and a baseline signal.")
    if tools or baseline:
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "Some breaking-change comparison evidence exists, but tooling or baseline evidence is missing.")
    if "has_api" in facts:
        return _eval(control, applicability, "FAIL", "E1_STATIC", [make_evidence("OBSERVATION", "E1_STATIC", "builtin.api_breaking", "API surface detected without recognizable breaking-change comparison tooling/baseline.", authority=.7, confidence=.78)], "No API breaking-change baseline mechanism was found.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No API fact was detected.")


def check_arch_ownership(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    rels = _all_relative(project)
    owners = [r for r in rels if r.endswith("codeowners") or r.endswith("owners")]
    manifests, locks = _manifest_and_lock(project)
    arch_docs = [r for r in rels if re.search(r"(^|/)(architecture|docs/architecture|adr|docs/adr)(/|\.|$)", r, re.I)]
    ev = []
    if owners:
        ev.append(make_evidence("CONFIG", "E1_STATIC", "builtin.arch_ownership", f"Ownership metadata found: {owners[:8]}.", digest_payload=owners, authority=.85, confidence=.9))
    if manifests or arch_docs:
        ev.append(make_evidence("DOCUMENTATION", "E1_STATIC", "builtin.arch_ownership", f"Dependency/architecture boundary evidence: manifests={manifests}, architecture_docs={arch_docs[:8]}.", digest_payload={"manifests": manifests, "docs": arch_docs}, authority=.8, confidence=.85))
    if owners and (manifests or arch_docs):
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "Ownership and dependency/architecture boundary evidence are both explicit.")
    if owners or manifests or arch_docs:
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "Only part of dependency/ownership boundary evidence is explicit.")
    return _eval(control, applicability, "FAIL", "E1_STATIC", [make_evidence("OBSERVATION", "E1_STATIC", "builtin.arch_ownership", "No ownership file, recognized dependency manifest, or architecture boundary documentation was found.", authority=.65, confidence=.72)], "Critical dependency/ownership boundaries are not explicit in the inspected tree.")


def check_data_schema(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    rels = _all_relative(project)
    schema = [r for r in rels if re.search(r"(schema\.prisma|/migrations?/|^migrations?/|schema\.(sql|graphql|json)|models?\.(py|ts|js)|entities?/)", r, re.I)]
    invariant = _find_patterns(project, [r"\b(check constraint|unique constraint|foreign key|not null|zod|joi|pydantic|validator|invariant)\b"], 25)
    ev: List[dict] = []
    if schema:
        ev.append(make_evidence("SCHEMA", "E1_STATIC", "builtin.data_schema", f"Schema/model/migration artifacts detected: {schema[:12]}.", digest_payload=schema, authority=.85, confidence=.9))
    if invariant:
        ev.append(make_evidence("CONFIG", "E1_STATIC", "builtin.data_schema", f"Invariant/validation signals detected in: {invariant[:10]}.", digest_payload=invariant, authority=.8, confidence=.82))
    if schema and invariant:
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "Data schema artifacts and explicit invariant/validation signals are present.")
    if schema:
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "Data schema artifacts exist, but explicit invariants were not located.")
    if "has_persistent_data" in facts or "has_backend" in facts:
        return _eval(control, applicability, "FAIL", "E1_STATIC", [make_evidence("OBSERVATION", "E1_STATIC", "builtin.data_schema", "Backend/persistent-data surface detected without recognizable schema/model/migration artifacts.", authority=.7, confidence=.75)], "Data schema and invariants are not explicit in the inspected tree.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No persistent-data surface was detected.")


def check_security_headers(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    signals = {
        "content-security-policy": [], "x-content-type-options": [],
        "referrer-policy": [], "strict-transport-security": [],
    }
    for p in _text_files(project):
        rel = _safe_rel(p, project)
        txt = _read_text(p, 500_000).lower()
        if not txt:
            continue
        for key in signals:
            if key in txt or (key == "content-security-policy" and "contentsecuritypolicy" in txt):
                signals[key].append(rel)
    present = [k for k, v in signals.items() if v]
    ev = [make_evidence("CONFIG", "E1_STATIC", "builtin.security_headers", f"Security header signals present: {present}; missing: {[k for k in signals if k not in present]}.", digest_payload=signals, authority=.8, confidence=.84)]
    if len(present) >= 3:
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "At least three major production security-header controls are explicitly configured.")
    if len(present) >= 1:
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "Some production security headers are explicit, but coverage is incomplete.")
    if "has_web_ui" in facts or "production_service" in facts:
        return _eval(control, applicability, "FAIL", "E1_STATIC", ev, "No recognized production security-header configuration was found for the detected web/production surface.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No web/production surface was detected.")


def check_perf_baseline(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    perf = _find_patterns(project, [r"lighthouse", r"web-vitals", r"k6", r"benchmark", r"performance budget", r"budgets\.json", r"autocannon", r"wrk"], 25)
    baselines = [p for p in _iter_project_files(project) if re.search(r"(perf|performance|lighthouse|benchmark).*(baseline|budget|golden|threshold)|baseline.*(perf|performance|lighthouse|benchmark)", _safe_rel(p, project), re.I)]
    relb = [_safe_rel(p, project) for p in baselines[:15]]
    ev = []
    if perf:
        ev.append(make_evidence("CONFIG", "E1_STATIC", "builtin.performance_baseline", f"Performance tooling/config detected in {perf[:10]}.", digest_payload=perf, authority=.8, confidence=.82))
    if relb:
        ev.append(make_evidence("BASELINE", "E1_STATIC", "builtin.performance_baseline", f"Performance baseline/budget artifacts detected: {relb}.", digest_payload=relb, authority=.82, confidence=.86))
    if perf and relb:
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "Performance test/tooling evidence and a baseline/budget signal are both present.")
    if perf or relb:
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "Performance regression evidence is incomplete: tooling/config or baseline/budget is missing.")
    return _eval(control, applicability, "FAIL", "E1_STATIC", [make_evidence("OBSERVATION", "E1_STATIC", "builtin.performance_baseline", "No recognized performance regression tooling or baseline/budget artifact was found.", authority=.65, confidence=.72)], "Performance regressions are not demonstrably compared against a baseline.")


def check_resilience_bounds(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    timeout_files: List[str] = []
    retry_files: List[str] = []
    bounded_retry_files: List[str] = []
    timeout_rx = re.compile(r"\b(timeout|connecttimeout|readtimeout|requesttimeout)\b.{0,80}\b\d{2,}\b", re.I | re.S)
    retry_rx = re.compile(r"\b(retr(?:y|ies)|maxretries|max_retries|retrycount|retry_count)\b", re.I)
    bounded_rx = re.compile(r"\b(maxretries|max_retries|retrycount|retry_count|attempts|maxattempts|max_attempts)\b.{0,60}\b\d+\b", re.I | re.S)
    for p in _text_files(project):
        rel = _safe_rel(p, project)
        txt = _read_text(p, 500_000)
        if timeout_rx.search(txt):
            timeout_files.append(rel)
        if retry_rx.search(txt):
            retry_files.append(rel)
        if bounded_rx.search(txt):
            bounded_retry_files.append(rel)
        if len(timeout_files) >= 20 and len(bounded_retry_files) >= 20:
            break
    ev: List[dict] = []
    if timeout_files:
        ev.append(make_evidence("CONFIG", "E1_STATIC", "builtin.resilience_bounds", f"Bounded timeout signals found in {timeout_files[:10]}.", digest_payload=timeout_files, authority=.8, confidence=.82))
    if bounded_retry_files:
        ev.append(make_evidence("CONFIG", "E1_STATIC", "builtin.resilience_bounds", f"Bounded retry/attempt signals found in {bounded_retry_files[:10]}.", digest_payload=bounded_retry_files, authority=.8, confidence=.82))
    elif retry_files:
        ev.append(make_evidence("OBSERVATION", "E1_STATIC", "builtin.resilience_bounds", f"Retry signals found without an obvious numeric bound in {retry_files[:10]}.", digest_payload=retry_files, authority=.75, confidence=.78))
    if timeout_files and bounded_retry_files:
        return _eval(control, applicability, "PASS", "E1_STATIC", ev, "Timeout and retry policies both show explicit bounded configuration signals.")
    if timeout_files or bounded_retry_files:
        return _eval(control, applicability, "PARTIAL", "E1_STATIC", ev, "Only timeout or retry bounds are explicit; full resilience-bound evidence is incomplete.")
    if retry_files:
        return _eval(control, applicability, "FAIL", "E1_STATIC", ev, "Retry behavior exists without a recognizable explicit bound and no bounded timeout signal was found.")
    if "has_backend" in facts or "has_api" in facts:
        return _eval(control, applicability, "FAIL", "E1_STATIC", [make_evidence("OBSERVATION", "E1_STATIC", "builtin.resilience_bounds", "Backend/API detected without explicit bounded timeout/retry policy signals.", authority=.7, confidence=.72)], "No bounded timeout/retry policy evidence was found for the backend/API surface.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "No backend/API surface was detected.")


BUILTIN_CHECKS = {
    "builtin.secret_scan": check_secret_scan,
    "builtin.security_headers": check_security_headers,
    "builtin.api_contract": check_api_contract,
    "builtin.api_breaking_baseline": check_api_breaking,
    "builtin.dependency_inventory": check_supply_inventory,
    "builtin.license_metadata": check_license,
    "builtin.environment_config": check_env_secret_safe,
    "builtin.production_debug": check_debug_disabled,
    "builtin.ai_inventory": check_ai_inventory,
    "builtin.authz_tests": check_authz_tests,
    "builtin.a11y_scan_evidence": check_accessibility_scan,
    "builtin.arch_ownership": check_arch_ownership,
    "builtin.data_schema": check_data_schema,
    "builtin.performance_baseline": check_perf_baseline,
    "builtin.resilience_bounds": check_resilience_bounds,
}


def execute_control(project: Path, control: dict, applicability: str, facts: set[str]) -> dict:
    if applicability == "NOT_APPLICABLE":
        return _eval(control, applicability, "NOT_APPLICABLE", "E0_CLAIM_ONLY", [], "Control is not applicable according to the applicability engine.")
    detectors = control.get("detectors", [])
    for detector_id in detectors:
        fn = BUILTIN_CHECKS.get(detector_id)
        if fn:
            return fn(project, control, applicability, facts)
    # Conservative fallback: no automated detector = no automatic PASS.
    if control.get("automation") == "AUTOMATED":
        return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "Automated control has no executable built-in detector in this runtime.")
    return _eval(control, applicability, "NOT_TESTED", "E0_CLAIM_ONLY", [], "Control requires manual, semi-automated, runtime, legal, or real-world evidence.")


# ------------------------- evidence import -------------------------

def load_external_evaluations(path: Optional[str]) -> Dict[str, dict]:
    if not path:
        return {}
    d = _load_json(path)
    rows = d.get("evaluations", d if isinstance(d, list) else [])
    out: Dict[str, dict] = {}
    for row in rows:
        cid = row.get("control_id")
        if not cid:
            continue
        status = row.get("status", "NOT_TESTED")
        level = row.get("evidence_level", "E0_CLAIM_ONLY")
        if status not in VALID_EVAL_STATUSES:
            raise ValueError(f"Invalid status for {cid}: {status}")
        if level not in EVIDENCE_RANK:
            raise ValueError(f"Invalid evidence_level for {cid}: {level}")
        out[cid] = row
    return out


def merge_external_evaluation(base: dict, supplied: Optional[dict]) -> dict:
    if not supplied:
        return base
    status = supplied.get("status", base["status"])
    level = supplied.get("evidence_level", base["evidence_level"])
    # FAIL from either source is never hidden without an explicit override.
    if base["status"] == "FAIL" and status == "PASS" and not supplied.get("override", False):
        status = "FAIL"
        level = base["evidence_level"]
    if EVIDENCE_RANK.get(level, 0) < EVIDENCE_RANK.get(base["evidence_level"], 0) and not supplied.get("override", False):
        level = base["evidence_level"]
    ev = list(base.get("evidence", []))
    for item in supplied.get("evidence", []):
        if isinstance(item, dict) and {"id", "type", "level", "source", "summary", "freshness", "authority", "confidence"} <= set(item):
            ev.append(item)
        else:
            ev.append(make_evidence(
                supplied.get("evidence_type", "USER_EVIDENCE"),
                supplied.get("evidence_level", "E1_STATIC"),
                supplied.get("source", "evidence-import"),
                str(item) if not isinstance(item, dict) else item.get("summary", "Imported evidence"),
                location=item.get("location") if isinstance(item, dict) else None,
                digest_payload=item,
                authority=float(supplied.get("authority", .8)),
                confidence=float(supplied.get("confidence", .8)),
            ))
    if not supplied.get("evidence") and supplied.get("summary"):
        ev.append(make_evidence(
            supplied.get("evidence_type", "USER_EVIDENCE"), level,
            supplied.get("source", "evidence-import"), supplied["summary"],
            location=supplied.get("location"), digest_payload=supplied.get("summary"),
            authority=float(supplied.get("authority", .8)), confidence=float(supplied.get("confidence", .8)),
        ))
    merged = dict(base)
    merged.update({
        "status": status,
        "evidence_level": level,
        "evidence": ev,
        "summary": supplied.get("summary", base.get("summary", "")),
        "source_method": "evidence-import+" + base.get("source_method", "builtin"),
    })
    return merged


# ------------------------- adapters -------------------------

def detect_adapters() -> List[dict]:
    out = []
    for a in load_adapters():
        executable = None
        for exe in a.get("detect", {}).get("executables", []):
            hit = shutil.which(exe)
            if hit:
                executable = hit
                break
        version = None
        if executable:
            try:
                cp = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=4, check=False)
                version = (cp.stdout or cp.stderr).strip().splitlines()[0][:300] if (cp.stdout or cp.stderr).strip() else None
            except Exception:
                version = None
        out.append({
            "id": a["id"], "available": bool(executable), "executable": executable,
            "version": version, "capabilities": a.get("capabilities", []),
            "network_intent": a.get("network_intent", {}),
            "execution": "OPT_IN",
        })
    return out


def _run_cmd(cmd: List[str], cwd: Path, timeout: int = 120) -> Tuple[int, str, str]:
    cp = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, check=False)
    return cp.returncode, cp.stdout, cp.stderr


def run_safe_adapter(adapter_id: str, project: Path) -> dict:
    """Run only explicitly supported no-network adapters. Caller must opt in."""
    inventory = {x["id"]: x for x in detect_adapters()}
    info = inventory.get(adapter_id)
    if not info:
        return {"id": adapter_id, "status": "UNKNOWN_ADAPTER"}
    if not info["available"]:
        return {"id": adapter_id, "status": "UNAVAILABLE"}
    if info.get("network_intent", {}).get("network_required"):
        return {"id": adapter_id, "status": "NETWORK_AUTHORIZATION_REQUIRED"}
    exe = info["executable"]
    try:
        if adapter_id == "syft":
            rc, out, err = _run_cmd([exe, f"dir:{project}", "-o", "cyclonedx-json"], project, 180)
            parsed = json.loads(out) if out.strip() else {}
            return {"id": adapter_id, "status": "PASS" if rc == 0 else "ERROR", "returncode": rc,
                    "summary": f"SBOM components: {len(parsed.get('components', []))}" if isinstance(parsed, dict) else "SBOM generated",
                    "raw_output_digest": hashlib.sha256(out.encode()).hexdigest(), "stderr": err[-1000:]}
        if adapter_id == "gitleaks":
            with tempfile.TemporaryDirectory() as td:
                report = Path(td) / "gitleaks.json"
                cmd = [exe, "detect", "--source", str(project), "--no-banner", "--report-format", "json", "--report-path", str(report)]
                rc, out, err = _run_cmd(cmd, project, 180)
                rows = _load_json(report) if report.exists() else []
                if not isinstance(rows, list):
                    rows = []
                if rows:
                    status = "FINDINGS"
                elif rc == 0:
                    status = "PASS"
                else:
                    status = "ERROR"
                return {"id": adapter_id, "status": status, "returncode": rc,
                        "summary": f"gitleaks findings: {len(rows)}",
                        "raw_output_digest": hashlib.sha256((out + err).encode()).hexdigest()}
        return {"id": adapter_id, "status": "AVAILABLE_NOT_IMPLEMENTED_IN_LOCAL_PROJECT_MODE",
                "reason": "Adapter is discovered and declared, but needs a target URL, test suite, script, or explicit network-capable mode."}
    except subprocess.TimeoutExpired:
        return {"id": adapter_id, "status": "TIMEOUT"}
    except Exception as exc:
        return {"id": adapter_id, "status": "ERROR", "error": str(exc)[:500]}


# ------------------------- findings, scores, maturity -------------------------

def make_finding(control: dict, evaluation: dict, project: Path) -> dict:
    ev = evaluation.get("evidence", [])
    location = next((x.get("location") for x in ev if x.get("location")), None)
    f = {
        "id": "FND-" + hashlib.sha256(f"{control['id']}|{evaluation['status']}|{location}".encode()).hexdigest()[:16],
        "audit_domain": control["domain"], "control_id": control["id"], "title": control["title"],
        "description": evaluation.get("summary", control.get("description", "")),
        "severity": control.get("severity_default", "MEDIUM"),
        "confidence": round(max([x.get("confidence", .6) for x in ev] or [.6]), 3),
        "applicability": evaluation.get("applicability", "UNKNOWN"),
        "evidence_level": evaluation.get("evidence_level", "E0_CLAIM_ONLY"),
        "evidence": ev,
        "affected_asset": project.name,
        "location": location,
        "business_impact": f"Readiness risk in {control['domain']}; verify impact against the product/business context.",
        "technical_impact": control.get("description", "Control requirement is not fully satisfied."),
        "operational_impact": "May create deployment, support, reliability, compliance, or delivery uncertainty depending on scope.",
        "remediation": control.get("checks", ["Provide the required evidence and close the control gap."])[0],
        "estimated_effort": None,
        "automation_level": control.get("automation", "MANUAL"),
        "source_method": evaluation.get("source_method", "builtin"),
        "standard_refs": control.get("references", []),
        "fingerprint": "",
        "first_seen": _now(), "last_seen": _now(), "status": "OPEN",
    }
    f["fingerprint"] = fingerprint(f)
    return f


def apply_adapter_runs(evals: List[dict], adapter_runs: List[dict]) -> List[dict]:
    """Attach explicitly authorized adapter evidence to the matching control evaluations."""
    by_id = {e["control_id"]: e for e in evals}
    for run in adapter_runs:
        aid = run.get("id")
        status = run.get("status")
        if aid == "gitleaks" and status in {"PASS", "FINDINGS"} and "BR360-SEC-002" in by_id:
            row = by_id["BR360-SEC-002"]
            if row["applicability"] == "NOT_APPLICABLE":
                continue
            ev = make_evidence(
                "EXTERNAL_TOOL_RESULT", "E2_TESTED", "adapter.gitleaks",
                run.get("summary", "gitleaks completed"),
                digest_payload={"digest": run.get("raw_output_digest"), "status": status},
                authority=.95, confidence=.95,
            )
            row["evidence"] = list(row.get("evidence", [])) + [ev]
            if status == "FINDINGS":
                row["status"] = "FAIL"
                row["summary"] = "Authorized gitleaks execution reported one or more secret findings."
            elif row["status"] != "FAIL":
                row["status"] = "PASS"
                row["summary"] = "Authorized gitleaks execution completed without reported secret findings."
            row["evidence_level"] = "E2_TESTED"
            row["source_method"] = row.get("source_method", "builtin") + "+adapter.gitleaks"
        elif aid == "syft" and status == "PASS" and "BR360-SC-002" in by_id:
            row = by_id["BR360-SC-002"]
            if row["applicability"] == "NOT_APPLICABLE":
                continue
            ev = make_evidence(
                "SBOM", "E2_TESTED", "adapter.syft", run.get("summary", "Syft SBOM generated"),
                digest_payload={"digest": run.get("raw_output_digest"), "status": status},
                authority=.95, confidence=.95,
            )
            row["evidence"] = list(row.get("evidence", [])) + [ev]
            if row["status"] != "FAIL":
                row["status"] = "PASS"
                row["summary"] = "Authorized Syft execution produced a CycloneDX JSON SBOM."
            row["evidence_level"] = "E2_TESTED"
            row["source_method"] = row.get("source_method", "builtin") + "+adapter.syft"
    return evals


def _coverage(evals: List[dict]) -> dict:
    applicable = [e for e in evals if e["applicability"] != "NOT_APPLICABLE"]
    completed = lambda rows: [e for e in rows if e["status"] in {"PASS", "PARTIAL", "FAIL"}]
    auto = [e for e in applicable if e["automation"] == "AUTOMATED"]
    manual = [e for e in applicable if e["automation"] in {"MANUAL", "SEMI_AUTOMATED", "LEGAL_REVIEW", "EXTERNAL_RESEARCH"}]
    rw = [e for e in applicable if e["automation"] == "REAL_WORLD_REQUIRED"]
    def ratio(rows: List[dict]) -> float:
        return round(len(completed(rows)) / len(rows), 4) if rows else 1.0
    return {"automated": ratio(auto), "manual": ratio(manual), "real_world": ratio(rw), "overall": ratio(applicable)}


def _confidence_and_strength(evals: List[dict]) -> Tuple[float, float]:
    applicable = [e for e in evals if e["applicability"] != "NOT_APPLICABLE"]
    if not applicable:
        return 0.0, 0.0
    completed = [e for e in applicable if e["status"] in {"PASS", "PARTIAL", "FAIL"}]
    coverage = len(completed) / len(applicable)
    strength = sum(EVIDENCE_RANK.get(e.get("evidence_level"), 0) / 4 for e in applicable) / len(applicable)
    evidence_conf = []
    for e in applicable:
        if e.get("evidence"):
            evidence_conf.extend(x.get("confidence", .5) for x in e["evidence"])
    raw_conf = sum(evidence_conf) / len(evidence_conf) if evidence_conf else .25
    confidence = 10 * coverage * (.55 + .45 * raw_conf)
    return round(min(10, confidence), 2), round(10 * strength, 2)


def maturity(evals: List[dict], scores: dict, coverage: dict) -> dict:
    r = scores.get("readiness", 0)
    v = scores.get("verification", 0)
    rw_controls = [e for e in evals if e["applicability"] != "NOT_APPLICABLE" and e["automation"] == "REAL_WORLD_REQUIRED"]
    rw = scores.get("real_world_evidence", 0)
    cov = coverage.get("overall", 0)
    if r >= 9 and v >= 8 and cov >= .90 and (not rw_controls or rw >= 8):
        level = 5
    elif r >= 7.5 and v >= 6 and cov >= .80:
        level = 4
    elif r >= 6 and cov >= .60:
        level = 3
    elif r >= 4 and cov >= .40:
        level = 2
    elif r > 0 or cov >= .15:
        level = 1
    else:
        level = 0
    names = {0: "ABSENT", 1: "AD_HOC", 2: "REPEATABLE", 3: "DEFINED", 4: "MEASURED", 5: "OPTIMIZED"}
    return {"level": level, "name": names[level]}


def _actions(findings: List[dict], evals: List[dict]) -> List[dict]:
    actions = []
    for f in findings:
        actions.append({
            "priority": f["severity"], "control_id": f["control_id"], "domain": f["audit_domain"],
            "action": f["remediation"], "reason": f["description"], "fingerprint": f["fingerprint"],
        })
    # Missing evidence is an action but not automatically a defect finding.
    for e in evals:
        if e["applicability"] != "NOT_APPLICABLE" and e["status"] == "NOT_TESTED":
            actions.append({"priority": "INFO", "control_id": e["control_id"], "domain": e["domain"],
                            "action": "Collect the required manual/runtime/real-world evidence and evaluate this control.",
                            "reason": e["summary"], "fingerprint": None})
    actions.sort(key=lambda x: (-SEVERITY_RANK.get(x["priority"], 0), x["control_id"]))
    return actions


def _final_status(scores: dict, evals: List[dict], findings: List[dict]) -> dict:
    critical_fail = any(f["severity"] == "CRITICAL" for f in findings)
    any_fail = any(e["status"] == "FAIL" for e in evals if e["applicability"] != "NOT_APPLICABLE")
    not_tested = sum(1 for e in evals if e["applicability"] != "NOT_APPLICABLE" and e["status"] == "NOT_TESTED")
    if critical_fail or scores["readiness"] < 4:
        status = "FAIL"
    elif not any_fail and not_tested == 0 and scores["readiness"] >= 8:
        status = "PASS"
    else:
        status = "PARTIAL"
    return {"status": status, "summary": f"Readiness {scores['readiness']}/10; {len(findings)} open gap finding(s); {not_tested} applicable control(s) still not tested."}


def audit(project: Path | str, profile: str = "AUTO", evidence_path: Optional[str] = None,
          allowed_adapters: Optional[List[str]] = None) -> dict:
    project = Path(project).resolve()
    if not project.exists() or not project.is_dir():
        raise FileNotFoundError(f"Project directory not found: {project}")
    det = detect_project(project)
    selected = select_controls(det["facts"], profile)
    control_map = {c["id"]: c for c in load_controls()}
    supplied = load_external_evaluations(evidence_path)
    facts = set(det["facts"])
    evals: List[dict] = []
    for row in selected:
        c = control_map[row["control_id"]]
        base = execute_control(project, c, row["applicability"], facts)
        evals.append(merge_external_evaluation(base, supplied.get(c["id"])))

    adapter_inventory = detect_adapters()
    adapter_runs = []
    for aid in allowed_adapters or []:
        adapter_runs.append(run_safe_adapter(aid, project))
    evals = apply_adapter_runs(evals, adapter_runs)

    findings = [make_finding(control_map[e["control_id"]], e, project) for e in evals if e["status"] in {"FAIL", "PARTIAL"}]
    sc = score(evals)
    cov = _coverage(evals)
    confidence, strength = _confidence_and_strength(evals)
    scores = {k: sc[k] for k in ["implementation", "verification", "real_world_evidence", "readiness"]}
    scores["confidence"] = confidence
    scores["evidence_strength"] = strength
    mat = maturity(evals, scores, cov)

    rw_missing = [e["control_id"] for e in evals if e["automation"] == "REAL_WORLD_REQUIRED" and e["applicability"] != "NOT_APPLICABLE" and e["evidence_level"] != "E4_REAL_WORLD"]
    manual_missing = [e["control_id"] for e in evals if e["applicability"] != "NOT_APPLICABLE" and e["status"] == "NOT_TESTED"]
    evidence = []
    for e in evals:
        evidence.extend(e.get("evidence", []))
    # de-duplicate evidence by id
    evidence = list({x["id"]: x for x in evidence}.values())
    blockers = [f["control_id"] for f in findings if f["severity"] == "CRITICAL"]
    result = {
        "schema": SCHEMA_VERSION,
        "pack_version": PACK_VERSION,
        "audit": {"id": "br360-" + hashlib.sha256(f"{project}|{_now()}".encode()).hexdigest()[:12], "mode": "READ_ONLY", "profile": profile, "created_at": _now(), "network_intent": [x.get("network_intent", {}) for x in adapter_inventory if x["id"] in (allowed_adapters or [])]},
        "project_profile": det,
        "applicability": {"controls": selected},
        "evaluations": evals,
        "evidence": evidence,
        "coverage": cov,
        "scores": scores,
        "maturity": mat,
        "findings": findings,
        "actions": _actions(findings, evals),
        "blockers": blockers,
        "audit_self_evaluation": {
            "audit_coverage": cov["overall"], "audit_confidence": round(confidence / 10, 4),
            "missing_tools": [], "missing_access": [], "missing_real_world_data": rw_missing,
            "unverified_assumptions": [f"{len(manual_missing)} applicable controls remain NOT_TESTED." ] if manual_missing else [],
            "license_review_gaps": [e["control_id"] for e in evals if e["domain"] == "licensing" and e["status"] == "NOT_TESTED"],
        },
        "final": _final_status(scores, evals, findings),
        "extensions": {"adapters": {"inventory": adapter_inventory, "runs": adapter_runs}, "engine": {"built_in_detectors": sorted(BUILTIN_CHECKS), "detector_catalog_count": len(load_detector_catalog())}},
    }
    return result


def preanalyse(project: Path | str, profile: str = "AUTO") -> dict:
    det = detect_project(project)
    selected = select_controls(det["facts"], profile)
    return {
        "schema": SCHEMA_VERSION, "pack_version": PACK_VERSION,
        "audit": {"id": "local-preanalysis", "mode": "READ_ONLY", "profile": profile, "created_at": _now(), "network_intent": []},
        "project_profile": det, "applicability": {"controls": selected},
        "coverage": {"automated": 0, "manual": 0, "real_world": 0, "overall": 0},
        "scores": {"implementation": 0, "verification": 0, "real_world_evidence": 0, "readiness": 0, "confidence": 0, "evidence_strength": 0},
        "maturity": {"level": 0, "name": "ABSENT"}, "evaluations": [], "evidence": [], "findings": [], "actions": [], "blockers": [],
        "audit_self_evaluation": {"audit_coverage": 0, "audit_confidence": 0, "missing_tools": [], "missing_access": [], "missing_real_world_data": [], "unverified_assumptions": ["Pre-analysis only; no checks executed."], "license_review_gaps": []},
        "final": {"status": "PARTIAL", "summary": "Pre-analysis only; selected controls are not evidence of PASS."}, "extensions": {},
    }


def _write_or_print(value: dict, out: Optional[str]) -> None:
    s = json.dumps(value, indent=2, ensure_ascii=False)
    if out:
        Path(out).write_text(s + "\n", encoding="utf-8")
    else:
        print(s)


def selftest() -> dict:
    controls = load_controls()
    ids = [c["id"] for c in controls]
    automated = [c for c in controls if c.get("automation") == "AUTOMATED"]
    missing_detectors = [c["id"] for c in automated if not any(x in BUILTIN_CHECKS for x in c.get("detectors", []))]
    checks = {
        "controls_present": len(controls) >= 100,
        "control_ids_unique": len(ids) == len(set(ids)),
        "automated_controls_have_builtin_detectors": not missing_detectors,
        "profiles_present": bool(load_profiles()),
        "adapters_present": bool(load_adapters()),
        "detector_catalog_present": bool(load_detector_catalog()),
    }
    return {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
            "counts": {"controls": len(controls), "automated_controls": len(automated), "builtin_detectors": len(BUILTIN_CHECKS), "adapters": len(load_adapters())},
            "missing_detectors": missing_detectors}


def main() -> None:
    # Backward compatibility: V2 accepted only --project/--profile/--out and performed pre-analysis.
    if len(os.sys.argv) > 1 and os.sys.argv[1].startswith("--"):
        ap = argparse.ArgumentParser(description="BR360 V3 (V2-compatible pre-analysis mode)")
        ap.add_argument("--project", default=".")
        ap.add_argument("--profile", default="AUTO")
        ap.add_argument("--out")
        args = ap.parse_args()
        _write_or_print(preanalyse(args.project, args.profile), args.out)
        return

    ap = argparse.ArgumentParser(description="AXDIA Business Readiness 360 V3")
    sp = ap.add_subparsers(dest="command", required=True)

    pa = sp.add_parser("audit", help="Run the read-only V3 audit engine")
    pa.add_argument("--project", default=".")
    pa.add_argument("--profile", default="AUTO")
    pa.add_argument("--evidence", help="JSON file with manual/runtime/real-world evaluations")
    pa.add_argument("--allow-adapter", action="append", default=[], help="Explicitly opt in to a supported local read-only adapter (repeatable)")
    pa.add_argument("--out")

    pp = sp.add_parser("preanalyse", help="Detect project facts and select applicable controls without executing checks")
    pp.add_argument("--project", default=".")
    pp.add_argument("--profile", default="AUTO")
    pp.add_argument("--out")

    pc = sp.add_parser("compare", help="Compare two BR360 result JSON files")
    pc.add_argument("--before", required=True)
    pc.add_argument("--after", required=True)
    pc.add_argument("--out")

    pad = sp.add_parser("adapters", help="List adapter availability without running adapters")
    pad.add_argument("--out")

    ps = sp.add_parser("selftest", help="Validate V3 runtime wiring")
    ps.add_argument("--out")

    args = ap.parse_args()
    if args.command == "audit":
        _write_or_print(audit(args.project, args.profile, args.evidence, args.allow_adapter), args.out)
    elif args.command == "preanalyse":
        _write_or_print(preanalyse(args.project, args.profile), args.out)
    elif args.command == "compare":
        _write_or_print(compare(_load_json(args.before), _load_json(args.after)), args.out)
    elif args.command == "adapters":
        _write_or_print({"pack_version": PACK_VERSION, "adapters": detect_adapters()}, args.out)
    elif args.command == "selftest":
        _write_or_print(selftest(), args.out)


if __name__ == "__main__":
    main()
