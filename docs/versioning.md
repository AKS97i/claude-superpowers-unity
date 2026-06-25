# Versioning

We version at **two levels** because users install the *collection* but rely on individual *Superpowers*.

## 1. Per-Superpower versioning (SemVer)

Each Superpower carries its own version in `SKILL.md` frontmatter (`metadata.version`) and evolves independently.

| Bump | When | Example |
| --- | --- | --- |
| **MAJOR** | Methodology/behavior changes users must relearn | Replacing the investigation pipeline |
| **MINOR** | Added coverage, heuristics, or references; backward-compatible | New edge-case handling |
| **PATCH** | Wording, typo, clarity, or reference fixes | Fixing a checklist item |

When a Superpower's methodology changes, **all three files (`DESIGN.md`, `SKILL.md`, `prompt.md`) bump together** — they describe the same system.

## 2. Collection versioning (SemVer)

The repository as a whole uses SemVer, tracked in [CHANGELOG.md](../CHANGELOG.md).

- **MAJOR** — breaking changes to repo structure, templates, or conventions that affect contributors/consumers.
- **MINOR** — new Superpowers, new docs/templates, new categories.
- **PATCH** — fixes and small improvements.

`v1.0.0` is a **quality milestone**: ≥ 20 `stable`, eval-backed Superpowers across all categories (see [roadmap.md](roadmap.md)).

## Stability tiers

Independent of version number, every Superpower advertises a maturity tier in its frontmatter and in the [catalog](catalog.md):

| Tier | Meaning | Bar |
| --- | --- | --- |
| `experimental` | Useful but unproven | All three files exist; methodology is sound |
| `beta` | Works and is tested | Evals pass; ≥1 worked example; reviewed |
| `stable` | Trusted for production use | Field-validated; comprehensive evals + examples; showcase media |

A Superpower can be `v0.3.0` and `stable`, or `v1.2.0` and `beta` — version tracks *change*, tier tracks *trust*.

## Deprecation

If a Superpower is superseded or merged into another:

1. Mark it `deprecated` in frontmatter and the catalog, with a pointer to the replacement.
2. Keep it for one MINOR collection release.
3. Remove it in the next, noting the removal in the CHANGELOG.

## Why two levels?

A single repo version would force every consumer to reason about the whole collection to understand one skill's maturity. Per-Superpower SemVer + tiers lets us **ship early without over-promising**: an `experimental` skill can land and improve without implying the whole library is unstable.
