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


if __name__ == "__main__":
    unittest.main()
