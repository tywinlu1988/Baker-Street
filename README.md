# 🔍 Baker Street — Sherlock Holmes Analytical Framework

> *"When you have eliminated the impossible, whatever remains, however improbable, must be the truth."*

A Claude Code skill that applies **7 distinct cognitive lenses** — each inspired by a character from the Sherlock Holmes canon — to analyze any problem, decision, or topic. The framework produces insights beyond what a single model response can achieve by mining **conflicts** and **blind spots** between independent perspectives.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](package.json)

---

## Installation

### Quick Install (Recommended)

```bash
npx baker-street
```

This copies the skill into `~/.claude/skills/sherlock/`. Restart Claude Code and use `/sherlock`.

To overwrite an existing installation:

```bash
npx baker-street --force
```

### Via Claude Code Plugin Marketplace

```bash
/plugin marketplace add tywinlu1988/Baker-Street
/plugin install sherlock@baker-street-marketplace
```

### Manual Install

```bash
git clone https://github.com/tywinlu1988/Baker-Street.git
cp -r Baker-Street/.claude/skills/sherlock ~/.claude/skills/
```

---

## Usage

```bash
# Standard analysis (3-4 personas)
/sherlock "Should I choose Rust or Go for my data pipeline?"

# Quick analysis (2 personas, lower cost)
/sherlock --depth quick "Summarize the risks of this approach"

# Deep analysis (all 7 personas)
/sherlock --depth deep "Audit our launch strategy"

# TL;DR — core findings + actions only
/sherlock --tldr "What's wrong with our onboarding flow?"

# Compare with raw model response
/sherlock --baseline "Evaluate this architectural decision"

# Choose specific personas
/sherlock --personas holmes,moriarty "Stress-test this business plan"
```

---

## The Seven Personas

| Persona | Cognitive Lens | Best For |
|---------|---------------|----------|
| 🔍 **Holmes** | Deductive reasoning, hypothesis elimination | Finding overlooked details, narrowing possibilities |
| 📋 **Watson** | Common-sense induction, practical judgment | Grounding analysis in everyday reality |
| 🧠 **Mycroft** | Systems thinking, structural analysis | Understanding root causes and large-scale patterns |
| ♟️ **Moriarty** | Adversarial thinking, game theory | Stress-testing plans, finding vulnerabilities |
| 👁️ **Adler** | Social/emotional intelligence | Reading motivations, power dynamics, hidden agendas |
| 🕵️ **Lestrade** | Evidence-based pragmatism | What's provable, what's executable right now |
| 🎯 **The Hound** | Fear & bias detection | Uncovering avoided truths, emotional distortion |

---

## What You Get

A structured report with:

- **🔬 Core Findings** — discoveries you wouldn't have made alone
- **⚔️ Key Divergences** — where personas genuinely disagree and why it matters
- **👁️ Silent Dimensions** — what NO persona covered (often the most valuable insight)
- **🗺️ Multi-Perspective Panorama** — each persona's thesis, conflicts annotated
- **🎯 Action Recommendations** — immediate, short-term, and long-term next steps

---

## Validation

The framework includes a quantitative validation suite:

- **5 test cases** covering technical decisions, business strategy, knowledge building, ethical dilemmas, and meta-analysis
- **5 scoring dimensions**: Novelty, Persona Fidelity, Rigor, Conflict Density, Actionability
- **LLM-as-Judge** evaluation with anchored 1-10 scales
- **v0.1 gate**: ≥4/5 test cases must pass

See [validate.md](.claude/skills/sherlock/validate.md) for details.

---

## Project Structure

```
baker-street/
├── .claude/skills/sherlock/
│   ├── skill.md              # Main orchestration skill
│   ├── personas/             # 7 character prompt files
│   ├── test-cases/           # 5 validation test cases
│   ├── judge.md              # LLM-as-Judge scoring prompt
│   ├── validate.md           # Validation suite runner
│   └── README.md             # Skill reference
├── .claude-plugin/
│   └── plugin.json           # Claude Code plugin manifest
├── install.js                # npx installer
├── package.json              # npm metadata
└── LICENSE                   # MIT
```

---

## Roadmap

- **v0.1** (current): 7 personas, 3-layer synthesis, quantitative validation, npx install
- **v0.2** (planned): Custom user-defined personas, persistent persona memory, domain-specific extensions
- **v1.0** (planned): Visual output (diagrams), streaming, fine-tuned evaluation models

---

## License

MIT © 2026 Tywin Lu. See [LICENSE](LICENSE).
