<!--
DESIGN.template.md — copy to superpowers/<category>/<name>/DESIGN.md

DESIGN.md is the SOURCE OF TRUTH for the Superpower. SKILL.md and prompt.md are
renderings of the system described here. Read docs/authoring-guide.md first.
Delete these comments and all <angle-bracket> placeholders before committing.
-->

# DESIGN — <Human Title>

> **Category:** <category> · **Name:** `<unity-domain-role>` · **Stability:** experimental · **Version:** 0.1.0

## Mission
<One paragraph: what class of problem/task this Superpower drives to a verified outcome, and the standard it holds (evidence, confidence, minimal change).>

## Scope
<The exact problem types in-bounds. Be concrete.>

## Goals
- <What a great outcome looks like.>

## Non-goals
- <What this explicitly refuses; name the Superpower it hands off to.>

## Inputs
<What the user provides. Mark which are essential vs. helpful, and note that the system asks for missing essentials rather than guessing.>

## Outputs
<What the system returns — point to the Reporting format below.>

## Investigation / decision methodology
<The staged pipeline — the heart of the system. Number the stages. Each stage:
what it does, what evidence it produces, when to move on.>

1. **Intake & triage** — …
2. **…** — …

## Decision trees
<Branch logic for the common forks. Use nested bullets or a fenced block.>

```
<fork> ?
├─ <condition A> → <action>
└─ <condition B> → <action>
```

## Confidence model
| Level | Evidence threshold |
| --- | --- |
| Confirmed | <…> |
| High | <…> |
| Medium | <…> |
| Low | <…> |
| Speculative | <…> |

Every conclusion states its level **and what would raise it.**

## Reporting format
```
<the exact output template the SKILL.md and prompt.md must produce>
```

## Heuristics
<Domain-specific pattern→cause / pattern→action mappings. Long tables belong in references/ and are linked here.>

## Edge cases
- <Heisenbugs / platform-only / insufficient info / cannot reproduce / version-specific engine bugs / etc.>

## Future improvements
- <Known gaps, planned references, hand-offs to other Superpowers.>
