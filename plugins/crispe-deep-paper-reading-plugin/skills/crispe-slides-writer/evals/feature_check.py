#!/usr/bin/env python3
"""Exercise actual playback timers, locale links and exact-source copying in Chrome."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    args = parser.parse_args()
    root = args.site.resolve()
    checks = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless=True)
        entry = browser.new_page(viewport={"width":390,"height":844})
        entry.goto((root / "index.html").as_uri())
        assert entry.locator(".locale-card").count() == 2
        for locale in ["zh-CN", "en-US"]:
            entry.goto((root / "index.html").as_uri())
            entry.locator(f'a[href="{locale}/index.html"]').click()
            assert entry.locator("html").get_attribute("lang") == locale
            assert entry.locator(".paper-card").count() == 2
        entry.close()
        checks.append("root language entry reaches both locale collections")
        for locale in ["zh-CN/", "en-US/"]:
            context = browser.new_context(viewport={"width":1600,"height":900})
            page = context.new_page()
            page.goto((root / locale / "index.html").as_uri())
            assert page.locator(".paper-score").all_text_contents() == (["深读评分 3/4"] * 2 if locale == "zh-CN/" else ["Reading score 3/4"] * 2)
            if locale == "en-US/":
                assert not page.locator("body").evaluate("e => {const c=e.cloneNode(true);c.querySelectorAll('.language-switch,script,style').forEach(n=>n.remove());return /[\u4e00-\u9fff]/.test(c.textContent)}")
            page.locator("details").evaluate("e => e.open=true")
            assert page.locator(".code-panel code.language-json .token.property").count() > 0
            # Exercise file:// clipboard fallback and compare content exactly, including whitespace.
            page.evaluate("""() => {
              Object.defineProperty(navigator, 'clipboard', {configurable:true,value:{writeText:async()=>{throw new Error('forced fallback')}}});
              document.execCommand = command => {if(command!=='copy')return false;window.copied=document.querySelector('textarea').value;return true;};
            }""")
            expected = page.locator(".code-panel code > .code-line").evaluate_all("es => es.map(e=>e.textContent).join('\\n')")
            page.locator(".copy-code").click()
            assert page.evaluate("window.copied") == expected.replace("\\n", "\n")
            assert json.loads(page.evaluate("window.copied"))["max_full_text"] == 2
            checks.append(locale + "scores, English content and exact JSON copy")
            page.goto((root / locale / "react.html").as_uri()+"#slide-mechanism")
            if locale == "en-US/":
                assert not page.locator("body").evaluate("e => {const c=e.cloneNode(true);c.querySelectorAll('.language-switch,script,style').forEach(n=>n.remove());return /[\u4e00-\u9fff]/.test(c.textContent)}")
            source = page.locator(".example > .code-panel code > .code-line").evaluate_all("es=>es.map(e=>e.textContent).join('\\n')")
            page.evaluate("""() => {window.copied=null;Object.defineProperty(navigator,'clipboard',{value:{writeText:async s=>{window.copied=s}},configurable:true});}""")
            page.locator(".example > .code-panel .copy-code").click()
            assert page.evaluate("window.copied") == source.replace("\\n", "\n")
            page.locator(".language-switch").click()
            assert page.url.endswith("react.html#slide-mechanism")
            assert page.locator("html").get_attribute("lang") == ("en-US" if locale == "zh-CN/" else "zh-CN")
            checks.append(locale + "Python source copy and same-slide language switch")
            page.goto((root / locale / "react.html").as_uri())
            page.clock.install()
            assert page.locator("#playback-speed option").evaluate_all("es=>es.map(e=>e.value)") == ["5000","15000","30000","60000"]
            def active():return page.locator(".slide.active").get_attribute("id")
            def advance(ms):page.clock.run_for(ms)
            assert page.locator("#autoplay").get_attribute("aria-pressed") == "false"
            advance(60001); assert active()=="slide-cover"
            for duration in [5000,15000,30000,60000]:
                page.locator("#playback-speed").select_option(str(duration))
                page.locator("#autoplay").click()
                first=active();advance(duration-1);assert active()==first
                advance(1);assert active()!=first
                page.locator("#autoplay").click(); stopped=active();advance(duration+1);assert active()==stopped
            checks.append(locale + "all four timer intervals and pause")
            page.keyboard.press("Home")
            page.locator("#playback-speed").select_option("60000")
            page.locator("#autoplay").click();advance(1000)
            page.locator("#playback-speed").select_option("5000")
            before=active();advance(4999);assert active()==before;advance(1);assert active()!=before
            # Native dialog holds playback, then restarts a full interval after closing.
            page.locator("#contents").click();before=active();advance(60001);assert active()==before
            page.keyboard.press("Escape");page.wait_for_function("!document.querySelector('#toc').open");advance(5100);assert active()!=before, page.evaluate("({playing,timer,current,hidden:document.hidden,toc:toc.open,now:Date.now()})")
            if page.locator("#autoplay").get_attribute("aria-pressed")=="true":page.locator("#autoplay").click()
            page.keyboard.press("Home");page.locator("#autoplay").click()
            page.evaluate("Object.defineProperty(document,'hidden',{value:true,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
            advance(60001);assert active()=="slide-cover"
            page.evaluate("Object.defineProperty(document,'hidden',{value:false,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
            advance(5000);assert active()=="slide-worked-case"
            page.clock.run_for(100000);assert active()=="slide-evidence"
            assert page.locator("#autoplay").get_attribute("aria-pressed")=="false"
            page.locator("#autoplay").click();assert active()=="slide-cover"
            checks.append(locale + "speed reschedule, dialog/hidden holds, end stop and restart")
            context.close()
        browser.close()
    print(json.dumps({"status":"passed","checks":checks},indent=2))

if __name__ == "__main__":
    main()
