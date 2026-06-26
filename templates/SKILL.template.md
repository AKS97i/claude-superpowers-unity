---
name: <unity-domain-role>
description: <Third person. What it does + WHEN to use it. List concrete inputs/scenarios and trigger phrases. See docs/naming-conventions.md.>
metadata:
  version: 0.1.0
  stability: experimental   # experimental | beta | stable
  category: <category>
---

<!--
SKILL.template.md — copy to superpowers/<category>/<name>/SKILL.md
Keep YAML frontmatter as the very first bytes of the file (no comment above it).

Production-ready Claude Code Skill. Keep the body LEAN; push depth into
references/ (progressive disclosure). The `description` decides triggering —
see docs/naming-conventions.md. Delete comments + placeholders before committing.
-->

# <Human Title>

## When to use this skill
<Concise triggers and scope. Mirror the description. Include what is OUT of scope and which sibling skill handles it.>

## Operating principles
- State confidence and what would raise it. Never fabricate a fix or claim unearned certainty.
- Ask for missing essential inputs before concluding.
- Prefer the smallest correct change; surface trade-offs; challenge bad asks.

## Methodology
<The staged pipeline, summarized as actionable steps. This is the operational spine.>

1. …
2. …

## Confidence model
<The named levels, briefly — full thresholds live in DESIGN.md / references.>

## Output format
```text
<the exact report template to produce>
```

## References
<Bulleted pointers into references/*.md, loaded on demand. e.g.:>
- `references/<topic>.md` — <when to consult it>
