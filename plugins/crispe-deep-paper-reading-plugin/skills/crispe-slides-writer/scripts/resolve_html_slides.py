#!/usr/bin/env python3
"""Resolve an external html-slides definition; never install or modify it."""
import argparse
import hashlib
import json
from pathlib import Path


def resolve(explicit=None):
    candidates=[Path(explicit).expanduser()] if explicit else []
    candidates += [Path.cwd()/".agents/skills/html-slides/SKILL.md",Path.cwd()/".claude/skills/html-slides/SKILL.md",Path.home()/".agents/skills/html-slides/SKILL.md",Path.home()/".claude/skills/html-slides/SKILL.md"]
    for path in candidates:
        if path.is_dir():path=path/"SKILL.md"
        if path.is_file():
            source=path.read_text()
            if "name: html-slides" not in source:continue
            return {"name":"html-slides","path":str(path.resolve()),"sha256":hashlib.sha256(source.encode()).hexdigest(),"runtime":"reveal.js","status":"definition-readable"}
    raise ValueError("html-slides not found. Load from the host registry/configured roots or review an immutable claude-office-skills/skills checkout and installer before explicit setup")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--path");args=parser.parse_args()
    try:print(json.dumps(resolve(args.path),indent=2))
    except ValueError as exc:parser.exit(1,str(exc)+"\n")
