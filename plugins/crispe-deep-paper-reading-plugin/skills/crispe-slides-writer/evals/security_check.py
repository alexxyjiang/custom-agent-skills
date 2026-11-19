#!/usr/bin/env python3
"""Local security regressions; does not emulate or claim a Snyk rating."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

SKILLS=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("exporter",SKILLS/"crispe-slides-to-pdf/scripts/export_pdf.py")
exporter=importlib.util.module_from_spec(spec);spec.loader.exec_module(exporter)

class DeckServerSecurity(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory()
        self.root=Path(self.folder.name)
        self.deck=self.root/"deck.html";self.deck.write_text("<html>selected deck</html>")
        (self.root/"secret.txt").write_text("must not be served")
        (self.root/"secret-link.html").symlink_to(self.root/"secret.txt")
        self.server,self.thread,self.url=exporter.deck_server(self.deck)
        self.origin=f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join()
        self.folder.cleanup()

    def denied(self,url,headers=None):
        with self.assertRaises(HTTPError) as caught:urlopen(Request(url,headers=headers or {}))
        self.assertEqual(caught.exception.code,404)

    def test_selected_bytes_and_csp(self):
        self.deck.write_text("changed after snapshot")
        with urlopen(self.url+"?print-pdf=") as response:
            self.assertEqual(response.read(),b"<html>selected deck</html>")
            csp=response.headers["Content-Security-Policy"]
            self.assertIn("connect-src 'none'",csp)
            self.assertIn("frame-src 'none'",csp)
            self.assertEqual(response.headers["Cache-Control"],"no-store")

    def test_no_directory_or_sibling_access(self):
        prefix=self.url.rsplit("/",1)[0]
        for path in [self.origin+"/",self.origin+"/deck.html",self.origin+"/secret.txt",prefix+"/secret.txt",prefix+"/secret-link.html",prefix+"/../secret.txt",prefix+"/%2e%2e/secret.txt",prefix+"/%2fsecret.txt"]:
            with self.subTest(path=path):self.denied(path)

    def test_reject_rebound_host(self):
        self.denied(self.url,{"Host":"attacker.invalid"})

    def test_local_links_confined_to_html_siblings(self):
        sibling=self.root/"other.html";sibling.write_text('<section id="slide-known"></section>')
        self.assertEqual(exporter.local_link(self.deck,urlparse("http://localhost/token/other.html#slide-known")),sibling.resolve())
        for value in ["http://localhost/token/secret.txt","http://localhost/token/secret-link.html","http://localhost/token/other.html#missing"]:
            with self.subTest(value=value),self.assertRaises(ValueError):exporter.local_link(self.deck,urlparse(value))


class BrowserIsolationSecurity(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("pypdf") and importlib.util.find_spec("playwright"), "Requires existing export dependencies")
    def test_output_must_not_overwrite_input_or_follow_symlink(self):
        from argparse import Namespace
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);source=root/"deck.html";source.write_text("original")
            args=Namespace(source=str(source),output=source,overwrite=True,allow_remote=False,chrome=None,timeout=1000)
            with self.assertRaisesRegex(ValueError,"overwrite source"):
                exporter.export(args)
            target=root/"protected.pdf";target.write_bytes(b"original pdf")
            link=root/"output.pdf";link.symlink_to(target);args.output=link
            with self.assertRaisesRegex(ValueError,"symlink"):
                exporter.export(args)
            self.assertEqual(source.read_text(),"original")
            self.assertEqual(target.read_bytes(),b"original pdf")

    @unittest.skipUnless(importlib.util.find_spec("playwright"), "Browser regression requires existing Playwright")
    def test_deck_cannot_read_siblings_or_send_network(self):
        from playwright.sync_api import sync_playwright
        import http.server
        import threading
        from argparse import Namespace
        requests=[]
        class Receiver(http.server.BaseHTTPRequestHandler):
            def log_message(self,*_):pass
            def do_GET(self):
                requests.append(self.path);self.send_response(200);self.end_headers()
        sink=http.server.ThreadingHTTPServer(("127.0.0.1",0),Receiver)
        worker=threading.Thread(target=sink.serve_forever,daemon=True);worker.start()
        try:
            with tempfile.TemporaryDirectory() as folder, sync_playwright() as pw:
                root=Path(folder);(root/"secret.txt").write_text("private")
                deck=root/"deck.html"
                deck.write_text("""<script>
                window.probes=[];
                for(const target of ['secret.txt','/secret.txt','http://127.0.0.1:PORT/exfil']){
                    fetch(target).then(r=>r.text()).then(t=>probes.push(t)).catch(()=>probes.push('blocked'));
                }
                const image=new Image();image.src='http://127.0.0.1:PORT/image';
                </script>""".replace("PORT",str(sink.server_port)))
                server,thread,url=exporter.deck_server(deck)
                try:
                    browser=pw.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",headless=True,chromium_sandbox=True)
                    page=browser.new_page();page.goto(url);page.wait_for_function("probes.length===3")
                    self.assertEqual(page.evaluate("probes"),['blocked']*3)
                    self.assertEqual(requests,[])
                    browser.close()
                finally:server.shutdown();server.server_close();thread.join()
                args=Namespace(source="https://example.invalid/deck.html",output=root/"out.pdf",overwrite=False,allow_remote=False,chrome=None,timeout=1000)
                with self.assertRaisesRegex(ValueError,"explicitly pass --allow-remote"):
                    exporter.export(args)
        finally:sink.shutdown();sink.server_close();worker.join()

if __name__=="__main__":unittest.main()
