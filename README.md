<div align="center">

# 🎮 Claude Superpowers — Unity

<!-- markdownlint-disable-next-line MD001 MD026 -- styled hero subtitle, intentionally h3 with a period -->
### AI Engineering Systems that turn Claude into an elite Unity engineering team.

**Debugging · Code Review · Architecture · Performance · Rendering · Netcode · Build & Ship**

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![Superpowers](https://img.shields.io/badge/superpowers-1%20live%20%2F%2061%20planned-blueviolet.svg)](docs/catalog.md)
[![Status](https://img.shields.io/badge/status-v0.1%20foundation-orange.svg)](docs/roadmap.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Unity](https://img.shields.io/badge/Unity-2021_LTS_→_6-000.svg)](#-compatibility)

*Not a plugin. Not a package. Not an asset.*
*A library of structured engineering methodologies that give Claude the judgment of a senior Unity team.*

</div>

---

## ✨ What is this?

**Claude Superpowers — Unity** is a curated collection of **AI Engineering Systems**: rigorously designed methodologies — investigation pipelines, decision frameworks, review checklists, confidence models, and root-cause workflows — that transform Claude into a specialized Unity expert across the **entire game-development lifecycle**.

Each "Superpower" is **not a prompt**. It is a repeatable engineering system that encodes *how a senior Unity engineer reasons* about a problem, so you get expert-grade help that is consistent, evidence-driven, and teachable.

Every Superpower ships as **three synchronized artifacts**:

| File | What it is | Use it in |
| --- | --- | --- |
| **`SKILL.md`** | A production-ready [Claude Code](https://claude.com/claude-code) Skill with progressive disclosure | Claude Code |
| **`prompt.md`** | A portable, self-contained Markdown prompt | Claude.ai, the API, any LLM |
| **`DESIGN.md`** | The engineering design: methodology, decision trees, confidence model | Humans (learn & contribute) |

> **Philosophy in one line:** we ship *engineering systems*, not prompts. The methodology is the product.

---

## 🚀 Quick start

### In Claude Code (recommended)

```bash
# Clone the collection
git clone https://github.com/AKS97i/claude-superpowers-unity.git

# Make a Superpower available to your project
mkdir -p .claude/skills
cp -R claude-superpowers-unity/superpowers/debugging/unity-debugging-expert .claude/skills/

# Then just describe your Unity bug — Claude invokes the skill automatically.
```

> Prefer it everywhere? Copy into `~/.claude/skills/` to make a Superpower available in every project.

### In Claude.ai, the API, or any other LLM

Open the Superpower's **`prompt.md`**, paste it as your system/context message, then describe your problem. No installation required.

---

## 🧠 Why this exists

Generic AI help for Unity tends to **guess**. It pattern-matches a plausible-looking fix, states it with unearned confidence, and ignores the engine-specific traps (lifecycle order, serialization, domain reload, IL2CPP stripping, prefab identity) that cause most real bugs.

Professional Unity teams don't work that way. They follow **methodology**: reproduce, gather evidence, localize, form ranked hypotheses, test cheaply, confirm root cause, fix minimally, and guard against regressions.

This repository encodes that discipline. Every Superpower:

- 🔬 **Reasons like an expert** — explicit investigation pipelines, not vibes.
- 🎯 **States its confidence** — and what would raise it. No fabricated certainty.
- 🧩 **Stays Unity-aware** — real APIs, Editor windows, log files, version-specific gotchas.
- ✅ **Is testable** — every Superpower ships evals and worked examples.
- 🔁 **Is portable** — works in Claude Code *and* anywhere else.

---

## 🦸 Superpower catalog

**1 live · 61 planned across 21 categories.** Full details, inputs/outputs, and priorities in **[docs/catalog.md](docs/catalog.md)**.

| Category | Flagship Superpower | Status |
| --- | --- | --- |
| 🐞 Debugging | **Unity Debugging Expert** | ✅ Live (v0.1) |
| 🔍 Code Review | Unity C# Code Review | 🗓️ Planned (P0) |
| ⚡ Performance | Performance Optimization Strategist | 🗓️ Planned (P0) |
| 📊 Profiling | Profiler Analysis Expert | 🗓️ Planned (P1) |
| 🧹 Memory | GC / Allocation Eliminator | 🗓️ Planned (P1) |
| 📱 Mobile | Mobile Performance Optimizer | 🗓️ Planned (P1) |
| 🏗️ Architecture | Unity Architecture Advisor | 🗓️ Planned (P1) |
| 📦 Build Systems | Platform Build Troubleshooter | 🗓️ Planned (P1) |
| 🎨 Rendering | Render Pipeline Advisor | 🗓️ Planned (P2) |
| 🌐 Netcode | Netcode for GameObjects Expert | 🗓️ Planned (P2) |
| 🧰 Editor Tooling | Editor Tool Builder | 🗓️ Planned (P2) |
| 🔧 Version Control | Version Control Hygiene Advisor | 🗓️ Planned (P1) |
| …and 10 more categories | | [See the full catalog →](docs/catalog.md) |

---

## 📁 Repository structure

```
claude-superpowers-unity/
├── README.md                 ← you are here
├── CONTRIBUTING.md           ← how to propose & author a Superpower
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── docs/                     ← vision, philosophy, roadmap, conventions, catalog
├── templates/                ← copy-to-create scaffolds (DESIGN/SKILL/prompt/eval)
├── showcases/                ← screenshots, GIFs & example conversations
└── superpowers/              ← the Engineering Systems, grouped by category
    └── debugging/
        └── unity-debugging-expert/
            ├── DESIGN.md     ← the engineering system spec
            ├── SKILL.md      ← Claude Code Skill (progressive disclosure)
            ├── prompt.md     ← portable prompt
            ├── references/   ← deep checklists & heuristics (loaded on demand)
            ├── examples/     ← worked before→after investigations
            └── evals/        ← scenario + rubric test cases
```

> Each Superpower is a **self-contained unit** — design, skill, prompt, references, examples, and tests travel together. Adding a Superpower means adding one folder.

---

## 🗺️ Roadmap

| Milestone | Version | Focus |
| --- | --- | --- |
| **M0 — Foundation** | v0.1 | Repository, docs, templates, community files, **Unity Debugging Expert** |
| **M1 — Hardening** | v0.2 | Evals + examples deepened; Debugging Expert → `stable` |
| **M2 — Core triad** | v0.3 | Code Review · Performance Strategist · Build Troubleshooter |
| **M3 — Breadth** | v0.4–0.6 | One flagship per remaining category |
| **M4 — v1.0** | v1.0 | ≥20 `stable`, eval-backed Superpowers; contributor flywheel |

Full detail and reasoning: **[docs/roadmap.md](docs/roadmap.md)**.

---

## 🤝 Contributing

We want this to become the **most trusted AI resource for Unity developers** — and that only happens with a community.

- 💡 **Propose a Superpower** → open a [New Superpower issue](.github/ISSUE_TEMPLATE/01-new-superpower.yml).
- 🐞 **Report a bad output** → open a [Superpower Bug issue](.github/ISSUE_TEMPLATE/02-superpower-bug.yml). Every confirmed bug becomes a permanent eval.
- ✍️ **Author one** → read the **[Authoring Guide](docs/authoring-guide.md)**, copy `templates/`, and open a PR.

Start with **[CONTRIBUTING.md](CONTRIBUTING.md)**. Good first issues are labeled `good-first-issue`.

---

## 🧪 Compatibility

Superpowers are written to be **version-agnostic across Unity 2021 LTS → Unity 6**, with version-specific behavior flagged inline (`⚠️ Unity 6+`, `⚠️ ≤2021 LTS`). No render pipeline is assumed — guidance calls out Built-in / URP / HDRP differences where they matter.

---

## 🔭 Future vision — the Claude Superpowers ecosystem

This repository is the first of a family. Its structure, documentation style, templates, and testing approach are **deliberately reusable** so sibling repositories share one architecture:

`claude-superpowers-web` · `claude-superpowers-qa` · `claude-superpowers-game-design` · `claude-superpowers-backend` · `claude-superpowers-devops`

See **[docs/ecosystem.md](docs/ecosystem.md)** for the shared blueprint.

---

<div align="center">

**Built by engineers, for engineers.** Optimized for quality, maintainability, and real-world usefulness.

⭐ Star the repo to follow along · [Read the philosophy →](docs/philosophy.md)

*Licensed under [MIT](LICENSE).*

</div>
