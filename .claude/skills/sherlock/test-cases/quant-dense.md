---
name: quant-dense
type: business-strategy
description: Pricing decision with concrete numbers — forces breakeven/simulation demands
---

# Test Case: Pricing Increase Decision

## Problem Statement

"Our project management SaaS charges $50/user/month. We have 400 customers averaging 12 users each ($2.88M ARR). Monthly churn is 3%. Our sales team reports a 25% win rate at $50, but a recent pilot quoting $65 to 40 prospects closed only 18%. CAC is $1,200 per customer. The CEO wants to raise the price to $65 next quarter. Should we do it?"

## Context

- Current MRR: $240K (400 customers × 12 users × $50)
- Proposed: $65/user/month (+30%)
- Gross margin: 80%
- Competitors price at $45-55/user/month
- Last price increase: 18 months ago, caused 5% one-time churn spike

## Expected Dispatch

- Standard depth: moriarty, watson, lestrade (numbers-heavy)
- Deep: all 7

## Evaluation Signals

### Minimum Bar
- [ ] At least one persona computes the breakeven churn tolerance (how much additional churn wipes out the price increase)
- [ ] Watson or Lestrade challenges the pilot's statistical validity (n=40, 18% vs 25% — is the difference significant?)
- [ ] Moriarty models competitive response at $65 vs the $45-55 band
- [ ] The analysis produces a quantitative verdict, not just "it depends"

### Good
- [ ] Monte Carlo or sensitivity analysis on churn scenarios
- [ ] A REVISED annotation shows data changing a persona's initial position
- [ ] CUR ≥ 0.5 (two-round mode)
