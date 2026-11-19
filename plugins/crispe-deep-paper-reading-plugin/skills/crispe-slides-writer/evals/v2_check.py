#!/usr/bin/env python3
"""Reveal migration regression: scale, numbering, Pretty Code and exact copy."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site",type=Path)
    args=parser.parse_args()
    skill=Path(__file__).resolve().parents[1]
    spec=importlib.util.spec_from_file_location("builder",skill/"scripts/build_site.py")
    builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
    fixture=json.loads((skill/"evals/contract-fixtures.json").read_text())["en-US"]
    checks=[]
    with sync_playwright() as pw, tempfile.TemporaryDirectory() as temporary:
        browser=pw.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",headless=True)
        for locale in ["zh-CN","en-US"]:
            for width,height in [(3840,2160),(2560,1440),(1600,900),(390,844)]:
                page=browser.new_page(viewport={"width":width,"height":height})
                page.goto((args.site.resolve()/locale/"reflexion.html").as_uri()+"#slide-code",wait_until="networkidle")
                page.wait_for_function("window.paperSlidesReady===true")
                stage=page.locator("#deck-stage").bounding_box()
                assert abs(stage["width"]/stage["height"]-16/9)<.001,stage
                assert stage["width"]/min(width,height*16/9)>.98,stage
                assert page.evaluate("getComputedStyle(document.body).backgroundColor")=="rgb(255, 255, 240)"
                example=page.locator(".slide.active .example")
                buttons=example.locator(".step")
                def selected(index):
                    assert buttons.nth(index).get_attribute("aria-pressed")=="true"
                    expected=json.loads(buttons.nth(index).get_attribute("data-lines"))
                    assert example.locator(".code-line.highlight").evaluate_all("es=>es.map(e=>Number(e.dataset.line))")==expected
                selected(0)
                page.keyboard.press("ArrowRight");selected(1)
                page.keyboard.press("ArrowRight");selected(2)
                page.keyboard.press("ArrowLeft");selected(1)
                buttons.nth(2).click();selected(2)
                page.locator("#contents").focus()
                page.keyboard.press("ArrowLeft");selected(1)
                page.keyboard.press("ArrowRight");selected(2)
                example.locator(".pretty-controls button").first.click();selected(1)
                example.locator(".pretty-controls button").last.click();selected(2)
                expected=example.locator(":scope > .code-panel .code-line").evaluate_all("es=>es.map(e=>e.textContent).join('\\n')")
                page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async s=>window.copied=s},configurable:true})")
                example.locator(".copy-code").first.click()
                assert page.evaluate("window.copied")==expected
                assert example.locator(".token.keyword").first.evaluate("e=>getComputedStyle(e).color")=="rgb(0, 119, 170)"
                assert page.locator(".katex-error").count()==0
                page.locator("#prev").click()
                assert page.locator(".slide.active .katex-display").count()==1
                assert page.locator(".slide.active .katex .mord").first.evaluate("e=>getComputedStyle(e).fontFamily").startswith("KaTeX_")
                page.locator("#next").click();selected(0)
                page.locator("#next").click();assert page.locator("section.slide.active").get_attribute("id")=="slide-counterexample"
                page.locator("#prev").click();selected(0)
                page.locator("#contents").click();assert page.locator("#toc").evaluate("e=>e.open")
                page.locator("#toc .close").click()
                page.locator("#autoplay").click();assert page.locator("#autoplay").get_attribute("aria-pressed")=="true"
                page.locator("#autoplay").click()
                checks.append(f"{locale}/{width}x{height}: scale, controls, fragments, exact copy, Prism default")
                page.close()
        for count,index,expected in [(4,0,"1 / 4"),(16,7,"08 / 16"),(105,3,"004 / 105")]:
            paper=copy.deepcopy(fixture["papers"][0]);cover=paper["slides"][0]
            paper["slides"]=[dict(copy.deepcopy(cover),id=f"page-{i}") for i in range(count)]
            path=Path(temporary)/f"number-{count}.html"
            path.write_text(builder.render_paper(paper,fixture,skill/"evals"))
            page=browser.new_page();page.goto(path.as_uri()+f"#slide-page-{index}")
            page.wait_for_function("window.paperSlidesReady===true")
            assert page.locator("#page").inner_text()==expected
            assert page.locator("section.slide.active header > span:last-child").inner_text()==expected
            checks.append("page number "+expected);page.close()
        browser.close()
    print(json.dumps({"status":"passed","checks":checks},indent=2))

if __name__=="__main__":main()
