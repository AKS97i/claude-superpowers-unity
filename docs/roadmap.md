# Roadmap

This roadmap optimizes for **real-world impact first**: the highest-frequency, broadest-audience pains ship before specialist tools. Reasoning for the ordering is in [catalog.md](catalog.md#ranking-by-real-world-impact).

> Versioning follows [SemVer](versioning.md). `v1.0.0` is a defined quality bar, not a calendar date.

## Milestones

### M0 — Foundation · `v0.1` ✅
The repository becomes a credible, contributable open-source project.

- Vision, philosophy, goals.
- Governance: README, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG.
- Docs: roadmap, naming conventions, versioning, authoring guide, testing strategy, glossary, ecosystem blueprint, catalog.
- Templates for `DESIGN.md` / `SKILL.md` / `prompt.md` / evals.
- GitHub community files (issue forms, PR template, CI validation).
- `showcases/` directory.
- **Unity Debugging Expert** shipped as `beta` (all three files, references, example, evals).

### M1 — Hardening · `v0.2`
Prove the quality model on the first Superpower.

- Expand Unity Debugging Expert evals and worked examples.
- Capture real showcase media.
- Promote Unity Debugging Expert → `stable`.
- Finalize CI eval harness conventions.

### M2 — Core triad · `v0.3`
Ship the three highest-frequency pains after debugging.

- **Unity C# Code Review** (P0)
- **Performance Optimization Strategist** (P0)
- **Platform Build Troubleshooter** (P1)

### M3 — Breadth · `v0.4 – v0.6`
One flagship Superpower per remaining category, prioritizing P1s:

- Profiler Analysis Expert, GC / Allocation Eliminator, Mobile Performance Optimizer, Version Control Hygiene Advisor (v0.4)
- Architecture Advisor, Build Size Reducer, Memory Leak Investigator, UI Performance Optimizer (v0.5)
- Netcode for GameObjects Expert, Editor Tool Builder, Addressables System Designer, Render Pipeline Advisor, Test Authoring Expert (v0.6)

### M4 — v1.0 · `v1.0`
The collection becomes a dependable standard.

- ≥ 20 `stable`, eval-backed Superpowers spanning all categories.
- Polished install + showcase gallery.
- Contributor flywheel running (proposals → reviews → merges at a steady cadence).

## Post-1.0 directions

- **Playbooks** — composite workflows chaining multiple Superpowers (e.g. "ship a mobile build" = perf → build-size → platform-troubleshoot).
- **Optional tooling** — helper scripts (log parsers), and later Unity-MCP / editor hooks for live inspection. Always additive, never required.
- **Skill system plugin packaging** — once the plugin ecosystem stabilizes, distribute as an installable plugin/marketplace. Deliberately out of scope until then.
- **Ecosystem siblings** — `superpowers-{web,qa,game-design,backend,devops}` sharing this architecture. See [ecosystem.md](ecosystem.md).
- **Localization & multi-tool exports** once core Superpowers are stable.

## How priorities are decided

`impact ≈ frequency of need × audience breadth × severity of pain × how poorly generic AI handles it unaided`

This is why debugging, performance, review, and build troubleshooting lead, while specialist rendering/netcode systems (high ceiling, narrower audience) follow. Full ranking and rationale: [catalog.md](catalog.md#ranking-by-real-world-impact).
