#!/usr/bin/env python3
"""Verify image/text layouts using explicit synthetic probes and actual figures."""
import argparse
import importlib.util
import json
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("example",type=Path)
    args=parser.parse_args()
    base=args.example.resolve()
    spec=importlib.util.spec_from_file_location("bounds",Path(__file__).with_name("browser_check.py"))
    checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)
    expected={"wide":"top","portrait":"left","right":"right","bottom":"bottom","full":"full","dense":"left"}
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",headless=True)
        for width,height in [(1600,900),(1280,720),(390,844)]:
            page=browser.new_page(viewport={"width":width,"height":height},reduced_motion="reduce")
            errors=[];page.on("pageerror",lambda error:errors.append(str(error)))
            for name,mode in expected.items():
                page.goto((base/"site/zh-CN/layout-probe.html").as_uri()+"#slide-appendix-"+name+"-figure",wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                root=page.locator(".slide.active .figure-layout")
                page.wait_for_function("document.querySelector('.slide.active .figure-layout').dataset.layoutStatus")
                assert root.get_attribute("data-layout")==mode,(name,root.get_attribute("data-layout"))
                assert root.get_attribute("data-layout-status")=="fit"
                shares=json.loads(root.get_attribute("data-region-shares"))
                assert all(share>=.298 for share in shares),(name,shares)
                assert not page.evaluate(checks.BOUNDS)["issues"],(name,page.evaluate(checks.BOUNDS)["issues"])
                image=page.locator(".slide.active img")
                assert image.evaluate("e=>Math.abs(e.clientWidth/e.clientHeight-e.naturalWidth/e.naturalHeight)<.02")
                assert page.locator(".slide.active .card p").evaluate_all("es=>es.every(e=>getComputedStyle(e).fontSize==='18px')")
                if width==1600:page.screenshot(path=str(base/(name+"-layout.png")))
                page.locator(".slide.active .zoom").click();assert page.locator("#image-view").evaluate("e=>e.open");page.keyboard.press("Escape")
            # Inject deliberately excessive notes into the same renderer; it must
            # report failure rather than label clipping as successful fitting.
            page.evaluate("""() => {
                const root=document.querySelector('.slide.active .figure-layout');
                root.dataset.hasNotes='true';
                root.querySelector('.figure-notes .cards').innerHTML=Array.from({length:8},()=>'<article class="card"><h3>Long note</h3><p>'+('Too much content. '.repeat(150))+'</p></article>').join('');
                window.fitPaperFigures(document.querySelector('.slide.active'));
            }""")
            assert page.locator(".slide.active .figure-layout").get_attribute("data-layout-status")=="overflow"
            assert not errors,errors
            results.append(f"{width}x{height}: six layouts, text/image bounds, unchanged aspect ratio/type size, zoom and no-fit detection passed")
            page.close()
        browser.close()
    print(json.dumps({"status":"passed","checks":results},indent=2))
    (base/"results.json").write_text(json.dumps(results,indent=2)+"\n")

if __name__=="__main__":main()
