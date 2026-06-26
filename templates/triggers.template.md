<!--
triggers.template.md — copy to superpowers/<category>/<name>/triggers.md
One triggers file per Superpower. See docs/testing-superpowers.md (layer 2).
Machine-checked by scripts/validate.py: keep the two required headings and quote each
phrasing as a bullet. Delete these comments before committing.

Requirements:
- "## Should fire (positive triggers)"  — at least 3 quoted phrasings.
- "## Should not fire (negative triggers)" — at least 2 quoted phrasings, each naming the
  sibling Superpower that should handle it instead (after an em dash).
-->

# Trigger tests — <Superpower name>

Phrasings that **should** invoke this skill and phrasings that **should not**. This protects
the `description`. Each bullet is one user message.

## Should fire (positive triggers)

- "<realistic phrasing that must invoke this skill>"
- "<another>"
- "<another>"

## Should not fire (negative triggers)

- "<phrasing that belongs to a sibling skill>" — <Sibling Superpower name>
- "<another>" — <Sibling Superpower name>

## Borderline (clarify or engage on the in-scope part)

- "<ambiguous phrasing>" — when to clarify vs. engage.

## Notes

<The one-line boundary rule that separates this skill from its neighbours.>
