#!/usr/bin/env python3
"""
make_run_package.py — assemble a sherlock run package with provenance.
Usage: python make_run_package.py <command> [args]

Commands:
  factbase [--skill-dir DIR] [--merged PATH] — build canonical fact-base.json with stable F-ids + sources.md
  sources [--skill-dir DIR] --out PATH   — build human-readable source manifest (fact-base.json if present, else research-output-*.json)
  assemble <run_dir> [--skill-dir DIR]   — move run artifacts into run_dir, clean skill dir
"""
import sys, json, glob, shutil
from pathlib import Path

SKILL_DIR_DEFAULT = ".claude/skills/sherlock"


def _load_facts(skill_dir):
    facts = []
    for f in sorted(glob.glob(str(Path(skill_dir) / "research-output-*.json"))):
        try:
            data = json.loads(Path(f).read_text(encoding="utf-8"))
            if isinstance(data, list):
                facts.extend(x for x in data if isinstance(x, dict))
        except (OSError, json.JSONDecodeError):
            continue
    return facts


def _conf(f):
    """Numeric confidence with coercion; non-numeric/missing -> 0 (never raises)."""
    try:
        return float(f.get("confidence", 0))
    except (TypeError, ValueError):
        return 0.0


def _write_sources(facts, out_path, with_ids):
    lines = ["# 数据源清单（Source Manifest）", ""]
    if with_ids:
        lines += ["| # | ID | 事实 | 来源 | 置信度 | 类型 |",
                  "|---|----|------|------|-------:|------|"]
    else:
        lines += ["| # | 事实 | 来源 | 置信度 | 类型 |",
                  "|---|------|------|-------:|------|"]
    for i, f in enumerate(facts, 1):
        claim = str(f.get("claim", "")).replace("|", "\\|")
        source = str(f.get("source", "")).replace("|", "\\|")
        conf = f.get("confidence", "?")
        ftype = f.get("type", "fact")
        if with_ids:
            lines.append(f"| {i} | {f.get('id', '')} | {claim} | {source} | {conf} | {ftype} |")
        else:
            lines.append(f"| {i} | {claim} | {source} | {conf} | {ftype} |")
    if not facts:
        lines.append("")
        lines.append("（无研究产物 — 本次运行未启用研究层或无有效输出）")
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_factbase(skill_dir, merged_path=None):
    """Build canonical fact-base.json (stable F-ids, confidence-sorted) + sources.md
    where row number == F-id number. Returns fact count."""
    skill_dir = Path(skill_dir)
    facts = None
    if merged_path is not None and Path(merged_path).exists():
        try:
            data = json.loads(Path(merged_path).read_text(encoding="utf-8"))
            if isinstance(data, list):
                facts = [x for x in data if isinstance(x, dict)]
        except (OSError, json.JSONDecodeError):
            facts = None  # corrupt merged file: fall back to research-output-*.json
    if facts is None:
        facts = _load_facts(skill_dir)
    facts = sorted(facts, key=_conf, reverse=True)
    for i, f in enumerate(facts, 1):
        f["id"] = f"F{i:03d}"
    (skill_dir / "fact-base.json").write_text(
        json.dumps(facts, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_sources(facts, skill_dir / "sources.md", with_ids=True)
    return len(facts)


def cmd_sources(skill_dir, out_path):
    skill_dir = Path(skill_dir)
    fb = skill_dir / "fact-base.json"
    if fb.exists():
        facts = json.loads(fb.read_text(encoding="utf-8"))
        _write_sources(facts, out_path, with_ids=True)
        return len(facts)
    facts = sorted(_load_facts(skill_dir), key=_conf, reverse=True)
    _write_sources(facts, out_path, with_ids=False)
    return len(facts)


def cmd_assemble(skill_dir, run_dir):
    skill_dir = Path(skill_dir)
    run_dir = Path(run_dir)
    (run_dir / "personas").mkdir(parents=True, exist_ok=True)
    (run_dir / "scripts").mkdir(parents=True, exist_ok=True)
    moved, missing = [], []

    # canonical fact base: generated at research-compile time (Step 1.4);
    # fallback: generate now for legacy/degraded runs
    if not (skill_dir / "fact-base.json").exists():
        cmd_factbase(skill_dir)

    def move(name, dest_dir=run_dir, required=False):
        src = skill_dir / name
        if src.exists():
            shutil.move(str(src), str(dest_dir / name))
            moved.append(name)
        elif required:
            missing.append(name)

    move("fact-base.json")
    move("fact-base-merged.json")
    move("sources.md")
    # raw per-agent research outputs: preserved in run dir (provenance), not deleted
    for f in glob.glob(str(skill_dir / "research-output-*.json")):
        shutil.move(f, str(run_dir / Path(f).name))
        moved.append(Path(f).name)

    move("quant-demands.json", required=True)
    move("quant-analysis-package.json", required=True)
    move("run-log.json", required=True)
    move("baseline-output.md")
    move("scout-output.md")
    for f in glob.glob(str(skill_dir / "persona-output-*.md")):
        shutil.move(f, str(run_dir / "personas" / Path(f).name))
        moved.append(Path(f).name)
    for f in glob.glob(str(skill_dir / "rebuttal-*.md")):
        shutil.move(f, str(run_dir / Path(f).name))
        moved.append(Path(f).name)

    # scripts: COPY from paths declared in the package (tools/ is a shared library)
    pkg = run_dir / "quant-analysis-package.json"
    if pkg.exists():
        try:
            for a in json.loads(pkg.read_text(encoding="utf-8")).get("analyses", []):
                script = a.get("script")
                if script and Path(script).exists() and Path(script).suffix == ".py":
                    shutil.copy2(script, str(run_dir / "scripts" / Path(script).name))
        except (OSError, json.JSONDecodeError):
            pass

    return {"moved": moved, "missing": missing}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    skill_dir = SKILL_DIR_DEFAULT
    if "--skill-dir" in argv:
        skill_dir = argv[argv.index("--skill-dir") + 1]
    if cmd == "factbase":
        merged = None
        if "--merged" in argv:
            merged = argv[argv.index("--merged") + 1]
        n = cmd_factbase(skill_dir, merged_path=merged)
        print(f"fact-base.json written: {n} facts")
        return 0
    if cmd == "sources":
        if "--out" not in argv:
            print("usage: make_run_package.py sources [--skill-dir DIR] --out PATH")
            return 2
        out = argv[argv.index("--out") + 1]
        n = cmd_sources(skill_dir, out)
        print(f"sources.md written: {n} facts")
        return 0
    if cmd == "assemble":
        if len(argv) < 3 or argv[2].startswith("--"):
            print("usage: make_run_package.py assemble <run_dir> [--skill-dir DIR]")
            return 2
        r = cmd_assemble(skill_dir, argv[2])
        print(f"assembled into {argv[2]}: {len(r['moved'])} moved, missing: {r['missing'] or 'none'}")
        return 0
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
