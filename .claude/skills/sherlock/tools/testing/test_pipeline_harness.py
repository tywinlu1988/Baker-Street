#!/usr/bin/env python3
import json, unittest, tempfile
from pathlib import Path
import pipeline_harness as ph

FAKE_PERSONA_MD = """---
name: holmes
---
You are Sherlock Holmes.

## Output Format

### Core Argument
### Key Observations
### Blind Spot Acknowledgment
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class DemandsCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name) / "run-1"
        self.run.mkdir(parents=True)
        write(self.run / "run-log.json", json.dumps({"agents": [
            {"name": "holmes", "role": "persona", "outcome": "success", "duration_s": 60},
            {"name": "moriarty", "role": "persona", "outcome": "success", "duration_s": 70},
            {"name": "baseline", "role": "baseline", "outcome": "success", "duration_s": 50},
        ]}))

    def test_expected_personas_excludes_baseline(self):
        self.assertEqual(ph.expected_personas(self.run), ["holmes", "moriarty"])

    def test_missing_demands_file_fails(self):
        r = ph.check_demands(self.run, ["holmes", "moriarty"])
        self.assertFalse(r["pass"])
        self.assertEqual(r["missing"], ["holmes", "moriarty"])

    def test_valid_demands_pass(self):
        write(self.run / "quant-demands.json", json.dumps({"demands": [
            {"persona": "holmes", "computation": "trend analysis on growth", "rationale": "test significance", "raw": "QUANT_DEMAND: trend analysis on growth — test significance"},
            {"persona": "moriarty", "computation": "monte carlo on churn", "rationale": "worst case", "raw": "QUANT_DEMAND: monte carlo on churn — worst case"},
        ]}))
        r = ph.check_demands(self.run, ["holmes", "moriarty"])
        self.assertTrue(r["pass"])
        self.assertEqual(r["missing"], [])
        self.assertEqual(r["malformed"], [])

    def test_persona_without_demand_is_missing(self):
        write(self.run / "quant-demands.json", json.dumps({"demands": [
            {"persona": "holmes", "computation": "trend", "rationale": "sig", "raw": "QUANT_DEMAND: trend — sig"},
        ]}))
        r = ph.check_demands(self.run, ["holmes", "moriarty"])
        self.assertFalse(r["pass"])
        self.assertEqual(r["missing"], ["moriarty"])

    def test_empty_computation_is_malformed(self):
        write(self.run / "quant-demands.json", json.dumps({"demands": [
            {"persona": "holmes", "computation": "", "rationale": "sig", "raw": "QUANT_DEMAND: — sig"},
            {"persona": "moriarty", "computation": "mc", "rationale": "wc", "raw": "QUANT_DEMAND: mc — wc"},
        ]}))
        r = ph.check_demands(self.run, ["holmes", "moriarty"])
        self.assertFalse(r["pass"])
        self.assertEqual(r["malformed"], ["holmes"])


class PackageCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name) / "run-1"
        self.run.mkdir(parents=True)

    def test_missing_package_fails(self):
        r = ph.check_package(self.run, ["holmes"])
        self.assertFalse(r["pass"])
        self.assertFalse(r["exists"])

    def test_analysis_missing_results_is_schema_error(self):
        write(self.run / "quant-analysis-package.json", json.dumps({"analyses": [
            {"requested_by": "holmes", "type": "trend"},
        ]}))
        r = ph.check_package(self.run, ["holmes"])
        self.assertFalse(r["pass"])
        self.assertTrue(any("results" in e for e in r["schema_errors"]))

    def test_uncovered_persona_fails(self):
        write(self.run / "quant-analysis-package.json", json.dumps({"analyses": [
            {"requested_by": "holmes", "type": "trend", "parameters": {}, "results": {"slope": 1.5}},
        ]}))
        r = ph.check_package(self.run, ["holmes", "moriarty"])
        self.assertFalse(r["pass"])
        self.assertEqual(r["uncovered_personas"], ["moriarty"])

    def test_full_coverage_passes(self):
        write(self.run / "quant-analysis-package.json", json.dumps({"analyses": [
            {"requested_by": "holmes", "type": "trend", "parameters": {}, "results": {"slope": 1.5}},
            {"requested_by": "moriarty", "type": "monte_carlo_simulation", "parameters": {}, "results": {"p_loss": 0.32}},
        ]}))
        r = ph.check_package(self.run, ["holmes", "moriarty"])
        self.assertTrue(r["pass"])
        self.assertEqual(r["analyses_count"], 2)


if __name__ == "__main__":
    unittest.main()
