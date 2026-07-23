#!/usr/bin/env python3
"""
Sherlock Quantitative Toolkit — Monte Carlo simulation.
Usage: python3 simulation.py <command> [args...]

Commands:
  monte_carlo --base <value> --growth <rate> --vol <volatility> --years <n> [--iterations <n>]
  scenario --base <value> --scenarios <name1=rate1,name2=rate2,...> --years <n>
"""
import sys, json, math, random

def monte_carlo(base, growth_rate, volatility, years, iterations=10000):
    """Project value forward with random growth each year."""
    results = []
    cumulative = []
    for _ in range(iterations):
        val = base
        for _ in range(years):
            annual_growth = random.gauss(growth_rate, volatility)
            val *= (1 + annual_growth)
        results.append(val)
        cumulative.append(val)
    s = sorted(results)
    def p(pct):
        idx = int(len(s) * pct / 100)
        return round(s[min(idx, len(s)-1)], 2)
    return {
        "iterations": iterations,
        "base": base,
        "growth_rate": growth_rate,
        "volatility": volatility,
        "years": years,
        "mean": round(sum(results) / len(results), 2),
        "median": p(50),
        "std": round((sum((x - sum(results)/len(results))**2 for x in results) / (len(results)-1)) ** 0.5, 2),
        "p10": p(10),
        "p25": p(25),
        "p75": p(75),
        "p90": p(90),
        "p95": p(95),
        "probability_of_loss": round(sum(1 for x in results if x < base) / len(results), 4),
        "value_at_risk_95": round(base - p(5), 2),
    }

def scenario(base, scenarios, years):
    """Project value under multiple deterministic scenarios."""
    results = {"base": base, "years": years, "scenarios": {}}
    for name, rate in scenarios.items():
        val = base
        for _ in range(years):
            val *= (1 + rate)
        results["scenarios"][name] = {
            "rate": rate,
            "final_value": round(val, 2),
            "total_return_pct": round((val/base - 1) * 100, 1),
        }
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command. Use: monte_carlo or scenario"}))
        sys.exit(1)

    cmd = sys.argv[1]
    try:
        if cmd == "monte_carlo":
            args = {sys.argv[i].lstrip('-'): sys.argv[i+1] for i in range(2, len(sys.argv), 2)}
            base = float(args.get('base', 100000))
            growth = float(args.get('growth', 0.10))
            vol = float(args.get('vol', 0.05))
            years = int(args.get('years', 5))
            iters = int(args.get('iters', 10000))
            print(json.dumps(monte_carlo(base, growth, vol, years, iters), indent=2))
        elif cmd == "scenario":
            args = {sys.argv[i].lstrip('-'): sys.argv[i+1] for i in range(2, len(sys.argv), 2)}
            base = float(args.get('base', 100000))
            years = int(args.get('years', 5))
            scenarios_raw = args.get('scenarios', 'base=0.10').split(',')
            scenarios = {}
            for s in scenarios_raw:
                name, rate = s.split('=')
                scenarios[name] = float(rate)
            print(json.dumps(scenario(base, scenarios, years), indent=2))
        else:
            print(json.dumps({"error": f"Unknown command: {cmd}"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
