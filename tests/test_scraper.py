import json, tempfile, unittest
from pathlib import Path
from headline_harvest.cli import export
from headline_harvest.parser import parse_headlines

class ScraperTests(unittest.TestCase):
    def setUp(self): self.html=(Path(__file__).parent/"fixture.html").read_text(encoding="utf-8")
    def test_parses_heading_links_and_joins_urls(self):
        items=parse_headlines(self.html,"https://example.com/start")
        self.assertEqual([item.title for item in items],["First headline","Second headline"])
        self.assertEqual(items[0].url,"https://example.com/news/one")
    def test_exports_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"items.json"; export(parse_headlines(self.html,"https://example.com"),path)
            self.assertEqual(len(json.loads(path.read_text(encoding="utf-8"))),2)
    def test_rejects_unknown_export_type(self):
        with self.assertRaisesRegex(ValueError,".json or .csv"): export([],Path("items.txt"))

if __name__=="__main__": unittest.main()

