# Testing Superpowers

You cannot unit-test a methodology for an exact string of output. So we test **behavior against rubrics** — the same way a senior engineer reviews a junior's investigation: not "did you produce my exact words" but "did you follow a sound process and reach a defensible, honestly-qualified conclusion?"

This eval-driven approach is the project's main quality differentiator.

## The four test layers

### 1. Eval cases (`evals/*.md`) — required, ≥2 per Superpower
A realistic input plus a **rubric**. The rubric is a list of checks in three buckets:

- **MUST do** — e.g. "asks for Unity version/platform if not provided", "produces the report format", "states a confidence level".
- **MUST NOT do** — e.g. "does not fabricate a fix without evidence", "does not claim Confirmed without a verified repro".
- **Confidence disclosure** — e.g. "states what additional evidence would raise confidence".

Rubrics are written so an AI-as-judge (or a human) can score pass/fail per item. This aligns with the `skill-creator` eval tooling.

### 2. Trigger tests — required (`triggers.md`)
A `triggers.md` file per Superpower listing phrasings that **should** invoke the skill and phrasings that **should not**. This protects the `description` (the single most failure-prone string). The file format is fixed and machine-checked (see [`templates/triggers.template.md`](../templates/triggers.template.md)): a `## Should fire (positive triggers)` heading with ≥3 quoted phrasings and a `## Should not fire (negative triggers)` heading with ≥2, each negative naming the sibling Superpower that should handle it. Example for the Debugging Expert:

- ✅ should fire: "Unity throws NullReferenceException on scene load", "works in editor but not in my Android build"
- ❌ should not fire: "how do I make my game faster" (that's the Performance Strategist), "review my code for style"

Each negative trigger should also have a matching scored eval with `should-fire: false` so the boundary is exercised, not just documented.

### 3. Golden example transcripts (`examples/*.md`) — required, ≥1
Maintainer-reviewed end-to-end sessions. They document the Superpower *and* serve as regression anchors and eval inputs.

### 4. Structural CI — automated
The checks live in [`scripts/validate.py`](../scripts/validate.py) — a single source of truth that runs identically **locally** (`python scripts/validate.py`, or pass a path to check one Superpower) and in CI via `.github/workflows/validate.yml`. It checks mechanics so humans focus on substance:

- Frontmatter schema (`name`, `description`, `metadata.version`, `metadata.stability`, `metadata.category`; `stability` is a known value).
- Required files present (`DESIGN.md`, `SKILL.md`, `prompt.md`, `triggers.md`, ≥1 example, ≥2 evals).
- Required `SKILL.md` sections present.
- **Eval structure** — every `evals/*.md` has the required sections (`Input`, `Expected triggering`, `Rubric` with `MUST` / `MUST NOT` / `Confidence disclosure`) and a `should-fire: true|false` line.
- **Trigger structure** — `triggers.md` has the positive/negative headings with the minimum number of entries.
- Markdown lint (separate `markdownlint.yml` workflow).

> The validator is intentionally structural — it does not judge the *content* of a rubric or trigger. That's what layers 1–3 (and human review) are for.

## Eval file format

See [`templates/eval.template.md`](../templates/eval.template.md). Each eval contains:

```markdown
# Eval: <scenario name>

## Input
<the exact user message(s) and any provided artifacts: stack trace, logs, code, version>

## Expected triggering
should-fire: true | false

## Rubric
### MUST
- [ ] <check>
### MUST NOT
- [ ] <check>
### Confidence disclosure
- [ ] <check>

## Notes
<edge cases, what a strong vs. weak response looks like>
```

## How to run evals

1. **Manual / AI-as-judge:** paste the eval `Input` into your AI assistant (with the Superpower active via `SKILL.md`, or `prompt.md` pasted), capture the response, and score it against the rubric. A second session can act as judge using the rubric.
2. **`skill-creator` tooling:** use the `skill-creator` skill to benchmark and measure triggering accuracy and behavior with variance analysis.
3. **CI (structural):** runs automatically on every PR.

> **Harness status (finalized in M1):** the eval/trigger *conventions* and the *structural* harness (layer 4, `scripts/validate.py`) are finalized and enforced in CI. Behavioral judging (layers 1–3) is run by the author and reviewer using AI-as-judge / `skill-creator` against the rubrics — it is deliberately **not** wired into CI, because that would require model access on every PR; running it is a documented author/reviewer step, not an automated gate.

## The regression rule

> Every confirmed `superpower-bug` becomes a new eval case **before** the issue is closed.

This is non-negotiable. It is how field failures become permanent guardrails and how the collection's quality compounds over time instead of decaying.

## What "passing" means by tier

| Tier | Eval bar |
| --- | --- |
| `experimental` | Rubrics drafted; may not all pass yet |
| `beta` | All eval rubrics pass; ≥1 golden example |
| `stable` | Comprehensive evals incl. edge cases; field-validated; showcase media |
