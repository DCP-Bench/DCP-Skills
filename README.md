# DCP skills

[![skills.sh](https://skills.sh/b/DCP-Bench/skills)](https://skills.sh/DCP-Bench/skills)
[![Checks](https://github.com/DCP-Bench/skills/actions/workflows/checks.yml/badge.svg)](https://github.com/DCP-Bench/skills/actions/workflows/checks.yml)
<!-- badges:start -->
[![solvers: 29](https://img.shields.io/badge/solvers-29-blue)](#catalog) [![paradigms: 8](https://img.shields.io/badge/paradigms-8-blue)](#catalog) [![languages: 11](https://img.shields.io/badge/languages-11-blue)](#catalog) [![updated: 2026-10-27](https://img.shields.io/badge/updated-2026--10--27-blue)](skills.lock.json)
<!-- badges:end -->

A collection of general purpose [agent skills](https://agentskills.io) for constraint (optimisation) solvers. 

One skill per solver, covering how to **install** it, **model** with it in (potentially multiple language interfaces),
**solve** a model, and read the **results**. The skills are generated as part of the [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta) project, and get evaluated on [DCP-Bench](https://github.com/DCP-Bench). 

This repository is a read-only mirror.


## Install

With the [skills CLI](https://skills.sh), for Claude Code, Codex, Cursor and other agents:

```console
npx skills add DCP-Bench/skills                    # pick from the list
npx skills add DCP-Bench/skills --skill dcp-cpmpy  # one skill
```

In Claude Code, as a plugin holding all the skills:

```console
/plugin install dcp-solvers --marketplace DCP-Bench/skills
```

Or copy a folder from `skills/` into your agent's skills directory, for example
`.agents/skills/` or `.claude/skills/`.

## Tracking origin

[`skills.lock.json`](skills.lock.json) records, for each skill, the upstream repository, its path there, the last upstream commit that changed it, and a digest of its content. `scripts/sync.py` writes the lock; nobody edits it, or `skills/`, by hand.

## Contributing

Report problems with a skill, and propose changes to one, in [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/issues). Changes reach this repository with the next sync. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Catalog

<!-- catalog:start -->
### Constraint programming (CP)

| Skill | Interfaces | What it covers | Source |
| --- | --- | --- | --- |
| [`dcp-choco`](skills/dcp-choco/) | java, python | Choco, an open-source constraint programming solver with integer, Boolean and set variables, a large catalogue of global constraints (all different, cumulative, table, circuit, regular and more), reification and optimisation, used from Java (choco-solver) or Python (pychoco, no Java install needed). | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/choco/skills/dcp-choco) |
| [`dcp-chuffed`](skills/dcp-chuffed/) | cpp | Chuffed, a lazy clause generation constraint programming solver, used directly from C++ through its native API (Problem subclass, IntVar/BoolView, int_linear, all_different, cumulative, branch, optimize, engine.solve), built with CMake. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/chuffed/skills/dcp-chuffed) |
| [`dcp-cpmpy`](skills/dcp-cpmpy/) | python | CPMpy is a Python constraint modelling library for constraint programming and optimisation, solved by OR-Tools CP-SAT by default (Python package cpmpy). | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/cpmpy/skills/dcp-cpmpy) |
| [`dcp-essence-prime`](skills/dcp-essence-prime/) | essence_prime | Essence' constraint modelling language run with Savile Row and its bundled Minion CP solver (given/find/letting, matrices, globals, minimising/maximising, .param files, solution files, -all-solutions, branching). | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/essence_prime/skills/dcp-essence-prime) |
| [`dcp-gecode`](skills/dcp-gecode/) | cpp | Gecode, a propagation-based constraint programming solver with a large library of global constraints, propagation levels and DFS/BAB search, used from C++ (gecode/int.hh, minimodel.hh, search.hh) with Space subclasses. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/gecode/skills/dcp-gecode) |
| [`dcp-huub`](skills/dcp-huub/) | rust | Huub, a constraint programming solver written in Rust (crate huub 100.1.0) that uses lazy clause generation, with integer and Boolean decision variables, linear, element, table, cumulative and disjunctive constraints, and proven optimisation. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/huub/skills/dcp-huub) |
| [`dcp-maxicp`](skills/dcp-maxicp/) | java | MaxiCP, a constraint programming solver from UCLouvain with integer and Boolean variables, global constraints, interval variables for scheduling, depth-first search, optimisation and solution enumeration, used from Java (org.maxicp:maxicp) through its raw API. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/maxicp/skills/dcp-maxicp) |
| [`dcp-minizinc`](skills/dcp-minizinc/) | minizinc | MiniZinc constraint modelling language solved by the Gecode constraint solver, from the command line or the minizinc-python API (package minizinc). | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/minizinc/skills/dcp-minizinc) |
| [`dcp-ortools-cp-sat`](skills/dcp-ortools-cp-sat/) | cpp, python | OR-Tools CP-SAT, Google's constraint programming and integer optimisation solver (propagation with clause learning), used from C++ (CpModelBuilder) or Python (ortools.sat.python.cp_model). | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/2df816fb3fd81ec6f63cd535bd8a9e0930af5233/solvers/ortools_cp_sat/skills/dcp-ortools-cp-sat) |
| [`dcp-picat`](skills/dcp-picat/) | picat | Picat, a logic-based language whose constraint modules cp and sat solve finite-domain and SAT-encoded problems. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/picat/skills/dcp-picat) |
| [`dcp-pumpkin`](skills/dcp-pumpkin/) | rust | Pumpkin, a constraint solver written in Rust (crate pumpkin-solver 0.5.0) with lazy clause generation, integer and Boolean variables, linear and global constraints, and proven optimisation. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/b41240bbcc285b7e6ce8fb548e99b179a1789fce/solvers/pumpkin/skills/dcp-pumpkin) |
| [`dcp-pycsp3`](skills/dcp-pycsp3/) | python | PyCSP3 is a Python library (pip package and import pycsp3) that compiles constraint models to XCSP3; the ACE solver ships inside the wheel as a Java jar and solves them. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/pycsp3/skills/dcp-pycsp3) |

