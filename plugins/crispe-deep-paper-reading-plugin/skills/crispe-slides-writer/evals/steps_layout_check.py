#!/usr/bin/env python3
"""Check dense walkthrough rails, inline-dollar TeX and literal prices in a real deck."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck",type=Path)
    parser.add_argument("--slide",default="slide-eq1-rm-loss-code")
    args=parser.parse_args()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",headless=True)
        for width,height in [(3840,2160),(1600,900),(1280,720),(390,844)]:
            page=browser.new_page(viewport={"width":width,"height":height})
            errors=[];page.on("pageerror",lambda error:errors.append(str(error)))
            page.goto(args.deck.resolve().as_uri()+"#"+args.slide,wait_until="networkidle")
            page.wait_for_function("window.paperSlidesReady===true")
            rail=page.locator("section.slide.active .steps")
            assert rail.locator(".step").count()>=5
            for button in rail.locator(".step").all():
                button.click()
                assert button.get_attribute("aria-pressed")=="true"
                assert rail.evaluate("e=>e.scrollHeight<=e.clientHeight+1&&e.scrollWidth<=e.clientWidth+1"), "Every selected step must fit without prose scrolling"
                assert button.evaluate("e=>{let a=e.getBoundingClientRect(),b=e.closest('.steps').getBoundingClientRect();return a.top>=b.top-1&&a.bottom<=b.bottom+1}")
            rail.locator("summary").click()
            assert rail.locator("details").evaluate("e=>e.open")
            assert rail.evaluate("e=>{let a=e.getBoundingClientRect(),f=e.closest('section').querySelector('footer').getBoundingClientRect(),b=document.querySelector('#bottom-bar').getBoundingClientRect();return a.bottom<Math.min(f.top,b.top)}")
            rail.locator("summary").click()
            # Publication prose must fit; scrollbar removal alone must not hide overflow.
            assert rail.evaluate("e=>getComputedStyle(e).overflowY==='visible'&&e.scrollHeight<=e.clientHeight+1&&e.scrollWidth<=e.clientWidth+1")
            annotations=page.locator("annotation").all_text_contents()
            assert all(tex in annotations for tex in [r"r_\theta(x,y)","y_w","y_l"])
            assert not page.locator(".katex-error").count()
            # Repeat the actual production renderer on a DOM-only probe; no source mutation.
            page.evaluate(r"""() => {
                const card=document.createElement('article');card.className='card';
                card.innerHTML='<p id="dollar-probe"></p><pre><code>$x$</code></pre>';
                card.querySelector('p').textContent=String.raw`Price $5 and $10; $x$ and $y_w$; numeric $2$; escaped \$z$; display $$x+1$$.`;
                document.body.append(card);
            }""")
            code=(Path(__file__).resolve().parents[1]/"assets/code.js").read_text()
            renderer=code[code.index("  // Normalize paired"):code.index('  document.querySelectorAll(".copy-code")')]
            page.evaluate("() => {"+renderer+"}")
            probe=page.locator("#dollar-probe")
            assert probe.locator(".katex").count()==3,probe.inner_text()
            assert "$5 and $10" in probe.inner_text()
            assert "$2$" in probe.inner_text()
            assert probe.locator(".katex-display").count()==1
            assert page.locator("article.card > pre code").last.inner_text()=="$x$"
            assert not errors,errors
            print(f"{width}x{height}: five steps, disclosure, footer clearance, inline math and prices passed")
            page.close()
        browser.close()

if __name__=="__main__":main()
