"""Meaningful rejection checks for research handoff boundaries (stdlib only)."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[5]
SKILL = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder", SKILL / "scripts/build_site.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
BASE = ROOT / "examples/deep-paper-reading"

class ContractChecks(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((BASE / "project.zh-CN.json").read_text())

    def reject(self, mutate):
        mutate(self.data)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            builder.validate(self.data, BASE)

    def test_valid_fixture(self):
        self.assertEqual(len(builder.validate(self.data, BASE)), 2)

    def test_required_numeric_score(self):
        self.reject(lambda d: d["papers"][0].pop("score"))

    def test_deferred_score_rejected(self):
        self.reject(lambda d: d["papers"][0]["score"].update(value="deferred"))

    def test_score_range(self):
        self.reject(lambda d: d["papers"][0]["score"].update(value=5))

    def test_score_requires_evidence(self):
        self.reject(lambda d: d["papers"][0]["score"].update(claim_ids=[]))

    def test_collection_score_and_semantic_code(self):
        rendered = builder.render_index(self.data)
        self.assertEqual(rendered.count('class="paper-score"'), 2)
        self.assertIn('language-json', rendered)
        self.assertIn('class="copy-code"', rendered)
        self.assertIn('Prism.tokenize', rendered)
        self.assertIn('code.dataset.highlighter', rendered)

    def test_english_bundle(self):
        import re
        data = json.loads((BASE / "project.en-US.json").read_text())
        builder.validate(data, BASE)
        self.assertIsNone(re.search(r"[\u4e00-\u9fff]", json.dumps(data, ensure_ascii=False)))

    def test_locale_directory_layout(self):
        english = json.loads((BASE / "project.en-US.json").read_text())
        output = builder.render_site([(self.data, BASE), (english, BASE)])
        self.assertEqual(set(output), {"index.html", "zh-CN/index.html", "zh-CN/react.html", "zh-CN/reflexion.html", "en-US/index.html", "en-US/react.html", "en-US/reflexion.html"})
        self.assertIn('href="zh-CN/index.html"', output["index.html"])
        self.assertIn('href="en-US/index.html"', output["index.html"])
        self.assertIn('href="../en-US/react.html" hreflang="en-US"', output["zh-CN/react.html"])
        self.assertIn('href="../zh-CN/react.html" hreflang="zh-CN"', output["en-US/react.html"])

    def test_unsupported_language_rejected(self):
        self.reject(lambda d: d.update(language="fr-FR"))

    def test_duplicate_locale_rejected(self):
        with self.assertRaises(ValueError):
            builder.render_site([(self.data, BASE), (self.data, BASE)])

    def test_translated_anchors_must_match(self):
        english = json.loads((BASE / "project.en-US.json").read_text())
        english["papers"][0]["slides"][0]["id"] = "different-cover"
        with self.assertRaises(ValueError):
            builder.render_site([(self.data, BASE), (english, BASE)])

    def test_unapproved_fulltext(self):
        self.reject(lambda d: d["scope"]["approved_full_text"].clear())

    def test_unread_cannot_be_fulltext(self):
        self.reject(lambda d: d["papers"][0]["read_coverage"].update(status="full-text"))

    def test_budget_not_expanded(self):
        self.reject(lambda d: d["scope"].update(max_full_text=1))

    def test_version_not_pinned(self):
        self.reject(lambda d: d["papers"][0].update(source_url="https://arxiv.org/abs/2210.03629"))

    def test_dangling_claim(self):
        self.reject(lambda d: d["papers"][0]["slides"][0]["claim_ids"].append("nonexistent"))

    def test_dangling_slide(self):
        self.reject(lambda d: d["relations"][0]["navigation"].update(to_slide="nonexistent"))

    def test_claim_ids_scoped_to_paper(self):
        self.reject(lambda d: d["relations"][0]["evidence"][0].update(claim_id="nonexistent"))

    def test_verified_needs_both_endpoints(self):
        self.reject(lambda d: d["relations"][0].update(evidence=[]))

    def test_line_range(self):
        self.reject(lambda d: d["papers"][0]["examples"][0]["steps"][0].update(lines=[999]))

    def test_passed_needs_actual_output(self):
        self.reject(lambda d: d["papers"][0]["examples"][0].update(actual_output=""))

    def test_reserved_index(self):
        self.reject(lambda d: d["papers"][0].update(id="index"))

    def test_report_traversal(self):
        self.reject(lambda d: d["papers"][0].update(report_path="../../README.md"))

    def test_remote_figure_rejected(self):
        def change(d):
            d["papers"][0]["slides"][0]["figure"] = dict(src="https://example.com/image.png", alt="x", caption="x", source_url="https://example.com", locator="Fig.1")
        self.reject(change)

    def test_text_escaping_no_template_replacement(self):
        paper = self.data["papers"][0]
        paper["slides"][0]["title"] = "<script>alert(1)</script>@@JS@@"
        rendered = builder.render_paper(paper, self.data, BASE)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;@@JS@@", rendered)
        self.assertNotIn("<script>alert(1)</script>", rendered)

    def test_unsafe_evidence_url(self):
        self.reject(lambda d: d["papers"][0]["claims"][0].update(url="javascript:alert(1)"))

class RenderingDependencyChecks(unittest.TestCase):
    def test_pinned_vendor_integrity(self):
        import hashlib
        vendor = SKILL / "assets/vendor"
        manifest = json.loads((vendor / "manifest.json").read_text())
        self.assertEqual(manifest["katex"]["version"], "0.16.22")
        self.assertEqual(manifest["prismjs"]["version"], "1.30.0")
        for package, record in manifest.items():
            self.assertEqual(record["license"], "MIT")
            for name, digest in record["files"].items():
                self.assertEqual(hashlib.sha256((vendor / package / name).read_bytes()).hexdigest(), digest)

    def test_embedded_math_fonts_and_font_stacks(self):
        import re
        css = builder.presentation_css()
        urls = re.findall(r"url\(([^)]+)\)", css)
        self.assertTrue(urls)
        self.assertTrue(all(u.startswith("data:font/woff2;base64,") for u in urls))
        self.assertIn('"Iosevka Aile","Noto Sans CJK SC",sans-serif', css)
        self.assertIn('"Iosevka Etoile","Noto Serif CJK SC",serif', css)
        self.assertIn('"IosevkaAlexJiang","Noto Sans Mono CJK SC",monospace', css)

    def test_escaped_source_before_prism(self):
        from html.parser import HTMLParser
        class Collector(HTMLParser):
            def __init__(self):
                super().__init__(); self.parts = []
            def handle_data(self, value):
                self.parts.append(value)
        source = '<script>alert("x")</script>'
        parser = Collector(); parser.feed(builder.highlighted_lines(source, "python"))
        self.assertEqual("".join(parser.parts), source)
        self.assertNotIn("<script>", builder.highlighted_lines(source, "python"))
        self.assertIn("Prism.tokenize", builder.presentation_js())


class AttributionChecks(unittest.TestCase):
    """Independent of the optional external paper example bundle."""

    def test_english_only_entry(self):
        import re
        page = builder.render_entry(["en-US"])
        self.assertIn('Generated with', page)
        self.assertIn(builder.SKILL_URL, page)
        self.assertIsNone(re.search(r'[\u4e00-\u9fff]', page))
        self.assertIn('href="en-US/index.html"', page)
        self.assertNotIn('href="zh-CN/index.html"', page)

    def test_single_locale_redirect_has_fallback(self):
        page = builder.render_entry(["zh-CN"])
        self.assertIn('new URL("zh-CN/index.html",location.href)', page)
        self.assertIn('location.replace(target.href)', page)
        self.assertIn('href="zh-CN/index.html"', page)
        self.assertIn('READ, THINK, PRESENTATION', page)
        self.assertNotIn('location.replace', builder.render_entry(["zh-CN", "en-US"]))

    def test_chinese_only_entry(self):
        page = builder.render_entry(["zh-CN"])
        self.assertIn('由 ', page)
        self.assertIn('crispe-deep-paper-reading</a> 生成', page)
        self.assertEqual(page.count('href="' + builder.SKILL_URL + '"'), 1)
        self.assertNotIn('Generated with', page)
        self.assertIn(builder.SKILL_URL, page)

    def test_bilingual_entry(self):
        page = builder.render_entry(["zh-CN", "en-US"])
        self.assertIn('Generated with', page)
        self.assertIn('由 ', page)
        self.assertEqual(page.count('class="generator-credit"'), 1)

    def test_locale_collection_credits(self):
        for locale in ["zh-CN", "en-US"]:
            data = {"language": locale, "title": "Test", "scope": {"question": "Test"}, "papers": [], "relations": []}
            page = builder.render_index(data)
            credit = page.split('<footer class="generator-credit">', 1)[1].split('</footer>', 1)[0]
            self.assertIn(builder.SKILL_URL, credit)
            self.assertIn('Generated with' if locale == 'en-US' else '由 ', credit)
            self.assertNotIn('由 ' if locale == 'en-US' else 'Generated with', credit)


if __name__ == "__main__":
    unittest.main()