### Constraint logic programming (CLP)

| Skill | Interfaces | What it covers | Source |
| --- | --- | --- | --- |
| [`dcp-eclipse`](skills/dcp-eclipse/) | prolog | ECLiPSe, the ECLiPSe Constraint Logic Programming system (version 7.x), used through its native Prolog interface (eclipse launcher, .ecl files), for finite-domain constraint satisfaction and optimisation in Prolog syntax with libraries ic, ic_global, gfd (Gecode), branch_and_bound and timeout. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/eclipse/skills/dcp-eclipse) |
| [`dcp-swipl`](skills/dcp-swipl/) | prolog | SWI-Prolog CLP(FD), the finite-domain constraint solver in library(clpfd) of SWI-Prolog 9.x, for constraint satisfaction and optimisation in Prolog. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/swipl/skills/dcp-swipl) |

### Boolean satisfiability (SAT)

| Skill | Interfaces | What it covers | Source |
| --- | --- | --- | --- |
| [`dcp-paramita`](skills/dcp-paramita/) | python | Paramita SAT and MaxSAT framework, used from Python (paramita 1.2.0) - Bool variables, propositional operators and pseudo-Boolean constraints from paramita.modelling, integers encoded as Booleans, satisfiability and all-solutions enumeration with CaDiCaL, and optimisation as MaxSAT with EvalMaxSAT2022. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/paramita/skills/dcp-paramita) |
| [`dcp-pysat`](skills/dcp-pysat/) | python | PySAT (python-sat), a Python library for SAT and MaxSAT modelling with CNF and WCNF formulas, cardinality and pseudo-Boolean encoders, finite-domain integers (pysat.integer), SAT solvers such as Glucose, and the RC2 MaxSAT solver. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/pysat/skills/dcp-pysat) |

### Satisfiability modulo theories (SMT)

