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

    def test_expected_personas_wrong_shape_json_returns_empty(self):
        write(self.run / "run-log.json", json.dumps([1, 2, 3]))
        self.assertEqual(ph.expected_personas(self.run), [])

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


class PersonaCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name) / "run-1"
        self.run.mkdir(parents=True)
        self.skill = Path(self.tmp.name) / "skill"
        write(self.skill / "personas" / "holmes.md", FAKE_PERSONA_MD)

    def test_persona_sections_parsed_from_file(self):
        self.assertEqual(ph.persona_sections(self.skill, "holmes"),
                         ["Core Argument", "Key Observations", "Blind Spot Acknowledgment"])

    def test_output_with_all_sections_passes(self):
        write(self.run / "persona-output-holmes.md",
              "### Core Argument\nx\n### Key Observations\n- a\n### Blind Spot Acknowledgment\ny\n")
        r = ph.check_persona(self.run, self.skill, "holmes", [], False)
        self.assertTrue(r["exists"])
        self.assertEqual(r["sections_missing"], [])
        self.assertFalse(r["collapsed"])

    def test_missing_two_sections_is_collapse(self):
        write(self.run / "persona-output-holmes.md", "### Core Argument\nonly one section\n")
        r = ph.check_persona(self.run, self.skill, "holmes", [], False)
        self.assertTrue(r["collapsed"])
        self.assertEqual(len(r["sections_missing"]), 2)

    def test_intake_marker_is_collapse(self):
        write(self.run / "persona-output-holmes.md",
              "🔍 **Sherlock Analysis — Intake**\nProceed with this configuration?\n"
              "### Core Argument\nx\n### Key Observations\n- a\n### Blind Spot Acknowledgment\ny\n")
        r = ph.check_persona(self.run, self.skill, "holmes", [], False)
        self.assertTrue(r["collapsed"])

    def test_references_package_via_result_number(self):
        write(self.run / "persona-output-holmes.md",
              "### Core Argument\nthe p_loss of 0.32 shows\n### Key Observations\n- a\n### Blind Spot Acknowledgment\ny\n")
        r = ph.check_persona(self.run, self.skill, "holmes", ["0.32"], True)
        self.assertTrue(r["references_package"])

    def test_no_reference_detected(self):
        write(self.run / "persona-output-holmes.md",
              "### Core Argument\nno numbers here\n### Key Observations\n- a\n### Blind Spot Acknowledgment\ny\n")
        r = ph.check_persona(self.run, self.skill, "holmes", ["0.32"], True)
        self.assertFalse(r["references_package"])

    def test_package_reference_skipped_when_no_package(self):
        write(self.run / "persona-output-holmes.md",
              "### Core Argument\nx\n### Key Observations\n- a\n### Blind Spot Acknowledgment\ny\n")
        r = ph.check_persona(self.run, self.skill, "holmes", [], False)
        self.assertIsNone(r["references_package"])

    def test_package_numbers_extracted(self):
        write(self.run / "quant-analysis-package.json", json.dumps({"analyses": [
            {"requested_by": "holmes", "type": "trend", "parameters": {}, "results": {"slope": 1.5, "p_value": 0.042}},
        ]}))
        nums = ph.package_numbers(self.run)
        self.assertIn("1.5", nums)
        self.assertIn("0.042", nums)

    def test_demand_personas_wrong_shape_json_returns_empty(self):
        write(self.run / "quant-demands.json", json.dumps([1, 2, 3]))
        self.assertEqual(ph.demand_personas(self.run), [])


class SummarizeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for i, (fails, collapsed, passed) in enumerate([(1, 0, True), (1, 1, False)], start=1):
            run = self.root / f"run-{i}"
            run.mkdir(parents=True)
            agents = [{"name": f"a{j}", "role": "persona",
                       "outcome": "timeout" if j < fails else "success", "duration_s": 60}
                      for j in range(4)]
            write(run / "run-log.json", json.dumps({"agents": agents}))
            write(run / "harness-result.json", json.dumps({
                "pass": passed,
                "checks": {"personas": {"results": [
                    {"persona": "a0", "collapsed": bool(collapsed)}]}},
            }))

    def test_summarize_aggregates_rates(self):
        md = ph.summarize(self.root)
        self.assertIn("25.0% (2/8)", md)   # 2 failures / 8 agents
        self.assertIn("**Persona collapses:** 1", md)
        self.assertIn("**Harness pass rate:** 1/2", md)
        self.assertIn("| run-1 |", md)
        self.assertIn("| run-2 |", md)

    def test_summarize_wrong_shape_run_log_treated_as_zero_agents(self):
        run = self.root / "run-3"
        run.mkdir(parents=True)
        write(run / "run-log.json", json.dumps([1, 2, 3]))
        md = ph.summarize(self.root)
        self.assertIn("| run-3 | 0 | 0 | 0 | FAIL |", md)
        self.assertIn("25.0% (2/8)", md)


class PartialPackageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name) / "run-1"
        self.run.mkdir(parents=True)

    def test_partial_package_with_uncovered_passes(self):
        write(self.run / "quant-analysis-package.json", json.dumps({
            "analyses": [
                {"requested_by": "holmes", "type": "trend", "parameters": {}, "results": {"slope": 1.5}},
            ],
            "status": "partial",
            "missing_demands": [{"persona": "moriarty", "computation": "monte carlo", "reason": "quant agent timeout"}],
        }))
        r = ph.check_package(self.run, ["holmes", "moriarty"])
        self.assertTrue(r["pass"])
        self.assertTrue(r["partial"])
        self.assertEqual(r["status"], "partial")

    def test_complete_package_with_uncovered_still_fails(self):
        write(self.run / "quant-analysis-package.json", json.dumps({
            "analyses": [
                {"requested_by": "holmes", "type": "trend", "parameters": {}, "results": {"slope": 1.5}},
            ],
            "status": "complete",
        }))
        r = ph.check_package(self.run, ["holmes", "moriarty"])
        self.assertFalse(r["pass"])
        self.assertFalse(r["partial"])

    def test_package_without_status_defaults_to_complete(self):
        write(self.run / "quant-analysis-package.json", json.dumps({"analyses": [
            {"requested_by": "holmes", "type": "trend", "parameters": {}, "results": {"slope": 1.5}},
        ]}))
        r = ph.check_package(self.run, ["holmes"])
        self.assertTrue(r["pass"])
        self.assertEqual(r["status"], "complete")
        self.assertFalse(r["partial"])

    def test_summarize_counts_partial_packages(self):
        root = self.run.parent
        write(self.run / "run-log.json", json.dumps({"agents": [
            {"name": "a0", "role": "persona", "outcome": "success", "duration_s": 60}]}))
        write(self.run / "harness-result.json", json.dumps({
            "pass": True,
            "checks": {"package": {"partial": True}, "personas": {"results": []}}}))
        md = ph.summarize(root)
        self.assertIn("**Partial packages:** 1", md)

    def test_unknown_status_normalized_to_complete(self):
        write(self.run / "quant-analysis-package.json", json.dumps({
            "analyses": [{"requested_by": "holmes", "type": "trend", "parameters": {}, "results": {"slope": 1.5}}],
            "status": "weird",
        }))
        r = ph.check_package(self.run, ["holmes"])
        self.assertEqual(r["status"], "complete")
        self.assertTrue(r["pass"])

    def test_non_dict_package_fails_without_crash(self):
        write(self.run / "quant-analysis-package.json", json.dumps([1, 2, 3]))
        r = ph.check_package(self.run, ["holmes"])
        self.assertFalse(r["pass"])


class DraftsCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name) / "run-1"
        self.run.mkdir(parents=True)

    def test_missing_draft_reported(self):
        r = ph.check_drafts(self.run, ["holmes", "moriarty"])
        self.assertFalse(r["pass"])
        self.assertEqual(r["missing_drafts"], ["holmes", "moriarty"])

    def test_present_drafts_pass(self):
        write(self.run / "persona-output-holmes-draft.md", "### Core Argument\nx\n")
        write(self.run / "persona-output-moriarty-draft.md", "### Core Argument\ny\n")
        r = ph.check_drafts(self.run, ["holmes", "moriarty"])
        self.assertTrue(r["pass"])
        self.assertEqual(r["missing_drafts"], [])

    def test_empty_draft_is_missing(self):
        write(self.run / "persona-output-holmes-draft.md", "   \n")
        r = ph.check_drafts(self.run, ["holmes"])
        self.assertFalse(r["pass"])


class AnnotationsCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name) / "run-1"
        self.run.mkdir(parents=True)

    def test_counts_annotations(self):
        write(self.run / "persona-output-holmes.md",
              "### Core Argument\nx\n[DATA: CONFIRMED] — Q001 slope confirms\n"
              "[DATA: REVISED] — thought growth stalled, Q002 shows decline\n"
              "### Data Revision Summary\n2 confirmed 1 revised\n")
        r = ph.check_annotations(self.run, ["holmes"])
        self.assertTrue(r["pass"])
        self.assertEqual(r["counts"], {"confirmed": 1, "revised": 1, "unsupported": 0})

    def test_unannotated_persona_fails(self):
        write(self.run / "persona-output-holmes.md", "### Core Argument\nno annotations\n")
        r = ph.check_annotations(self.run, ["holmes"])
        self.assertFalse(r["pass"])
        self.assertEqual(r["unannotated"], ["holmes"])

    def test_missing_final_is_unannotated(self):
        r = ph.check_annotations(self.run, ["holmes"])
        self.assertFalse(r["pass"])
        self.assertEqual(r["unannotated"], ["holmes"])


class AnnotationExemptionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name) / "run-1"
        self.run.mkdir(parents=True)

    def make_log(self, agents):
        write(self.run / "run-log.json", json.dumps({"agents": agents}))

    def test_is_two_round_detects_revision_role(self):
        self.make_log([{"name": "2b-holmes", "role": "revision", "outcome": "success", "duration_s": 60}])
        self.assertTrue(ph.is_two_round(self.run))

    def test_single_round_detected(self):
        self.make_log([{"name": "holmes", "role": "persona", "outcome": "success", "duration_s": 60}])
        self.assertFalse(ph.is_two_round(self.run))

    def test_no_package_exempts_all(self):
        r = ph.check_annotations_exempt(self.run, ["holmes", "moriarty"], package_available=False)
        self.assertTrue(r["pass"])
        self.assertEqual(len(r["exempted"]), 2)
        self.assertEqual(r["exempted"][0]["reason"], "no package")

    def test_failed_2b_exempts_that_persona(self):
        self.make_log([
            {"name": "2b-holmes", "role": "revision", "outcome": "timeout", "duration_s": 360},
            {"name": "2b-moriarty", "role": "revision", "outcome": "success", "duration_s": 200},
        ])
        write(self.run / "persona-output-moriarty.md", "[DATA: CONFIRMED] — ok\n")
        r = ph.check_annotations_exempt(self.run, ["holmes", "moriarty"], package_available=True)
        self.assertTrue(r["pass"])
        self.assertEqual([e["persona"] for e in r["exempted"]], ["holmes"])

    def test_successful_2b_without_annotations_fails(self):
        self.make_log([{"name": "2b-holmes", "role": "revision", "outcome": "success", "duration_s": 200}])
        write(self.run / "persona-output-holmes.md", "### Core Argument\nnothing\n")
        r = ph.check_annotations_exempt(self.run, ["holmes"], package_available=True)
        self.assertFalse(r["pass"])
        self.assertEqual(r["unannotated"], ["holmes"])

    def test_summarize_annotations_aggregate(self):
        root = self.run.parent
        self.make_log([{"name": "a0", "role": "persona", "outcome": "success", "duration_s": 60}])
        write(self.run / "harness-result.json", json.dumps({
            "pass": True,
            "checks": {"package": {"partial": False},
                       "personas": {"results": []},
                       "annotations": {"counts": {"confirmed": 3, "revised": 1, "unsupported": 2}}}}))
        md = ph.summarize(root)
        self.assertIn("**Annotations (C/R/U):** 3/1/2", md)


class TwoRoundIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name) / "run-1"
        self.run.mkdir(parents=True)
        self.skill = Path(self.tmp.name) / "skill"
        write(self.skill / "personas" / "holmes.md", FAKE_PERSONA_MD)
        write(self.run / "run-log.json", json.dumps({"agents": [
            {"name": "holmes", "role": "persona", "outcome": "success", "duration_s": 60},
            {"name": "2b-holmes", "role": "revision", "outcome": "success", "duration_s": 90},
        ]}))
        write(self.run / "quant-demands.json", json.dumps({"demands": [
            {"persona": "holmes", "computation": "trend", "rationale": "sig", "raw": "QUANT_DEMAND: trend — sig"}]}))
        write(self.run / "quant-analysis-package.json", json.dumps({"analyses": [
            {"requested_by": "holmes", "type": "trend", "parameters": {}, "results": {"slope": 1.5}}],
            "status": "complete"}))
        write(self.run / "persona-output-holmes-draft.md",
              "### Core Argument\nx\n### Key Observations\n- a\n### Blind Spot Acknowledgment\ny\n")
        write(self.run / "persona-output-holmes.md",
              "### Core Argument\nx\n[DATA: CONFIRMED] — slope 1.5 confirms\n### Key Observations\n- a\n### Blind Spot Acknowledgment\ny\n### Data Revision Summary\n1 confirmed\n")

    def test_two_round_run_passes_with_drafts_and_annotations(self):
        r = ph.check_run(self.run, self.skill)
        self.assertTrue(r["pass"])
        self.assertIn("drafts", r["checks"])
        self.assertIn("annotations", r["checks"])

    def test_single_round_run_skips_two_round_checks(self):
        log = load = json.loads((self.run / "run-log.json").read_text(encoding="utf-8"))
        log["agents"] = [a for a in log["agents"] if a["role"] != "revision"]
        (self.run / "run-log.json").write_text(json.dumps(log), encoding="utf-8")
        (self.run / "persona-output-holmes-draft.md").unlink()
        r = ph.check_run(self.run, self.skill)
        self.assertNotIn("drafts", r["checks"])
        self.assertNotIn("annotations", r["checks"])


if __name__ == "__main__":
    unittest.main()


class TechDebtFixTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name) / "run-1"
        self.run.mkdir(parents=True)
        self.skill = Path(self.tmp.name) / "skill"
        write(self.skill / "personas" / "holmes.md", FAKE_PERSONA_MD)

    def test_prose_analyses_does_not_count_as_package_reference(self):
        write(self.run / "persona-output-holmes.md",
              "### Core Argument\nour analyses show concerns\n### Key Observations\n- a\n### Blind Spot Acknowledgment\ny\n")
        r = ph.check_persona(self.run, self.skill, "holmes", [], True)
        self.assertFalse(r["references_package"])

    def test_section_mentioned_in_prose_is_still_missing(self):
        write(self.run / "persona-output-holmes.md",
              "I will give my Core Argument now, plus Key Observations and a Blind Spot Acknowledgment.\n")
        r = ph.check_persona(self.run, self.skill, "holmes", [], False)
        self.assertEqual(len(r["sections_missing"]), 3)

    def test_single_digit_result_number_extracted(self):
        write(self.run / "quant-analysis-package.json", json.dumps({"analyses": [
            {"requested_by": "holmes", "type": "compare", "parameters": {}, "results": {"count": 5, "slope": 1.5}},
        ]}))
        nums = ph.package_numbers(self.run)
        self.assertIn("5", nums)
        self.assertIn("1.5", nums)

    def test_number_matches_only_as_token(self):
        write(self.run / "persona-output-holmes.md",
              "### Core Argument\nthe value 11.5 shows growth\n### Key Observations\n- a\n### Blind Spot Acknowledgment\ny\n")
        r = ph.check_persona(self.run, self.skill, "holmes", ["1.5"], True)
        self.assertFalse(r["references_package"])
        write(self.run / "persona-output-holmes.md",
              "### Core Argument\nthe value 1.5 shows growth\n### Key Observations\n- a\n### Blind Spot Acknowledgment\ny\n")
        r = ph.check_persona(self.run, self.skill, "holmes", ["1.5"], True)
        self.assertTrue(r["references_package"])
