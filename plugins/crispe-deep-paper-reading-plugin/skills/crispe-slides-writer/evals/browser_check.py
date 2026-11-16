#!/usr/bin/env python3
"""Read-only rendered smoke checks for a generated slides-writer collection.

uv run --with playwright python browser_check.py SITE [--output DIRECTORY]
Exit 0: checks pass; 1: failures; 2: invalid/changing inputs or launch failure.
Screenshots are evidence for human review, not a subjective visual approval.
Only --output is written; synthetic figure markup exists in browser memory only.
"""
from __future__ import annotations

import argparse
import contextlib
import functools
import hashlib
import http.server
import json
from pathlib import Path
import threading
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright


# CSS-pixel bounds are converted back to unscaled stage pixels for tolerances.
# Text ranges catch painted glyph overflow that scrollHeight alone can miss.
BOUNDS = r"""() => {
 const issues = [], metrics = [];
 const active = document.querySelector('.slide.active');
 const root = active || document.querySelector('main');
 const stage = document.querySelector('#deck-stage');
 const scale = stage ? stage.getBoundingClientRect().width / stage.offsetWidth : 1;
 const eps = Math.max(.4, scale * 1.5);
 const rect = e => {const r=e.getBoundingClientRect();return {left:r.left,top:r.top,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};
 const label = e => e.id ? '#'+e.id : e.tagName.toLowerCase()+'.'+[...e.classList].join('.')+' '+e.textContent.trim().slice(0,55);
 const visible = e => {const s=getComputedStyle(e),r=rect(e);return s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0 && !e.closest('dialog:not([open])') && ![...document.querySelectorAll('details:not([open])')].some(d=>d.contains(e) && e!==d && !e.closest('summary'))};
 const outside = (a,b,vertical=true) => a.left < b.left-eps || a.right > b.right+eps || (vertical && (a.top < b.top-eps || a.bottom > b.bottom+eps));
 const add = (kind,e,container,r,b) => issues.push({kind,element:label(e),container:label(container),rect:r,bounds:b});
 if (!root) return {issues:[{kind:'missing content root'}],metrics};
 if (stage && outside(rect(stage),{left:0,top:0,right:innerWidth,bottom:innerHeight})) add('stage outside viewport',stage,document.documentElement,rect(stage),{width:innerWidth,height:innerHeight});
 if (document.documentElement.scrollWidth > innerWidth+2) issues.push({kind:'document horizontal overflow',scrollWidth:document.documentElement.scrollWidth,width:innerWidth});
 const bar = document.querySelector('#bottom-bar');
 const safe = stage ? {...rect(stage),bottom:rect(bar).top} : null;
 const all = [root,...root.querySelectorAll('*')].filter(visible);
 for (const e of all) {
   const r=rect(e);
   // Descendants of pre intentionally scroll: validate the box and reachability separately.
   const pre=e.closest('pre');
   if (pre && pre!==e) continue;
   if (safe && e!==root && outside(r,safe)) add('content outside stage safe area',e,stage,r,safe);
   const parent=e.parentElement;
   if (parent && parent.matches('.slide-body,.cards,.card,.example,.steps,.paper-card,.paper-grid') && outside(r,rect(parent))) add('child outside container',e,parent,r,rect(parent));
   if (e.matches('pre')) {
     const cs=getComputedStyle(e);
     metrics.push({element:label(e),rect:r,clientWidth:e.clientWidth,clientHeight:e.clientHeight,scrollWidth:e.scrollWidth,scrollHeight:e.scrollHeight,overflowX:cs.overflowX,overflowY:cs.overflowY});
     if (e.scrollHeight>e.clientHeight+2 && !/auto|scroll/.test(cs.overflowY)) add('unscrollable code height',e,e,r,r);
     if (e.scrollWidth>e.clientWidth+2 && !/auto|scroll/.test(cs.overflowX) && cs.whiteSpace!=='pre-wrap') add('unscrollable code width',e,e,r,r);
     continue;
   }
   // Direct text-node rectangles, including wrapped line fragments.
   for (const node of e.childNodes) {
     if(node.nodeType!==Node.TEXT_NODE || !node.textContent.trim()) continue;
     const range=document.createRange(); range.selectNodeContents(node);
     for (const tr of range.getClientRects()) {
       const t={left:tr.left,top:tr.top,right:tr.right,bottom:tr.bottom,width:tr.width,height:tr.height};
       if (outside(t,r)) metrics.push({kind:'text range overhang (may include hanging punctuation)',element:label(e),rect:t,bounds:r});
       const card=e.closest('.card,.paper-card');
       if(card && outside(t,rect(card))) add('text outside card',e,card,t,rect(card));
       if(safe && outside(t,safe)) add('text outside stage safe area',e,stage,t,safe);
     }
   }
 }
 // Sibling boxes may overlap even when both fit inside the stage.
 // Descendant paint can exceed its layout box and overlap a later sibling.
 if(active) {
   const sections=[...active.children].filter(visible);
   for(let i=0;i<sections.length;i++) for(let j=i+1;j<sections.length;j++) {
     const later=sections[j], b=rect(later);
     for(const e of [sections[i],...sections[i].querySelectorAll('pre,.steps,details,.card')].filter(visible)) {
       const a=rect(e);
       if(Math.min(a.right,b.right)-Math.max(a.left,b.left)>eps && Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>eps)
         issues.push({kind:'paint overlaps later slide section',element:label(e),other:label(later),rect:a,otherRect:b});
     }
   }
 }
 for(const parent of all.filter(e=>e.matches('.slide,.slide-body,.cards,.example,.steps,.card,.paper-card,#bottom-bar'))) {
   const children=[...parent.children].filter(visible);
   for(let i=0;i<children.length;i++) for(let j=i+1;j<children.length;j++) {
     const a=rect(children[i]),b=rect(children[j]);
     if(Math.min(a.right,b.right)-Math.max(a.left,b.left)>eps && Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>eps)
       issues.push({kind:'sibling overlap',element:label(children[i]),other:label(children[j]),rect:a,otherRect:b});
   }
 }
 if(bar) {
   const b=rect(bar);
   for(const e of bar.children) if(visible(e) && outside(rect(e),b)) add('navigation outside bar',e,bar,rect(e),b);
 }
 return {issues,metrics,scale};
}"""


