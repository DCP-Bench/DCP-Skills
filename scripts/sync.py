#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Mirror the skills of the upstream repositories listed in sources/ into skills/.

For every sources/<id>.yml this clones the repository (or uses a local checkout,
--local <id>=<path>), copies each matched skill folder verbatim to skills/<name>/,
removes the skills of that source that disappeared upstream, and rewrites
skills.lock.json (where each skill came from), the catalog table in README.md and
the plugin marketplace in .claude-plugin/.

Nothing in skills/ is edited by hand: a fix belongs in the upstream repository.
The lock holds no timestamps, so a run with nothing new upstream changes nothing.

    uv run scripts/sync.py                                  # from GitHub
    uv run scripts/sync.py --local dcp-rosetta=../DCP-Rosetta
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
SKILLS = ROOT / "skills"
LOCK = ROOT / "skills.lock.json"
README = ROOT / "README.md"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CATALOG_START, CATALOG_END = "<!-- catalog:start -->", "<!-- catalog:end -->"
# More removals than this in one run is more likely a broken source than a real
# change upstream; it needs --allow-removals.
MAX_REMOVALS = 5


class SyncError(Exception):
    pass


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def digest(folder):
    """sha256 over the sorted `path\\0sha256(content)` lines of every file in a folder."""
    lines = sorted(f"{path.relative_to(folder).as_posix()}\0{hashlib.sha256(path.read_bytes()).hexdigest()}\n"
                   for path in folder.rglob("*") if path.is_file())
    return "sha256:" + hashlib.sha256("".join(lines).encode()).hexdigest()


def frontmatter(skill):
    match = re.match(r"---\n(.*?)\n---\n", (skill / "SKILL.md").read_text(encoding="utf-8"), re.DOTALL)
    return yaml.safe_load(match.group(1)) if match else {}


def checkout(source_id, config, local, scratch):
    """The repository to read a source from: the local path given for it, or a clone
    of its ref holding only the folders the source needs."""
    if source_id in local:
        return Path(local[source_id]).resolve()
    repo = scratch / source_id
    git(scratch, "clone", "--quiet", "--filter=blob:none", "--no-checkout", "--branch", config.get("ref", "main"),
        f"https://github.com/{config['repo']}.git", str(repo))
    patterns = [f"/{glob}/" for glob in config["include"]] + ([f"/{config['paradigms']}"] if config.get("paradigms") else [])
    git(repo, "sparse-checkout", "set", "--no-cone", *patterns)
    git(repo, "checkout", "--quiet")
    return repo


def read_source(source_id, config, repo):
    """The skill folders a source publishes, as {name: (path in repo, tracked files)},
    and the source's own lock entry."""
    excluded = {entry["path"].rstrip("/") for entry in config.get("exclude") or []}
    found = {}
    for glob in config["include"]:
        for folder in sorted(repo.glob(glob)):
            path = folder.relative_to(repo).as_posix()
            if path in excluded or not (folder / "SKILL.md").is_file():
                continue
            if folder.name in found:
                raise SyncError(f"{source_id}: two skills named {folder.name}: {found[folder.name][0]} and {path}")
            files = git(repo, "ls-files", "-z", "--", path).split("\0")
            found[folder.name] = (path, [Path(file).relative_to(path) for file in files if file])
    for path in excluded - {path for path, _ in found.values()}:
        if not (repo / path).is_dir():
            print(f"warning: {source_id}: excluded path {path} no longer exists", file=sys.stderr)
    # The last commit that touched what is published, not HEAD: the source moves on
    # without its skills changing, and that must not change the lock.
    paths = list(config["include"]) + ([config["paradigms"]] if config.get("paradigms") else [])
    entry = {"repo": config["repo"], "ref": config.get("ref", "main"),
             "commit": git(repo, "log", "-1", "--format=%H", "--", *paths).strip()}
    if git(repo, "status", "--porcelain", "--", *paths).strip():
        entry["dirty"] = True
    return found, entry


def skill_entry(source_id, repo, path):
    last = git(repo, "log", "-1", "--format=%H %cs", "--", path).split()
    entry = {"source": source_id, "path": path,
             "commit": last[0] if last else None, "commit_date": last[1] if last else None}
    if git(repo, "status", "--porcelain", "--", path).strip():
        entry["dirty"] = True
    return entry


def copy_skill(repo, path, files, name):
    target = SKILLS / name
    if target.exists():
        shutil.rmtree(target)
    for file in files:
        (target / file).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repo / path / file, target / file)
    return digest(target)


def first_sentence(text):
    # A sentence ends at a full stop followed by a capital, so "e.g. pychoco" does not end one.
    return re.split(r"(?<=\.)\s+(?=[A-Z])", " ".join(text.split()))[0]


def catalog(lock, labels):
    """The README catalog: one table per paradigm, in the order the sources name them."""
    groups = {}
    for name, entry in sorted(lock["skills"].items()):
        meta = frontmatter(SKILLS / name).get("metadata") or {}
        groups.setdefault(meta.get("paradigm", "other"), []).append((name, entry, meta))
    order = [paradigm for paradigm in labels if paradigm in groups] + sorted(set(groups) - set(labels))
    parts = []
    for paradigm in order:
        rows = ["| Skill | Interfaces | What it covers | Source |", "| --- | --- | --- | --- |"]
        for name, entry, meta in groups[paradigm]:
            source = lock["sources"][entry["source"]]
            ref = entry["commit"] or source["ref"]
            description = first_sentence(frontmatter(SKILLS / name).get("description", "")).replace("|", "\\|")
            rows.append(f"| [`{name}`](skills/{name}/) | {meta.get('interfaces', '')} | {description} "
                        f"| [{source['repo'].split('/')[-1]}](https://github.com/{source['repo']}/tree/{ref}/{entry['path']}) |")
        parts.append(f"### {labels.get(paradigm, paradigm)}\n\n" + "\n".join(rows))
    return "\n\n".join(parts)


