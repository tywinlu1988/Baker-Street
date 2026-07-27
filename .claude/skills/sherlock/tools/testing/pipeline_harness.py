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


def check_package(run_dir, demand_personas):
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
    result["uncovered_personas"] = [p for p in demand_personas if p not in covered]
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
PACKAGE_REF_HINTS = ("quantitative analysis package", "requested_by", "analyses")


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
        nums.update(re.findall(r"-?\d+\.\d+|-?\d{2,}", blob))
    return sorted(nums)


def check_persona(run_dir, skill_dir, persona, ref_numbers, package_available):
    path = Path(run_dir) / f"persona-output-{persona}.md"
    result = {"persona": persona, "exists": path.exists(),
              "sections_missing": [], "collapsed": False, "references_package": None}
    if not path.exists():
        result["collapsed"] = True
        return result
    text = path.read_text(encoding="utf-8")
    result["sections_missing"] = [s for s in persona_sections(skill_dir, persona) if s not in text]
    markers = [m for m in COLLAPSE_MARKERS if m in text]
    result["collapsed"] = len(result["sections_missing"]) >= 2 or bool(markers)
    if package_available:
        low = text.lower()
        result["references_package"] = (any(n in text for n in ref_numbers)
                                        or any(h in low for h in PACKAGE_REF_HINTS))
    return result


ANNOTATION_RE = re.compile(r"\[DATA: (CONFIRMED|REVISED|UNSUPPORTED)\]")


def check_drafts(run_dir, personas):
    result = {"pass": True, "missing_drafts": []}
    for p in personas:
        path = Path(run_dir) / f"persona-output-{p}-draft.md"
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
        path = Path(run_dir) / f"persona-output-{p}.md"
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


def check_run(run_dir, skill_dir=SKILL_DIR_DEFAULT):
    personas = expected_personas(run_dir)
    demands = check_demands(run_dir, personas)
    package = check_package(run_dir, demand_personas(run_dir))
    ref_numbers = package_numbers(run_dir)
    persona_results = [check_persona(run_dir, skill_dir, p, ref_numbers, package["valid_json"])
                       for p in personas]
    personas_pass = all(r["exists"] and not r["collapsed"] and not r["sections_missing"]
                        for r in persona_results)
    result = {
        "run_dir": str(run_dir),
        "checks": {"demands": demands, "package": package,
                   "personas": {"pass": personas_pass, "results": persona_results}},
        "pass": demands["pass"] and package["pass"] and personas_pass and bool(personas),
    }
    Path(run_dir, "harness-result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


def summarize(results_dir):
    runs = sorted(Path(results_dir).glob("run-*/"))
    total = failures = collapses = passes = partials = 0
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
        lines.append(f"| {run.name} | {len(agents)} | {n_fail} | {n_collapse} | {'PASS' if passed else 'FAIL'} |")
    rate = (failures / total * 100) if total else 0.0
    lines += ["",
              f"**Agent failure rate:** {rate:.1f}% ({failures}/{total})",
              f"**Persona collapses:** {collapses}",
              f"**Harness pass rate:** {passes}/{len(runs)}",
              f"**Partial packages:** {partials}"]
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
