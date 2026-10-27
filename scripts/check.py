#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Check that skills/ is exactly what scripts/sync.py last wrote.

- every folder in skills/ has an entry in skills.lock.json, and every entry a folder
- each folder's content digest matches the lock, so nothing was edited by hand
- no entry was synced from uncommitted upstream changes
- each skill's frontmatter name equals its folder name and starts with the prefix
- the plugin marketplace is the one the sync writes for this lock

The format of each skill is checked separately, with skills-ref (see CI).

    uv run scripts/check.py
"""

import json
import sys

from sync import LOCK, MARKETPLACE, SKILLS, digest, frontmatter, marketplace

PREFIX = "dcp-"


def problems():
    full = json.loads(LOCK.read_text())
    lock = full["skills"]
    if not MARKETPLACE.exists() or json.loads(MARKETPLACE.read_text()) != marketplace(full):
        yield f"{MARKETPLACE.relative_to(MARKETPLACE.parent.parent)}: out of date; run the sync"
    folders = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    for name in sorted(folders - set(lock)):
        yield f"skills/{name}: not in skills.lock.json; skills are added by scripts/sync.py, not by hand"
    for name in sorted(set(lock) - folders):
        yield f"skills/{name}: in skills.lock.json but missing"
    for name in sorted(folders & set(lock)):
        entry = lock[name]
        if digest(SKILLS / name) != entry["digest"]:
            yield (f"skills/{name}: differs from what was synced from {entry['path']}; "
                   "change it upstream and sync, rather than editing it here")
        if entry.get("dirty"):
            yield f"skills/{name}: synced from uncommitted upstream changes; sync again from a commit"
        declared = frontmatter(SKILLS / name).get("name")
        if declared != name:
            yield f"skills/{name}: frontmatter name is {declared!r}, not the folder name"
        if not name.startswith(PREFIX):
            yield f"skills/{name}: name does not start with {PREFIX!r}"


def main():
    found = list(problems())
    for problem in found:
        print(problem, file=sys.stderr)
    if found:
        sys.exit(1)
    print("skills/ matches skills.lock.json")


if __name__ == "__main__":
    main()
