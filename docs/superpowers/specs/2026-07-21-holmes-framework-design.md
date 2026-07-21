# Sherlock Holmes Analytical Framework — Design Spec v0.1

## Overview

A Claude Code skill that applies multi-perspective analytical thinking inspired by characters from the Sherlock Holmes canon. The framework uses **independent character personas** as cognitive lenses to analyze problems, producing insights beyond what a single model response can achieve.

**Repository**: https://github.com/tywinlu1988/Baker-Street
**License**: MIT
**Status**: Draft

---

## 1. Core Insight

Even the most powerful models (Fable 5, Opus 4.8) produce "structured answers" that are fundamentally rearrangements of known knowledge. They lack genuine **discovery** and **reasoning depth**. This framework addresses that gap by:

1. Forcing independent perspectives via isolated persona agents
2. Mining **conflicts** between perspectives as a source of novel insight
3. Exposing **blind spots** that no single viewpoint can see

---

## 2. Architecture

### 2.1 Two-Phase Design

```
Phase 1: Dispatch (low cost)
  User query → problem classifier → persona selection (2-4 personas)
  User may override selection via --personas flag

Phase 2: Analysis (precision investment)
  Selected personas run in parallel as independent agents
  → Conflict mining → Targeted conflict rebuttal → Final synthesis
```

### 2.2 Cost Control Strategy

| Strategy | Implementation |
|----------|---------------|
| Needs-based selection | Not all 7 personas run every time; 2-4 selected by problem type |
| Depth tiers | `--depth quick` (2 personas), `standard` (3-4), `deep` (all 7) |
| Persona model gating | Lightweight personas (Watson) can use smaller models; heavy reasoning (Holmes, Moriarty) use full models |
| Conflict rebuttal cap | Maximum 2 conflict pairs rebutted per analysis |

### 2.3 File Structure

```
.claude/skills/holmes-framework/
├── skill.md              # Main skill: dispatch + synthesis logic
├── personas/
│   ├── holmes.md         # Deductive reasoning
│   ├── watson.md         # Common-sense induction
│   ├── mycroft.md        # Systems thinking
│   ├── moriarty.md       # Game theory / adversarial testing
│   ├── adler.md          # Emotional intelligence / social dynamics
│   ├── lestrade.md       # Evidence chain / pragmatic action
│   └── hound.md          # Fear & bias detection
├── judge.md              # LLM-as-Judge evaluation prompt
├── test-cases/
│   ├── tech-decision.md      # Rust vs Go scenario
│   ├── business-strategy.md  # SaaS growth stagnation
│   ├── knowledge-building.md # Quantum computing & cryptography
│   ├── ethical-dilemma.md    # Co-founder legal risk
│   └── meta-analysis.md      # Framework self-critique
└── README.md             # Usage documentation
```

---

## 3. Persona Design

### 3.1 Unified Persona Structure

Every persona prompt contains three elements:

1. **Mind Anchor** — A one-sentence core cognitive stance (canonical quote where possible)
2. **Core Questions** — 3-5 questions this persona always asks about a problem
3. **Blind Spot Declaration** — What this persona naturally overlooks or undervalues

### 3.2 The Seven Personas

#### 🔍 Sherlock Holmes — Deductive Reasoning
- **Anchor**: "When you have eliminated the impossible, whatever remains, however improbable, must be the truth."
- **Core Questions**: What details are others ignoring? What hypotheses have been ruled out? Does the evidence chain close?
- **Blind Spot**: Emotional factors, social conventions, moral intuition

#### 📋 Dr. Watson — Common-Sense Induction
- **Anchor**: "What seems extraordinary is often the result of ordinary causes."
- **Core Questions**: What's the most mundane explanation? What does prior experience suggest? What would an ordinary person do here?
- **Blind Spot**: Rare events, edge cases, counter-intuitive truths

#### 🧠 Mycroft Holmes — Systems Thinking
- **Anchor**: "The problem is never isolated. Every fact is a node in a larger system."
- **Core Questions**: What is the larger system at play? What indirect or distal factors are operating? What are the structural/policy-level root causes?
- **Blind Spot**: Execution details, individual variance, emotion-driven behavior

#### ♟️ Professor Moriarty — Adversarial / Game Theory
- **Anchor**: "Every system has a vulnerability. Every plan has a counter-plan."
- **Core Questions**: Where would a smart adversary strike? What's the worst case? What are we overconfident about?
- **Blind Spot**: Good-faith assumptions, cooperative dynamics, ethical boundaries

