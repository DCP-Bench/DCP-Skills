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
  than 5 at once. It then rewrites `skills.lock.json` and the catalog in `README.md`.
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

## Sync pull requests

`sync.yml` runs daily, and on demand from the Actions tab. When upstream changed, it opens one
pull request on `automated/sync-skills`, or updates the open one. The PR links each changed
skill to its upstream diff. The same checks as `checks.yml` run before the PR is opened.
Review the PR and merge it. A sync that fails its checks opens no PR; the failed run shows
which skill to fix upstream.

## Checks

- **`checks.yml`** runs on every PR and every push to main. It fails when:
  - `skills/` differs from `skills.lock.json`: a folder was edited, added or removed by hand
  - a skill doesn't pass [`skills-ref validate`](https://github.com/agentskills/agentskills)
  - a skill's name doesn't match its folder or lacks the `dcp-` prefix
  - an internal link or anchor is broken
- **`links.yml`** checks external links weekly and opens an issue for broken ones.

A failing skill is fixed upstream, then synced.

## Adding a source

Add `sources/<id>.yml`, using [`sources/dcp-rosetta.yml`](sources/dcp-rosetta.yml) as the
template. Skill names must be unique across all sources and start with `dcp-`.
