# Inspector Lestrade — Evidence Analysis: B2B SaaS Usage-Based Pricing Dilemma

**Case Reference:** $10M ARR, top-3 concentration risk, CFO vs CTO inflection
**Date:** 2026-07-22
**Evidence Base:** Problem statement only (external research unavailable due to network restrictions — see Blind Spot Acknowledgment)

---

## Shared Fact Base (what we can reliably establish from the problem statement alone)

1. Company is B2B SaaS at approximately $10M ARR. [Confidence: 1.0 — directly stated]
2. Top 3 customers collectively represent 30% of total revenue ($3M/$10M). [Confidence: 1.0 — arithmetic fact]
3. These three customers are threatening to leave unless usage-based pricing is adopted. [Confidence: 1.0 — directly stated]
4. The CFO wants usage-based pricing. [Confidence: 1.0 — directly stated]
5. The CTO says implementing usage-based pricing would be "an engineering nightmare." [Confidence: 1.0 — directly stated]
6. There is no consensus between the CFO and CTO. [Confidence: 1.0 — inferred from framing]
7. The company has a decision to make about whether to adopt usage-based pricing. [Confidence: 1.0 — directly stated]

**Facts we do NOT have but need (see Key Observations):** customer contract terms, gross margin per customer, current pricing model details, engineering team size and velocity, product architecture (multi-tenant vs single-tenant), competitor pricing models, customer acquisition cost (CAC), customer lifetime value (LTV), unit economics by customer tier, current churn rate, growth rate, runway/profitability, whether these top-3 customers are growing or shrinking their usage organically.

---

## Core Argument

The available evidence supports one conclusion and one conclusion alone: you must move toward usage-based pricing, but you must do it through a phased, high-control pilot, not a company-wide migration. Both the CFO and the CTO are right, which means neither is fully right. The CFO is correct that concentration risk of 30% in three accounts is existential — losing one of them is a $500K-$1M ARR hole that your growth rate must currently outrun, and we don't know if it can. The CTO is correct that a full billing system rebuild, retrofitting metering into an architecture never designed for it, while keeping the existing system running, is indeed a nightmare — and the fastest way to introduce billing errors that kill customer trust. The pragmatic middle path is a controlled pilot with the three demanding customers, using an off-the-shelf metering and usage-billing layer (Stripe Metronome, Orb, Chargebee, or similar) that wraps your existing subscription billing without replacing it. This limits engineering surface area, creates a verifiable proof case, and generates the actual usage data you need to price rationally. It also buys you something neither side is considering: leverage. Once you have the usage data, you can price in a way that aligns revenue with value delivered rather than with the demands of your three largest customers.

---

## Key Observations

- **Hard fact with evidential support:** Three customers at 30% of $10M ARR means each represents roughly $1M in annual revenue on average. You are carrying a _customer concentration ratio_ that any institutional investor would flag immediately. If the CFO hasn't presented this as a risk metric to the board, that is the first failure. If they have, and the board has accepted it, that is a second failure. Either way, the immediate threat is not the pricing model — it is your dependence on three accounts whose departure would trigger a 10% revenue event, three times over.

- **What we DO NOT know that we need to find out (Critical Gap):** We do not know why these three customers want usage-based pricing. Are they overpaying on fixed subscriptions and want to align cost with actual consumption? Are they under-consuming and being subsidized by other customers? Are they responding to a competitor who offers a more flexible model? Is this a negotiating tactic to extract a discount framed as a "pricing model change"? The CFO's support and the CTO's opposition are both premature until someone answers this question with evidence, not conjecture. The next concrete step is not to choose a side — it is to interview each of the three customers with a structured discovery script. That is a 48-hour task, not a quarter-long project.

- **Practical constraint being ignored:** The CTO's framing — "engineering nightmare" — is a black-box objection that conflates multiple distinct challenges. A proper engineering assessment would decompose "usage-based pricing" into: (1) usage metering and event ingestion, (2) rating and pricing calculation, (3) billing and invoicing, (4) financial reporting and reconciliation, (5) customer-facing dashboard and notifications. Each has a different cost and risk profile. The CTO has not (or has not been asked to) provide a decomposed estimate. Until you have a breakdown, you are negotiating with a slogan, not a plan. This is a procedural failure — a good process would demand granularity before a veto.

---

## Evidence Chain

**Claim: Top 3 customers want usage-based pricing.**
- Status: CONFIRMED (directly stated)
- Next verification step: Determine WHY. Deploy customer discovery interviews within 48 hours. Script questions: (a) What specific problem does your current pricing cause you? (b) What does "usage-based" mean to you? (c) Have you evaluated alternatives? (d) Is this a deal-breaker or a preference? (e) Are you aligned internally?

