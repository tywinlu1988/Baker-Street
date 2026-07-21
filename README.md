# 🔍 Baker Street — Sherlock Holmes Analytical Framework

> *"When you have eliminated the impossible, whatever remains, however improbable, must be the truth."*
> *—— Sherlock Holmes, The Sign of the Four*

**Baker Street** is a Claude Code skill that applies **7 distinct cognitive archetypes** — each inspired by a character from the Sherlock Holmes canon — to analyze any problem, decision, or topic. It works as a **thinking engine**, not a templated answer generator: independent persona agents analyze in parallel, then a synthesis layer mines their conflicts and blind spots to produce insights no single model response can achieve.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.1-blue.svg)](package.json)

English | [中文](README_CN.md)

---

## Table of Contents

1. [Why This Exists](#1-why-this-exists)
2. [Design Philosophy](#2-design-philosophy)
3. [The Seven Cognitive Archetypes](#3-the-seven-cognitive-archetypes)
4. [How It Works](#4-how-it-works)
5. [Quantitative Validation](#5-quantitative-validation)
6. [Installation & Usage](#6-installation--usage)
7. [Project Structure](#7-project-structure)
8. [Roadmap](#8-roadmap)

---

## 1. Why This Exists

### The Problem

Models like Fable 5 and Opus 4.8 already produce well-structured answers. But structure is not insight. What they produce is **knowledge rearrangement** — extracting, organizing, and formatting patterns from training data. This process misses two things:

1. **Genuine discovery** — Models don't challenge your framing. They optimize within the question you asked, rather than telling you you're asking the wrong question.
2. **Cognitive friction** — Deep thinking involves self-doubt, self-refutation, and value trade-offs. A single-pass model output lacks this productive tension.

### The Solution

Baker Street forces **independent multi-perspective parallel analysis**:

```
Not:  one model → one answer → "looks good"
But:  7 independent cognitive archetypes → parallel analysis
      → conflict mining → blind spot detection → synthesized insight
```

The key word is **independent**. Each persona agent analyzes without knowing what the others think. This means:

- They may reach **contradictory conclusions** from different premises and different value priorities
- These contradictions are not noise — they are the framework's primary value source, exposing the complexity masked by any single perspective
- The synthesis layer doesn't average or harmonize — it **amplifies conflict** so the user can see the full picture

### Measuring It

We quantify this with **Framework Gain**:

```
Framework Gain = mean novelty of framework output / novelty of raw model output
```

The v0.1 target is ≥ 1.5 — the framework should produce at least 50% more novel insights than asking the model directly. This is validated through 5 standardized test cases with LLM-as-Judge scoring.

---

## 2. Design Philosophy

### Why Sherlock Holmes?

Conan Doyle created characters with **radically different cognitive styles** — not just personalities, but fundamentally different ways of processing information, forming conclusions, and deciding what matters. Each character is a **cognitive archetype**: a stable, transferable thinking methodology. The framework extracts the archetype, not the literary persona.

### Why Parallel + Independent?

If a single model "role-plays" different characters sequentially, later personas know what earlier ones said. This unconsciously smooths over cognitive conflicts. **Parallel + independent = real disagreement.** That's the prerequisite for multi-perspective value.

### Conflict Is a Feature

A quick health check: **if all personas agree, either the question is trivial or the personas aren't trying hard enough.**

The synthesis layer starts with Conflict Mining — not surface disagreements ("use Rust" vs "use Go"), but three types of deep conflict:

| Conflict Type | Meaning | Example |
|--------------|---------|---------|
| **Assumption Conflict** | Two personas make contradictory assumptions about the same variable | Holmes assumes the team can learn Rust; Lestrade assumes the learning curve is the decisive bottleneck |
| **Weighting Conflict** | Personas assign different priority orderings to the same factors | Moriarty ranks security #1; Watson ranks development speed #1 |
| **Interpretation Conflict** | Same fact, different causal reading | "Growth stalled" → Adler reads it as positioning; Lestrade reads it as execution |

### Honesty Over Completeness

Every persona has a **Blind Spot Declaration** — what it knows it overlooks. No one pretends to be omniscient. The synthesis layer then checks: which dimensions did **no persona** cover? These silences are often the most valuable findings in the entire report.

### Cost Consciousness

The framework doesn't deploy all 7 personas by default. v0.1 cost controls:
- **Needs-based selection**: 2-4 most relevant personas matched to problem type
- **Depth tiers**: `--depth quick` (2), `standard` (3), `deep` (7)
- **Rebuttal cap**: At most 2 conflict pairs get the back-and-forth treatment

---

## 3. The Seven Cognitive Archetypes

### 🔍 Sherlock Holmes — Deductive Reasoning

> *"When you have eliminated the impossible, whatever remains, however improbable, must be the truth."*

**Stance**: Observe all details before forming any theory. Generate multiple hypotheses, then systematically eliminate them. When two explanations remain, the simpler one is usually correct. Pay special attention to anomalies — and to **what is not there** ("the dog that didn't bark").

**Always asks**: What are others ignoring? What's been ruled out? Does the evidence chain close? What must have been true for this to occur?

**Blind spot**: Emotional factors, social conventions, moral intuition. Systematically undervalues the human dimension.

**Best for**: Technical decisions, factual investigations, scenarios requiring hypothesis elimination.

---

### 📋 Dr. John Watson — Common-Sense Induction

> *"What seems extraordinary is often the result of ordinary causes."*

**Stance**: Ground every analysis in real-world experience. Trust instincts about people. Notice when theories drift too far from everyday reality. The ultimate test: "If I told this to a friend over a drink, would it make sense?"

**Always asks**: What's the most mundane explanation? What does prior experience suggest? What would a reasonable person do? Are we being seduced by a clever theory when the simple answer is right here?

**Blind spot**: Rare events, edge cases, counter-intuitive truths. The preference for ordinary explanations can miss the genuinely extraordinary.

**Best for**: Reality checks, product decisions, user behavior analysis.

---

### 🧠 Mycroft Holmes — Systems Thinking

> *"The problem is never isolated. Every fact is a node in a larger system."*

**Stance**: Map the full system before analyzing any component. Identify feedback loops, incentive structures, and constraints. Prefer root causes over symptoms. Thinks, doesn't act — pure structural reasoning from the armchair.

**Always asks**: What's the larger system? What distal factors are driving this? What are the structural root causes? Who benefits from the current arrangement?

**Blind spot**: Execution details, individual variance, emotion-driven behavior. Elegant structural solutions may fail because people are not rational actors.

**Best for**: Organizational diagnosis, policy analysis, macro strategy, understanding complex ecosystems.

---

### ♟️ Professor Moriarty — Adversarial / Game Theory

> *"Every system has a vulnerability. Every plan has a counter-plan."*

**Stance**: Think like the opposition. Model the situation as a game: players, payoffs, strategies. Attack every assumption — especially the ones nobody questions. The absence of a visible threat does not mean there is no threat.

**Always asks**: Where would a smart adversary strike? What are we most overconfident about? What are the hidden incentives? What if we assume everyone is optimizing for themselves?

**Blind spot**: Defaults to adversarial intent and self-interest. May miss genuine cooperation, altruism, and good-faith dynamics. Has no ethical boundaries — may surface "optimal" moves that are morally unacceptable.

**Best for**: Risk assessment, competitive analysis, security auditing, strategy stress-testing.

---

### 👁️ Irene Adler — Social/Emotional Intelligence

> *"People reveal more in what they hide than in what they show."*

**Stance**: People are the real terrain. Read between the lines — the most important information is often what people are NOT saying. Map the social graph: who influences whom, who owes what to whom. The best move is often the one that understands what the other side truly fears or desires.

**Always asks**: What do people actually want (vs. what they claim)? How do power structures shape this? What assumptions is everyone making that nobody has stated? What's being deliberately hidden?

**Blind spot**: Over-indexes on human factors. A pipe doesn't care about social dynamics; a compiler doesn't have hidden motives. Can overcomplicate situations with straightforward non-human explanations.

**Best for**: Interpersonal dilemmas, team conflicts, negotiation strategy, user motivation analysis.

---

### 🕵️ Inspector Lestrade — Evidence & Pragmatism

> *"A theory is only as good as the evidence that supports it — and the action it enables."*

**Stance**: Start from evidence, not theory. Every conclusion must pair with a verification step. If a plan can't survive contact with reality, it's not a plan — it's a wish. Trust procedure: good process beats brilliant improvisation in the long run.

**Always asks**: What hard evidence do we actually have? What's the next verifiable step? Is this executable with available resources? What would prove us right or wrong?

**Blind spot**: Focus on evidence and procedure can miss theoretical breakthroughs, disruptive innovation, and possibilities with no precedent. Optimizes for today's actionable when tomorrow's vision is needed.

**Best for**: Execution planning, operational decisions, compliance review, scenarios needing clear next steps.

---

### 🎯 The Hound of the Baskervilles — Fear & Bias Detection

> *"What you fear most is often what you should examine closest."*

**Stance**: Follow the fear — the thing people least want to look at is often where the truth lives. Identify the "glow-in-the-dark hound" — the terrifying symbol that's actually a painted dog. Check every conclusion for emotional contamination: are we concluding X because evidence supports it, or because X is what we need to believe?

**Always asks**: What is everyone most afraid to admit? What assumptions go unchallenged because challenging them would hurt? Where might cognitive bias, groupthink, or emotional reactivity be masquerading as rational analysis?

**Blind spot**: Relentless suspicion can miss genuine opportunities, warranted confidence, and facts that don't require deconstruction. Not every shadow hides a threat. Sometimes a cigar is just a cigar.

**Best for**: High-stakes emotional auditing, identifying groupthink, challenging "the elephant in the room," avoiding misdirection.

---

## 4. How It Works

### Two-Phase Architecture

```
User query
    │
    ▼
┌──────────────────────────────────────┐
│ Phase 1: Dispatch (low cost)          │
│                                      │
│ Problem classifier → auto-select     │
│ 2-4 personas (overridable)           │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ Phase 2: Analysis (precision spend)   │
│                                      │
│ Selected personas → parallel run     │
│     │                                │
│     ▼                                │
│ Three-Layer Synthesis:               │
│   ① Conflict Mining                   │
│   ② Targeted Rebuttal (top-2)        │
│   ③ Blind Spot Detection              │
│   ④ Action Pathway Generation        │
│     │                                │
│     ▼                                │
│ Output: Full report / TL;DR          │
└──────────────────────────────────────┘
```

### Problem Classification

| Problem Type | Quick (2) | Standard (3) |
|-------------|:---------:|:-----------:|
| Technical Decision | Holmes + Lestrade | + Moriarty |
| Business Strategy | Moriarty + Adler | + Hound |
| Knowledge Building | Watson + Holmes | + Mycroft |
| Interpersonal/Ethical | Adler + Lestrade | + Moriarty |
| Creative/Ideation | Adler + Watson | + Holmes |
| Risk Assessment | Moriarty + Hound | + Mycroft |
| General/Mixed | Holmes + Watson | + Moriarty |

`--depth deep` uses all 7 personas regardless of type.

### The Synthesis Engine

**Layer 1 — Conflict Mining**: Detect assumption, weighting, and interpretation conflicts. Rank by impact on the decision.

**Layer 1.5 — Targeted Rebuttal**: For the top 2 conflicts, have the personas respond to each other's reasoning. Rebuttal agents receive their persona prompt, their prior analysis, and the conflicting argument to produce a genuine dialogue.

**Layer 2 — Blind Spot Synthesis**: Aggregate all blind spot declarations. Find dimensions that zero personas covered. Report these silences.

**Layer 3 — Action Pathway**: Generate immediate (24h), short-term (1-2 weeks), and long-term recommendations grounded in specific persona insights.

### Output

The report includes **Core Findings** (discoveries, not conclusions), **Framework Delta** (what the framework added over the raw model baseline), **Key Divergences** (substantive disagreements and what they mean), **Silent Dimensions** (what nobody covered), a **Multi-Perspective Panorama** (each persona's thesis, conflicts annotated), and **Action Recommendations** at three time horizons. A baseline comparison runs automatically on every analysis. Use `--tldr` for core findings + delta + actions only (one screen).

---

## 5. Quantitative Validation

The framework isn't just asserted to work — it's tested.

### 5 Scoring Dimensions (LLM-as-Judge, 1-10 scales)

| Dimension | Measures | 1-Point Anchor | 10-Point Anchor |
|-----------|----------|---------------|-----------------|
| **Novelty** | Does it go beyond the baseline? | Identical to raw model | Reframes the user's question |
| **Persona Fidelity** | Does it feel like that specific character? | Could swap name, output unchanged | Cognitive fingerprint is unmistakable |
| **Rigor** | Is the reasoning sound? | Obvious logical gaps | Every assertion has explicit derivation |
| **Conflict Density** | Does it substantively disagree with others? | Aligned with all personas | Core-level viewpoint collision |
| **Actionability** | Can the user act on it? | Abstract conclusions only | Immediately executable steps |

### Aggregate Metrics

| Metric | Formula | v0.1 Threshold |
|--------|---------|:-------------:|
| **Framework Gain** | mean(Framework Novelty) / Baseline Novelty | ≥ 1.5 |
| **Perspective Dispersion** | Qualitative divergence assessment | ≥ 0.3 |
| **Blind Spot Coverage** | New dimensions surfaced / persona count | ≥ 0.5 |

### Baseline Methodology

Each test case runs three groups: **A** (raw model, no framework), **B** (framework, single persona), **C** (framework, full pipeline). Comparisons: C vs A (total gain), C vs B (multi-perspective increment), B vs A (persona value alone).

### 5 Standardized Test Cases

1. **Tech Decision**: Rust vs Go for real-time data (Python team)
2. **Business Strategy**: SaaS growth stall with team dynamics
3. **Knowledge Building**: Quantum computing for non-experts
4. **Ethical Dilemma**: Co-founder concealed legal risk during fundraising
5. **Meta-Analysis**: Framework critiques its own design

**v0.1 gate**: ≥ 4/5 cases must pass all metrics.

---

## 6. Installation & Usage

### Install

**Quick Install (Recommended)**
```bash
npx github:tywinlu1988/Baker-Street
```
Copies the skill to `~/.claude/skills/sherlock/`. Overwrite with `--force`.

**Via Plugin Marketplace**
```bash
/plugin marketplace add tywinlu1988/Baker-Street
/plugin install sherlock@baker-street
```

**Manual**
```bash
git clone https://github.com/tywinlu1988/Baker-Street.git
cp -r Baker-Street/.claude/skills/sherlock ~/.claude/skills/
```

### Usage

```bash
/sherlock "Your question"                              # Standard (3-4 personas)
/sherlock --depth quick "Your question"                # Quick (2 personas)
/sherlock --depth deep "Your question"                 # Deep (all 7)
/sherlock --tldr "Your question"                       # Core findings + actions
/sherlock --auto "Your question"                       # Skip intake, use defaults
/sherlock --personas holmes,moriarty "Your question"   # Choose personas
```

### Cost

Each persona is an independent agent. Standard depth uses 3-4 agents; deep uses all 7. Use `--depth quick` (2 agents) for cost-sensitive scenarios. v0.1 uses the session's default model for all personas.

---

## 7. Project Structure

```
baker-street/
├── README.md                 # English docs
├── README_CN.md              # Chinese docs
├── LICENSE                   # MIT
├── package.json              # npm metadata
├── install.js                # npx installer
├── .claude-plugin/
│   └── plugin.json           # Claude Code plugin manifest
├── .claude/skills/sherlock/
│   ├── skill.md              # Main orchestration (5-phase pipeline)
│   ├── personas/             # 7 character prompt files
│   ├── test-cases/           # 5 validation test cases
│   ├── judge.md              # LLM-as-Judge scoring prompt
│   └── validate.md           # Validation suite runner
└── docs/superpowers/
    ├── specs/                # Design spec
    └── plans/                # Implementation plan
```

---

## 8. Roadmap

| Version | Scope |
|---------|-------|
| **v0.1** (current) | 7 personas, 3-layer synthesis, LLM-as-Judge validation, npx install |
| **v0.2** (planned) | Custom personas, persistent persona memory, domain-specific extensions |
| **v1.0** (planned) | Visual output (diagrams), streaming, fine-tuned evaluation models |

---

## License

MIT © 2026 Tywin Lu. See [LICENSE](LICENSE).

---

*The game is afoot.*
