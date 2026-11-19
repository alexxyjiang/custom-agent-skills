#!/usr/bin/env python3
"""Export a Reveal paper deck as searchable vector/text PDF using Chromium.

Optional isolated dependencies: uv run --with playwright --with pypdf python ...
Only exports a concrete paper deck, never a site chooser/collection page.
"""
import argparse
import functools
import http.server
import json
import os
from pathlib import Path
import shutil
import threading
import tempfile
from urllib.parse import urlparse,urlunparse,parse_qsl,urlencode,unquote,quote


def export(args):
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import TextStringObject
    if not args.output.parent.is_dir():raise ValueError("Verify/create output parent first")
    if args.output.exists() and not args.overwrite:raise ValueError("PDF exists; pass --overwrite")
    server = None
    thread = None
    source = args.source
    local = Path(source).expanduser()
    if local.is_file():
        local = local.resolve()
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*_): pass
        server = http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(Quiet,directory=str(local.parent)))
        thread = threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        url = f"http://127.0.0.1:{server.server_port}/{local.name}"
    else:
        parsed = urlparse(source)
        if parsed.scheme not in {"http","https"}: raise ValueError("Source must be an existing deck HTML or HTTP(S) URL")
        url = source
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query,keep_blank_values=True));query["print-pdf"]=""
    url = urlunparse(parsed._replace(query=urlencode(query),fragment=""))
    report = {}
    temporary = tempfile.TemporaryDirectory(prefix="slides-pdf-",dir=args.output.parent)
    candidate_pdf = Path(temporary.name)/"deck.pdf"
    try:
        with sync_playwright() as pw:
            executable = args.chrome
            if executable is None:
                candidate = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
                executable = str(candidate) if candidate.is_file() else shutil.which("chromium") or shutil.which("google-chrome")
            browser = pw.chromium.launch(executable_path=executable,headless=True)
            page = browser.new_page(viewport={"width":1600,"height":900},reduced_motion="reduce")
            errors=[];page.on("pageerror",lambda error:errors.append(str(error)))
            page.on("requestfailed",lambda request:errors.append("Failed resource: "+request.url))
            page.on("response",lambda response:errors.append(f"HTTP {response.status}: {response.url}") if response.status>=400 else None)
            page.goto(url,wait_until="networkidle",timeout=args.timeout)
            if page.locator(".reveal .slides section.slide").count()==0:raise ValueError("Not a paper deck: chooser/collection pages cannot be exported")
            page.wait_for_function("window.paperSlidesReady===true",timeout=args.timeout)
            page.evaluate("document.fonts.ready")
            page.evaluate("window.paperSlidesPreparePrint?.()")
            page.wait_for_function("document.querySelectorAll('.pdf-page').length>0",timeout=args.timeout)
            page.wait_for_timeout(500)
            broken=page.locator("section.slide img").evaluate_all("es=>es.filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src.slice(0,120))")
            if broken:raise ValueError("Missing images: "+json.dumps(broken))
            count=page.locator(".slides section.slide").count()
            bad=page.evaluate("""() => [...document.querySelectorAll('section.slide')].flatMap(slide => {
                const issues=[];const rect=slide.getBoundingClientRect();
                if(slide.dataset.mathLayoutStatus==='overflow')issues.push('math overflow');
                if(slide.querySelector('[data-layout-status=overflow]'))issues.push('figure layout overflow');
                slide.querySelectorAll('.card,.takeaway,footer,figcaption,.code-panel').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width||!r.height)return;if(r.top<rect.top-2||r.left<rect.left-2||r.bottom>rect.bottom+2||r.right>rect.right+2)issues.push(e.className+' outside page');});
                slide.querySelectorAll('.code-panel pre').forEach(e=>{if(e.clientWidth&&e.clientHeight&&(e.scrollWidth>e.clientWidth+2||e.scrollHeight>e.clientHeight+2))issues.push('code needs print continuation');});
                return issues.map(issue=>({slide:slide.id,issue}));
            })""")
            if bad:raise ValueError("Print layout failed: "+json.dumps(bad))
            if errors:raise ValueError("Page errors: "+json.dumps(errors))
            page.pdf(path=str(candidate_pdf),width="1600px",height="900px",print_background=True,prefer_css_page_size=True,margin={"top":"0","right":"0","bottom":"0","left":"0"})
            browser.close()
        reader=PdfReader(str(candidate_pdf));actual=len(reader.pages)
        if actual!=count:raise ValueError(f"Expected {count} slides/pages, exported {actual}")
        sizes=[(round(float(p.mediabox.width),1),round(float(p.mediabox.height),1)) for p in reader.pages]
        if any(abs(w/h-16/9)>.01 for w,h in sizes):raise ValueError("Unexpected page aspect ratio")
        if not all((p.extract_text() or '').strip() for p in reader.pages):raise ValueError("PDF has empty/unsearchable slide pages")
        report={"status":"passed","source":source,"pdf":str(args.output),"slides":count,"pages":actual,"page_sizes_points":sizes,"searchable_text":True,"export":"Chromium Reveal print-pdf; fragments combined"}
        # Chromium resolves relative HTML links against the temporary server.
        # Rewrite those annotations relative to the PDF, so delivery survives shutdown.
        writer=PdfWriter(clone_from=reader)
        for pdf_page in writer.pages:
            for reference in pdf_page.get("/Annots",[]):
                action=reference.get_object().get("/A",{})
                uri=urlparse(str(action.get("/URI","")))
                if server and uri.netloc==urlparse(url).netloc:
                    target=(local.parent/unquote(uri.path).lstrip("/")).resolve()
                    if not target.is_file():raise ValueError("Missing local link target: "+str(target))
                    if uri.fragment and ('id="'+unquote(uri.fragment)+'"') not in target.read_text():
                        raise ValueError("Missing local slide anchor: "+uri.fragment)
                    relative=quote(os.path.relpath(target,args.output.parent.resolve()),safe="/")
                    action[TextStringObject("/URI")]=TextStringObject(relative+("#"+uri.fragment if uri.fragment else ""))
        rewritten=Path(temporary.name)/"linked.pdf"
        writer.write(str(rewritten))
        candidate_pdf=rewritten
        reader=PdfReader(str(candidate_pdf))
        links=[]
        for number,page in enumerate(reader.pages,1):
            for reference in page.get("/Annots",[]):
                annotation=reference.get_object()
                if annotation.get("/Subtype")=="/Link":
                    action=annotation.get("/A",{})
                    links.append({"page":number,"uri":str(action.get("/URI","")),"destination":str(annotation.get("/Dest",action.get("/D","")))})
        report["links"]=links
        report["link_validation"]="Local HTML targets/anchors verified and relative to PDF; remote reachability and cross-deck PDF remapping not inferred"
        candidate_pdf.replace(args.output)
        args.output.with_suffix(".export.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
        return report
    finally:
        temporary.cleanup()
        if server:server.shutdown();server.server_close();thread.join()


def main():
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source")
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--chrome")
    parser.add_argument("--timeout",type=int,default=30000)
    parser.add_argument("--overwrite",action="store_true")
    args=parser.parse_args()
    try:print(json.dumps(export(args),ensure_ascii=False,indent=2))
    except (ValueError,OSError) as exc:parser.exit(1,str(exc)+"\n")

if __name__=="__main__":main()
