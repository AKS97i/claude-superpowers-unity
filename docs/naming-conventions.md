# Naming Conventions

Consistent naming makes Superpowers discoverable, prevents collisions, and — critically — makes Claude Code skill **auto-triggering** reliable. These rules are enforced in review and partly in CI.

## Superpower (skill) names

- **Format:** `kebab-case`, following the pattern **`unity-<domain>-<role>`**.
- **Examples:** `unity-debugging-expert`, `unity-performance-strategist`, `unity-addressables-architect`, `unity-code-review`.
- **Why the `unity-` prefix?** A user may have many skills installed. The prefix guarantees these never collide with non-Unity skills and signals domain at a glance. Sibling ecosystems use their own prefix (`web-`, `qa-`, …) — see [ecosystem.md](ecosystem.md).
- **The folder name, the `name:` frontmatter, and the catalog entry must all match exactly.**

## Categories

- **Format:** lowercase plural nouns, `kebab-case` if multi-word.
- **Examples:** `debugging/`, `code-review/`, `rendering/`, `editor-tooling/`, `version-control/`.
- A category folder is created only when its first Superpower lands (no empty/dead folders).

## Fixed file names (per Superpower)

| File | Required | Purpose |
| --- | --- | --- |
| `DESIGN.md` | ✅ | The engineering system spec (source of truth). |
| `SKILL.md` | ✅ | Claude Code Skill. |
| `prompt.md` | ✅ | Portable prompt. |
| `references/*.md` | as needed | Deep checklists/heuristics (kebab-case). |
| `examples/*.md` | ✅ (≥1) | Worked narratives (kebab-case, scenario-named). |
| `evals/*.md` | ✅ (≥2) | Scenario + rubric (kebab-case, scenario-named). |

- **Reference/example/eval files:** `kebab-case`, named by scenario, e.g. `null-ref-on-scene-load.md`, `coroutine-stops-on-disable.md`.

## The `SKILL.md` `description` (most important string in the repo)

The `description` is what Claude Code uses to decide whether to invoke the skill. Get it wrong and the best methodology never fires.

Rules:

- **Third person**, describing what the skill does and *when to use it*.
- **List concrete inputs and scenarios** the user is likely to mention (error messages, stack traces, "works in editor but not build", platform names, log files).
- **Include trigger phrases** a real user would type.
- **Be specific, not grandiose.** "Diagnoses Unity runtime errors, crashes, and incorrect behavior from stack traces, logs, and repro steps" beats "The ultimate Unity debugger."
- Keep it to a few tight sentences.

✅ Good:
> Diagnoses Unity runtime bugs — NullReferenceExceptions, crashes, incorrect behavior, editor-vs-build discrepancies, and platform-specific issues. Use when the user shares a Unity error message, stack trace, Editor.log/Player.log, or describes a Unity bug or unexpected behavior and wants the root cause and a fix.

❌ Bad:
> An expert Unity debugging assistant.

See [authoring-guide.md](authoring-guide.md) for the full `SKILL.md` structure and [naming-conventions.md](naming-conventions.md) here for the rules.

## Version-specific callouts

Use blockquote callouts inline so guidance stays version-agnostic but precise:

```markdown
> ⚠️ **Unity 6+:** Enter Play Mode Options are on by default; static fields are not reset between play sessions.
> ⚠️ **≤2021 LTS:** ...
```

## Frontmatter (SKILL.md)

```yaml
---
name: unity-debugging-expert
description: <trigger-optimized, see rules above>
metadata:
  version: 0.1.0
  stability: beta            # experimental | beta | stable
  category: debugging
---
```

## Commit & branch naming

- **Branches:** `superpower/<name>`, `docs/<topic>`, `fix/<short-desc>`.
- **Commits / PR titles:** [Conventional Commits](https://www.conventionalcommits.org/) — `feat(debugging): add unity-debugging-expert`, `docs: clarify confidence model`, `fix(catalog): correct priority`.