#### 👁️ Irene Adler — Social/Emotional Intelligence
- **Anchor**: "People reveal more in what they hide than in what they show."
- **Core Questions**: What are people's real motivations (vs. stated ones)? How do social dynamics affect outcomes? What hidden assumptions are unspoken?
- **Blind Spot**: Pure technical/physical constraints, non-social problems

#### 🕵️ Inspector Lestrade — Evidence & Pragmatism
- **Anchor**: "A theory is only as good as the evidence that supports it—and the action it enables."
- **Core Questions**: What hard evidence do we have? What's the next verifiable step? Is this procedurally sound? Is the plan executable?
- **Blind Spot**: Theoretical breakthroughs, disruptive innovation, long-term vision

#### 🎯 The Hound — Fear & Bias Detection
- **Anchor**: "What you fear most is often what you should examine closest."
- **Core Questions**: What are we most afraid to admit? What assumptions remain unchallenged out of fear? What information is being avoided or exaggerated? Where might superstition, bias, or emotion-driven judgment be at play?
- **Blind Spot**: Genuine opportunities, warranted optimism, established facts not requiring suspicion

---

## 4. Dispatch Logic

### 4.1 Problem Classification

A lightweight initial prompt classifies the user's query into one of:

| Problem Type | Default Personas (standard) | Rationale |
|-------------|---------------------------|-----------|
| Technical Decision | holmes, lestrade, moriarty | Deduction + evidence + stress-test |
| Business Strategy | moriarty, adler, hound | Competition + human factors + bias check |
| Knowledge Building | watson, mycroft, holmes | Accessibility + structure + core causality |
| Interpersonal/Ethical | adler, lestrade, moriarty | Motivation + process + game theory |
| Creative/Ideation | adler, watson, holmes | Human insight + accessibility + pattern recognition |
| Risk Assessment | moriarty, hound, mycroft | Adversarial + bias + systems |
| General/Mixed | holmes, watson, moriarty | Broad coverage default |

`--depth quick` takes the first 2; `--depth deep` uses all 7.

### 4.2 CLI Interface

```
/sherlock [--depth quick|standard|deep] [--personas holmes,moriarty] [--tldr] [--baseline] "<query>"
```

| Flag | Default | Description |
|------|---------|-------------|
| `--depth` | `standard` | Analysis depth: 2 / 3-4 / 7 personas |
| `--personas` | auto | Comma-separated persona override |
| `--tldr` | false | Core findings + actions only |
| `--baseline` | false | Include raw model response for comparison |

---

## 5. Synthesis Logic

### 5.1 Three-Layer Synthesis

```
Persona outputs → Layer 1: Conflict Mining → Layer 2: Blind Spot Synthesis → Layer 3: Action Pathway → Final Report
```

### 5.2 Layer 1: Conflict Mining

Detect three types of deep conflict (not surface disagreements):

| Conflict Type | Detection Pattern | Example |
|--------------|------------------|---------|
| Assumption Conflict | Two personas make contradictory assumptions about the same variable | Holmes assumes team can learn Rust; Lestrade assumes learning curve is the decisive bottleneck |
| Weighting Conflict | Personas assign different priority orderings to the same factors | Moriarty ranks attack surface #1; Watson ranks development speed #1 |
| Interpretation Conflict | Same fact, different interpretations | "Growth stalled" → Adler: positioning problem; Lestrade: execution problem |

### 5.3 Targeted Conflict Rebuttal

- Select top-2 conflicts by impact-on-decision ranking
- Construct rebuttal prompt: "Persona A argues X. You argue Y. Specifically address A's reasoning. Where does A go wrong?"
- Both personas respond; synthesis layer makes final adjudication

### 5.4 Layer 2: Blind Spot Synthesis

- Aggregate all persona blind spot declarations
- Identify dimensions where **zero personas** have coverage
- Report these silences as the most valuable findings

### 5.5 Layer 3: Action Pathway

Generate three tiers of actionable next steps:

- **Immediate** (within 24h): Based on Holmes + Lestrade consensus
- **Short-term** (1-2 weeks): Based on Moriarty's pressure points
- **Long-term**: Based on Mycroft's systemic observations

### 5.6 Output Formats

**Full Report**:
```markdown
# Analysis: {query summary}

## 🔬 Core Findings
(3-5 key discoveries — not conclusions, but "what we found")

## ⚔️ Key Divergences
| Divergence | Persona A | Persona B | Implication |

## 👁️ Silent Dimensions
(What no persona covered — potentially the real blind spot)

## 🗺️ Multi-Perspective Panorama
(Each persona's core argument, conflicts annotated)

## 🎯 Action Recommendations
- [Immediate] ...
- [Short-term] ...
- [Long-term] ...

## 📊 Analysis Metadata
- Personas dispatched: {list}
- Persona fidelity score: {score}
- Confidence: {high/medium/low with rationale}
```

