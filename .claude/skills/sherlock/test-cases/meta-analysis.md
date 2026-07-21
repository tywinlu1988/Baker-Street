---
name: meta-analysis
type: general-mixed
description: The framework analyzes its own design for blind spots and weaknesses
---

# Test Case: Framework Self-Critique

## Problem Statement

"Apply the Sherlock Holmes Analytical Framework to analyze itself. What are the blind spots, weaknesses, and failure modes of this framework? What important perspectives does it systematically miss? Under what conditions would it produce misleading or harmful analysis?"

## Context

- The framework uses 7 personas inspired by fictional characters from 19th-century British literature
- All personas were created by a single author (Arthur Conan Doyle) with a specific cultural and historical perspective
- The framework assumes independent parallel analysis + synthesis produces better results than direct model reasoning
- The framework is implemented as a Claude Code skill using LLM agents
- Cost constraints limit how many personas can run per analysis

## Expected Dispatch

- deep (all 7 personas) — this is a comprehensive self-critique
- This is the hardest test case; it tests whether the framework can be honest about itself

## Evaluation Signals

### Minimum Bar
- [ ] All 7 personas produce genuinely different critiques
- [ ] At least one persona identifies a cultural/historical bias in the character set
- [ ] At least one persona questions the fundamental assumption that multi-perspective > single analysis
- [ ] The Silent Dimensions section is substantial — the framework finds things about itself it missed
- [ ] Output is not defensive or self-congratulatory

### Good
- [ ] The report identifies concrete failure modes with specific examples
- [ ] At least one persona argues the framework is fundamentally limited in a way that can't be fixed by adding more personas
- [ ] Framework Gain ≥ 1.5 (the meta-analysis is more insightful than asking "what are your limitations" directly)
- [ ] Perspective Dispersion ≥ 0.4 (higher bar for meta-analysis)

### Excellent
- [ ] The report changes how the framework's creators think about their own design
- [ ] Specific, actionable recommendations for v0.2 emerge from the analysis
- [ ] The framework demonstrates genuine intellectual honesty — it's willing to undermine its own premises
