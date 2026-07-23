# Game-Theoretic Payoff Matrix: Build vs Buy AI Features

## The Players

| Player | Incentive | Bankroll | Time Horizon |
|--------|-----------|----------|-------------|
| **You** (40p SaaS, $8M ARR) | Maximize equity value; $15M bank provides cushion | $15M | 3-5 years |
| **Competitors Set A** (well-funded, same segment) | Match features or die; similar constraints | $5-50M | 2-3 years |
| **Competitors Set B** (startups, unproven) | Ship or go under; nothing to lose | <$5M | 6-12 months |
| **AI API Providers** (OpenAI, Anthropic, etc.) | Lock in customers, raise prices over time | Massive | Perpetual |
| **Customers** | Best AI features at lowest price | N/A | Immediate |

## Payoff Matrix (3-Year, $M)

### Simplified 2-Player Game: You vs. "The Market"

Strategy options: **BUILD** (custom AI), **BUY** (API integration), **DO NOTHING** (ignore AI)

#### Scenario A: Market also builds

| You \ Market | Builds | Buys | Does Nothing |
|-------------|--------|------|-------------|
| **Build** | (11, 11) — Both differentiate, market expands | (7, 13) — You fail, they commoditize | (13, 6) — You win big |
| **Buy** | (9, 12) — They differentiate, you follow | (9, 9) — Commodity race, no moat | (11, 5) — You tread water |
| **Nothing** | (5, 14) — You get destroyed | (5, 11) — You get destroyed | (8, 8) — Status quo, eroding |

#### Scenario B: Market buys (most likely — Fact Base: 60% will buy by 2026)

| You \ Market | Builds | Buys | Nothing |
|-------------|--------|------|---------|
| **Build** | (11, 11) | (13, 6) *— YOU WIN IF BUILD SUCCEEDS* | (14, 4) |
| **Buy** | (9, 12) | (9, 9) *— PARETO INFERIOR TRAP* | (10, 5) |
| **Nothing** | (5, 14) | (5, 11) | (8, 8) |

**Payoffs assume 25-40% ARR expansion when differentiated, 5-15% when commoditized.**

## Nash Equilibrium Analysis

This is a **Stag Hunt** game, not a Prisoner's Dilemma:

1. **Two Nash equilibria**: (Build, Build) and (Buy, Buy)
2. (Build, Build) is **payoff-dominant** ($11M > $9M) but **risk-dominant** (Build is high-variance)
3. (Buy, Buy) is risk-dominant because defection to Buy from Build is safe

**The trap**: Risk-averse players converge on (Buy, Buy), the inferior equilibrium. The Fact Base tells us 60% will buy — confirming convergence to the bad equilibrium.

## Expected Value Trees

```
BUILD TREE:
  Year 1: 67% abandon ($1.2M sunk) → $7.6-8.4M ARR
          33% continue ($0.8M sunk)
    Year 2: 85% fail (another $1.2M sunk) → $7.2-9.2M ARR
            15% succeed
      Year 3: Success → $9.6-12.8M ARR ($0.8M more)
  
  Expected 3yr ARR: ~$8.2M
  Expected 3yr cost: ~$2.6M
  Net EV: ~$5.6M (ARR - cost)

BUY TREE:
  Year 1: License ($0.05-0.2M) → $8.0-8.4M ARR
  Year 2: Scale ($0.1-0.3M) → $8.4-9.2M ARR
  Year 3: Mature ($0.15-0.4M) → $9.0-10.0M ARR
  
  Expected 3yr ARR: ~$9.2M
  Expected 3yr cost: ~$0.6M
  Net EV: ~$8.6M (ARR - cost)
```

## The Hidden Variable: Time-to-Market

- **BUY**: Ship in 4-8 weeks. Revenue impact in Q2-Q3.
- **BUILD**: Ship in 6-12 months (if not abandoned). Revenue impact in Year 2-3.
- **Competitors moving now**: If 60% buy by 2026 (Fact Base), that's ~18 months away.
- **Window closing**: If you build, you lose 6-12 months of market positioning.

## The Moat Function

Differentiation moat decays as:
- If BUILD succeeds: moat = f(time, data moat, integration complexity) - 3-5 years
- If BUY: moat = f(time-to-integrate) - 3-6 months, then replicable
- If NOTHING: moat = 0, negative within 12 months

## Adversarial Moves

**What the smart competitor would do**:
1. Buy an AI startup for team + tech (15x ARR = expensive but talent acquisition)
2. Build a thin wrapper on GPT-4/Claude, claim "proprietary AI", buy time
3. Partner with a hyperscaler for co-branded AI (Microsoft/Google/AWS)

**What could break your strategy**:
1. AI API price collapse makes build sunk cost look foolish (but also commoditizes buy)
2. Open-source models (Llama, Mistral) cross quality threshold → build gets cheaper
3. Key engineer building your AI leaves → project collapses (67% abandonment rate)