class SiteChanged(RuntimeError):
    pass


class Checker:
    def __init__(self, site: Path, output: Path | None):
        self.site, self.output = site, output
        self.baseline = self.snapshot()
        if 'index.html' not in self.baseline or len(self.baseline) < 3:
            raise ValueError('Expected index.html and at least two generated HTML decks')
        self.results = []
        self.coverage = []
        self.browser_name = ''

    def snapshot(self):
        return {str(p.relative_to(self.site)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(self.site.rglob('*')) if p.is_file()}

    def stable(self):
        if self.snapshot() != self.baseline:
            raise SiteChanged('Generated site changed during verification; stop and rerun after rebuild completes')

    def record(self, name, ok, detail=None):
        row = {'check': name, 'ok': bool(ok)}
        if detail is not None:
            row['detail'] = detail
        self.results.append(row)

    def attempt(self, name, action):
        self.stable()
        try:
            action()
        except SiteChanged:
            raise
        except Exception as exc:
            self.record(name, False, str(exc))
        else:
            self.record(name, True)
        self.stable()

    def goto(self, page, url):
        self.stable()
        response = page.goto(url, wait_until='networkidle')
        if response is not None:
            assert response.ok, f'HTTP {response.status}: {url}'
        page.evaluate('document.fonts.ready')
        self.stable()

    def screenshot(self, page, name):
        if self.output:
            page.screenshot(path=str(self.output / (name + '.png')), full_page=True)

    def bounds(self, page, name):
        result = page.evaluate(BOUNDS)
        self.record(name + '/rendered-bounds', not result['issues'], result)

    def selected(self, page, slide_id):
        assert page.locator('.slide.active').count() == 1
        assert page.locator('.slide.active').get_attribute('id') == slide_id
        assert unquote(urlsplit(page.url).fragment) == slide_id
        assert page.locator('#prev').is_disabled() == (page.locator('.slide').first.get_attribute('id') == slide_id)
        assert page.locator('#next').is_disabled() == (page.locator('.slide').last.get_attribute('id') == slide_id)
        bad = page.locator('.slide').evaluate_all("es => es.filter(e => e.inert === e.classList.contains('active') || e.getAttribute('aria-hidden') !== String(!e.classList.contains('active'))).map(e=>e.id)")
        assert not bad, f'Hidden slides not inert/aria-hidden: {bad}'
        # Attempt programmatic focus: inert controls must reject it.
        assert page.evaluate("""() => {for(const e of document.querySelectorAll('.slide:not(.active) a,.slide:not(.active) button')) {e.focus(); if(document.activeElement===e)return false;}return true;}""")

    def scroll_code(self, page, name):
        for i, pre in enumerate(page.locator('.slide.active pre:visible').all()):
            info = pre.evaluate(r"""e => {
              const old=[e.scrollLeft,e.scrollTop];
              const r=e.getBoundingClientRect(), s=r.width/e.offsetWidth;
              e.scrollTo(e.scrollWidth,e.scrollHeight);
              const end={left:e.scrollLeft,top:e.scrollTop};
              const range=document.createRange();range.selectNodeContents(e);
              const boxes=[...range.getClientRects()].filter(r=>r.width&&r.height);
              const maxBottom=Math.max(...boxes.map(r=>r.bottom));
              const maxRight=Math.max(...boxes.map(r=>r.right));
              const okY=e.scrollHeight<=e.clientHeight+2 || (end.top>0 && maxBottom<=r.bottom+2*s);
              const okX=e.scrollWidth<=e.clientWidth+2 || (end.left>0 && maxRight<=r.right+2*s);
              e.scrollTo(...old);
              return {ok:okX&&okY,okX,okY,end,rect:{x:r.x,y:r.y,width:r.width,height:r.height},maxBottom,maxRight};
            }""")
            self.record(f'{name}/code-scroll-{i}', info.pop('ok'), info)

    def interactions(self, page, base, filename, ids, name):
        url = base + filename
        def nav():
            self.goto(page, url + '#' + ids[0])
            for i in range(1, len(ids)):
                page.locator('#next').click()
                self.selected(page, ids[i])
            for i in range(len(ids)-2, -1, -1):
                page.locator('#prev').click()
                self.selected(page, ids[i])
            # Unfocus button: Home/End should be dispatched on the document.
            page.locator('#contents').focus()
            for key, index in [('End',-1),('Home',0),('ArrowRight',1),('ArrowDown',2),('ArrowLeft',1),('ArrowUp',0)]:
                page.keyboard.press(key)
                self.selected(page, ids[index])
        self.attempt(name + '/buttons-and-keyboard', nav)

        def toc():
            self.goto(page, url + '#' + ids[0])
            button=page.locator('#contents')
            button.focus()
            page.keyboard.press('Enter')
            assert page.locator('#toc').evaluate('e=>e.open')
            assert page.evaluate("document.activeElement.closest('#toc') !== null")
            before=page.locator('.slide.active').get_attribute('id')
            page.keyboard.press('ArrowRight')
            assert page.locator('.slide.active').get_attribute('id') == before
            # Tab containment in native modal.
            for _ in range(len(ids)+3):
                page.keyboard.press('Tab')
                assert page.evaluate("document.activeElement===document.body || document.activeElement.closest('#toc') !== null")
            page.keyboard.press('Escape')
            assert not page.locator('#toc').evaluate('e=>e.open')
            assert button.evaluate('e=>document.activeElement===e'), 'TOC Escape did not restore trigger focus'
            button.press('Enter')
            page.locator('#toc nav a').last.focus()
            page.keyboard.press('Enter')
            self.selected(page, ids[-1])
            assert not page.locator('#toc').evaluate('e=>e.open')
        self.attempt(name + '/toc-keyboard-escape-focus', toc)

        def links():
            found=[]
            for slide_id in ids:
                self.goto(page, url + '#' + slide_id)
                links=page.locator('.slide.active a[href]')
                for j in range(links.count()):
                    href=links.nth(j).get_attribute('href')
                    target=urlsplit(href)
                    if target.scheme or not target.path or Path(target.path).name==filename:
                        continue
                    if target.path.endswith('.html'):
                        found.append((slide_id,j,href))
            assert found, 'No cross-paper relation link found'
            for slide_id,j,href in found:
                self.goto(page, url+'#'+slide_id)
                page.locator('.slide.active a[href]').nth(j).click()
                page.wait_for_load_state('networkidle')
                assert Path(urlsplit(page.url).path).name == Path(urlsplit(href).path).name
                self.selected(page, urlsplit(href).fragment or 'slide-cover')
        self.attempt(name + '/cross-paper-navigation', links)

    def deck(self, page, base, filename, name):
        self.goto(page, base+filename)
        ids=page.locator('.slide').evaluate_all('es=>es.map(e=>e.id)')
        assert ids and len(ids)==len(set(ids)), 'Missing/duplicate slide IDs'
        self.coverage.append({'run':name,'slides':ids})
        for slide_id in ids:
            self.goto(page, base+filename+'#'+slide_id)
            self.attempt(name+'/'+slide_id+'/deep-link-inert', lambda: self.selected(page,slide_id))
            self.bounds(page,name+'/'+slide_id)
            self.scroll_code(page,name+'/'+slide_id)
            for i,example in enumerate(page.locator('.slide.active .example').all()):
                for j,button in enumerate(example.locator('.step').all()):
                    def step(button=button,example=example):
                        button.click()
                        expected=json.loads(button.get_attribute('data-lines'))
                        actual=example.locator('.code-line.highlight').evaluate_all('es=>es.map(e=>Number(e.dataset.line))')
                        assert sorted(expected)==sorted(actual), f'expected {expected}, highlighted {actual}'
                        assert button.get_attribute('aria-pressed')=='true'
                        assert example.locator('.step[aria-pressed=true]').count()==1
                    self.attempt(f'{name}/{slide_id}/example-{i}-step-{j}',step)
            if page.locator('.slide.active .example').count():
                self.screenshot(page, name+'-code')
                # Disclosure expansion is a separate real layout state.
                for d,details in enumerate(page.locator('.slide.active details').all()):
                    self.attempt(f'{name}/{slide_id}/disclosure-{d}-pointer',
                                 lambda details=details: details.locator('summary').click(timeout=1500))
                    # Keyboard expansion still exercises the open state if pointer is occluded.
                    if not details.evaluate('e=>e.open'):
                        details.locator('summary').focus()
                        page.keyboard.press('Enter')
                    self.record(f'{name}/{slide_id}/disclosure-{d}-expanded', details.evaluate('e=>e.open'))
                if page.locator('.slide.active details').count():
                    self.bounds(page,name+'/'+slide_id+'/details-open')
                    self.scroll_code(page,name+'/'+slide_id+'/details-open')
                    self.screenshot(page,name+'-code-details-open')
        self.interactions(page,base,filename,ids,name)

    def synthetic_figure(self, page, filename):
        source=(self.site/filename).read_text()
        svg="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='400'%3E%3Crect width='800' height='400' fill='indigo'/%3E%3C/svg%3E"
        markup=f'<figure><button class="zoom" type="button"><img src="{svg}" alt="Synthetic zoom probe"></button><figcaption>Synthetic only</figcaption></figure>'
        # Insert before runtime executes so the real .zoom registration is exercised.
        source=source.replace('</section>',markup+'</section>',1)
        page.set_content(source,wait_until='networkidle')
        page.locator('.slide.active .zoom').click()
        viewer=page.locator('#image-view')
        assert viewer.evaluate('e=>e.open')
        assert viewer.locator('img').get_attribute('alt')=='Synthetic zoom probe'
        assert viewer.locator('img').evaluate('e=>e.complete && e.naturalWidth===800')
        page.keyboard.press('ArrowRight')
        assert page.locator('.slide.active').get_attribute('id')=='slide-cover'
        page.keyboard.press('Escape')
        assert not viewer.evaluate('e=>e.open')
        assert page.locator('.zoom').evaluate('e=>document.activeElement===e')
        page.locator('.zoom').click()
        viewer.locator('.close').click()
        assert not viewer.evaluate('e=>e.open')

    def run(self, browser, bases):
        for protocol,base in bases:
            for width,height in [(1600,900),(1280,720),(390,844)]:
                context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
                page=context.new_page()
                page.set_default_timeout(5000)
                errors=[]
                external=[]
                missing=[]
                page.on('pageerror',lambda e: errors.append(str(e)))
                page.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
                def route(r):
                    u=urlsplit(r.request.url)
                    if u.scheme in ('http','https') and not (protocol=='http' and u.netloc==urlsplit(base).netloc):
                        external.append(r.request.url)
                        r.abort()
                    else:
                        r.continue_()
                page.route('**/*',route)
                page.on('requestfailed',lambda r: missing.append({'url':r.url,'failure':r.failure}))
                page.on('response',lambda r: missing.append({'url':r.url,'status':r.status}) if r.status>=400 else None)
                prefix=f'{protocol}-{width}x{height}'
                def collection():
                    self.goto(page,base+'index.html')
                    cards=page.locator('.paper-card')
                    assert cards.count()>=2
                    self.bounds(page,prefix+'/collection')
                    self.screenshot(page,prefix+'-collection')
                    # Click both actual cards, verifying active deck and back navigation.
                    hrefs=cards.evaluate_all('es=>es.map(e=>e.getAttribute("href"))')
                    for i,href in enumerate(hrefs):
                        self.goto(page,base+'index.html')
                        page.locator('.paper-card').nth(i).click()
                        page.wait_for_load_state('networkidle')
                        assert Path(urlsplit(page.url).path).name==Path(urlsplit(href).path).name
                        assert page.locator('.slide.active').count()==1
                        page.go_back(wait_until='networkidle')
                        assert page.locator('.paper-card').count()==len(hrefs)
                self.attempt(prefix+'/collection-navigation',collection)
                for filename in sorted(k for k in self.baseline if k.endswith('.html') and k!='index.html' and '/' not in k):
                    name=prefix+'-'+Path(filename).stem
                    self.attempt(name+'/deck',lambda filename=filename,name=name:self.deck(page,base,filename,name))
                self.record(prefix+'/console-page-errors',not errors,errors)
                self.record(prefix+'/no-external-resource-dependencies',not external,external)
                self.record(prefix+'/no-failed-resources',not missing,missing)
                context.close()
        context=browser.new_context(viewport={'width':1600,'height':900},reduced_motion='reduce')
        page=context.new_page()
        page.set_default_timeout(5000)
        self.attempt('synthetic-only/figure-zoom-real-runtime',lambda:self.synthetic_figure(page,next(k for k in self.baseline if k.endswith('.html') and k!='index.html' and '/' not in k)))
        context.close()

    def report(self, invalid=None):
        failures=[r for r in self.results if not r['ok']]
        report={'status':'invalid' if invalid else ('failed' if failures else 'passed'),
                'browser':self.browser_name,'site':str(self.site),'source_sha256':self.baseline,
                'checks':len(self.results),'failures':len(failures),'coverage':self.coverage,
                'invalid_reason':invalid,'results':self.results,
                'visual_review':'Automated rendered bounds and interaction checks only; screenshots require human review.'}
        if self.output:
            (self.output/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k not in ('results','source_sha256')},indent=2,ensure_ascii=False))
        for r in failures:
            print('FAIL '+r['check']+': '+json.dumps(r.get('detail'),ensure_ascii=False)[:1500])
        return 2 if invalid else int(bool(failures))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main():
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('site',type=Path)
    parser.add_argument('--output',type=Path,help='Optional screenshots and report.json directory')
    parser.add_argument('--no-http',action='store_true',help='Only file:// checks')
    parser.add_argument('--chrome',type=Path,help='Explicit installed Chromium/Chrome executable')
    args=parser.parse_args()
    site=args.site.expanduser().resolve(strict=True)
    if not site.is_dir():
        parser.error('site must be a directory')
    output=args.output.expanduser().resolve() if args.output else None
    if output:
        if output==site or site in output.parents:
            parser.error('output must be outside the generated site')
        if not output.parent.is_dir():
            parser.error('output parent must already exist')
        output.mkdir(exist_ok=True)
    checker=Checker(site,output)
    invalid=None
    try:
        with contextlib.ExitStack() as stack:
            bases=[('file',site.as_uri()+'/')]
            if not args.no_http:
                handler=functools.partial(QuietHandler,directory=str(site))
                server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
                stack.callback(server.server_close)
                thread=threading.Thread(target=server.serve_forever,daemon=True)
                thread.start()
                stack.callback(thread.join,5)
                stack.callback(server.shutdown)
                bases.append(('http',f'http://127.0.0.1:{server.server_port}/'))
            pw=stack.enter_context(sync_playwright())
            if args.chrome:
                browser=pw.chromium.launch(executable_path=str(args.chrome),headless=True)
                checker.browser_name=str(args.chrome)
            else:
                try:
                    browser=pw.chromium.launch(headless=True)
                    checker.browser_name='Playwright Chromium'
                except Exception as exc:
                    chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
                    if not chrome.is_file():
                        raise RuntimeError(f'Bundled Chromium unavailable; use --chrome: {exc}') from exc
                    browser=pw.chromium.launch(executable_path=str(chrome),headless=True)
                    checker.browser_name=str(chrome)
            stack.callback(browser.close)
            checker.run(browser,bases)
            checker.stable()
    except Exception as exc:
        invalid=f'{type(exc).__name__}: {exc}'
    return checker.report(invalid)


if __name__=='__main__':
    raise SystemExit(main())
