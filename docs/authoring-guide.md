# Authoring Guide

This is the gold-standard reference for writing a Superpower. If you follow it, your contribution will sail through review. It uses the **Unity Debugging Expert** (`superpowers/debugging/unity-debugging-expert/`) as the canonical example.

> Read [philosophy.md](philosophy.md) first. A Superpower is an **AI Engineering System**, not a prompt.

---

## Step 0 — Get your proposal accepted

Open a [New Superpower issue](../.github/ISSUE_TEMPLATE/01-new-superpower.yml) with the seven catalog fields. A maintainer confirms scope and category before you write. This prevents duplicate or overly broad Superpowers.

**Scope rule:** one Superpower = one job. If it does three things, it's three Superpowers.

---

## Step 1 — Copy the templates

```bash
mkdir -p superpowers/<category>/<name>/{references,examples,evals}
cp templates/DESIGN.template.md   superpowers/<category>/<name>/DESIGN.md
cp templates/SKILL.template.md    superpowers/<category>/<name>/SKILL.md
cp templates/prompt.template.md   superpowers/<category>/<name>/prompt.md
cp templates/triggers.template.md superpowers/<category>/<name>/triggers.md
cp templates/eval.template.md     superpowers/<category>/<name>/evals/<scenario>.md
```

Follow [naming-conventions.md](naming-conventions.md) for names.

---

## Step 2 — Write `DESIGN.md` first (it's the source of truth)

`DESIGN.md` is where you do the real engineering. `SKILL.md` and `prompt.md` are renderings of it. Cover:

1. **Mission** — one paragraph: what defect/task class this drives to a verified outcome.
2. **Scope** — the exact problem types in-bounds.
3. **Goals / Non-goals** — what success is; what you explicitly refuse (hand-offs to other Superpowers belong here).
4. **Inputs / Outputs** — what the user provides; what the Superpower returns.
5. **Investigation / decision methodology** — the staged pipeline. This is the heart.
6. **Decision trees** — branch logic for common forks (e.g. "reproduced vs. not").
7. **Confidence model** — named levels with explicit evidence thresholds.
8. **Reporting format** — the exact output template.
9. **Heuristics** — domain-specific, fast pattern→cause mappings (often pushed to `references/`).
10. **Edge cases** — heisenbugs, platform-only, insufficient info, etc.
11. **Future improvements** — known gaps and hand-offs.

> **Tip:** decision trees and confidence models are what separate an engineering system from a prompt. Don't skip them.

---

## Step 3 — Write `SKILL.md` (lean + progressive disclosure)

Structure:

```markdown
---
name: <unity-domain-role>
description: <trigger-optimized — see naming-conventions.md>
metadata:
  version: 0.1.0
  stability: experimental
  category: <category>
---

# <Human Title>

## When to use this skill
<concise triggers and scope — mirror the description>

## Methodology
<the staged pipeline, summarized — the operational spine>

## Confidence model
<the named levels, briefly>

## Output format
<the report template the skill must produce>

## References
<bulleted pointers into references/*.md, loaded on demand>
```

Rules:

- **Keep the body lean.** Long checklists and heuristic tables go into `references/` and are referenced by name. They are loaded only when relevant. This keeps triggering reliable and context cheap.
- **The `description` is critical** — see [naming-conventions.md](naming-conventions.md#the-skillmd-description-most-important-string-in-the-repo).
- **Make the output format explicit.** Consistent, structured output is half the value.
- **Bake in honesty.** Instruct the skill to state confidence and ask for missing inputs rather than guessing.

---

## Step 4 — Write `prompt.md` (portable, self-contained)

The portable version must work when pasted as a system prompt into any AI assistant **with no external files**. So:

- **Inline the essentials** that `SKILL.md` defers to `references/` (the portable version has no progressive disclosure).
- Keep the **same methodology, confidence model, and output format** as `SKILL.md`.
- Start with a clear role + mission, then the methodology, then the output template.
- End with an instruction to ask for missing inputs before diagnosing.

A CI check warns if `SKILL.md` and `prompt.md` drift on core sections (methodology, confidence model, output format).

---

## Step 5 — Add `references/`

Deep material that would bloat the skill body:

- Pattern→cause heuristic tables (e.g. "NullRef top causes").
- Long checklists.
- Decision-tree detail.
- Curated known-issue references.

Name files by topic (`null-reference-heuristics.md`). Reference them from `SKILL.md`.

---

## Step 6 — Add `examples/` (≥1)

A worked **before → investigation → after** narrative using a realistic (redacted) scenario. It:

- Demonstrates the methodology in action.
- Doubles as documentation.
- Can be reused as an eval input.

---

## Step 7 — Add `evals/` (≥2) and `triggers.md`

See [testing-superpowers.md](testing-superpowers.md). Each eval = realistic input + a rubric of **must-do / must-not-do / confidence-disclosure** checks, plus a `should-fire: true|false` line. Fill in `triggers.md` (positive + negative phrasings), and give each negative trigger a matching `should-fire: false` eval so the boundary is scored, not just listed.

Validate structure locally and fix what fails **before** opening the PR:

```bash
python scripts/validate.py superpowers/<category>/<name>
```

Then run your Superpower against the eval rubrics (AI-as-judge / `skill-creator`) and fix any rubric failures.

---

## Step 8 — Update catalog + changelog, open the PR

- Add/update the row in [catalog.md](catalog.md).
- Add an entry to [CHANGELOG.md](../CHANGELOG.md) under `[Unreleased]`.
- Open the PR with the template checklist filled in.

---

## The synchronization rule (never break this)

`DESIGN.md` ⟶ `SKILL.md` ⟶ `prompt.md` describe **one** system. If you change the methodology, the confidence model, or the output format, **update all three in the same PR.** Drift is the fastest way to lose user trust.

---

## Quality self-check (mirror of the reviewer rubric)

- [ ] Does it do exactly one job?
- [ ] Is the methodology explicit and repeatable (not a list of answers)?
- [ ] Does it gather evidence and disclose confidence?
- [ ] Are Unity APIs, windows, logs, and version notes accurate?
- [ ] Does the description fire on the right prompts (and not the wrong ones)?
- [ ] Is `prompt.md` self-contained and equivalent to `SKILL.md`?
- [ ] Do all three files agree?
- [ ] Do the evals actually exercise it?
- [ ] Would a working Unity dev be measurably better off?
