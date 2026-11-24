#!/usr/bin/env python3
"""Verify exact reuse and impact invalidation using an existing deck, in a private copy."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site",type=Path)
    parser.add_argument("--deck",required=True)
    parser.add_argument("--slide",required=True)
    args=parser.parse_args()
    script=Path(__file__).resolve().parents[1]/"scripts/verify_site.py"
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder);site=root/"site";shutil.copytree(args.site,site);cache=root/"cache.json"
        reports=[]
        def run(level="content",extra=(),expected="passed"):
            command=[sys.executable,"-B",str(script),str(site),"--level",level,"--cache",str(cache)]
            if level=="content":command += ["--deck",args.deck,"--slide",args.slide]
            result=subprocess.run(command+list(extra),capture_output=True,text=True)
            if not cache.with_suffix(".report.json").is_file():raise AssertionError(result.stderr)
            report=json.loads(cache.with_suffix(".report.json").read_text())
            assert report["status"]==expected,(result.stdout,result.stderr)
            assert result.returncode==(0 if expected=="passed" else 1)
            reports.append({k:report[k] for k in ["status","effective_level","seconds","executed","reused"]})
            return report
        assert run("layout")["executed"]>0
        assert run("layout")["reused"]>0
        assert run()["effective_level"]=="content"
        assert run()["reused"]==1
        deck=site/args.deck
        source=deck.read_text()
        # Append an inert text comment: changes bytes without changing JS/CSS or geometry.
        deck.write_text(source.replace("</body>","<!-- content revision --> </body>",1))
        assert run()["executed"]==1
        deck.write_text(deck.read_text().replace("</style>","/* changed shared runtime */</style>",1))
        assert run()["effective_level"]=="layout"
        assert run(extra=["--fresh"])["executed"]==1
        # Impossible content must fail, even when a previous revision passed.
        marker='id="'+args.slide+'"'
        current=deck.read_text();index=current.index(marker);body=current.index('<div class="slide-body">',index)
        current=current[:body]+current[body:].replace('<div class="slide-body">','<div class="slide-body"><p style="width:10000px;height:10000px">Deliberate overflow</p>',1)
        deck.write_text(current)
        assert run(expected="failed")["executed"]==1
        assert run(expected="failed")["executed"]==1
        print(json.dumps({"status":"passed","scenarios":["exact reuse","content change invalidation","shared runtime promotion","fresh bypass","overflow rejection","failed checks never reused"],"runs":reports},indent=2))

if __name__=="__main__":main()
