#!/usr/bin/env python3
"""Validate research handoffs and render offline paper-reading sites. Stdlib only."""
import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path
import re
from urllib.parse import urlparse

SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
ROOT = Path(__file__).resolve().parents[1]
LOCALES = {"zh-CN": "中文", "en-US": "English"}
SKILL_URL = "https://github.com/alexxyjiang/custom-agent-skills/tree/master/plugins/crispe-deep-paper-reading-plugin"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def text(value):
    return html.escape(str(value), quote=True)

def url(value):
    parsed = urlparse(value)
    require(parsed.scheme in {"http", "https"} and bool(parsed.netloc), f"Expected HTTP(S) URL: {value}")
    return text(value)

def keyed(items, label):
    require(isinstance(items, list), f"{label} must be a list")
    result = {}
    for item in items:
        key = item.get("id", "")
        require(isinstance(key, str) and SLUG.fullmatch(key), f"Invalid {label} id: {key}")
        require(key not in result, f"Duplicate {label} id: {key}")
        result[key] = item
    return result

def validate(data, base):
    require(data.get("schema_version") == 1, "schema_version must equal 1")
    require(data.get("language") in LOCALES, "language must be zh-CN or en-US")
    require(bool(data.get("title")), "Missing collection title")
    scope = data.get("scope", {})
    for field in ["question", "approved_full_text", "max_metadata_records", "max_full_text", "stop_conditions", "search_log", "exclusions"]:
        require(field in scope, f"Missing scope.{field}")
    require(isinstance(scope["approved_full_text"], list), "approved_full_text must be a list")
    for budget in ["max_metadata_records", "max_full_text"]:
        require(type(scope[budget]) is int and scope[budget] >= 0, f"Invalid scope.{budget}")
    require(len(scope["approved_full_text"]) <= scope["max_full_text"], "Approved full-text set exceeds budget")
    papers = keyed(data.get("papers", []), "paper")
    require(bool(papers), "At least one paper is required")
    require(set(scope["approved_full_text"]) <= set(papers), "Unknown approved paper id")
    require("index" not in papers, "Paper id index conflicts with collection index.html")
    for pid, paper in papers.items():
        for field in ["title", "source_url", "version", "topic", "summary", "score", "read_coverage", "claims", "examples", "slides"]:
            require(field in paper, f"{pid}: missing {field}")
        url(paper["source_url"])
        if "arxiv.org/" in paper["source_url"]:
            require(re.search(r"v[1-9][0-9]*(?:$|[?#])", paper["source_url"]) is not None, f"{pid}: pin arXiv version")
        if "report_path" in paper:
            report = (base / paper["report_path"]).resolve()
            require(not Path(paper["report_path"]).is_absolute() and report.is_relative_to(base.resolve()) and report.is_file(), f"{pid}: report path missing or outside bundle")
        cov = paper["read_coverage"]
        require(cov.get("status") in {"full-text", "partial", "metadata-only"}, f"{pid}: invalid read coverage")
        require(isinstance(cov.get("read"), list) and isinstance(cov.get("unread"), list), f"{pid}: read/unread lists required")
        require(not (cov["status"] == "full-text" and cov["unread"]), f"{pid}: unread material cannot be full-text")
        require(cov["status"] == "metadata-only" or pid in scope["approved_full_text"], f"{pid}: full-text reading not approved")
        claims = keyed(paper["claims"], f"{pid} claim")
        score = paper["score"]
        require(isinstance(score, dict) and type(score.get("value")) is int and 1 <= score["value"] <= 4, f"{pid}: score.value must be an integer from 1 to 4; no deferred scores")
        require(isinstance(score.get("rationale"), str) and bool(score["rationale"].strip()), f"{pid}: score requires a rationale")
        require(isinstance(score.get("claim_ids"), list) and bool(score["claim_ids"]) and all(c in claims for c in score["claim_ids"]), f"{pid}: score requires existing evidence claim_ids")
        require(cov["status"] != "metadata-only", f"{pid}: analyze the paper before assigning a collection score")
        examples = keyed(paper["examples"], f"{pid} example")
        slides = keyed(paper["slides"], f"{pid} slide")
        require(bool(slides), f"{pid}: no slides")
        for claim in claims.values():
            require(claim.get("kind") in {"paper-claim", "external-evidence", "analyst-inference"}, "Invalid claim kind")
            require(bool(claim.get("text")) and bool(claim.get("locator")) and "limits" in claim, "Claim needs text, locator and limits")
            url(claim.get("url", ""))
        for example in examples.values():
            require(example.get("kind") in {"teaching", "original", "reproduction"}, "Invalid example kind")
            require(example.get("execution") in {"passed", "not-run", "failed"}, "Invalid execution status")
            for field in ["code", "source_locator", "language", "run_command", "expected_output", "actual_output", "limitations", "steps"]:
                require(field in example, f"Missing example.{field}")
            require(bool(example["code"]), "Empty example code")
            require(example["execution"] != "passed" or bool(example["actual_output"]), "Passed example requires actual output")
            for step in example["steps"]:
                require(bool(step.get("explanation")) and "state" in step and bool(step.get("lines")), "Step needs lines, explanation and state")
                require(all(type(n) is int and 1 <= n <= len(example["code"].splitlines()) for n in step["lines"]), "Code line mapping out of range")
        for slide in slides.values():
            require(bool(slide.get("title")), "Missing slide title")
            for field in ["chapter", "lead", "cards", "claim_ids", "links"]:
                require(field in slide, f"Missing slide.{field}")
            require(isinstance(slide.get("appendix"), bool), "Slide requires appendix boolean")
            for cid in slide.get("claim_ids", []):
                require(cid in claims, f"Unknown claim: {pid}/{cid}")
            if "example_id" in slide:
                require(slide["example_id"] in examples, f"Unknown example: {pid}/{slide['example_id']}")
            for card in slide.get("cards", []):
                require(card.get("tone", "indigo") in {"indigo", "emerald", "amber", "rose"}, "Invalid card tone")
            if "figure" in slide:
                fig = slide["figure"]
                require(all(fig.get(k) for k in ["src", "alt", "caption", "source_url", "locator"]), "Incomplete figure provenance")
                asset = (base / fig["src"]).resolve()
                require(not Path(fig["src"]).is_absolute() and asset.is_relative_to(base.resolve()), "Figure must be a relative asset inside bundle")
                require(asset.is_file() and asset.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}, "Figure asset missing or unsupported (use raster)")
                url(fig["source_url"])
    for pid, paper in papers.items():
        for slide in paper["slides"]:
            for link in slide.get("links", []):
                target = papers.get(link.get("paper_id"))
                require(target is not None, "Unknown linked paper")
                require(link.get("slide_id") in keyed(target["slides"], "slide"), "Unknown linked slide")
    for relation in keyed(data.get("relations", []), "relation").values():
        require(relation.get("from") in papers and relation.get("to") in papers, "Relation endpoint missing")
        require(relation.get("type") in {"cites", "extends", "supports", "contradicts", "similar", "replicates"}, "Invalid relation type")
        require(relation.get("status") in {"verified", "provisional", "unresolved"}, "Invalid relation status")
        require(bool(relation.get("statement")), "Missing relation statement")
        evidence = relation.get("evidence", [])
        if relation["status"] == "verified":
            require(bool(evidence), "Verified relation requires evidence")
            if relation["type"] in {"cites", "extends", "supports", "contradicts", "similar", "replicates"}:
                require({e.get("paper_id") for e in evidence} >= {relation["from"], relation["to"]}, "Evidence relation needs both papers")
        for entry in evidence:
            require(entry.get("paper_id") in papers, "Unknown evidence paper")
            require(entry.get("claim_id") in keyed(papers[entry["paper_id"]]["claims"], "claim"), "Unknown evidence claim")
        comparison = relation.get("comparability", {})
        require(comparison.get("status") in {"comparable", "not-comparable", "not-assessed"} and bool(comparison.get("reason")), "Missing comparability judgment")
        nav = relation.get("navigation", {})
        for end, field in [("from", "from_slide"), ("to", "to_slide")]:
            require(nav.get(field) in keyed(papers[relation[end]]["slides"], "slide"), "Invalid relation navigation")
    return papers

