#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Name the next catalog release and write its notes.

Releases are CalVer tags, vYYYY.MM.N (N counts from 0 within the month). The
notes list the skills added, changed and removed since the previous release, by
comparing skills.lock.json at that tag with the current one. Prints the tag, or
exits with an error when nothing changed since the previous release.

    uv run scripts/release.py --notes notes.md
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

from sync import LOCK, ROOT, git, summary

EMPTY = {"schema": 1, "sources": {}, "skills": {}}


def releases():
    tags = git(ROOT, "tag", "--list", "v*", "--sort=-creatordate").split()
    return [tag for tag in tags if re.fullmatch(r"v\d{4}\.\d{2}\.\d+", tag)]


def next_tag(previous, today):
    month = f"v{today:%Y.%m}."
    used = [int(tag.removeprefix(month)) for tag in previous if tag.startswith(month)]
    return f"{month}{max(used) + 1 if used else 0}"


def changes(old, new):
    before, after = old["skills"], new["skills"]
    return {"added": sorted(set(after) - set(before)),
            "changed": sorted(name for name in set(after) & set(before)
                              if after[name]["digest"] != before[name]["digest"]),
            "removed": sorted(set(before) - set(after))}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--notes", type=Path, required=True, help="where to write the release notes")
    args = parser.parse_args()
    previous = releases()
    old = json.loads(git(ROOT, "show", f"{previous[0]}:skills.lock.json")) if previous else EMPTY
    new = json.loads(LOCK.read_text())
    diff = changes(old, new)
    if not any(diff.values()):
        sys.exit(f"nothing changed since {previous[0]}")
    since = f"Changes since [{previous[0]}](../../releases/tag/{previous[0]}).\n\n" if previous else "First release.\n\n"
    args.notes.write_text(since + summary(old, new, diff))
    print(next_tag(previous, datetime.date.today()))


if __name__ == "__main__":
    main()
