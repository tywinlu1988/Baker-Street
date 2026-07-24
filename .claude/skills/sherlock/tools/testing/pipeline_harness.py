#!/usr/bin/env python3
"""
Sherlock Pipeline Harness — behavioral checks for pipeline run artifacts.
Usage: python pipeline_harness.py <command> [args]

Commands:
  check [run_dir] [--skill-dir DIR] — validate one run's artifacts, write harness-result.json into run_dir
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
    log = load_json(Path(run_dir) / "run-log.json") or {}
    return [a["name"] for a in log.get("agents", [])
            if a.get("role") == "persona" and a.get("name") != "baseline"]


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
              "analyses_count": 0, "schema_errors": [], "uncovered_personas": []}
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
    result["pass"] = (result["analyses_count"] > 0
                      and not result["schema_errors"]
                      and not result["uncovered_personas"])
    return result


def demand_personas(run_dir):
    data = load_json(Path(run_dir) / "quant-demands.json") or {}
    return sorted({d.get("persona") for d in data.get("demands", []) if d.get("persona")})


def check_run(run_dir, skill_dir=SKILL_DIR_DEFAULT):
    personas = expected_personas(run_dir)
    demands = check_demands(run_dir, personas)
    package = check_package(run_dir, demand_personas(run_dir))
    result = {
        "run_dir": str(run_dir),
        "checks": {"demands": demands, "package": package},
        "pass": demands["pass"] and package["pass"] and bool(personas),
    }
    Path(run_dir, "harness-result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


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
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
