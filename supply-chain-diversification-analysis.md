# Supply Chain Diversification Analysis

## Inspector Lestrade — Operational Assessment

**Case:** Hardware startup, single Taiwan-based chip supplier, nervous investors.
**Date:** 23 July 2026
**Status:** ACTIONABLE — moderate urgency, not crisis

---

## Core Argument

The evidence supports that diversification is necessary but not immediately urgent at the existential level. The Fact Base confirms no imminent Chinese invasion of Taiwan before 2027 (confidence 0.85), giving the startup a window of approximately 12-18 months to execute a structured diversification plan. However, the concentration risk is real and growing: TSMC controls ~95% of advanced node production (confidence 0.9), and US chip production remains at only ~10% of global supply (confidence 0.85). The startup should begin diversification immediately — not because Taiwan falls tomorrow, but because the lead time for alternatives (38 months US fab construction, confidence 0.8) means the decision-to-delivery gap is the real threat. The Jan 2026 US-Taiwan Silicon Pact ($500B, confidence 0.9) signals that both governments treat this as a systemic risk. A hardware startup that cannot demonstrate a credible diversification plan to its investors by Q4 2026 is accepting valuation haircuts it does not need to accept.

---

## Key Observations

- **TSMC concentration is the single biggest supply-chain vulnerability in the industry.** At ~70% global foundry share and ~95% of sub-7nm production, there are no equivalent alternatives for advanced nodes. This is not speculative — it is the current state of the market.

- **The threat timeline gives you 12-18 months, not 3-5 years.** US intelligence assesses no invasion before 2027 (confidence 0.85). But "no imminent invasion" is not "no risk." Trade disruptions, export controls, or a blockade could materialize with far less lead time than a military invasion.

- **Alternative foundries exist but with serious trade-offs.** Samsung 2nm yields are stuck at ~50% (confidence 0.8) — not viable for production. Intel 18A yields are healthy at 85% but the foundry division is losing $2.4B/quarter (confidence 0.8), raising questions about long-term commitment. Qualcomm (confidence 0.8) and AMD (confidence 0.8) are already moving to dual-sourcing, which validates the strategy but also means they will consume the available capacity.

- **The US fab buildout is real but slow.** 38 months vs 20 months in Taiwan, at roughly 2x cost (confidence 0.8). TSMC Arizona's 3nm production is expected H2 2027 (confidence 0.85) — that is the earliest meaningful US-based advanced node capacity, and it is already spoken for by Apple and Nvidia.

---

## Evidence Chain

| Claim | Confidence | Status | Verification Step |
|-------|-----------|--------|-------------------|
| TSMC ~70% foundry share, ~95% advanced node | 0.9 | CONFIRMED | Cross-check IC Insights Q2 2026 data |
| No imminent Chinese invasion before 2027 | 0.85 | CONFIRMED | Monitor CIA/DoD quarterly threat assessments |
| TSMC Arizona 3nm production H2 2027 | 0.85 | CONFIRMED | Track TSMC Arizona construction milestones |
| Samsung 2nm yields ~50% | 0.8 | CONFIRMED | Request Samsung foundry qualification samples |
| Intel 18A yields 85%, losing $2.4B/quarter | 0.8 | CONFIRMED | Monitor Intel foundry earnings calls |
| US-Taiwan Silicon Pact $500B | 0.9 | CONFIRMED | Verify pact appropriations status |
| US fab construction 38 months, ~2x cost | 0.8 | CONFIRMED | Compare with actual TSMC Arizona timeline |
| Qualcomm dual-sourcing TSMC+Samsung | 0.8 | CONFIRMED | Verify Qualcomm supplier disclosures |
| AMD Samsung 2nm for EPYC 2027 | 0.8 | CONFIRMED | Check AMD foundry announcements |
| US ~10% global chip production | 0.85 | CONFIRMED | Cross-check SIA data |

**Blind spots in the evidence:**
- Unknown: What node does this startup need? If it is 28nm+ (mature nodes), alternatives exist (UMC, GlobalFoundries, SMIC). This distinction is critical and is NOT in the Fact Base.
- Unknown: Startup's current volume and annual wafer demand. Diversification feasibility depends entirely on scale.
- Unknown: Whether the startup's chip is designed for a specific TSMC process (e.g., N3, N5) or is process-agnostic.

---

## Explicit Assumptions

1. **The startup is on an advanced node (<7nm).** If it is on a mature node, the urgency drops sharply and alternatives already exist. This assumption MUST be verified.

2. **The startup has at least 18 months of cash runway.** Diversification requires NRE (non-recurring engineering) costs for porting to a second foundry — typically $5M-$20M depending on design complexity.

3. **Investor nervousness is the binding constraint.** Technical risk can be managed; loss of investor confidence cannot be ignored because it cuts off the capital needed to execute the technical solution.