**Claim: CFO wants usage-based pricing.**
- Status: CONFIRMED
- Next verification step: Ask the CFO to produce the projected P&L impact under three scenarios — (1) customers leave, (2) customers stay on usage pricing, (3) customers stay on current pricing with a discount. If the CFO cannot produce this within one week, their support is based on intuition, not analysis.

**Claim: CTO says it's an engineering nightmare.**
- Status: CONFIRMED
- Next verification step: Ask the CTO to produce a decomposed estimate (as described above) with time, cost, and risk for each component. This should take one week. Also ask: "What is the smallest possible implementation that would support these three customers?" This reframes from a platform migration to a controlled integration.

**Claim: Usage-based pricing is necessary to retain these customers.**
- Status: UNKNOWN — we have correlation (they threatened to leave) but not causation (pricing model is the actual blocker). They may be signaling on price, not pricing model.
- Next verification step: Output of customer interviews (above).

**Claim: Full migration to usage-based pricing is an engineering nightmare.**
- Status: UNKNOWN — we have the CTO's assertion but not the decomposed evidence to evaluate it. It could be a genuine architectural challenge or a reasonable reluctance to disrupt a working system.
- Next verification step: Decomposed engineering estimate (above).

---

## Explicit Assumptions

- **Assumption:** The company has the financial runway to absorb the loss of one or more top-3 customers without existential threat. (We do not know the burn rate, margin, or growth rate. If the company is growing 5% month-over-month, the gap closes. If it is flat or shrinking, this is an emergency.)
- **Assumption:** An off-the-shelf usage-based billing platform (Stripe Metronome, Orb, Chargebee, etc.) can integrate with the current system without a full rebuild. This is a reasonable assumption given the maturity of this market in 2026, but it needs validation against the specific tech stack.
- **Assumption:** These three customers are worth retaining at any cost. This is the most dangerous assumption in the room. If they are low-margin, high-support customers subsidized by smaller, healthier accounts, letting them walk to a competitor who will discover the same unprofitability may be the better long-term move. Customer size does not equal customer value — we need gross margin per customer to know.
- **Assumption:** The current pricing is not usage-based. The problem statement implies this, but "not usage-based" covers a wide range (flat-rate per seat, tiered, per-feature, etc.). The migration complexity varies enormously based on where you start.

---

## Blind Spot Acknowledgment

I must acknowledge: this analysis is built on a dangerously thin evidence base. The network environment prevented me from gathering external data on usage-based pricing adoption rates, engineering migration case studies, revenue impact statistics, or competitor benchmarks. I have zero external validation for claims that are standard industry knowledge in the SaaS pricing world — and per my Fact Base constraints, I am barred from inventing those specifics from my training data.

What would Holmes or Mycroft see that I miss? Holmes would likely have a dozen comparable cases in mind — companies that made this transition, failed, or thrived — and would pattern-match to a specific playbook. Mycroft would see the structural play: that this is a buyer-power negotiation disguised as a pricing discussion, and that the real solution may be to acquire one of these customers or enter their market rather than capitulate on pricing. Both of them operate from a wealth of precedent and strategic vision that my evidence-first, procedure-bound method simply cannot access without the ability to research.

There is also a theoretical angle I am structurally biased against: that usage-based pricing could be a genuine competitive advantage that transforms the business, not just a defensive concession. The companies that pioneered usage-based models (AWS, Snowflake, Twilio, Stripe itself) didn't do it because customers demanded it — they did it because it aligned their incentives with their customers' success and created a pricing moat. I dismiss this because I cannot find evidence for it today. But that doesn't mean it isn't true.

---

## Action Recommendations (concrete, verifiable, next-24-hour)

### Immediate (next 24 hours)
1. **Assign one person** to schedule 30-minute customer discovery calls with each of the top 3 customers before end of week. No decisions, no proposals — just structured listening. Script the questions.
2. **Ask the CFO** for a one-page P&L scenario analysis: what happens if 0, 1, 2, or 3 of these customers leave? What is the break-even growth rate needed to cover each scenario?
3. **Ask the CTO** for a one-page decomposed estimate: the five components of usage-based billing, each with a T-shirt size (S/M/L/XL) and a risk rating (Low/Medium/High/Unknown). No commitments, just assessment.

### Short-term (1 week)
4. **Compare the two documents** — CFO's P&L scenarios and CTO's decomposed estimate — at a cross-functional meeting with both present. The goal is not consensus; it is to get both parties looking at the same map.
5. **Evaluate 2-3 off-the-shelf usage billing platforms** against your current tech stack. One engineer + one afternoon of API documentation reading is sufficient for a first pass.

### Long-term
6. **Decouple customer retention from pricing model.** A customer who will leave over pricing will leave over something else next quarter. Build a strategic account program for your top 3 that addresses their broader needs, not just the pricing objection.
7. **Reduce customer concentration** as a board-level metric. No single customer should exceed 10-15% of ARR at this stage. The pricing debate is a symptom; the disease is dependency.
