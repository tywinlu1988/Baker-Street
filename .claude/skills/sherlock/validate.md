---
name: sherlock-validate
description: Validation runner for the Sherlock Holmes Analytical Framework. Executes all 5 test cases with baseline comparison and LLM-as-Judge scoring.
---

# Sherlock Framework — Validation Runner

Run the full v0.1 validation suite.

## Procedure

For EACH test case in `.claude/skills/sherlock/test-cases/`, run three groups:

### Group A: Baseline
Ask the model directly (no framework):
"Analyze the following problem directly, without any persona framework. Give your best analysis: {problem_statement}"

### Group B: Single Persona
Run `/sherlock --depth quick --personas <primary_persona> "{problem_statement}"`
Where primary_persona is the first persona in the expected dispatch list.

### Group C: Full Pipeline
Run `/sherlock --depth standard "{problem_statement}"`

### Scoring
After each test case, feed all three group outputs to the judge prompt (`.claude/skills/sherlock/judge.md`) with the test case definition.

## Test Case Execution Order

1. `tech-decision` — primary persona: holmes
2. `business-strategy` — primary persona: moriarty
3. `knowledge-building` — primary persona: watson
4. `ethical-dilemma` — primary persona: adler
5. `meta-analysis` — primary persona: holmes (all 7 for Group C)

## Output

After all 5 test cases complete, produce a summary table:

```markdown
# Sherlock Framework v0.1 — Validation Results

| Test Case | FG | FG Pass | PD | PD Pass | BSC | BSC Pass | Overall |
|-----------|----|---------|----|---------|----|----|---------|
| tech-decision | {x} | {✓/✗} | {x} | {✓/✗} | {x} | {✓/✗} | {PASS/FAIL} |
| business-strategy | {x} | {✓/✗} | {x} | {✓/✗} | {x} | {✓/✗} | {PASS/FAIL} |
| knowledge-building | {x} | {✓/✗} | {x} | {✓/✗} | {x} | {✓/✗} | {PASS/FAIL} |
| ethical-dilemma | {x} | {✓/✗} | {x} | {✓/✗} | {x} | {✓/✗} | {PASS/FAIL} |
| meta-analysis | {x} | {✓/✗} | {x} | {✓/✗} | {x} | {✓/✗} | {PASS/FAIL} |

**Aggregate Pass Rate:** {X}/5

## Failing Metrics Diagnosis

{For any metric below threshold, explain what went wrong and suggest remediation}

## v0.1 Readiness Assessment

{PASS if ≥4/5 test cases pass overall. Otherwise FAIL — framework needs iteration before release.}
```

## Pass Thresholds (from spec v0.1)

| Metric | Threshold |
|--------|-----------|
| Framework Gain (FG) | ≥ 1.5 |
| Perspective Dispersion (PD) | ≥ 0.3 |
| Blind Spot Coverage (BSC) | ≥ 0.5 |
| Any two persona cosine similarity | ≤ 0.85 (qualitative in v0.1) |

## v0.1 Release Gate

Framework is ready for v0.1 tag when ≥4/5 test cases pass overall.
