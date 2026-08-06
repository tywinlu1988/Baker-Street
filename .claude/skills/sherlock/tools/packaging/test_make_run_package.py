#!/usr/bin/env python3
import json, unittest, tempfile
from pathlib import Path
import make_run_package as mrp


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class SourcesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.skill = Path(self.tmp.name) / "skill"
        self.skill.mkdir(parents=True)
        write(self.skill / "research-output-1.json", json.dumps([
            {"claim": "A股实行T+1", "source": "https://sse.com/rules", "confidence": 0.98},
            {"claim": "散户年均亏损", "source": "JFQA 2025", "confidence": 0.9, "type": "counter-evidence"},
        ]))
        write(self.skill / "research-output-2.json", json.dumps([
            {"claim": "佣金万2.5最低5元", "source": "computed", "confidence": 0.85},
        ]))

    def test_sources_merges_and_sorts(self):
        out = Path(self.tmp.name) / "sources.md"
        n = mrp.cmd_sources(self.skill, out)
        self.assertEqual(n, 3)
        text = out.read_text(encoding="utf-8")
        self.assertIn("A股实行T+1", text)
        self.assertIn("counter-evidence", text)
        # sorted by confidence desc: 0.98 first data row
        first_row = [l for l in text.splitlines() if l.startswith("| 1")][0]
        self.assertIn("A股实行T+1", first_row)

    def test_sources_tolerates_bad_file(self):
        write(self.skill / "research-output-3.json", "{not valid json")
        out = Path(self.tmp.name) / "sources.md"
        n = mrp.cmd_sources(self.skill, out)
        self.assertEqual(n, 3)  # bad file skipped

    def test_sources_empty_when_no_files(self):
        empty = Path(self.tmp.name) / "empty-skill"
        empty.mkdir()
        out = Path(self.tmp.name) / "sources.md"
        n = mrp.cmd_sources(empty, out)
        self.assertEqual(n, 0)
        self.assertIn("无研究产物", out.read_text(encoding="utf-8"))


class AssembleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.skill = Path(self.tmp.name) / "skill"
        self.skill.mkdir(parents=True)
        self.run = Path(self.tmp.name) / "sherlock-runs" / "20260806-120000"
        write(self.skill / "research-output-1.json", json.dumps([
            {"claim": "fact A", "source": "s1", "confidence": 0.9}]))
        write(self.skill / "quant-demands.json", json.dumps({"demands": []}))
        write(self.skill / "quant-analysis-package.json", json.dumps({
            "analyses": [{"requested_by": "holmes", "type": "mc",
                          "results": {}, "script": str(self.skill / "tools" / "analysis" / "mc_engine.py")}]}))
        write(self.skill / "tools" / "analysis" / "mc_engine.py", "# script")
        write(self.skill / "persona-output-holmes-draft.md", "draft")
        write(self.skill / "persona-output-holmes.md", "final")
        write(self.skill / "run-log.json", json.dumps({"agents": []}))

    def test_assemble_moves_and_cleans(self):
        r = mrp.cmd_assemble(self.skill, self.run)
        self.assertTrue((self.run / "fact-base.json").exists())
        self.assertTrue((self.run / "sources.md").exists())
        # provenance generated before research outputs were deleted
        self.assertIn("fact A", (self.run / "sources.md").read_text(encoding="utf-8"))
        self.assertTrue((self.run / "personas" / "persona-output-holmes-draft.md").exists())
        self.assertTrue((self.run / "personas" / "persona-output-holmes.md").exists())
        self.assertTrue((self.run / "quant-analysis-package.json").exists())
        self.assertTrue((self.run / "scripts" / "mc_engine.py").exists())
        # skill dir cleaned; raw research outputs moved (not deleted) into run dir
        self.assertFalse((self.skill / "research-output-1.json").exists())
        self.assertTrue((self.run / "research-output-1.json").exists())
        self.assertFalse((self.skill / "persona-output-holmes.md").exists())
        self.assertFalse((self.skill / "run-log.json").exists())
        # shared script NOT moved (copied only)
        self.assertTrue((self.skill / "tools" / "analysis" / "mc_engine.py").exists())

    def test_assemble_tolerates_missing(self):
        (self.skill / "quant-demands.json").unlink()
        (self.skill / "run-log.json").unlink()
        r = mrp.cmd_assemble(self.skill, self.run)
        self.assertIn("quant-demands.json", r["missing"])
        self.assertTrue((self.run / "fact-base.json").exists())


class FactbaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.skill = Path(self.tmp.name) / "skill"
        self.skill.mkdir(parents=True)
        write(self.skill / "research-output-1.json", json.dumps([
            {"claim": "low conf fact", "source": "s1", "confidence": 0.5},
            {"claim": "high conf fact", "source": "s2", "confidence": 0.95},
        ]))

    def test_factbase_assigns_sorted_ids(self):
        n = mrp.cmd_factbase(self.skill)
        self.assertEqual(n, 2)
        facts = json.loads((self.skill / "fact-base.json").read_text(encoding="utf-8"))
        self.assertEqual(facts[0]["id"], "F001")
        self.assertEqual(facts[0]["claim"], "high conf fact")  # sorted desc
        self.assertEqual(facts[1]["id"], "F002")
        # sources.md row 1 == F001
        text = (self.skill / "sources.md").read_text(encoding="utf-8")
        row1 = [l for l in text.splitlines() if l.startswith("| 1")][0]
        self.assertIn("F001", row1)
        self.assertIn("high conf fact", row1)

    def test_factbase_uses_merged_file(self):
        write(self.skill / "merged.json", json.dumps([
            {"claim": "deduped fact", "source": "s9", "confidence": 0.8}]))
        n = mrp.cmd_factbase(self.skill, merged_path=self.skill / "merged.json")
        self.assertEqual(n, 1)
        facts = json.loads((self.skill / "fact-base.json").read_text(encoding="utf-8"))
        self.assertEqual(facts[0]["claim"], "deduped fact")

    def test_factbase_coerces_nonnumeric_confidence(self):
        write(self.skill / "research-output-2.json", json.dumps([
            {"claim": "string conf", "source": "s3", "confidence": "high"},
            {"claim": "null conf", "source": "s4", "confidence": None},
        ]))
        n = mrp.cmd_factbase(self.skill)  # must not raise
        self.assertEqual(n, 4)

    def test_assemble_moves_factbase_and_sources(self):
        mrp.cmd_factbase(self.skill)
        write(self.skill / "run-log.json", json.dumps({"agents": []}))
        run = Path(self.tmp.name) / "run"
        r = mrp.cmd_assemble(self.skill, run)
        self.assertTrue((run / "fact-base.json").exists())
        self.assertTrue((run / "sources.md").exists())
        self.assertFalse((self.skill / "fact-base.json").exists())
        # raw research outputs preserved in run dir, not deleted
        self.assertTrue((run / "research-output-1.json").exists())
        self.assertFalse((self.skill / "research-output-1.json").exists())
        # sources.md carries F-ids
        self.assertIn("F001", (run / "sources.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