def highlighted_lines(source, language):
    """Escaped source scaffold; PrismJS tokenizes the full block in the browser."""
    return "".join(f'<span class="code-line" data-line="{i}">{text(line)}</span>' for i, line in enumerate(source.splitlines() or [""], 1))

def presentation_css():
    vendor = ROOT / "assets/vendor"
    css_path = vendor / "katex/dist/katex.min.css"
    css = css_path.read_text()
    def embed_font(match):
        relative = match[1].strip('\'"')
        if relative.endswith(".woff2"):
            encoded = base64.b64encode((css_path.parent / relative).read_bytes()).decode()
            return f"url(data:font/woff2;base64,{encoded}) format('woff2')"
        return ""
    # Keep only modern WOFF2 sources; no relative font request survives embedding.
    css = re.sub(r"url\(([^)]+)\)\s*format\([^)]+\),?", embed_font, css)
    prism = (vendor / "prismjs/themes/prism-tomorrow.min.css").read_text()
    return css + "\n" + prism + "\n" + (ROOT / "assets/style.css").read_text()

def presentation_js():
    vendor = ROOT / "assets/vendor"
    paths = ["prismjs/components/prism-core.min.js", "prismjs/components/prism-clike.min.js", "prismjs/components/prism-javascript.min.js", "prismjs/components/prism-python.min.js", "prismjs/components/prism-json.min.js", "prismjs/components/prism-bash.min.js", "prismjs/components/prism-sql.min.js", "katex/dist/katex.min.js", "katex/dist/contrib/auto-render.min.js"]
    licenses = "\n".join("/* " + (vendor / package / "LICENSE").read_text().replace("*/", "* /") + " */" for package in ["katex", "prismjs"])
    runtime = licenses + "\nwindow.Prism={manual:true};\n" + "\n;\n".join((vendor / path).read_text() for path in paths)
    runtime += "\n;\n" + (ROOT / "assets/code.js").read_text()
    # Inline scripts must never be terminated by library source text.
    return re.sub(r"</script", r"<\/script", runtime, flags=re.I)

