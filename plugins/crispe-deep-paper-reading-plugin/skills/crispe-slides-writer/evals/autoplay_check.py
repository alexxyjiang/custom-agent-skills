#!/usr/bin/env python3
"""Exercise any generated deck, including real-time playback and dynamic holds."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck",type=Path)
    parser.add_argument("--real-time",action="store_true")
    args=parser.parse_args()
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",headless=True)
        context=browser.new_context(viewport={"width":1600,"height":900})
        page=context.new_page();errors=[]
        page.on("pageerror",lambda error:errors.append(str(error)))
        url=args.deck.resolve().as_uri()
        page.goto(url,wait_until="networkidle")
        ids=page.locator(".slide").evaluate_all("es=>es.map(e=>e.id)")
        assert len(ids)>=3
        def active():return page.locator(".slide.active").get_attribute("id")
        if args.real_time:
            page.locator("#playback-speed").select_option("5000")
            page.locator("#autoplay").click()
            assert page.locator("#playback-status").inner_text()
            page.wait_for_function("id=>document.querySelector('.slide.active').id!==id",arg=ids[0],timeout=8000)
            page.locator("#autoplay").click()
            page.evaluate("""() => {const d=document.createElement('details');d.id='dynamic-probe';d.innerHTML='<summary>Probe</summary><p>Details</p>';document.querySelector('.slide.active .slide-body').append(d);d.open=true;}""")
            before=active();page.locator("#autoplay").click()
            page.wait_for_timeout(5500)
            assert active()==before and page.locator("#autoplay").get_attribute("data-state")=="waiting"
            page.evaluate("document.querySelector('#dynamic-probe').open=false")
            page.wait_for_function("id=>document.querySelector('.slide.active').id!==id",arg=before,timeout=8000)
            results.append("real 5-second page advancement and dynamic-details hold/resume")
        page.goto(url,wait_until="networkidle");page.clock.install()
        def advance(ms):page.clock.run_for(ms)
        assert page.locator("#autoplay").get_attribute("aria-pressed")=="false"
        advance(60001);assert active()==ids[0]
        for duration in [5000,15000,30000,60000]:
            page.locator("#playback-speed").select_option(str(duration));page.locator("#autoplay").click()
            before=active();advance(duration-1);assert active()==before
            advance(1);assert active()!=before
            page.locator("#autoplay").click();before=active();advance(duration+1);assert active()==before
        results.append("opt-in, all four intervals, countdown, pause")
        page.keyboard.press("Home");page.locator("#playback-speed").select_option("5000")
        page.evaluate("""() => {const d=document.createElement('details');d.id='dynamic-probe';d.innerHTML='<summary>Probe</summary>';document.querySelector('.slide.active .slide-body').append(d);d.open=true;}""")
        page.locator("#autoplay").click();advance(20000)
        assert active()==ids[0] and page.locator("#autoplay").get_attribute("data-state")=="waiting"
        page.evaluate("document.querySelector('#dynamic-probe').open=false");advance(5500);assert active()!=ids[0]
        page.evaluate("document.querySelector('#dynamic-probe').remove()")
        results.append("generic dynamically inserted details cannot strand playback")
        page.locator("#contents").click();before=active();advance(20000);assert active()==before
        page.keyboard.press("Escape");advance(5500);assert active()!=before
        page.evaluate("Object.defineProperty(document,'hidden',{value:true,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
        before=active();advance(20000);assert active()==before
        page.evaluate("Object.defineProperty(document,'hidden',{value:false,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
        advance(5000);assert active()!=before
        results.append("dialog Escape and tab visibility resume")
        if page.locator("#autoplay").get_attribute("aria-pressed")=="true":page.locator("#autoplay").click()
        page.keyboard.press("Home");page.locator("#playback-speed").select_option("60000");page.locator("#autoplay").click();advance(1000)
        page.locator("#playback-speed").select_option("5000");advance(4999);assert active()==ids[0]
        advance(1);assert active()==ids[1]
        page.locator("#next").click();before=active();advance(4999);assert active()==before
        advance(1);assert active()!=before
        advance(len(ids)*5000)
        assert active()==ids[-1] and page.locator("#autoplay").get_attribute("aria-pressed")=="false"
        page.locator("#autoplay").click();assert active()==ids[0]
        results.append("speed/manual navigation reschedule, last-page stop, restart")
        assert not errors,errors
        browser.close()
    print(json.dumps({"status":"passed","checks":results},indent=2))

if __name__=="__main__":main()
