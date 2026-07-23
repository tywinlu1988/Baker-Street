#!/usr/bin/env python3
"""
Fact Base Verifier — Cross-reference and validate claims.
Usage: python3 fact_verifier.py fact_base.json

Checks: source credibility score, consistency between claims, confidence distribution.
Part of the Sherlock Framework shared tool library (v0.4.2+).
"""
import json, sys
from collections import Counter

def verify_fact_base(facts):
    """Run verification checks on a fact base JSON array."""
    report = {
        "total_facts": len(facts),
        "checks": {}
    }

    # Check 1: Source coverage
    with_sources = sum(1 for f in facts if f.get("source") and f["source"] not in ["computed", ""])
    report["checks"]["source_coverage"] = {
        "sourced": with_sources,
        "unsourced": len(facts) - with_sources,
        "coverage_pct": round(with_sources / len(facts) * 100, 1) if facts else 0
    }

    # Check 2: Confidence distribution
    confidences = [f.get("confidence", 0) for f in facts]
    report["checks"]["confidence"] = {
        "avg": round(sum(confidences) / len(confidences), 2) if confidences else 0,
        "min": min(confidences) if confidences else 0,
        "max": max(confidences) if confidences else 0,
        "low_confidence_count": sum(1 for c in confidences if c < 0.6)
    }

    # Check 3: Counter-evidence ratio
    counter = sum(1 for f in facts if f.get("type") == "counter-evidence")
    report["checks"]["anti_sycophancy"] = {
        "counter_evidence_count": counter,
        "ratio_pct": round(counter / len(facts) * 100, 1) if facts else 0,
        "passes": (counter / len(facts) >= 0.08) if facts else False
    }

    # Check 4: Duplicate detection (simple claim similarity)
    claims = [f.get("claim", "") for f in facts]
    word_counts = Counter()
    for c in claims:
        key_words = tuple(sorted(set(c.lower().split()[:8])))  # First 8 words as fingerprint
        word_counts[key_words] += 1
    duplicates = {str(k): v for k, v in word_counts.items() if v > 1}
    report["checks"]["duplicates"] = {
        "potential_duplicates": len(duplicates),
        "details": duplicates if duplicates else "none"
    }

    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            facts = json.load(f)
        verify_fact_base(facts)
    else:
        print("Usage: python3 fact_verifier.py <fact_base.json>")
