#!/usr/bin/env python3
"""
Sherlock Pipeline Harness — behavioral checks for pipeline run artifacts.
Usage: python pipeline_harness.py <command> [args]

Commands:
  check [run_dir] [--skill-dir DIR] — validate one run's artifacts, write harness-result.json into run_dir
  summarize <results_dir>           — aggregate archived runs (run-*/), print markdown baseline
"""
import sys, json, re
from pathlib import Path

SKILL_DIR_DEFAULT = ".claude/skills/sherlock"


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def expected_personas(run_dir):
    log = load_json(Path(run_dir) / "run-log.json")
    if not isinstance(log, dict):
        return []
    return [a.get("name") for a in log.get("agents", [])
            if a.get("role") == "persona" and a.get("name") and a.get("name") != "baseline"]


def check_demands(run_dir, personas):
    data = load_json(Path(run_dir) / "quant-demands.json")
    result = {"pass": False, "personas_expected": list(personas),
              "personas_submitted": [], "missing": [], "malformed": []}
    if data is None:
        result["missing"] = list(personas)
        return result
    demands = data.get("demands", []) if isinstance(data, dict) else []
    submitted = set()
    for d in demands:
        persona = d.get("persona", "")
        if not d.get("computation") or not d.get("rationale"):
            result["malformed"].append(persona or "<unknown>")
        else:
            submitted.add(persona)
    result["personas_submitted"] = sorted(submitted)
    result["missing"] = [p for p in personas if p not in submitted]
    result["pass"] = not result["missing"] and not result["malformed"]
    return result


REQUIRED_ANALYSIS_KEYS = ("requested_by", "type", "results")


def check_package(run_dir, demander_names):
    path = Path(run_dir) / "quant-analysis-package.json"
    data = load_json(path)
    result = {"pass": False, "exists": path.exists(), "valid_json": data is not None,
              "analyses_count": 0, "schema_errors": [], "uncovered_personas": [],
              "status": "missing", "partial": False}
    if data is None:
        return result
    analyses = data.get("analyses", []) if isinstance(data, dict) else []
    result["analyses_count"] = len(analyses)
    covered = set()
    for i, a in enumerate(analyses):
        if not isinstance(a, dict):
            result["schema_errors"].append(f"analyses[{i}] is not an object")
            continue
        for k in REQUIRED_ANALYSIS_KEYS:
            if k not in a or a[k] in (None, "", {}, []):
                result["schema_errors"].append(f"analyses[{i}] missing/empty '{k}'")
        if a.get("requested_by"):
            covered.add(a["requested_by"])
    result["uncovered_personas"] = [p for p in demander_names if p not in covered]
    status = data.get("status", "complete") if isinstance(data, dict) else "complete"
    if status not in ("complete", "partial"):
        status = "complete"
    result["status"] = status
    result["partial"] = (status == "partial")
    result["pass"] = (result["analyses_count"] > 0
                      and not result["schema_errors"]
                      and (not result["uncovered_personas"] or result["partial"]))
    return result


def demand_personas(run_dir):
    data = load_json(Path(run_dir) / "quant-demands.json")
    if not isinstance(data, dict):
        return []
    return sorted({d.get("persona") for d in data.get("demands", []) if d.get("persona")})


COLLAPSE_MARKERS = (
    "Sherlock Analysis — Intake",
    "Proceed with this configuration",
    "Problem Map",
)
PACKAGE_REF_HINTS = ("quantitative analysis package", "requested_by")


def persona_sections(skill_dir, persona):
    path = Path(skill_dir) / "personas" / f"{persona}.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    m = re.search(r"^## Output Format\s*$", text, re.MULTILINE)
    if not m:
        return []
    return re.findall(r"^### (.+)$", text[m.end():], re.MULTILINE)


def package_numbers(run_dir):
    data = load_json(Path(run_dir) / "quant-analysis-package.json")
    if not isinstance(data, dict):
        return []
    nums = set()
    for a in data.get("analyses", []):
        blob = json.dumps(a.get("results", {}))
        nums.update(re.findall(r"-?\d+\.\d+|-?\d+", blob))
    return sorted(nums)


