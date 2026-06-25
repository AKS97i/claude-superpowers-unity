# Testing Superpowers

You cannot unit-test a methodology for an exact string of output. So we test **behavior against rubrics** — the same way a senior engineer reviews a junior's investigation: not "did you produce my exact words" but "did you follow a sound process and reach a defensible, honestly-qualified conclusion?"

This eval-driven approach is the project's main quality differentiator.

## The four test layers

### 1. Eval cases (`evals/*.md`) — required, ≥2 per Superpower
A realistic input plus a **rubric**. The rubric is a list of checks in three buckets:

- **MUST do** — e.g. "asks for Unity version/platform if not provided", "produces the report format", "states a confidence level".
- **MUST NOT do** — e.g. "does not fabricate a fix without evidence", "does not claim Confirmed without a verified repro".
- **Confidence disclosure** — e.g. "states what additional evidence would raise confidence".

Rubrics are written so an LLM-as-judge (or a human) can score pass/fail per item. This aligns with the `skill-creator` eval tooling available in Claude Code.

### 2. Trigger tests — required
Lists of phrasings that **should** invoke the skill and phrasings that **should not**. This protects the `description` (the single most failure-prone string). Example for the Debugging Expert:

- ✅ should fire: "Unity throws NullReferenceException on scene load", "works in editor but not in my Android build"
- ❌ should not fire: "how do I make my game faster" (that's the Performance Strategist), "review my code for style"

### 3. Golden example transcripts (`examples/*.md`) — required, ≥1
Maintainer-reviewed end-to-end sessions. They document the Superpower *and* serve as regression anchors and eval inputs.

### 4. Structural CI — automated
The `.github/workflows/validate.yml` workflow checks mechanics so humans focus on substance:

- Frontmatter schema (`name`, `description`, `metadata.version`, `metadata.stability`, `metadata.category`).
- Required files present (`DESIGN.md`, `SKILL.md`, `prompt.md`, ≥1 example, ≥2 evals).
- Required `SKILL.md` sections present.
- Link integrity (no broken relative links).
- `SKILL.md` ↔ `prompt.md` core-section parity (warn on drift).
- Markdown lint.

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

1. **Manual / LLM-as-judge:** paste the eval `Input` into Claude (with the Superpower active via `SKILL.md`, or `prompt.md` pasted), capture the response, and score it against the rubric. A second Claude session can act as judge using the rubric.
2. **`skill-creator` tooling:** use Claude Code's `skill-creator` skill to benchmark and measure triggering accuracy and behavior with variance analysis.
3. **CI (structural):** runs automatically on every PR.

> Behavioral evals (layers 1–3) are run by the author and reviewer today; an automated behavioral harness is a roadmap item (M1). Structural checks (layer 4) are automated now.

## The regression rule

> Every confirmed `superpower-bug` becomes a new eval case **before** the issue is closed.

This is non-negotiable. It is how field failures become permanent guardrails and how the collection's quality compounds over time instead of decaying.

## What "passing" means by tier

| Tier | Eval bar |
| --- | --- |
| `experimental` | Rubrics drafted; may not all pass yet |
| `beta` | All eval rubrics pass; ≥1 golden example |
| `stable` | Comprehensive evals incl. edge cases; field-validated; showcase media |
