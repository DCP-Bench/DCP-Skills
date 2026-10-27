# DCP-Bench skills

[Agent skills](https://agentskills.io) for constraint and optimisation solvers: one skill per
solver, covering how to install it, model with it from each of its language interfaces,
solve, and read the results. Each skill comes with runnable examples under `assets/`.

The skills are written and tested in [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta),
where each one is used to generate and verify models for the
[DCP-Bench](https://github.com/DCP-Bench) problems. This repository is a read-only mirror
of them, flattened into `skills/` so that skill tools can find them.

## Install

With the [skills CLI](https://skills.sh), for Claude Code, Codex, Cursor and other agents:

```console
npx skills add DCP-Bench/skills                    # pick from the list
npx skills add DCP-Bench/skills --skill dcp-cpmpy  # one skill
```

Or copy a folder from `skills/` into your agent's skills directory, for example
`.agents/skills/` or `.claude/skills/`.

Every skill name starts with `dcp-`. Skills have no namespaces, and the prefix keeps these
apart from a solver's own official skill of the same name.

## Where a skill comes from

[`skills.lock.json`](skills.lock.json) records, for each skill, the upstream repository,
its path there, the last upstream commit that changed it, and a digest of its content. The
Source column below links to that exact commit. `scripts/sync.py` writes the lock; nobody
edits it, or `skills/`, by hand.

## Contributing

Report problems with a skill, and propose changes to one, in
[DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/issues). Changes reach this
repository with the next sync. Issues here are for the mirror itself. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Catalog

<!-- catalog:start -->
<!-- catalog:end -->

## License

The skills are licensed as stated in each skill's `license` field. Everything else in this
repository is licensed under [Apache-2.0](LICENSE).
