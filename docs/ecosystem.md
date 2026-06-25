# The Claude Superpowers Ecosystem

This repository is the **first of a family**. Its architecture is deliberately generic so that sibling repositories can reuse the same structure, documentation style, templates, testing model, and governance — only the *domain content* changes.

## Planned siblings

| Repository | Domain |
| --- | --- |
| `claude-superpowers-unity` | Unity game development *(this repo)* |
| `claude-superpowers-web` | Web / frontend engineering |
| `claude-superpowers-qa` | Quality assurance & test engineering |
| `claude-superpowers-game-design` | Game & systems design |
| `claude-superpowers-backend` | Backend / distributed systems |
| `claude-superpowers-devops` | DevOps / infrastructure / CI-CD |

## The shared blueprint

Everything below is **domain-agnostic** and should be copied as-is (adapting only domain specifics) into any new ecosystem repository:

### Structure
```
<repo>/
├── README.md            # flagship hero + catalog + roadmap
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── docs/                # vision, philosophy, roadmap, naming, versioning,
│                        #   authoring-guide, testing, catalog, glossary, ecosystem
├── templates/           # DESIGN / SKILL / prompt / eval scaffolds
├── showcases/           # screenshots, GIFs, example conversations
└── superpowers/<category>/<name>/
    ├── DESIGN.md
    ├── SKILL.md
    ├── prompt.md
    ├── references/
    ├── examples/
    └── evals/
```

### Shared conventions
- **Framing:** Superpowers are **AI Engineering Systems**, not prompts. (See [philosophy.md](philosophy.md).)
- **Three synchronized files** per Superpower: `DESIGN.md` + `SKILL.md` + `prompt.md`.
- **Naming:** `<prefix>-<domain>-<role>` in `kebab-case`. The prefix is the ecosystem domain (`unity-`, `web-`, `qa-`, `backend-`, `devops-`, `gamedesign-`). The prefix guarantees skills from different ecosystems never collide in one user's environment.
- **Versioning:** per-Superpower SemVer + stability tiers; collection-level SemVer. (See [versioning.md](versioning.md).)
- **Testing:** eval-driven (rubrics + golden examples + trigger tests + structural CI). (See [testing-superpowers.md](testing-superpowers.md).)
- **Governance:** issue forms, PR template, quality rubric, lifecycle. (See [CONTRIBUTING.md](../CONTRIBUTING.md).)
- **Progressive disclosure** in every `SKILL.md`.

### What changes per repository
- The **catalog** of Superpowers and their categories.
- Domain-specific **heuristics, references, and version/platform callouts**.
- The **prefix** in skill names.
- Hero copy and showcase media.

## Why design for an ecosystem now

1. **Consistency builds trust.** A developer who learns one repo instantly understands the others.
2. **Templates compound.** Improvements to the authoring/testing model propagate across the family.
3. **Cross-linking.** A full-stack team can install Unity + backend + devops Superpowers that share conventions and compose cleanly.
4. **Lower marginal cost.** Each new ecosystem repo starts from a proven skeleton instead of a blank page.

## Extraction checklist (to spin up a new sibling)

1. Copy `docs/`, `templates/`, `.github/`, root governance files, and `showcases/` skeleton.
2. Find-and-replace the domain prefix and hero copy.
3. Replace `docs/catalog.md` with the new domain's catalog.
4. Keep `philosophy.md`, `versioning.md`, `testing-superpowers.md`, `authoring-guide.md`, and this file nearly verbatim.
5. Ship the first flagship Superpower as `beta` to prove the skeleton — exactly as this repo does with the Unity Debugging Expert.
