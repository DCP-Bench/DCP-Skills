# Contributing

This repository mirrors skills that are maintained elsewhere. Where a change goes depends on
what it is.

| You want to | Go to |
| --- | --- |
| Fix or improve a skill, or report a problem with one | The source repository named in the skill's Source column, for now [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta) |
| Add a solver | DCP-Rosetta: follow its `skills/solver-setup` |
| Change how the mirror works: sync, checks, catalog, packaging | This repository |

## How the mirror works

- `sources/<id>.yml` names an upstream repository, the branch to follow, and globs for the
  skill folders it publishes. Folders it leaves out are listed under `exclude`, each with a
  reason.
- `scripts/sync.py` clones each source and copies every matched folder verbatim to
  `skills/<folder name>/`. It removes skills that disappeared upstream, refusing to remove more
  than 5 at once. It then rewrites `skills.lock.json` and the badges and catalog in `README.md`.
- Because the lock holds no timestamps, rerunning the sync with nothing new upstream changes
  nothing.

`make` lists the commands. CI runs the same ones.

```console
make sync                                # clone the sources from GitHub and mirror them
make sync LOCAL=dcp-rosetta=../DCP-Rosetta   # or mirror a local checkout
make check                               # skills/ matches the lock, and every skill follows the spec
make links                               # internal links and anchors (needs Docker)
```

A skill synced from uncommitted upstream changes is marked `"dirty": true` in the lock, and
`make check` fails on it.

## Automatic sync

Every push to DCP-Rosetta's main starts `sync.yml` here: Rosetta's `mirror-skills.yml` sends
a `repository_dispatch`, using its `SKILLS_MIRROR_TOKEN` secret. `sync.yml` also runs daily, in
case a dispatch went missing, and on demand from the Actions tab.

When upstream changed, the sync runs the same checks as `checks.yml` and pushes the result
straight to main, with no pull request. Its commit, by `github-actions[bot]`, links each
changed skill to its upstream diff. A sync that fails its checks pushes nothing; the failed
run shows which skill to fix upstream, and the next push there retries.

## Checks

- **`checks.yml`** runs on every PR and every push to main. It fails when:
  - `skills/` differs from `skills.lock.json`: a folder was edited, added or removed by hand
  - a skill doesn't pass [`skills-ref validate`](https://github.com/agentskills/agentskills)
  - a skill's name doesn't match its folder or lacks the `dcp-` prefix
  - an internal link or anchor is broken
- **`links.yml`** checks external links weekly and opens an issue for broken ones.

Each link check writes its report, the lychee table with a note on what was checked and
how to read it, to the run's summary page; `links.yml` also puts it in the issue. The
note comes from `scripts/link-report.sh`.

A failing skill is fixed upstream, then synced.

## Adding a source

Add `sources/<id>.yml`, using [`sources/dcp-rosetta.yml`](sources/dcp-rosetta.yml) as the
template. Skill names must be unique across all sources and start with `dcp-`.

## Releases

`main` is always installable, and installs follow it. To give users a fixed point to pin,
run the Release workflow from the Actions tab. It tags `main` as `vYYYY.MM.N` (CalVer, with
N counting from 0 within the month). The release notes list the skills added, changed and
removed since the previous release, each linked to its upstream diff. A skill has no version
of its own; `skills.lock.json` at a tag says exactly which upstream commit each skill came
from.
