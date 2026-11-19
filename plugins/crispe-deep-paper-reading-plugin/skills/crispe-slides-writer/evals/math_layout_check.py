#!/usr/bin/env python3
"""Check real formulas and column-to-row fallback without changing their TeX."""
import argparse
import importlib.util
import json
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck",type=Path)
    args=parser.parse_args()
    spec=importlib.util.spec_from_file_location("bounds",Path(__file__).with_name("browser_check.py"))
    checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",headless=True)
        for width,height in [(1600,900),(1280,720),(390,844)]:
            page=browser.new_page(viewport={"width":width,"height":height},reduced_motion="reduce")
            errors=[];page.on("pageerror",lambda error:errors.append(str(error)))
            page.goto(args.deck.resolve().as_uri()+"#slide-retrieval-formula",wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_function("document.querySelector('.slide.active').dataset.mathLayoutStatus")
            slide=page.locator(".slide.active")
            assert slide.get_attribute("data-math-layout-status")=="fit"
            assert slide.locator(".katex-display.math-wrap").count()>0
            assert slide.locator(".katex-display").evaluate_all("es=>es.every(e=>e.scrollWidth<=e.clientWidth+2)")
            tex=slide.locator('annotation[encoding="application/x-tex"]').all_text_contents()
            assert any(r"\alpha_{relevance}\cdot relevance" in value for value in tex)
            assert not page.evaluate(checks.BOUNDS)["issues"],page.evaluate(checks.BOUNDS)["issues"]
            # A single text atom is unbreakable inside KaTeX, but fits a full row.
            page.evaluate(r"""() => {
                document.querySelectorAll('.slide.active .card p').forEach(p=>p.replaceChildren());
                const target=document.querySelector('.slide.active .card:nth-child(2) p');
                katex.render(String.raw`\text{One indivisible mathematical term requiring a wider card}`,target,{displayMode:true,throwOnError:false});
                window.fitPaperMath(document.querySelector('.slide.active'));
            }""")
            assert slide.locator('.math-stacked').count()==1
            assert slide.get_attribute('data-math-layout-status')=='fit'
            assert not page.evaluate(checks.BOUNDS)["issues"],page.evaluate(checks.BOUNDS)["issues"]
            page.evaluate(r"""() => {
                const target=document.querySelector('.slide.active .card:nth-child(2) p');
                target.replaceChildren();
                katex.render(String.raw`\underbrace{`+('abcdefghij'.repeat(30))+'}_{x}',target,{displayMode:true,throwOnError:false});
                window.fitPaperMath(document.querySelector('.slide.active'));
            }""")
            assert slide.get_attribute('data-math-layout-status')=='overflow'
            assert not errors,errors
            results.append(f'{width}x{height}: original TeX, complete wrap, no overlap, atomic row fallback and no-fit detection passed')
            page.close()
        browser.close()
    print(json.dumps({"status":"passed","checks":results},indent=2))

if __name__=="__main__":main()
