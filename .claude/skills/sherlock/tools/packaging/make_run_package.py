#!/usr/bin/env python3
"""
make_run_package.py — assemble a sherlock run package with provenance.
Usage: python make_run_package.py <command> [args]

Commands:
  sources [--skill-dir DIR] --out PATH   — build human-readable source manifest from research-output-*.json
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


def cmd_sources(skill_dir, out_path):
    facts = sorted(_load_facts(skill_dir),
                   key=lambda x: x.get("confidence", 0), reverse=True)
    lines = ["# 数据源清单（Source Manifest）", "",
             "| # | 事实 | 来源 | 置信度 | 类型 |",
             "|---|------|------|-------:|------|"]
    for i, f in enumerate(facts, 1):
        claim = str(f.get("claim", "")).replace("|", "\\|")
        source = str(f.get("source", "")).replace("|", "\\|")
        lines.append(f"| {i} | {claim} | {source} | {f.get('confidence', '?')} | {f.get('type', 'fact')} |")
    if not facts:
        lines.append("")
        lines.append("（无研究产物 — 本次运行未启用研究层或无有效输出）")
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(facts)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    skill_dir = SKILL_DIR_DEFAULT
    if "--skill-dir" in argv:
        skill_dir = argv[argv.index("--skill-dir") + 1]
    if cmd == "sources":
        if "--out" not in argv:
            print("usage: make_run_package.py sources [--skill-dir DIR] --out PATH")
            return 2
        out = argv[argv.index("--out") + 1]
        n = cmd_sources(skill_dir, out)
        print(f"sources.md written: {n} facts")
        return 0
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
