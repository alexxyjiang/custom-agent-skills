#!/usr/bin/env python3
"""Verify real KaTeX/PrismJS rendering, font role stacks and unchanged source."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site",type=Path)
    args=parser.parse_args()
    root=args.site.resolve()
    stacks={"ui": '\"Iosevka Aile\", \"Noto Sans CJK SC\", sans-serif', "body": '\"Iosevka Etoile\", \"Noto Serif CJK SC\", serif', "code": 'IosevkaAlexJiang, \"Noto Sans Mono CJK SC\", monospace'}
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",headless=True)
        for locale in ["zh-CN","en-US"]:
            page=browser.new_page(viewport={"width":1600,"height":900})
            errors=[];external=[]
            page.on("pageerror",lambda error:errors.append(str(error)))
            page.on("request",lambda request:external.append(request.url) if request.url.startswith(("http:","https:")) else None)
            for paper in ["react","reflexion"]:
                page.goto((root/locale/(paper+".html")).as_uri()+"#slide-worked-case",wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                assert page.evaluate("katex.version")=="0.16.22"
                assert page.locator(".slide.active .katex").count()==2
                assert page.locator(".slide.active .katex-display").count()==1
                assert page.locator(".katex-error").count()==0
                assert "$5" in page.locator(".slide.active .card p").first.inner_text()
                for selector,role in [(".slide.active h1","ui"),("#next","ui"),(".slide.active .card p","body")]:
                    assert page.locator(selector).first.evaluate("e=>getComputedStyle(e).fontFamily")==stacks[role]
                # KaTeX's glyph families must not be overwritten by prose typography.
                assert page.locator(".slide.active .katex .mord").first.evaluate("e=>getComputedStyle(e).fontFamily").startswith("KaTeX_")
                page.goto((root/locale/(paper+".html")).as_uri()+"#slide-mechanism",wait_until="networkidle")
                code=page.locator(".example > .code-panel code")
                assert code.get_attribute("data-highlighter")=="prismjs"
                assert code.locator('.code-line[data-line="2"] .token.string').count()>0
                assert code.locator('.code-line[data-line="3"] .token.string').count()>0
                assert code.locator('.code-line[data-line="4"] .token.keyword').count()>0
                assert code.locator(".code-line").first.evaluate("e=>getComputedStyle(e).fontFamily")==stacks["code"]
                assert code.locator(".katex").count()==0
                source=code.locator(":scope > .code-line").evaluate_all("es=>es.map(e=>e.textContent).join('\\n')")
                page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async s=>window.copied=s},configurable:true})")
                page.locator(".example > .code-panel .copy-code").click()
                assert page.evaluate("window.copied")==source
                results.append(locale+"/"+paper+": KaTeX inline/display, prices, Prism multiline tokens, fonts and source copy")
            # Untrusted math must never become executable HTML; malformed TeX stays visible.
            page.evaluate(r"""() => {
                const p=document.createElement('p');p.className='math-probe';document.body.append(p);
                p.textContent='\\(\\unknownCommand{x}\\)';
                renderMathInElement(p,{delimiters:[{left:'\\(',right:'\\)',display:false}],throwOnError:false,trust:false});
                window.invalidMathVisible=!!p.textContent;
                p.textContent='\\(\\href{javascript:alert(1)}{click}\\)';
                renderMathInElement(p,{delimiters:[{left:'\\(',right:'\\)',display:false}],throwOnError:false,trust:false});
            }""")
            assert page.evaluate("window.invalidMathVisible")
            assert page.locator(".math-probe a").count()==0
            assert not errors,errors
            assert not external,external
            page.close()
        browser.close()
    print(json.dumps({"status":"passed","checks":results},indent=2))

if __name__=="__main__":main()
