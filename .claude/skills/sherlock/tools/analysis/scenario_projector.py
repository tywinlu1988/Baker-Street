#!/usr/bin/env python3
"""
Scenario Projector — Multi-year cost/revenue projection tool.
Usage: python3 scenario_projector.py <initial_value> <growth_rate> <years> [scenarios...]

Projects financial metrics across multiple scenarios for comparison.
Part of the Sherlock Framework shared tool library (v0.4.2+).
"""
import sys, json

def project(base, rate, years, label="base"):
    """Project a value forward with compound growth."""
    values = []
    current = base
    for y in range(years + 1):
        values.append({"year": y, "value": round(current, 2)})
        current *= (1 + rate)
    return {"label": label, "base": base, "rate": rate, "projection": values}

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        base = float(sys.argv[1])
        rate = float(sys.argv[2])
        years = int(sys.argv[3])

        scenarios = []
        # Default: base case
        scenarios.append(project(base, rate, years, "base"))

        # Additional scenarios from remaining args
        for i in range(4, len(sys.argv), 2):
            if i + 1 < len(sys.argv):
                label = sys.argv[i]
                alt_rate = float(sys.argv[i+1])
                scenarios.append(project(base, alt_rate, years, label))

        result = {
            "initial_value": base,
            "years": years,
            "scenarios": scenarios,
            "comparison": {}
        }

        # Year-by-year comparison
        for y in range(years + 1):
            yr_data = {}
            for s in scenarios:
                yr_data[s["label"]] = s["projection"][y]["value"]
            result["comparison"][f"year_{y}"] = yr_data

        print(json.dumps(result, indent=2))
    else:
        # Example
        result = {
            "initial_value": 100000,
            "years": 5,
            "scenarios": [
                project(100000, 0.40, 5, "optimistic_40pct"),
                project(100000, 0.25, 5, "realistic_25pct"),
                project(100000, 0.10, 5, "conservative_10pct"),
            ]
        }
        print(json.dumps(result, indent=2))