def code_block(source, language, title, zh):
    language = language if re.fullmatch(r"[a-z0-9-]+", language) else "text"
    return (f'<div class="code-panel"><div class="code-toolbar"><span class="code-label">{text(title)}</span>'
            f'<span class="code-language">{text(language.upper())}</span><button class="copy-code" type="button">{"复制" if zh else "Copy"}</button>'
            f'<span class="copy-status" role="status"></span></div><pre tabindex="0" aria-label="{text(title)}"><code class="language-{language}">{highlighted_lines(source, language)}</code></pre></div>')

def render_example(ex, zh):
    steps = "".join(f'<button class="step" type="button" data-lines="{text(json.dumps(s["lines"]))}" aria-pressed="false"><strong>{i}. {text(s["explanation"])}</strong><span>{text(s["state"])}</span></button>' for i, s in enumerate(ex["steps"], 1))
    labels = {"teaching": "教学", "original": "原始", "reproduction": "复现", "passed": "已通过", "not-run": "未运行", "failed": "失败"} if zh else {}
    def parsed(value):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return value
    record = json.dumps({"command": ex["run_command"], "expected": parsed(ex["expected_output"]), "actual": parsed(ex["actual_output"]), "execution": ex["execution"]}, ensure_ascii=False, indent=2)
    code = code_block(ex["code"], ex["language"], "教学函数" if zh else "Teaching function", zh)
    execution = code_block(record, "json", "运行记录" if zh else "Execution record", zh)
    return f'<div class="example">{code}<div class="steps"><p class="badge">{text(labels.get(ex["kind"], ex["kind"]))} · {text(labels.get(ex["execution"], ex["execution"]))}</p>{steps}<p>{text(ex["limitations"])}</p><small>{text(ex["source_locator"])}</small><details><summary>{"运行记录" if zh else "Execution record"}</summary>{execution}</details></div></div>'

def language_link(alternate, paper_id=None):
    if not alternate:
        return ""
    target = str(Path(alternate).parent / f"{paper_id}.html") if paper_id else alternate
    locale = Path(alternate).parent.name
    require(locale in LOCALES, "Unknown alternate locale")
    return f'<a class="language-switch" href="{text(target)}" hreflang="{locale}">{LOCALES[locale]}</a>'

