<!-- Thanks for contributing! Fill out the checklist so reviewers can focus on the
quality of the reasoning encoded, not mechanics. See CONTRIBUTING.md. -->

## What does this PR do?

<!-- One or two sentences. Link the proposal issue: Closes #__ -->

## Type of change

- [ ] New Superpower
- [ ] Improvement to an existing Superpower
- [ ] Bug fix (wrong/misleading output) — eval added
- [ ] Docs / templates / tooling

## Scope check

- [ ] This PR changes **one** Superpower (or is docs/tooling only).
- [ ] The Superpower does **one job** (no scope creep).

## Three-file synchronization

- [ ] `DESIGN.md`, `SKILL.md`, and `prompt.md` are all present and **agree** on methodology, confidence model, and output format.
- [ ] `prompt.md` is self-contained (everything `SKILL.md` defers to `references/` is inlined).

## Quality (mirrors the reviewer rubric)

- [ ] Methodology is explicit and repeatable — not a list of canned answers.
- [ ] It gathers evidence and discloses confidence (and what would raise it).
- [ ] Unity APIs, Editor windows, log files, and version notes are accurate; version-specific behavior is flagged inline.
- [ ] The `SKILL.md` `description` fires on the right prompts and not the wrong ones.

## Testing

- [ ] ≥ 2 eval cases added/updated in `evals/`.
- [ ] ≥ 1 worked example in `examples/`.
- [ ] Trigger phrasings (should-fire / should-not-fire) included.
- [ ] I ran the Superpower against its evals and it passes the rubric.

## Housekeeping

- [ ] [`docs/catalog.md`](../blob/main/docs/catalog.md) updated.
- [ ] [`CHANGELOG.md`](../blob/main/CHANGELOG.md) updated under `[Unreleased]`.
- [ ] Stability tier declared in `SKILL.md` frontmatter.

## Notes for reviewers

<!-- Anything that needs context: trade-offs, open questions, follow-ups. -->
