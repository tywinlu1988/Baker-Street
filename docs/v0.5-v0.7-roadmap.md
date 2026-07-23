# v0.5-v0.7 Roadmap: Quantitative Pipeline + Champion Mode

## Context

v0.1-v0.4 established the qualitative pipeline: 7 personas with tool access, anti-sycophancy research, CUR metrics, cross-platform support. The framework's proven value is in three structural advantages: anti-sycophancy (counter-evidence enforced), context expansion (multi-agent research beyond single prompt window), and perspective divergence (independent agents, measurable output diversity).

What's missing: the framework operates at the qualitative level. Personas reason from facts but cannot perform statistical analysis, model trends, or verify claims with mathematical rigor. v0.5-v0.7 address this by introducing a quantitative layer, then building toward a "champion mode" where the strongest persona in any given debate can activate deep investigation capabilities.

---

## v0.5: Quantitative Research Layer

### Goal
Add a quantitative analysis pipeline between qualitative research and persona reasoning.

### New Pipeline

```
Phase 1: Research Layer (unchanged)
  → Shared fact base (qualitative)

Phase 1.5: Quantitative Demand Collection (NEW)
  → Each persona submits a data/analysis demand:
    Holmes: "I need time series data to test causality between X and Y"
    Watson: "Calculate ROI and payback period for this investment"
    Moriarty: "Run Monte Carlo simulation on worst-case scenario"
    Lestrade: "Verify claim accuracy with statistical significance testing"
    ...

Phase 1.6: Quantitative Analysis Agent (NEW, single agent)
  → Receives all persona demands
  → Understands, models, computes, collects data
  → Produces: Quantitative Analysis Package (shared JSON)
    {
      "analyses": [
        {
          "requested_by": "moriarty",
          "type": "monte_carlo_simulation",
          "parameters": {...},
          "results": {...},
          "script": "path/to/generated_script.py"
        }
      ]
    }

Phase 2: Reasoning Layer (unchanged)
  → Each persona reads the SAME Quantitative Analysis Package
  → Forms independent quantitative interpretation
```

### Key Design Decisions
- Quantitative analysis is SHARED — all personas see the same numbers, just as they see the same fact base
- The analysis agent is a single executor — not 7 different analysts
- Persona demands are collected BEFORE analysis — no persona runs analysis on its own
- Existing pipeline phases (intake, research, reasoning) are unchanged

### Files to Create/Modify
- NEW: `quantitative-agent-prompt.md` — analysis agent specification
- NEW: `.claude/skills/sherlock/tools/analysis/stats.py` — reusable statistical functions
- NEW: `.claude/skills/sherlock/tools/analysis/simulation.py` — Monte Carlo/forecasting
- MODIFY: `skill.md` — insert Phase 1.5 and 1.6
- MODIFY: persona prompts — add demand submission instruction

### Verification
- 3 E2E tests with quantitative demands
- Each test: verify analysis package contains valid results for each persona demand
- Anti-sycophancy score maintained (>8%)

---

## v0.6: Quantitative Reasoning Layer

### Goal
Constrain persona outputs to be supported by quantitative evidence.

### Changes
1. **Evidence Chain** must cite specific entries from the Quantitative Analysis Package
2. **"Claim → p-value" rule**: qualitative claims about trends, effects, or comparisons must reference statistical results. If unavailable, flagged as unsupported.
3. **CUR extension**: expanded to "Quantitative Support Ratio" — percentage of persona claims backed by analysis results
4. **Report metadata**: new "Quantitative Confidence" section

### Key Design
- Personas are not FORCED to use quantitative analysis — but unsupported claims are flagged
- The synthesis layer checks: "did this persona's key claim cite analysis data?" 
- Honesty principle: better to flag "unsupported" than to force fake quantification

### Files to Modify
- MODIFY: `skill.md` — Layer 1.75 (quantitative support check)
- MODIFY: persona prompts — evidence citation requirements
- MODIFY: `judge.md` — add Quantitative Support scoring dimension

### Verification
- 3 E2E tests: baseline (no quant) vs v0.6 (with quant constraint)
- Framework Gain maintained or improved
- ≥50% of persona claims have quantitative support in v0.6 tests

---

## v0.7: Champion Mode

### Goal
After normal pipeline completes, identify the "breakthrough" persona whose reasoning most decisively won the debate, then activate that persona's deep investigation capabilities.

### Trigger Mechanism
1. Standard pipeline runs (with v0.6 quantitative constraints)
2. Post-synthesis, the conflict layer evaluates: **which persona's core argument was most resistant to rebuttal?**
   - Did other personas fail to counter this persona's key claims?
   - Did this persona's quantitative analysis support hold up better?
   - Did CUR analysis show this persona introduced the most unique insights?
3. If a "champion" emerges (one persona clearly out-argued others), the system offers: "**{Persona} won this debate. Activate deep investigation mode?**"
4. User confirms → Champion Mode activates

### Champion Mode Capabilities (per persona)

| Persona | Deep Mode | Output |
|---------|-----------|--------|
| **Holmes** | Evidence chain closure — cross-reference ALL claims, identify gaps, attempt to fill them via additional research. Build complete deductive tree. | Investigation Report — traceable from evidence to conclusion |
| **Watson** | Practical validation — survey literature for real-world cases that confirm or refute the analysis. Ground every abstract claim in concrete precedent. | Case Documentation — 3-5 real-world examples with lessons |
| **Mycroft** | System dynamics modeling — build causal loop diagrams, simulate feedback effects, project multi-year outcomes under different policy scenarios. | Systems Analysis — structural root causes mapped |
| **Moriarty** | Full adversarial campaign — model competitor responses, run stress scenarios, identify and exploit every vulnerability in the recommended strategy. | Red Team Report — complete adversarial assessment |
| **Adler** | Stakeholder deep-dive — interview simulations, relationship mapping, hidden incentive analysis. Who benefits, who loses, who will resist? | Power Map — complete social/incentive structure |
| **Lestrade** | Systematic verification — every claim tested against hard data. Build verification protocol. Flag unverifiable claims. | Verification Report — what's proven vs what's assumed |
| **Hound** | Fear excavation — structured sessions to surface organizational defense mechanisms, sacred cows, and avoided conversations. | Bias Audit — systematic cognitive distortion mapping |

### Key Design
- Champion Mode is USER-CONFIRMED, not automatic
- It's a separate second phase — the standard report is already delivered
- Champion produces additional file artifacts and an extended report section
- Only ONE persona enters Champion Mode per session

### Files to Create/Modify
- NEW: `champion-prompt.md` — champion mode orchestration
- NEW: persona deep-mode capability specs (one per persona, merged into existing files)
- MODIFY: `skill.md` — champion trigger logic post-synthesis
- MODIFY: report template — Champion Mode section

### Verification
- 3 E2E tests: pipeline → champion identification → deep investigation
- Champion Mode produces measurably novel output (novel claims > baseline + pipeline)
- Champion output is traceable to analysis data
- User confirmation gate works correctly

---

## Summary

| Version | Focus | Pipeline Change | Key New Capability |
|---------|-------|-----------------|-------------------|
| **v0.5** | Quantitative Research | +Phase 1.5, 1.6 | Shared quantitative analysis package |
| **v0.6** | Quantitative Reasoning | Layer 1.75 constraint | Persona claims backed by data |
| **v0.7** | Champion Mode | Post-synthesis trigger | Winner persona deep investigation |
