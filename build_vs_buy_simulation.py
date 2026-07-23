#!/usr/bin/env python3
"""Build vs Buy AI Features — Monte Carlo Simulation for Moriarty Analysis"""

import random
import statistics
import math

NUM_SIMULATIONS = 100000
CURRENT_ARR = 8_000_000
BANK = 15_000_000

def simulate_build_outcome():
    """Simulate build strategy"""
    eng_team = random.randint(4, 6)
    eng_salary = 200_000
    infra_per_year = random.uniform(300_000, 800_000)
    yr1_cost = eng_team * eng_salary + infra_per_year + random.uniform(200_000, 500_000)

    abandons = random.random() < 0.67
    if abandons:
        total_cost = yr1_cost
        arr_multiplier = random.uniform(-0.05, 0.05)
        return max(0, CURRENT_ARR * (1 + arr_multiplier)), total_cost, False

    yr2_cost = eng_team * eng_salary + infra_per_year * 1.3 + random.uniform(100_000, 300_000)
    fails = random.random() < 0.85
    if fails:
        total_cost = yr1_cost + yr2_cost
        arr_multiplier = random.uniform(-0.1, 0.15)
        return max(0, CURRENT_ARR * (1 + arr_multiplier)), total_cost, False

    yr3_cost = eng_team * eng_salary * 0.8 + infra_per_year * 1.5
    total_cost = yr1_cost + yr2_cost + yr3_cost
    arr_uplift = random.uniform(0.1, 0.6)
    arr_adj = CURRENT_ARR * (1 + arr_uplift)
    return arr_adj, total_cost, True

def simulate_buy_outcome():
    """Simulate buy strategy"""
    yr1_cost = random.uniform(50_000, 200_000)
    yr2_cost = random.uniform(100_000, 300_000)
    yr3_cost = random.uniform(150_000, 400_000)
    total_cost = yr1_cost + yr2_cost + yr3_cost
    arr_uplift = random.uniform(0.05, 0.25)
    return CURRENT_ARR * (1 + arr_uplift), total_cost, True

build_results = [simulate_build_outcome() for _ in range(NUM_SIMULATIONS)]
buy_results = [simulate_buy_outcome() for _ in range(NUM_SIMULATIONS)]

build_arrs = [r[0] for r in build_results]
build_costs = [r[1] for r in build_results]
build_success = [r[2] for r in build_results]
build_failure_rate = 1 - (sum(build_success) / len(build_success))

buy_arrs = [r[0] for r in buy_results]
buy_costs = [r[1] for r in buy_results]

print("=" * 70)
print("BUILD vs BUY: MONTE CARLO SIMULATION (100,000 runs)")
print("Base: $8M ARR SaaS, 40 people, $15M bank")
print("=" * 70)
print(f"\n--- BUILD STRATEGY ---")
print(f"  Mean ARR after 3 years: ${statistics.mean(build_arrs):,.0f}")
print(f"  Median ARR after 3 years: ${statistics.median(build_arrs):,.0f}")
print(f"  Mean total cost (3yr): ${statistics.mean(build_costs):,.0f}")
print(f"  SD of costs: ${statistics.stdev(build_costs):,.0f}")
print(f"  Overall 'success' rate: {sum(build_success)/len(build_success)*100:.1f}%")
print(f"  Implied failure rate: {build_failure_rate*100:.1f}%")
print(f"  Probability ARR declines: {sum(1 for a in build_arrs if a < CURRENT_ARR)/len(build_arrs)*100:.1f}%")
print(f"  95th percentile ARR: ${sorted(build_arrs)[int(NUM_SIMULATIONS*0.95)]:,.0f}")
print(f"  5th percentile ARR: ${sorted(build_arrs)[int(NUM_SIMULATIONS*0.05)]:,.0f}")
print(f"  Expected value (ARR - cost): ${statistics.mean(build_arrs) - statistics.mean(build_costs):,.0f}")

print(f"\n--- BUY STRATEGY ---")
print(f"  Mean ARR after 3 years: ${statistics.mean(buy_arrs):,.0f}")
print(f"  Median ARR after 3 years: ${statistics.median(buy_arrs):,.0f}")
print(f"  Mean total cost (3yr): ${statistics.mean(buy_costs):,.0f}")
print(f"  SD of costs: ${statistics.stdev(buy_costs):,.0f}")
print(f"  Probability ARR declines: {sum(1 for a in buy_arrs if a < CURRENT_ARR)/len(buy_arrs)*100:.1f}%")
print(f"  95th percentile ARR: ${sorted(buy_arrs)[int(NUM_SIMULATIONS*0.95)]:,.0f}")
print(f"  5th percentile ARR: ${sorted(buy_arrs)[int(NUM_SIMULATIONS*0.05)]:,.0f}")
print(f"  Expected value (ARR - cost): ${statistics.mean(buy_arrs) - statistics.mean(buy_costs):,.0f}")

print("\n\n--- CRITICAL THRESHOLD ANALYSIS ---")
for threshold in [0.3, 0.4, 0.5, 0.6, 0.7]:
    ev_build = (threshold * (CURRENT_ARR * 1.35 - 2_500_000) +
                (1-threshold) * (CURRENT_ARR * 0.98 - 1_200_000))
    ev_buy = CURRENT_ARR * 1.15 - 650_000
    verdict = "BUILD" if ev_build > ev_buy else "BUY"
    print(f"  Success={threshold*100:.0f}%: EV(build)=${ev_build:,.0f}, EV(buy)=${ev_buy:,.0f} => {verdict}")