**TL;DR Mode** (`--tldr`): Core Findings + Action Recommendations only (fits one screen).

---

## 6. Quantitative Validation Framework

### 6.1 Scoring Dimensions (1-10 per persona per test case)

| Dimension | 1-point Anchor | 5-point Anchor | 10-point Anchor |
|-----------|---------------|----------------|-----------------|
| **Novelty** | Identical to raw model response | 2-3 new angles | Reframes the user's initial framing |
| **Persona Fidelity** | Could swap name, output unchanged | Clear persona signature | Bears the persona's unique cognitive signature |
| **Rigor** | Obvious logical gaps | Complete traceable reasoning chain | Every assertion has explicit derivation |
| **Conflict Density** | Aligns with all other personas | Substantive disagreement with ≥1 persona | Core-level viewpoint collision |
| **Actionability** | Abstract conclusions only | Concrete directions given | Immediately executable next steps |

### 6.2 Aggregate Metrics

| Metric | Formula | v0.1 Pass Threshold |
|--------|---------|---------------------|
| Framework Gain (FG) | mean(Novelty_framework) / Novelty_baseline | ≥ 1.5 |
| Perspective Dispersion (PD) | std(pairwise cosine distances of persona output embeddings) | ≥ 0.3 |
| Blind Spot Coverage (BSC) | count(new dimensions in report not in original query) / persona_count | ≥ 0.5 |

### 6.3 Baseline Comparison

Three-group design per test case:

| Group | What It Measures |
|-------|-----------------|
| A (Raw model, no framework) | Baseline |
| B (Framework, single persona only) | Single-persona value |
| C (Framework, full pipeline) | Total framework gain |

Comparisons: C vs A (total gain), C vs B (multi-perspective increment), B vs A (persona fidelity alone).

### 6.4 Scoring Method

LLM-as-Judge: a standalone evaluation prompt (`judge.md`) receives the test case definition + persona outputs + baseline output, and returns structured scores. The judge prompt itself must pass the validation suite (meta-evaluation).

### 6.5 Test Cases (v0.1)

1. **tech-decision**: Rust vs Go for real-time data processing (Python team)
2. **business-strategy**: SaaS growth stagnation with team blame dynamics
3. **knowledge-building**: Quantum computing impact on cryptography (non-expert)
4. **ethical-dilemma**: Co-founder concealed legal risk during fundraising
5. **meta-analysis**: Apply the framework to critique itself

### 6.6 Test Output Format

```json
{
  "test_case": "tech-decision-rust-vs-go",
  "timestamp": "2026-07-21",
  "baseline": { "novelty": 3.2, "rigor": 5.1, "actionability": 4.0 },
  "framework": {
    "framework_gain": 2.1,
    "perspective_dispersion": 0.38,
    "blind_spot_coverage": 0.71,
    "character_scores": {
      "holmes":   { "novelty": 7, "persona_fidelity": 8, "rigor": 9, "conflict_density": 6, "actionability": 7 },
      "watson":   { "novelty": 4, "persona_fidelity": 7, "rigor": 6, "conflict_density": 2, "actionability": 5 },
      "moriarty": { "novelty": 8, "persona_fidelity": 9, "rigor": 7, "conflict_density": 9, "actionability": 6 }
    }
  }
}
```

### 6.7 Pass/Fail Criteria

| Metric | Threshold |
|--------|-----------|
| Framework Gain | ≥ 1.5 |
| Perspective Dispersion | ≥ 0.3 |
| Blind Spot Coverage | ≥ 0.5 |
| Any two persona outputs cosine similarity | ≤ 0.85 |

---

## 7. v0.1 Scope Boundary

### In Scope
- 7 persona definitions with unified structure
- Problem classifier + dispatch layer
- Multi-agent parallel analysis
- Three-layer synthesis (conflict + blind spot + action)
- Full report + TL;DR output
- 5-dimensional quantitative scoring via LLM-as-Judge
- 5 test cases with baseline comparison
- MIT license, public GitHub repo

### Out of Scope (future versions)
- Persistent persona memory across sessions
- Custom user-defined personas
- Domain-specific persona extensions
- Visual output (diagrams, dashboards)
- Integration with external data sources
- Streaming output
- Fine-tuned evaluation models