def render_paper(paper, data, base, alternate=None):
    zh = data["language"] == "zh-CN"
    claims = keyed(paper["claims"], "claim")
    examples = keyed(paper["examples"], "example")
    sections, toc = [], []
    for number, slide in enumerate(paper["slides"], 1):
        sid = slide["id"]
        toc.append(f'<a href="#slide-{sid}">{number:02} · {text(slide["title"])}</a>')
        cards = "".join(f'<article class="card {text(c.get("tone", "indigo"))}"><h3>{text(c["title"])}</h3><p>{text(c["text"])}</p></article>' for c in slide.get("cards", []))
        body = f'<div class="cards">{cards}</div>' if cards else ""
        if "example_id" in slide:
            body += render_example(examples[slide["example_id"]], zh)
        if "figure" in slide:
            fig = slide["figure"]
            asset = base / fig["src"]
            mime = mimetypes.guess_type(asset.name)[0]
            encoded = base64.b64encode(asset.read_bytes()).decode()
            body += f'<figure><button class="zoom" type="button" aria-label="{text(fig["alt"])}"><img src="data:{mime};base64,{encoded}" alt="{text(fig["alt"])}"></button><figcaption>{text(fig["caption"])} · <a href="{url(fig["source_url"])}">{text(fig["locator"])}</a></figcaption></figure>'
        refs = "".join(f'<a href="{url(claims[c]["url"])}" title="{text(claims[c]["limits"])}">{text(claims[c]["locator"])} [{text(claims[c]["kind"])}]</a>' for c in slide.get("claim_ids", []))
        links = list(slide.get("links", []))
        for rel in data.get("relations", []):
            if rel["from"] == paper["id"] and rel["navigation"]["from_slide"] == sid:
                links.append({"paper_id": rel["to"], "slide_id": rel["navigation"]["to_slide"], "label": f'{rel["type"]} · {rel["status"]}: {rel["statement"]}'})
        nav = "".join(f'<a class="cross-link" href="{text(l["paper_id"])}.html#slide-{text(l["slide_id"])}">{text(l["label"])}</a>' for l in links)
        tag = ("附录 · " if zh else "Appendix · ") if slide["appendix"] else ""
        sections.append(f'<section class="slide" id="slide-{sid}" aria-label="{text(slide["title"])}"><header><span class="badge">{tag}{text(slide.get("chapter", ""))}</span><span>{number:02} / {len(paper["slides"])}</span></header><h1>{text(slide["title"])}</h1><p class="lead">{text(slide.get("lead", ""))}</p><div class="slide-body">{body}{nav}</div><p class="takeaway">{text(slide.get("takeaway", ""))}</p><footer>{refs}</footer></section>')
    cov = paper["read_coverage"]
    coverage = f'{cov["status"]} · ' + ("未覆盖：" if zh else "Unread: ") + "; ".join(cov["unread"])
    template = (ROOT / "assets/deck.html").read_text()
    replacements = {"LANG": data["language"], "TITLE": text(paper["title"]), "SLIDES": "".join(sections), "TOC": "".join(toc), "CSS": presentation_css(), "JS": (ROOT / "assets/deck.js").read_text(), "COVERAGE": text(coverage), "HOME": "论文集合" if zh else "Collection", "CONTENTS": "目录" if zh else "Contents", "CLOSE": "关闭" if zh else "Close", "PREV": "上一页" if zh else "Previous", "NEXT": "下一页" if zh else "Next", "PLAY": "自动播放" if zh else "Autoplay", "SPEED": "每页时长" if zh else "Time per slide", "LANGUAGE": language_link(alternate, paper["id"])}
    replacements["JS"] = presentation_js() + "\n" + replacements["JS"]
    # Single pass: inserted research text cannot turn into template directives.
    return re.sub(r"@@([A-Z]+)@@", lambda m: replacements[m[1]], template)

def render_attribution(locales):
    messages = []
    for locale in LOCALES:
        if locale not in locales:
            continue
        link = f'<a href="{SKILL_URL}" target="_blank" rel="noopener noreferrer">crispe-deep-paper-reading</a>'
        message = f'由 {link} 生成' if locale == "zh-CN" else f'Generated with {link}'
        messages.append(f'<p lang="{locale}">{message}</p>')
    return '<footer class="generator-credit">' + "".join(messages) + '</footer>'

def render_index(data, alternate=None):
    zh = data["language"] == "zh-CN"
    groups = {}
    for p in data["papers"]:
        groups.setdefault(p["topic"], []).append(p)
    sections = []
    for i, (topic, papers) in enumerate(groups.items(), 1):
        cards = "".join(f'<a class="paper-card" href="{text(p["id"])}.html"><span>{text(p["version"])}</span><h3>{text(p["title"])}</h3><strong class="paper-score" title="{text(p["score"]["rationale"])}">{"深读评分" if zh else "Reading score"} {p["score"]["value"]}/4</strong><p>{text(p["summary"])}</p><small>{text(p["read_coverage"]["status"])}</small></a>' for p in papers)
        sections.append(f'<section id="topic-{i}"><h2>{i:02} · {text(topic)}</h2><div class="paper-grid">{cards}</div></section>')
    relations = []
    for rel in data.get("relations", []):
        refs = []
        for evidence in rel["evidence"]:
            paper = next(p for p in data["papers"] if p["id"] == evidence["paper_id"])
            claim = next(c for c in paper["claims"] if c["id"] == evidence["claim_id"])
            refs.append(f'<a href="{url(claim["url"])}">{text(evidence["paper_id"])}: {text(claim["locator"])}</a>')
        relations.append(f'<article class="relation"><strong>{text(rel["from"])} → {text(rel["to"])} · {text(rel["type"])} · {text(rel["status"])}</strong><p>{text(rel["statement"])}</p><p>{text(rel["comparability"]["status"])}: {text(rel["comparability"]["reason"])}</p>{" · ".join(refs)}</article>')
    css = presentation_css()
    scope = code_block(json.dumps(data["scope"], ensure_ascii=False, indent=2), "json", "阅读范围 · JSON" if zh else "Reading scope · JSON", zh)
    script = presentation_js()
    return f'<!doctype html><html lang="{data["language"]}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{text(data["title"])}</title><style>{css}</style><body class="collection"><main>{language_link(alternate)}<p class="eyebrow">READ · THINK · BUILD</p><h1>{text(data["title"])}</h1><p class="intro">{text(data["scope"]["question"])}</p><p>{len(data["papers"])} {"篇论文" if zh else "papers"} · {len(groups)} {"条阅读路线" if zh else "reading routes"}</p>{"".join(sections)}<section><h2>{"论文关系与证据" if zh else "Connections and evidence"}</h2>{"".join(relations)}</section><details><summary>{"阅读范围" if zh else "Reading scope"}</summary>{scope}</details>{render_attribution([data["language"]])}</main><script>{script}</script></body></html>'

