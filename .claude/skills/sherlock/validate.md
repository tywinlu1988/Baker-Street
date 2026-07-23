---
name: sherlock-validate
description: Validation runner for the Sherlock Holmes Analytical Framework. Executes all 5 test cases with baseline comparison and LLM-as-Judge scoring.
---

# Sherlock Framework — Validation Runner

Run the v0.3.x validation suite.

## Procedure

For EACH test case in `.claude/skills/sherlock/test-cases/`, run four groups:

### Group A: Baseline (raw model)
Ask the model directly: "Analyze the following problem directly, without any persona framework. Give your best analysis: {problem_statement}"

### Group B: Monolithic Multi-Perspective (comparison, added v0.3.0)
Give the model all 7 persona definitions + the problem in a single prompt. This is the **critical comparison** — measuring whether the pipeline adds value over a well-crafted flat prompt.

### Group C: Full Pipeline (standard)
Run `/sherlock --depth standard "{problem_statement}"`

### Group D: Full Pipeline (deep research)
Run `/sherlock --depth deep --research-depth deep "{problem_statement}"`

### Scoring
After each test case, feed all four group outputs to the judge prompt (`.claude/skills/sherlock/judge.md`). Score on all 7 v0.3.x dimensions: FG, PD, BSC, CUR, Anti-Sycophancy Score, Tool Usage Effectiveness, Persona Distinctiveness.

## Test Case Execution Order

1. `tech-decision` — primary persona: holmes
2. `business-strategy` — primary persona: moriarty
3. `knowledge-building` — primary persona: watson
4. `ethical-dilemma` — primary persona: adler
5. `meta-analysis` — primary persona: holmes (all 7 for Group C)

## Output

After all 5 test cases complete, produce a summary table:

```markdown
# Sherlock Framework v0.3.x — Validation Results

| Test Case | FG | PD | CUR | AS% | TUE | Distinct | Overall |
|-----------|:--:|:--:|:--:|:--:|:--:|:--------:|:-------:|
| tech-decision | {x} | {x} | {x} | {x}% | {x} | {N}/7 | {PASS/FAIL} |
| business-strategy | {x} | {x} | {x} | {x}% | {x} | {N}/7 | {PASS/FAIL} |
| knowledge-building | {x} | {x} | {x} | {x}% | {x} | {N}/7 | {PASS/FAIL} |
| ethical-dilemma | {x} | {x} | {x} | {x}% | {x} | {N}/7 | {PASS/FAIL} |
| meta-analysis | {x} | {x} | {x} | {x}% | {x} | {N}/7 | {PASS/FAIL} |

**Aggregate Pass Rate:** {X}/5 (v0.3.x: ≥ 4/5 for provisional, ≥ 5/5 for full)

### A/B Delta (Pipeline vs Monolithic)

| Test Case | Pipeline Gain | Worth the tokens? |
|-----------|:------------:|:-----------------:|
| tech-decision | {x} | {yes/no} |
| ... | | |

## Failing Metrics Diagnosis

{For any metric below threshold, explain what went wrong and suggest remediation}

## v0.3.x Readiness Assessment

{PASS if ≥4/5 test cases pass overall AND pipeline shows measurable gain over Group B in ≥3/5 cases.}
```

## Pass Thresholds (v0.3.x)

| Metric | Threshold |
|--------|-----------|
| Framework Gain (FG) | ≥ 1.5 |
| Perspective Dispersion (PD) | ≥ 0.3 |
| Claim Uniqueness Ratio (CUR) | ≥ 0.5 |
| Anti-Sycophancy Score (AS) | ≥ 8% |
| Tool Usage Effectiveness (TUE) | ≥ 5 |
| Persona Distinctiveness | ≥ 3/7 distinguishable |
| Blind Spot Coverage (BSC) | ≥ 0.5 |

## v0.3.x Release Gate

Framework is ready for v0.3.x tag when:
- ≥ 4/5 test cases pass overall (provisional)
- ≥ 5/5 for full release
- Pipeline shows measurable anti-sycophancy gain over Group B (monolithic) in ≥ 3/5 cases
