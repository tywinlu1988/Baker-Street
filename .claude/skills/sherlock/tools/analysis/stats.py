#!/usr/bin/env python3
"""
Sherlock Quantitative Toolkit — Statistical analysis functions.
Usage: python3 stats.py <command> [args...]

Commands:
  describe <values...>              — mean, median, std, percentiles
  trend <y1> <y2> ...              — linear regression slope, R², significance
  compare <group1_v1,v2,...> <group2_v1,v2,...> — Welch t-test
  breakeven <fixed_cost> <unit_price> <unit_cost> — breakeven units
  sensitivity <base> <pct_changes...>  — sensitivity table
"""
import sys, json, math

def mean(vals):
    return sum(vals) / len(vals)

def median(vals):
    s = sorted(vals)
    n = len(s)
    if n % 2 == 0:
        return (s[n//2-1] + s[n//2]) / 2
    return s[n//2]

def stddev(vals):
    m = mean(vals)
    return math.sqrt(sum((x - m)**2 for x in vals) / (len(vals) - 1))

def percentile(vals, p):
    s = sorted(vals)
    k = (len(s) - 1) * p / 100
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s[int(k)]
    return s[int(f)] * (c - k) + s[int(c)] * (k - f)

def describe(vals):
    return {
        "count": len(vals),
        "mean": round(mean(vals), 2),
        "median": round(median(vals), 2),
        "std": round(stddev(vals), 2),
        "min": min(vals),
        "max": max(vals),
        "p25": round(percentile(vals, 25), 2),
        "p75": round(percentile(vals, 75), 2),
        "p95": round(percentile(vals, 95), 2),
    }

def trend(ys):
    """Simple linear regression: y = a + bx. Returns slope, intercept, R², p-value estimate."""
    n = len(ys)
    xs = list(range(n))
    xm, ym = mean(xs), mean(ys)
    num = sum((xs[i] - xm) * (ys[i] - ym) for i in range(n))
    den = sum((xs[i] - xm) ** 2 for i in range(n))
    b = num / den if den != 0 else 0
    a = ym - b * xm
    y_pred = [a + b * x for x in xs]
    ss_res = sum((ys[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((ys[i] - ym) ** 2 for i in range(n))
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    # rough t-stat for slope significance
    se_b = math.sqrt(ss_res / (n - 2) / den) if den != 0 and n > 2 else float('inf')
    t_stat = b / se_b if se_b != 0 else 0
    return {
        "slope": round(b, 4),
        "intercept": round(a, 2),
        "r_squared": round(r2, 4),
        "t_statistic": round(t_stat, 4),
        "direction": "increasing" if b > 0 else "decreasing" if b < 0 else "flat",
        "n": n,
    }

def compare(g1, g2):
    """Welch t-test for two independent samples."""
    m1, m2 = mean(g1), mean(g2)
    v1, v2 = stddev(g1)**2, stddev(g2)**2
    n1, n2 = len(g1), len(g2)
    se = math.sqrt(v1/n1 + v2/n2)
    t = (m1 - m2) / se if se != 0 else 0
    df_num = (v1/n1 + v2/n2) ** 2
    df_den = (v1/n1)**2/(n1-1) + (v2/n2)**2/(n2-1)
    df = df_num / df_den if df_den != 0 else 1
    return {
        "mean_1": round(m1, 2), "mean_2": round(m2, 2),
        "difference": round(m1 - m2, 2),
        "t_statistic": round(t, 4),
        "approx_df": round(df, 1),
        "significant_at_05": abs(t) > 1.96,  # crude approximation
    }

def breakeven(fixed_cost, unit_price, unit_cost):
    margin = unit_price - unit_cost
    if margin <= 0:
        return {"breakeven_units": float('inf'), "note": "Negative margin — never breaks even"}
    return {"breakeven_units": math.ceil(fixed_cost / margin), "margin_per_unit": margin}

def sensitivity(base, changes_pct):
    results = {}
    for pct in changes_pct:
        val = base * (1 + pct/100)
        results[f"{pct:+d}%"] = round(val, 2)
    return {"base": base, "scenarios": results}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command. Use: describe, trend, compare, breakeven, sensitivity"}))
        sys.exit(1)

    cmd = sys.argv[1]
    try:
        if cmd == "describe":
            vals = [float(x) for x in sys.argv[2:]]
            print(json.dumps(describe(vals), indent=2))
        elif cmd == "trend":
            vals = [float(x) for x in sys.argv[2:]]
            print(json.dumps(trend(vals), indent=2))
        elif cmd == "compare":
            args = sys.argv[2:]
            sep = args.index("--") if "--" in args else -1
            g1 = [float(x) for x in args[:sep]]
            g2 = [float(x) for x in args[sep+1:]] if sep >= 0 else []
            print(json.dumps(compare(g1, g2), indent=2))
        elif cmd == "breakeven":
            fc = float(sys.argv[2]); up = float(sys.argv[3]); uc = float(sys.argv[4])
            print(json.dumps(breakeven(fc, up, uc), indent=2))
        elif cmd == "sensitivity":
            base = float(sys.argv[2])
            changes = [float(x) for x in sys.argv[3:]]
            print(json.dumps(sensitivity(base, changes), indent=2))
        else:
            print(json.dumps({"error": f"Unknown command: {cmd}"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