def _persona_file(run_dir, name, draft=False):
    suffix = "-draft" if draft else ""
    fname = f"persona-output-{name}{suffix}.md"
    for base in (Path(run_dir), Path(run_dir) / "personas"):
        p = base / fname
        if p.exists():
            return p
    return Path(run_dir) / fname  # default path for not-found reporting


def check_persona(run_dir, skill_dir, persona, ref_numbers, package_available):
    path = _persona_file(run_dir, persona)
    result = {"persona": persona, "exists": path.exists(),
              "sections_missing": [], "collapsed": False, "references_package": None}
    if not path.exists():
        result["collapsed"] = True
        return result
    text = path.read_text(encoding="utf-8")
    result["sections_missing"] = [
        s for s in persona_sections(skill_dir, persona)
        if not re.search(rf"^###\s+{re.escape(s)}\s*$", text, re.MULTILINE)]
    markers = [m for m in COLLAPSE_MARKERS if m in text]
    result["collapsed"] = len(result["sections_missing"]) >= 2 or bool(markers)
    if package_available:
        low = text.lower()
        result["references_package"] = (
            any(re.search(rf"(?<![\d.]){re.escape(n)}(?![\d.])", text) for n in ref_numbers)
            or any(h in low for h in PACKAGE_REF_HINTS))
    return result


ANNOTATION_RE = re.compile(r"\[DATA: (CONFIRMED|REVISED|UNSUPPORTED)\]")


def check_drafts(run_dir, personas):
    result = {"pass": True, "missing_drafts": []}
    for p in personas:
        path = _persona_file(run_dir, p, draft=True)
        try:
            empty = not path.read_text(encoding="utf-8").strip()
        except OSError:
            empty = True
        if empty:
            result["missing_drafts"].append(p)
    result["pass"] = not result["missing_drafts"]
    return result


def check_annotations(run_dir, personas):
    result = {"pass": True,
              "counts": {"confirmed": 0, "revised": 0, "unsupported": 0},
              "unannotated": []}
    for p in personas:
        path = _persona_file(run_dir, p)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            text = ""
        found = ANNOTATION_RE.findall(text)
        if not found:
            result["unannotated"].append(p)
        for f in found:
            result["counts"][f.lower()] += 1
    result["pass"] = not result["unannotated"]
    return result


def revision_outcomes(run_dir):
    # Names are unique per run by design (2b agents are never retried — 教训 7),
    # so the dict comprehension cannot silently collapse duplicates in practice.
    log = load_json(Path(run_dir) / "run-log.json")
    if not isinstance(log, dict):
        return {}
    return {a["name"]: a.get("outcome") for a in log.get("agents", [])
            if isinstance(a, dict) and a.get("role") == "revision" and a.get("name")}


def is_two_round(run_dir):
    return bool(revision_outcomes(run_dir))


def check_annotations_exempt(run_dir, personas, package_available):
    base = check_annotations(run_dir, personas)
    if not package_available:
        base["exempted"] = [{"persona": p, "reason": "no package"} for p in personas]
        base["unannotated"] = []
        base["pass"] = True
        return base
    outcomes = revision_outcomes(run_dir)
    exempted = []
    still_un = []
    for p in base["unannotated"]:
        outcome = outcomes.get(f"2b-{p}")
        if outcome is not None and outcome != "success":
            exempted.append({"persona": p, "reason": f"2b {outcome}"})
        else:
            still_un.append(p)
    base["exempted"] = exempted
    base["unannotated"] = still_un
    base["pass"] = not still_un
    return base


LENGTH_WARN_THRESHOLD = 1.5


def _word_count(path):
    try:
        return len(Path(path).read_text(encoding="utf-8").split())
    except OSError:
        return None


def check_length_ratio(run_dir, personas):
    ratios = {}
    for p in personas:
        draft = _word_count(Path(run_dir) / f"persona-output-{p}-draft.md")
        final = _word_count(Path(run_dir) / f"persona-output-{p}.md")
        if draft and final:
            ratios[p] = round(final / draft, 2)
    warnings = [p for p, r in ratios.items() if r > LENGTH_WARN_THRESHOLD]
    return {"ratios": ratios,
            "max_ratio": max(ratios.values()) if ratios else None,
            "length_warnings": warnings}


