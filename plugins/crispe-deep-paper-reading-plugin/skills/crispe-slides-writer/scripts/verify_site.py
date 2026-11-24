#!/usr/bin/env python3
"""Impact-scoped rendered checks with exact-input reuse; not scientific validation.
Use an existing Playwright environment. Cache/reports must be outside the site.
"""
import argparse
import hashlib
import importlib.util
import json
import platform
import subprocess
import time
from pathlib import Path

SKILL=Path(__file__).resolve().parents[1]
DEFAULT_CHROME=Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def digest(value):
    return hashlib.sha256(value).hexdigest()


def snapshot(site):
    return {str(p.relative_to(site)):digest(p.read_bytes()) for p in sorted(site.rglob("*")) if p.is_file()}


def signature(page):
    import re
    return digest("".join(re.findall(r"<(?:script|style)\b[^>]*>(.*?)</(?:script|style)>",page,re.S)).encode())


def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site",type=Path,help="Locale collection directory")
    parser.add_argument("--level",choices=["content","layout","full"],default="layout")
    parser.add_argument("--deck",action="append",default=[],help="Relative deck filename; repeatable")
    parser.add_argument("--slide",action="append",default=[],help="Affected canonical slide id; content level only")
    parser.add_argument("--cache",type=Path,required=True)
    parser.add_argument("--chrome",type=Path,default=DEFAULT_CHROME)
    parser.add_argument("--fresh",action="store_true")
    parser.add_argument("--max-age",type=int,default=86400)
    args=parser.parse_args()
    site=args.site.resolve(strict=True);cache=args.cache.resolve()
    if not cache.parent.is_dir() or cache==site or site in cache.parents or args.cache.is_symlink() or args.cache.with_suffix(".report.json").is_symlink():parser.error("cache needs an existing parent outside site and cannot be a symlink")
    if args.level=="content" and (not args.deck or not args.slide):parser.error("content requires --deck and --slide; otherwise use layout")
    if args.slide and args.level!="content":parser.error("--slide is only for content checks")
    before=snapshot(site)
    documents={name:(site/name).read_text() for name in before if name.endswith(".html")}
    decks=args.deck or sorted(name for name in before if name.endswith(".html") and name!="index.html" and "/" not in name)
    if args.level=="full":decks=sorted(name for name in before if name.endswith(".html") and name!="index.html" and "/" not in name)
    if not decks:parser.error("no decks")
    for name in decks:
        if name not in before or Path(name).name!=name or not name.endswith(".html"):parser.error("deck must be an existing sibling HTML filename")
    previous={}
    if cache.is_file():
        try:previous=json.loads(cache.read_text())
        except (ValueError,OSError):pass
    if not isinstance(previous,dict):previous={}
    tools={str(p.relative_to(SKILL)):digest(p.read_bytes()) for folder in ["assets","scripts","evals"] for p in sorted((SKILL/folder).rglob("*")) if p.is_file() and p.suffix in {".py",".js",".css",".html",".json"}}
    environment={"platform":platform.platform(),"browser":subprocess.check_output([str(args.chrome),"--version"],text=True).strip()}
    from importlib.metadata import version
    environment["playwright"]=version("playwright")
    # Font installation changes invalidate environment-dependent rendering.
    environment["fonts"]={str(folder):[(str(p),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(folder.rglob("*")) if p.is_file()] for folder in [Path.home()/"Library/Fonts",Path("/Library/Fonts"),Path("/System/Library/Fonts")] if folder.is_dir()}
    environment["browser_path"]=str(args.chrome.resolve())
    environment["browser_stat"]=[args.chrome.stat().st_size,args.chrome.stat().st_mtime_ns]
    env_hash=digest(json.dumps(environment,sort_keys=True).encode())
    level=args.level
    runtime={name:signature(documents[name]) for name in before if name.endswith(".html") and name!="index.html" and "/" not in name}
    if level=="content" and (previous.get("tools")!=tools or previous.get("environment")!=env_hash or any(previous.get("runtime",{}).get(name)!=value for name,value in runtime.items())):
        level="layout";decks=sorted(name for name in before if name.endswith(".html") and name!="index.html" and "/" not in name)
    views=[(1600,900),(390,844)] if level!="full" else [(3840,2160),(2560,1440),(1600,900),(390,844)]
    from playwright.sync_api import sync_playwright
    bounds=load_module("bounds",SKILL/"evals/browser_check.py").BOUNDS
    entries=dict(previous.get("entries",{}));results=[];started=time.perf_counter()
    with sync_playwright() as pw:
        browser=None
        for name in decks:
            selected=args.slide if level=="content" else []
            key=digest(json.dumps({"deck":name,"site":str(site),"source":before,"tools":tools,"environment":env_hash,"level":level,"slides":selected,"views":views},sort_keys=True).encode())
            old=entries.get(key,{})
            if not args.fresh and old.get("status")=="passed" and 0<=time.time()-old.get("time",0)<=args.max_age:
                results.append(dict(old,reused=True));continue
            if browser is None:browser=pw.chromium.launch(executable_path=str(args.chrome),headless=True,chromium_sandbox=True)
            failures=[];states=0;ids=[]
            for width,height in views:
                context=browser.new_context(viewport={"width":width,"height":height},reduced_motion="reduce",service_workers="block")
                page=context.new_page();page.set_default_timeout(5000)
                errors=[];page.on("pageerror",lambda error:errors.append(str(error)))
                context.route("**/*",lambda route:route.abort() if route.request.url.startswith(("http:","https:")) else route.continue_())
                page.on("requestfailed",lambda request:errors.append("resource failed: "+request.url[:160]))
                try:
                    page.goto((site/name).as_uri(),wait_until="load");page.wait_for_function("window.paperSlidesReady===true")
                    all_ids=page.locator("section.slide").evaluate_all("es=>es.map(e=>e.id)")
                    ids=selected or all_ids
                    if any(sid not in all_ids for sid in ids):raise ValueError("Unknown requested slide id")
                    for sid in ids:
                        page.evaluate("id=>location.hash=id",sid)
                        page.wait_for_function("id=>document.querySelector('section.slide.active')?.id===id",arg=sid)
                        def check(state):
                            nonlocal states
                            states+=1
                            found=page.evaluate(bounds)["issues"]
                            if found:failures.append({"slide":sid,"viewport":[width,height],"state":state,"issues":found})
                        check("initial")
                        for button in page.locator("section.slide.active .step").all():button.click();check("step:"+button.inner_text()[:60])
                        for detail in page.locator("section.slide.active details").all():
                            detail.locator("summary").click();check("details-open");detail.locator("summary").click()
                        for zoom in page.locator("section.slide.active .zoom").all():
                            zoom.click();assert page.locator("#image-view").evaluate("e=>e.open");page.keyboard.press("Escape")
                        for link in page.locator("section.slide.active a[href]").all():
                            from urllib.parse import urlsplit
                            target=urlsplit(link.get_attribute("href"))
                            if not target.scheme and target.path.endswith(".html"):
                                destination=(site/target.path).resolve()
                                if not destination.is_relative_to(site) or not destination.is_file():raise ValueError("Missing/out-of-scope link target")
                                if target.fragment and ('id="'+target.fragment+'"') not in documents.get(str(destination.relative_to(site)),""):raise ValueError("Missing canonical link anchor")
                        if page.locator("section.slide.active .figure-layout[data-layout-status=overflow],section.slide.active[data-math-layout-status=overflow]").count():raise ValueError("Layout no-fit status")
                    if level!="content":
                        page.locator("#contents").click();assert page.locator("#toc").evaluate("e=>e.open");page.keyboard.press("Escape")
                        page.keyboard.press("Home")
                        if len(all_ids)>1:
                            page.locator("#next").click();assert page.locator("section.slide.active").get_attribute("id")==all_ids[1]
                            page.locator("#prev").click();assert page.locator("section.slide.active").get_attribute("id")==all_ids[0]
                    if errors:raise ValueError(str(errors))
                except Exception as exc:failures.append({"viewport":[width,height],"error":str(exc)})
                context.close()
            result={"deck":name,"level":level,"status":"failed" if failures else "passed","time":time.time(),"states":states,"slides":ids,"failures":failures,"reused":False}
            results.append(result)
            if not failures:entries[key]=result
        if browser:browser.close()
    stable=snapshot(site)==before
    passed=stable and all(r["status"]=="passed" for r in results)
    report={"status":"passed" if passed else "failed","requested_level":args.level,"effective_level":level,"seconds":round(time.perf_counter()-started,3),"reused":sum(r["reused"] for r in results),"executed":sum(not r["reused"] for r in results),"source_stable":stable,"protocols":["file"],"results":results}
    if passed:
        cache.write_text(json.dumps({"tools":tools,"environment":env_hash,"runtime":{name:signature(documents[name]) for name in before if name.endswith(".html")},"entries":entries},ensure_ascii=False,indent=2)+"\n")
    cache.with_suffix(".report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k!="results"},ensure_ascii=False))
    for row in results:
        if row["failures"]:print(json.dumps({"deck":row["deck"],"failures":row["failures"]},ensure_ascii=False)[:3000])
    return 0 if passed else 1

if __name__=="__main__":raise SystemExit(main())
