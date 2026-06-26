# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Each Superpower also carries its own version in its `SKILL.md` metadata; this
changelog tracks the collection as a whole. See [docs/versioning.md](docs/versioning.md).

## [Unreleased]

### Added — Hardening (M1, in progress)

- **Unity Debugging Expert evals** expanded from 2 to 10, covering serialization
  rename data-loss, destroyed-object access (`==`/`?.` traps), stale statics under
  disabled Domain Reload, Awake-vs-Start execution order, intermittent/heisenbug
  discipline, object-pool stale state, and two negative-trigger (handoff) boundary cases.
- **Worked example** added: singleton null on the second Play (Enter Play Mode Options).
- **Showcase conversations** (textual): coroutine-respawn diagnosis and the
  vague-"crashes sometimes" honest-intake session, linked from the showcase README.
- **Eval harness conventions finalized:** required per-Superpower `triggers.md`
  (with `templates/triggers.template.md`), and a runnable structural validator
  (`scripts/validate.py`) that checks frontmatter, required files, eval section
  structure, and trigger files — used by CI and runnable locally.
- Authoring guide and testing strategy updated for the finalized conventions.

### Notes

- Unity Debugging Expert remains `beta`. Remaining gate for `stable`: captured
  showcase media and field validation (see
  `showcases/unity-debugging-expert/README.md`). On promotion, bump its `SKILL.md`
  / `DESIGN.md` metadata to `0.2.0` + `stability: stable`.

## [0.1.0] — 2026-06-25

### Added — Foundation (M0)

- Repository vision, philosophy, and goals (`docs/`).
- Flagship `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`.
- Documentation: roadmap, naming conventions, versioning, authoring guide,
  testing strategy, glossary, ecosystem blueprint, and the Superpower catalog
  (61 planned Superpowers across 21 categories).
- Authoring templates: `DESIGN.template.md`, `SKILL.template.md`,
  `prompt.template.md`, `eval.template.md`.
- GitHub community files: 4 issue forms, PR template, and CI workflows
  (structure validation + markdown lint).
- `showcases/` directory for screenshots, GIFs, and example conversations.
- **First Superpower — Unity Debugging Expert** (`beta`): production-ready
  `DESIGN.md`, `SKILL.md`, and `prompt.md`, with references, a worked example,
  and eval cases.

[Unreleased]: https://github.com/AKS97i/claude-superpowers-unity/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AKS97i/claude-superpowers-unity/releases/tag/v0.1.0