def write_readme(text):
    readme = README.read_text(encoding="utf-8")
    start, end = readme.index(CATALOG_START) + len(CATALOG_START), readme.index(CATALOG_END)
    README.write_text(f"{readme[:start]}\n{text}\n{readme[end:]}", encoding="utf-8")


def marketplace(lock):
    """The Claude Code plugin marketplace: one plugin holding every skill. It has no
    version, so an installed plugin follows this repository's commits."""
    return {
        "name": "dcp-bench",
        "owner": {"name": "DCP-Bench"},
        "metadata": {"description": "Agent skills for constraint and optimisation solvers, from DCP-Bench"},
        "plugins": [{
            "name": "dcp-solvers",
            "description": "One skill per solver: install it, model with it from each of its language "
                           "interfaces, solve, and read the results",
            "source": "./",
            "strict": False,
            "skills": [f"./skills/{name}" for name in sorted(lock["skills"])],
        }],
    }


def sync(local, allow_removals):
    old = json.loads(LOCK.read_text()) if LOCK.exists() else {"schema": 1, "sources": {}, "skills": {}}
    lock = {"schema": 1, "sources": {}, "skills": {}}
    labels, changes = {}, {"added": [], "changed": [], "removed": []}
    with tempfile.TemporaryDirectory() as scratch:
        plans = []
        for config_file in sorted(SOURCES.glob("*.yml")):
            source_id, config = config_file.stem, yaml.safe_load(config_file.read_text())
            repo = checkout(source_id, config, local, Path(scratch))
            found, lock["sources"][source_id] = read_source(source_id, config, repo)
            for name in found:
                if any(name in other for *_, other in plans):
                    raise SyncError(f"{name} is published by more than one source")
            plans.append((source_id, config, repo, found))
            if config.get("paradigms"):
                labels.update({entry["id"]: entry["name"] for entry in json.loads((repo / config["paradigms"]).read_text())})
        published = {name for *_, found in plans for name in found}
        removed = sorted(name for name in old["skills"] if name not in published)
        if len(removed) > MAX_REMOVALS and not allow_removals:
            raise SyncError(f"refusing to remove {len(removed)} skills at once ({', '.join(removed)}); "
                            "check the sources, or pass --allow-removals")

        for source_id, config, repo, found in plans:
            for name, (path, files) in sorted(found.items()):
                entry = skill_entry(source_id, repo, path)
                entry["digest"] = copy_skill(repo, path, files, name)
                lock["skills"][name] = entry
                before = old["skills"].get(name)
                if before is None:
                    changes["added"].append(name)
                elif before["digest"] != entry["digest"]:
                    changes["changed"].append(name)
        for name in removed:
            shutil.rmtree(SKILLS / name, ignore_errors=True)
            changes["removed"].append(name)

    LOCK.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n")
    write_readme(catalog(lock, labels))
    MARKETPLACE.parent.mkdir(exist_ok=True)
    MARKETPLACE.write_text(json.dumps(marketplace(lock), indent=2) + "\n")
    return old, lock, changes


def summary(old, lock, changes):
    """A Markdown account of a sync for its pull request: each change links to the
    upstream diff (or history) of that skill."""
    def link(entry, before=None):
        repo = lock["sources"].get(entry["source"], old["sources"].get(entry["source"], {})).get("repo")
        if before and before.get("commit") and entry.get("commit"):
            return f"https://github.com/{repo}/compare/{before['commit']}...{entry['commit']}"
        return f"https://github.com/{repo}/commits/{entry.get('commit') or 'HEAD'}/{entry['path']}"
    lines = []
    for kind, names in changes.items():
        if names:
            lines += [f"### {kind.capitalize()}", ""]
            for name in names:
                entry = lock["skills"].get(name) or old["skills"][name]
                before = old["skills"].get(name) if kind == "changed" else None
                lines.append(f"- [`{name}`]({link(entry, before)}) from `{entry['path']}`")
            lines.append("")
    sources = ", ".join(f"[{source['repo']}](https://github.com/{source['repo']}/commit/{source['commit']}) "
                        f"at `{source['commit'][:12]}`" for source in lock["sources"].values())
    return "\n".join(lines + [f"Synced from {sources}.", ""])


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--local", action="append", default=[], metavar="ID=PATH",
                        help="read source ID from a local checkout instead of cloning it")
    parser.add_argument("--allow-removals", action="store_true",
                        help=f"remove more than {MAX_REMOVALS} skills in one run")
    parser.add_argument("--summary", type=Path, metavar="FILE",
                        help="write a Markdown summary of the changes, and a title as its first line")
    args = parser.parse_args()
    local = dict(item.split("=", 1) for item in args.local)
    try:
        old, lock, changes = sync(local, args.allow_removals)
    except (SyncError, subprocess.CalledProcessError) as error:
        sys.exit(f"sync failed: {getattr(error, 'stderr', None) or error}")
    for kind, names in changes.items():
        if names:
            print(f"{kind}: {', '.join(names)}")
    dirty = [name for name, entry in lock["skills"].items() if entry.get("dirty")]
    if dirty:
        print(f"warning: synced uncommitted upstream changes: {', '.join(dirty)}", file=sys.stderr)
    print(f"{len(lock['skills'])} skills from {len(lock['sources'])} source(s)")
    if args.summary:
        counts = ", ".join(f"{len(names)} {kind}" for kind, names in changes.items() if names) or "no changes"
        args.summary.write_text(f"Sync skills: {counts}\n{summary(old, lock, changes)}")


if __name__ == "__main__":
    main()