def check_run(run_dir, skill_dir=SKILL_DIR_DEFAULT):
    personas = expected_personas(run_dir)
    demands = check_demands(run_dir, personas)
    package = check_package(run_dir, demand_personas(run_dir))
    ref_numbers = package_numbers(run_dir)
    persona_results = [check_persona(run_dir, skill_dir, p, ref_numbers, package["valid_json"])
                       for p in personas]
    personas_pass = all(r["exists"] and not r["collapsed"] and not r["sections_missing"]
                        for r in persona_results)
    checks = {"demands": demands, "package": package,
              "personas": {"pass": personas_pass, "results": persona_results}}
    overall = demands["pass"] and package["pass"] and personas_pass and bool(personas)
    if is_two_round(run_dir):
        drafts = check_drafts(run_dir, personas)
        annotations = check_annotations_exempt(
            run_dir, personas,
            package_available=package["valid_json"] and package["analyses_count"] > 0)
        checks["drafts"] = drafts
        checks["annotations"] = annotations
        checks["length_ratio"] = check_length_ratio(run_dir, personas)
        overall = overall and drafts["pass"] and annotations["pass"]
    result = {
        "run_dir": str(run_dir),
        "checks": checks,
        "pass": overall,
    }
    Path(run_dir, "harness-result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


def summarize(results_dir):
    runs = sorted(Path(results_dir).glob("run-*/"))
    total = failures = collapses = passes = partials = 0
    ann = {"confirmed": 0, "revised": 0, "unsupported": 0}
    max_ratio = None
    lines = ["# Baseline Summary", "",
             "| Run | Agents | Failures | Collapses | Harness |",
             "|-----|-------:|---------:|----------:|:-------:|"]
    for run in runs:
        log = load_json(run / "run-log.json")
        harness = load_json(run / "harness-result.json") or {}
        agents = log.get("agents", []) if isinstance(log, dict) else []
        n_fail = sum(1 for a in agents if a.get("outcome") in ("timeout", "empty", "error"))
        persona_results = harness.get("checks", {}).get("personas", {}).get("results", [])
        n_collapse = sum(1 for r in persona_results if r.get("collapsed"))
        passed = bool(harness.get("pass"))
        total += len(agents)
        failures += n_fail
        collapses += n_collapse
        passes += int(passed)
        if harness.get("checks", {}).get("package", {}).get("partial"):
            partials += 1
        for k in ann:
            ann[k] += harness.get("checks", {}).get("annotations", {}).get("counts", {}).get(k, 0)
        mr = harness.get("checks", {}).get("length_ratio", {}).get("max_ratio")
        if mr is not None:
            max_ratio = mr if max_ratio is None else max(max_ratio, mr)
        lines.append(f"| {run.name} | {len(agents)} | {n_fail} | {n_collapse} | {'PASS' if passed else 'FAIL'} |")
    rate = (failures / total * 100) if total else 0.0
    lines += ["",
              f"**Agent failure rate:** {rate:.1f}% ({failures}/{total})",
              f"**Persona collapses:** {collapses}",
              f"**Harness pass rate:** {passes}/{len(runs)}",
              f"**Partial packages:** {partials}",
              f"**Annotations (C/R/U):** {ann['confirmed']}/{ann['revised']}/{ann['unsupported']}",
              f"**Max final/draft ratio:** {f'{max_ratio}x' if max_ratio is not None else 'n/a'}"]
    return "\n".join(lines)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "check":
        run_dir = argv[2] if len(argv) > 2 and not argv[2].startswith("--") else SKILL_DIR_DEFAULT
        skill_dir = SKILL_DIR_DEFAULT
        if "--skill-dir" in argv:
            skill_dir = argv[argv.index("--skill-dir") + 1]
        result = check_run(run_dir, skill_dir)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["pass"] else 1
    if cmd == "summarize":
        if len(argv) < 3:
            print("usage: pipeline_harness.py summarize <results_dir>")
            return 2
        print(summarize(argv[2]))
        return 0
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