def render_entry(locales):
    """Use exactly the generated languages, including the entry and credit."""
    available = [locale for locale in LOCALES if locale in locales]
    zh, en = "zh-CN" in available, "en-US" in available
    title = "论文精读 · Paper reading" if zh and en else "论文精读" if zh else "Paper reading"
    intro = "选择阅读语言 / Choose your reading language" if zh and en else "选择阅读语言" if zh else "Choose your reading language"
    links = "".join(f'<a class="locale-card" href="{locale}/index.html" hreflang="{locale}" lang="{locale}"><strong>{LOCALES[locale]}</strong><span>{locale}</span></a>' for locale in available)
    css = (ROOT / "assets/style.css").read_text()
    return f'<!doctype html><html lang="{available[0]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{css}</style></head><body class="collection"><main class="language-entry"><p class="eyebrow">READ · THINK · BUILD</p><h1>{title}</h1><p class="intro">{intro}</p><nav class="locale-grid" aria-label="{intro}">{links}</nav>{render_attribution(available)}</main></body></html>'

def render_site(bundles):
    """Validate complete locale bundles first, then render the root and locale trees."""
    rendered = {}
    paper_sets = []
    for data, base in bundles:
        papers = validate(data, base)
        locale = data["language"]
        require(locale not in paper_sets, f"Duplicate locale: {locale}")
        paper_sets.append(locale)
    for data, base in bundles:
        locale = data["language"]
        alternate = next((f"../{other}/index.html" for other in paper_sets if other != locale), None)
        for paper in data["papers"]:
            if alternate:
                other_data = next(d for d, _ in bundles if d["language"] != locale)
                other_paper = next((p for p in other_data["papers"] if p["id"] == paper["id"]), None)
                require(other_paper is not None, f"Translated paper missing: {paper['id']}")
                require({s["id"] for s in other_paper["slides"]} == {s["id"] for s in paper["slides"]}, f"Translated slide anchors differ: {paper['id']}")
            rendered[f"{locale}/{paper['id']}.html"] = render_paper(paper, data, base, alternate)
        rendered[f"{locale}/index.html"] = render_index(data, alternate)
    rendered["index.html"] = render_entry(paper_sets)
    return rendered

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--translation", type=Path, action="append", default=[], help="Translated project bundle (currently zh-CN and en-US only)")
    parser.add_argument("--output", type=Path, help="Site root; language folders and entry index.html are generated automatically")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        bundles = [(json.loads(path.read_text()), path.parent) for path in [args.bundle, *args.translation]]
        rendered = render_site(bundles)
        if not args.check:
            require(args.output is not None, "Supply --output or --check")
            args.output.mkdir(parents=True, exist_ok=True)
            for name in rendered:
                destination = args.output / name
                require(not destination.is_symlink() and not destination.parent.is_symlink(), f"Refusing output symlink: {destination}")
            for name, content in rendered.items():
                destination = args.output / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(content)
        papers = sum(len(d["papers"]) for d, _ in bundles)
        slides = sum(len(p["slides"]) for d, _ in bundles for p in d["papers"])
        print(f"Validated {len(bundles)} locales, {papers} paper pages, {slides} slides; root language entry + {', '.join(d['language'] for d, _ in bundles)}")
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f"Invalid bundle: {exc}\n")

if __name__ == "__main__":
    main()
