# 🔍 Sherlock — Multi-Perspective Analysis Framework

A Claude Code skill that applies 7 distinct cognitive lenses — each inspired by a character from the Sherlock Holmes canon — to analyze any problem, decision, or topic. The framework produces insights that go beyond what any single model response can achieve by mining the **conflicts** and **blind spots** between independent perspectives.

## Quick Start

```
/sherlock "Should I choose Rust or Go for my data pipeline rewrite?"
```

This runs a standard-depth analysis (3-4 personas) and produces a full report.

## Commands

```bash
# Standard analysis (3-4 personas)
/sherlock "Your question here"

# Quick analysis (2 personas, lower cost)
/sherlock --depth quick "Your question here"

# Deep analysis (all 7 personas)
/sherlock --depth deep "Your question here"

# TL;DR — just the findings and actions
/sherlock --tldr "Your question here"

# Compare with raw model response
/sherlock --baseline "Your question here"

# Specify which personas to use
/sherlock --personas holmes,moriarty "Your question here"
```

## The Seven Personas

| Persona | Role | Best For |
|---------|------|----------|
| 🔍 **Holmes** | Deductive reasoning | Finding what others missed, eliminating false explanations |
| 📋 **Watson** | Common-sense induction | Grounding analysis in practical reality |
| 🧠 **Mycroft** | Systems thinking | Understanding structural causes and large-scale patterns |
| ♟️ **Moriarty** | Adversarial analysis | Stress-testing plans, finding vulnerabilities |
| 👁️ **Adler** | Social/emotional intelligence | Reading motivations, power dynamics, hidden agendas |
| 🕵️ **Lestrade** | Evidence & pragmatism | What's provable, what's executable right now |
| 🎯 **The Hound** | Fear & bias detection | Uncovering avoided truths, emotional distortion, misdirection |

## What You Get

A structured report with:

- **Core Findings** — discoveries, not conclusions
- **Key Divergences** — where personas genuinely disagree and why it matters
- **Silent Dimensions** — what NO persona covered (often the most important part)
- **Multi-Perspective Panorama** — each persona's thesis
- **Action Recommendations** — immediate, short-term, and long-term next steps

## When to Use

- Making a high-stakes decision with no obvious right answer
- Understanding a complex topic from multiple angles
- Breaking through analysis paralysis
- Finding blind spots in your own thinking
- Stress-testing a plan or strategy

## When NOT to Use

- Simple factual questions (just ask the model directly)
- Tasks that require a single correct answer (math, coding syntax)
- Quick lookups or definitions

## Cost Note

Each persona runs as an independent agent. Standard depth uses 3-4 agents; deep uses all 7. Use `--depth quick` for cost-sensitive scenarios.

## Validation

The framework includes a quantitative validation suite (5 test cases, LLM-as-Judge scoring). See `validate.md` for details.

## License

MIT — see repository root `LICENSE`.
