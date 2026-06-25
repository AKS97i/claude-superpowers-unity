# Contributing to Claude Superpowers — Unity

Thank you for helping build the most trusted AI engineering resource for Unity developers. 🎮

This project ships **AI Engineering Systems**, not prompts. The bar is high on purpose: a Superpower earns a place here when it encodes *expert reasoning* that is consistent, evidence-driven, testable, and genuinely useful in production.

This guide explains how to propose, author, test, and submit a Superpower.

---

## Table of contents

1. [Ways to contribute](#ways-to-contribute)
2. [The lifecycle of a Superpower](#the-lifecycle-of-a-superpower)
3. [Anatomy of a Superpower](#anatomy-of-a-superpower)
4. [Authoring standards](#authoring-standards)
5. [Testing your Superpower](#testing-your-superpower)
6. [Pull request workflow](#pull-request-workflow)
7. [Quality rubric (what reviewers check)](#quality-rubric)
8. [Stability tiers](#stability-tiers)

---

## Ways to contribute

| You want to… | Do this |
| --- | --- |
| Propose a new Superpower | Open a **[New Superpower](.github/ISSUE_TEMPLATE/01-new-superpower.yml)** issue |
| Report a wrong/misleading output | Open a **[Superpower Bug](.github/ISSUE_TEMPLATE/02-superpower-bug.yml)** issue (include the transcript) |
| Suggest an improvement | Open an **[Improvement](.github/ISSUE_TEMPLATE/03-improvement.yml)** issue |
| Report a skill that mis-fired | Open a **[Trigger Issue](.github/ISSUE_TEMPLATE/04-trigger-issue.yml)** |
| Author a Superpower | Read this guide → copy `templates/` → open a PR |
| Improve docs | PR directly |

You don't need to be a prompt engineer. If you're a Unity developer with hard-won methodology, **you have something to contribute** — we can help shape it into the three-file format.

---

## The lifecycle of a Superpower

```
Proposal (issue)  →  Acceptance  →  Authoring  →  Self-eval  →  PR  →  Review  →  Tier assignment  →  Merge
```

1. **Proposal.** Open a New Superpower issue with the 7 catalog fields (purpose, audience, inputs, outputs, value, priority, category). This lets us avoid duplicates and agree on scope before you write.
2. **Acceptance.** A maintainer labels it `status:accepted` and assigns a `category:*` and `priority`.
3. **Authoring.** Copy the templates, follow the [Authoring Guide](docs/authoring-guide.md).
4. **Self-eval.** Run your Superpower against its own eval cases. Fix what fails.
5. **PR.** Open a pull request using the template checklist.
6. **Review.** At least one maintainer reviews against the [rubric](#quality-rubric).
7. **Tier.** We assign a [stability tier](#stability-tiers) and merge.

> **Scope rule: one Superpower = one job.** Debugging ≠ profiling ≠ review. Narrow scope means reliable triggering, simpler evals, and clean composition. If your idea does three things, it's three Superpowers.

---

## Anatomy of a Superpower

Every Superpower lives in `superpowers/<category>/<name>/` and **must contain all three core files from day one**:

```
superpowers/<category>/<name>/
├── DESIGN.md      # The engineering system: mission, scope, methodology,
│                  #   decision trees, confidence model, heuristics, edge cases.
├── SKILL.md       # Production-ready Claude Code Skill. Lean body + progressive
│                  #   disclosure into references/. Trigger-optimized description.
├── prompt.md      # Portable, self-contained prompt for Claude.ai / API / any LLM.
├── references/    # Deep checklists & heuristics, loaded on demand by SKILL.md.
├── examples/      # Worked before→investigation→after narratives (also used as evals).
└── evals/         # Scenario + rubric test cases.
```

**The three files must stay synchronized.** `DESIGN.md` is the source of truth for the methodology; `SKILL.md` and `prompt.md` are two delivery surfaces for the *same* system. If you change the methodology, update all three.

Copy the scaffolds from [`templates/`](templates/) to start.

---

## Authoring standards

Full detail in the **[Authoring Guide](docs/authoring-guide.md)**. The essentials:

- **Methodology over answers.** Encode *how to reason*, not a list of canned fixes.
- **Evidence & confidence.** The Superpower must state confidence and what would raise it. Never fabricate certainty or invent fixes.
- **Minimal change bias.** Recommend the smallest correct change; surface trade-offs; challenge bad asks.
- **Unity-accurate & version-aware.** Reference real APIs, Editor windows, and log files. Flag version-specific behavior inline (`⚠️ Unity 6+`, `⚠️ ≤2021 LTS`). Don't assume a render pipeline — call out Built-in/URP/HDRP differences where relevant.
- **Trigger-friendly description.** The `SKILL.md` `description` is third-person and lists concrete inputs and scenarios. This is what makes auto-invocation reliable. See [naming conventions](docs/naming-conventions.md).
- **Lean SKILL.md.** Keep the skill body focused; push long checklists into `references/`.
- **No placeholders.** Ship publishable content, not "TODO".

---

## Testing your Superpower

We can't assert exact output, so we test **behavior against rubrics**. See **[docs/testing-superpowers.md](docs/testing-superpowers.md)**.

At minimum, before opening a PR:

- [ ] Add **≥2 eval cases** in `evals/` (realistic input + rubric of must-do / must-not-do / confidence-disclosure checks).
- [ ] Add **≥1 worked example** in `examples/`.
- [ ] Add **trigger phrasings** (should-fire and should-not-fire) to verify the description.
- [ ] Run the Superpower against its evals and confirm it passes the rubric.

> Every confirmed `superpower-bug` becomes a **new eval case** before the issue is closed. That's how field failures become permanent guardrails.

---

## Pull request workflow

1. Fork → branch from `main` (`superpower/<name>` or `docs/<topic>`).
2. Make your change. **One Superpower per PR** keeps reviews focused.
3. Fill out the PR template checklist completely.
4. Update **[docs/catalog.md](docs/catalog.md)** and **[CHANGELOG.md](CHANGELOG.md)**.
5. Ensure CI passes (frontmatter schema, required sections, link integrity, markdownlint).
6. Request review. Address feedback. We squash-merge with a [Conventional Commit](https://www.conventionalcommits.org/) title.

CI handles mechanics so human reviewers can focus on **the quality of the reasoning encoded.**

---

## Quality rubric

Reviewers evaluate every new/changed Superpower against:

| Dimension | Question |
| --- | --- |
| **Scope** | Does it do exactly one job? |
| **Methodology** | Is there a clear, repeatable investigation/decision workflow — not just answers? |
| **Evidence** | Does it gather evidence and state confidence honestly? |
| **Unity accuracy** | Are APIs, windows, logs, and version notes correct? |
| **Triggering** | Does the description fire on the right prompts and not the wrong ones? |
| **Portability** | Is `prompt.md` self-contained and equivalent to `SKILL.md`? |
| **Synchronization** | Do `DESIGN.md`, `SKILL.md`, `prompt.md` agree? |
| **Testability** | Are there evals and examples that actually exercise it? |
| **Usefulness** | Would a working Unity dev be measurably better off? |

---

## Stability tiers

| Tier | Meaning |
| --- | --- |
| `experimental` | Useful but unproven; no eval bar met yet. |
| `beta` | Evals pass; limited field use. |
| `stable` | Reviewed, evals + examples present, validated in real use. |

Tiers are shown in the [catalog](docs/catalog.md) so users know what to expect.

---

## Code of conduct

Participation is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). Be excellent to each other.

---

By contributing, you agree your work is licensed under the repository's [MIT License](LICENSE).
