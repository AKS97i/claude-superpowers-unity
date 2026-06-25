# Philosophy — AI Engineering Systems, not prompts

This is the most important document in the repository. It defines *what* we build and *why*, and it governs every other decision.

## The core idea

A **Superpower is an AI Engineering System**: a structured, repeatable methodology that encodes how a senior Unity engineer reasons about a class of problems.

A prompt says *"help me debug this."* An engineering system says:

> Reproduce → gather evidence → localize → form ranked hypotheses → test cheaply → confirm root cause to a confidence threshold → fix minimally → guard against regression.

The difference is the difference between a hint and a discipline. We ship disciplines.

## Why "systems" and not "prompts"

1. **Prompts rot; methodologies endure.** Unity ships new versions, APIs change, render pipelines evolve. A canned answer goes stale. A *way of reasoning* — "always check execution order, serialization, and domain-reload state for a NullRef" — stays true.
2. **Systems are consistent.** A methodology produces the same disciplined process regardless of who is asking or how they phrase it.
3. **Systems are testable.** You can write a rubric for "did it follow the methodology and disclose confidence?" You cannot meaningfully test "was the prompt good?"
4. **Systems teach.** A developer who uses one becomes a better engineer, because the reasoning is visible.

## The seven principles

Every Superpower must embody these. Reviewers enforce them (see [CONTRIBUTING.md](../CONTRIBUTING.md)).

### 1. Methodology over answers
Encode *how to reason*, not a lookup table of fixes. The workflow is the product.

### 2. Evidence over confidence
Gather evidence before concluding. State a confidence level (and what would raise it) on every diagnosis or recommendation. **Never fabricate a fix or claim certainty you can't justify.**

### 3. Minimal, reversible change
Favor the smallest correct change. Surface trade-offs. Challenge a bad request rather than executing it silently.

### 4. Portable *and* native
Each Superpower works beautifully inside Claude Code (`SKILL.md`) and anywhere else (`prompt.md`). We never lock the methodology to one platform.

### 5. Testable by construction
If we can't write an eval or rubric for it, it isn't ready. Examples double as evals.

### 6. Progressive disclosure
The `SKILL.md` body stays lean and reliable; depth lives in `references/`, loaded only when relevant. This keeps triggering accurate and context cost low.

### 7. Unity reality, version-aware
Reference real APIs, Editor windows, and log files. Flag version-specific behavior inline (`⚠️ Unity 6+`, `⚠️ ≤2021 LTS`). Don't assume a render pipeline.

## The three artifacts, and why all three

Every Superpower ships **`DESIGN.md` + `SKILL.md` + `prompt.md`**, kept synchronized:

- **`DESIGN.md`** is the source of truth — the engineering system itself (methodology, decision trees, confidence model, heuristics, edge cases). Humans read it to learn and contribute.
- **`SKILL.md`** is the production delivery surface for Claude Code (progressive disclosure, trigger-optimized).
- **`prompt.md`** is the portable delivery surface for Claude.ai, the API, and any other LLM.

`SKILL.md` and `prompt.md` are two renderings of the *same* system described in `DESIGN.md`. Change the methodology, change all three.

## What we explicitly reject

- ❌ "Awesome-prompt" lists with no methodology, no tests, no honesty about confidence.
- ❌ Output that sounds authoritative but guesses.
- ❌ Breadth at the expense of accuracy.
- ❌ Platform lock-in.

## The litmus test

Before shipping any Superpower, ask:

> Would a senior Unity engineer recognize this as *how they actually work* — and would they trust it in front of their team?

If not, it's not ready.