| Skill | Interfaces | What it covers | Source |
| --- | --- | --- | --- |
| [`dcp-cvc5`](skills/dcp-cvc5/) | python | cvc5, an SMT solver used for finite-domain combinatorial models, from Python (pip package cvc5, module cvc5.pythonic, Z3-style). | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/cvc5/skills/dcp-cvc5) |
| [`dcp-idp-z3`](skills/dcp-idp-z3/) | idp | IDP-Z3, a reasoning engine for FO(.) ("FO-dot") knowledge bases (vocabulary, theory, structure) built on Z3; pip package idp-engine, Python module idp_engine, command idp-engine. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/idp_z3/skills/dcp-idp-z3) |
| [`dcp-z3`](skills/dcp-z3/) | python | Z3, an SMT solver with a Python API (pip package z3-solver, import z3) for integer, Boolean and array constraints, satisfiability checks, optimisation and solution enumeration. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/z3/skills/dcp-z3) |

### Mixed integer programming (MIP)

| Skill | Interfaces | What it covers | Source |
| --- | --- | --- | --- |
| [`dcp-docplex`](skills/dcp-docplex/) | python | DOcplex (docplex.mp), the Python modelling API of IBM CPLEX, for mixed-integer linear models with integer, binary and continuous variables, linear, indicator and logical constraints, optimisation and enumeration of solutions. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/docplex/skills/dcp-docplex) |
| [`dcp-gurobi`](skills/dcp-gurobi/) | python | Gurobi, a solver for linear, mixed-integer and indicator-constrained optimisation models (branch-and-cut), used from Python (gurobipy). | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/gurobi/skills/dcp-gurobi) |
| [`dcp-highs`](skills/dcp-highs/) | cpp | HiGHS, a mixed-integer linear programming solver, used from C++ through its Highs class (built from source), covering columns and rows, integrality, objective, run(), model status, and enumerating solutions with no-goods. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/highs/skills/dcp-highs) |
| [`dcp-jump`](skills/dcp-jump/) | julia | JuMP, the Julia modelling language for optimisation, with HiGHS as its mixed-integer linear programming solver (Julia, packages JuMP and HiGHS.jl). | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/2df816fb3fd81ec6f63cd535bd8a9e0930af5233/solvers/jump/skills/dcp-jump) |
| [`dcp-pulp`](skills/dcp-pulp/) | python | PuLP, a modelling library for linear and mixed-integer programs solved by the CBC solver it bundles, used from Python (PuLP 3.x). | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/pulp/skills/dcp-pulp) |
| [`dcp-python-mip`](skills/dcp-python-mip/) | python | Python-MIP (import mip), a Python library for linear and mixed-integer programs, solved by its default solver CBC. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/python_mip/skills/dcp-python-mip) |
| [`dcp-scip`](skills/dcp-scip/) | python | SCIP, a branch-and-cut mixed-integer and nonlinear solver with native general constraints (and/or/xor, indicator, cardinality, SOS, cumulative, nonlinear), used from Python (PySCIPOpt, pip package and import `pyscipopt`). | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/scip/skills/dcp-scip) |

### Answer set programming (ASP)

| Skill | Interfaces | What it covers | Source |
| --- | --- | --- | --- |
| [`dcp-clingo`](skills/dcp-clingo/) | asp | clingo, an answer set programming (ASP) system. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/clingo/skills/dcp-clingo) |

### Maximum satisfiability (MaxSAT)

| Skill | Interfaces | What it covers | Source |
| --- | --- | --- | --- |
| [`dcp-hermax`](skills/dcp-hermax/) | python | hermax is a MaxSAT modelling library (hermax.model.Model over PySAT) with Boolean and integer variables, hard constraints, weighted soft clauses for minimise and maximise, and solution enumeration. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/hermax/skills/dcp-hermax) |

### Pseudo-Boolean (PB)

| Skill | Interfaces | What it covers | Source |
| --- | --- | --- | --- |
| [`dcp-exact`](skills/dcp-exact/) | python | Exact, a pseudo-Boolean and integer linear solver with Python bindings (package exact, import exact, class Exact) that builds models from named integer and 0/1 variables, linear constraints, reification and multiplication. | [DCP-Rosetta](https://github.com/DCP-Bench/DCP-Rosetta/tree/8356c30bf653991ea7a1321454340cd17bdd5a92/solvers/exact/skills/dcp-exact) |
<!-- catalog:end -->

## License

The skills are licensed as stated in each skill's `license` field. Everything else in this
repository is licensed under [Apache-2.0](LICENSE).
