# 🔍 Sherlock — Multi-Perspective Analysis Framework

A Claude Code skill that applies 7 distinct cognitive lenses — each inspired by a character from the Sherlock Holmes canon — to analyze any problem, decision, or topic.

> 📦 **Installation & full documentation:** [github.com/tywinlu1988/Baker-Street](https://github.com/tywinlu1988/Baker-Street)

## Quick Start

```
/sherlock "Should I choose Rust or Go for my data pipeline rewrite?"
```

This runs a standard-depth analysis (3-4 personas) and produces a full report.

## Commands

```bash
/sherlock "Your question"                          # Standard (3-4 personas)
/sherlock --depth quick "Your question"            # Quick (2 personas)
/sherlock --depth deep "Your question"             # Deep (all 7 personas)
/sherlock --tldr "Your question"                   # Core findings + actions only
/sherlock --baseline "Your question"               # Compare with raw model response
/sherlock --personas holmes,moriarty "Your question"  # Choose specific personas
```

## The Seven Personas

| Persona | Role |
|---------|------|
| 🔍 **Holmes** | Deductive reasoning — finding what others missed |
| 📋 **Watson** | Common-sense induction — practical reality check |
| 🧠 **Mycroft** | Systems thinking — structural root causes |
| ♟️ **Moriarty** | Adversarial analysis — stress-testing & vulnerabilities |
| 👁️ **Adler** | Social/emotional intelligence — hidden motivations |
| 🕵️ **Lestrade** | Evidence & pragmatism — what's provable & executable |
| 🎯 **The Hound** | Fear & bias detection — uncovering avoided truths |

## What You Get

- **Core Findings** — discoveries, not conclusions
- **Key Divergences** — where personas genuinely disagree
- **Silent Dimensions** — what NO persona covered
- **Action Recommendations** — immediate, short-term, long-term

## When to Use

High-stakes decisions, complex topics, analysis paralysis, blind spot detection, strategy stress-testing.

## When NOT to Use

Simple factual questions, single-answer tasks, quick lookups.

## Cost Note

Standard depth uses 3-4 agents; deep uses all 7. Use `--depth quick` for cost-sensitive scenarios.

## Files

- `skill.md` — Main orchestration (5-phase pipeline)
- `personas/` — 7 character prompt files
- `test-cases/` — 5 validation test cases
- `judge.md` — LLM-as-Judge scoring prompt
- `validate.md` — Validation suite runner

## License

MIT — see repository root.