4. **The startup's current sole supplier is TSMC specifically.** If it is another Taiwan-based foundry (e.g., Vanguard, Powerchip), the analysis shifts but the geographic concentration risk remains.

---

## Concrete Action Plan

### Phase 1 — Diagnostics (Weeks 1-4)

| Step | Owner | Deadline | Verifiable Outcome |
|------|-------|----------|-------------------|
| 1.1 Pin your exact process node and TSMC process name | Engineering lead | Week 1 | Document with TSMC process design kit (PDK) version |
| 1.2 Calculate annual wafer volume, projected 3-year demand | Ops + Finance | Week 2 | Signed-off demand forecast |
| 1.3 Request porting feasibility study from Samsung Foundry | Engineering | Week 3 | Samsung PDK compatibility report |
| 1.4 Request porting feasibility study from Intel Foundry | Engineering | Week 4 | Intel 18A PDK compatibility report |
| 1.5 Survey non-TSMC Taiwan foundries (UMC, Powerchip) as interim hedge | Supply chain | Week 4 | Alternative foundry capability matrix |

### Phase 2 — Decision (Weeks 5-8)

| Step | Owner | Deadline | Verifiable Outcome |
|------|-------|----------|-------------------|
| 2.1 Compile porting cost estimates (NRE) for each alternative | Engineering + Finance | Week 6 | Cost comparison table |
| 2.2 Assess yield risk: Samsung 50% yields vs Intel $2.4B/quarter loss | CTO | Week 7 | Risk-adjusted cost-per-good-die model |
| 2.3 Present dual-sourcing strategy to board | CEO | Week 8 | Board resolution authorizing diversification |
| 2.4 Draft investor communication plan | CEO + IR | Week 8 | Investor FAQ document on supply chain resilience |

### Phase 3 — Execution (Months 3-12)

| Step | Owner | Deadline | Verifiable Outcome |
|------|-------|----------|-------------------|
| 3.1 Begin tape-out on secondary foundry | Engineering | Month 3 | GDSII submitted to secondary foundry |
| 3.2 Negotiate capacity reservation agreement with secondary foundry | Supply chain + Legal | Month 4 | Signed LTA (Long-Term Agreement) |
| 3.3 First engineering samples from secondary foundry | Engineering | Month 8 | First silicon — functional verification |
| 3.4 Qualification and reliability testing | Quality | Month 10 | Qualification report signed off |
| 3.5 Ramp secondary source to 20-30% of volume | Ops | Month 12 | Secondary source shipping production wafers |

### Investor Communication Timeline

- **Q3 2026:** Present diversification plan to key investors. "We have identified the risk and have a structured mitigation plan with clear milestones."
- **Q4 2026:** Announce dual-sourcing agreement. "We have signed with [Samsung/Intel/UMC] as our second source. First silicon expected Q2 2027."
- **Q2 2027:** First engineering samples from secondary source. "Dual-sourcing is now operational. We are on track to de-risk 30% of volume by Q4 2027."

---

## Verification Protocol

How will we know if the plan is working or failing?

**Green lights (plan on track):**
- Samsung/Intel PDK compatibility report returned positive by Week 4
- Porting NRE cost within 15% of initial estimate
- First silicon from secondary foundry meets >80% of performance targets

**Red flags (escalate immediately):**
- Samsung yields remain below 60% through Q1 2027
- Intel Foundry division announces restructuring or divestiture
- US intelligence assessment changes to "credible threat within 12 months"
- TSMC Arizona 3nm slips beyond H2 2027

---

## Blind Spot Acknowledgment

I am dismissing, because the evidence does not yet exist for it, the possibility that a **disruptive innovation in chip design** could bypass the foundry concentration problem entirely. If this startup's chip could be redesigned for a more mature, multi-sourced node — or if chiplets/advanced packaging allow mixing dies from different foundries — the urgency drops significantly. Holmes or Mycroft might ask: "What if your chip doesn't need the most advanced node? What if you can partition so only one die stays on TSMC N3 and the rest move?" My evidence-first method cannot answer that without the design details. I also cannot assess the viability of **RISC-V + open-source PDK flows** as a long-term hedge — that is too speculative for my methodology but may be the actual solution.

**The single question I cannot answer from the Fact Base but that would resolve the entire analysis:** What process node does this startup's chip require? The answer determines whether this is a 12-alarm fire or a manageable operational risk.

---

## Summary for the Investor Deck

> "We are single-sourced on TSMC, which carries real geopolitical concentration risk. US intelligence assesses no invasion before 2027, giving us an 18-month window. We are initiating a dual-sourcing program immediately: porting feasibility Q3 2026, first silicon from secondary foundry Q2 2027, 30% volume diversified by Q4 2027. Estimated NRE cost: $5-15M. This is a known problem with a known solution. What would be inexcusable is doing nothing."
