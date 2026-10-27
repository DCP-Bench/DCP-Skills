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

To run the sync locally against a checkout of the source:

```console
uv run scripts/sync.py --local dcp-rosetta=../DCP-Rosetta
```

Without `--local`, the script clones the source from GitHub. A skill synced from
uncommitted upstream changes is marked `"dirty": true` in the lock. Don't merge such a sync.

## Adding a source

Add `sources/<id>.yml`, using [`sources/dcp-rosetta.yml`](sources/dcp-rosetta.yml) as the
template. Skill names must be unique across all sources and start with `dcp-`.
