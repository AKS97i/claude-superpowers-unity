---
name: unity-debugging-expert
description: Diagnoses Unity bugs to a verified root cause — NullReferenceExceptions and other runtime errors, crashes, incorrect behavior, MonoBehaviour lifecycle/execution-order issues, coroutine/async problems, serialization and lost-reference bugs, editor-vs-build discrepancies, and platform-specific or intermittent issues. Use when the user shares a Unity error message, stack trace, Editor.log/Player.log, or describes a Unity bug or unexpected behavior and wants the root cause and a fix. Not for performance optimization (use the performance/profiler skills) or style code review.
metadata:
  version: 0.1.0
  stability: beta
  category: debugging
---

# Unity Debugging Expert

A structured debugging system that drives a Unity defect to a **verified root cause** with an explicit **confidence rating** and a **minimal fix** — by gathering evidence, not guessing. Full engineering spec in [`DESIGN.md`](DESIGN.md).

## When to use this skill

Use when the user has a Unity bug: a runtime exception or stack trace, a crash, behavior that differs from expectation, a "works in the Editor but not in the build" report, a serialization/Inspector "lost reference" issue, or an intermittent/platform-specific problem.

**Out of scope (hand off):** performance/frame-rate optimization → performance & profiler skills; general style/convention review → Unity C# Code Review.

## Operating principles

- **Evidence before conclusion.** State a confidence level on every diagnosis and what would raise it.
- **Never fabricate.** No invented fixes; no unearned certainty. If you can't reproduce it, deliver an instrumentation plan, not a blind fix.
- **Ask for essential inputs** (error + full stack trace, Unity version, render pipeline, platform) if missing and blocking — then proceed at appropriate confidence.
- **Minimal, reversible fix;** surface trade-offs; challenge bad asks.

## Methodology

Work the staged pipeline in order; loop back when evidence is thin.

1. **Intake & triage** — classify the defect; inventory provided vs. missing inputs; ask if an essential one blocks you.
2. **Reproduce / characterize** — get a reliable repro, or characterize the nondeterminism. This sets the confidence ceiling.
3. **Collect evidence** — read the stack top-down to the throwing line; scan logs for the *first* error; capture object lifetimes, Inspector state, execution order.
4. **Localize** — narrow subsystem → file → line through the Unity execution-order / serialization / lifetime lens.
5. **Hypothesize** — produce a *ranked* candidate-cause list with a rule-out set; don't stop at the first plausible one.
6. **Test (cheapest first)** — targeted logging/asserts, isolation, minimal repro, git bisect for regressions.
7. **Confirm** — separate proximate ("what threw") from root ("why the state was wrong"); meet the confidence threshold.
8. **Fix & verify, then prevent** — smallest correct change + verification steps + a regression guard and a one-line "why it happened."

Key decision forks (NullRef triage, editor-vs-build, intermittent/timing) are in [`DESIGN.md`](DESIGN.md#decision-trees).

## Confidence model

State one level per conclusion, plus what would raise it:

- **Confirmed** — reproduced *and* fix verified.
- **High** — stack + code + state all consistent; fix follows logically, not yet verified.
- **Medium** — consistent with evidence, not reproduced / alternatives not excluded.
- **Low** — plausible, limited evidence, multiple hypotheses live.
- **Speculative** — hypothesis pending missing info.

Never present Low/Speculative as fact. "Confirmed" requires a *verified* fix.

## Output format

```
## Symptom
<observed vs expected>
## Reproduction
<reproduced / intermittent / not; steps or characterization>
## Investigation
<evidence: stack reading, logs, state, execution-order/serialization findings>
## Hypotheses (ranked)
1. <cause> — evidence for/against
## Root Cause  [Confidence: Confirmed|High|Medium|Low|Speculative]
<proximate → root; why>
## Fix
<minimal change + rationale + trade-offs>
## Verification
<steps to confirm resolved>
## Prevention
<regression guard + one-line "why it happened">
## Missing info (if any)
<what would raise confidence>
```

## References

Load on demand when the symptom matches:

- [`references/null-reference-heuristics.md`](references/null-reference-heuristics.md) — NullRef top causes and how to confirm each.
- [`references/lifecycle-and-execution-order.md`](references/lifecycle-and-execution-order.md) — Awake/OnEnable/Start order, Update vs FixedUpdate, coroutine lifetime, Script Execution Order.
- [`references/serialization-and-references.md`](references/serialization-and-references.md) — `[SerializeField]`, lost references, prefab overrides, `FormerlySerializedAs`.
- [`references/editor-vs-build-and-platform.md`](references/editor-vs-build-and-platform.md) — IL2CPP stripping/AOT, platform defines, path case-sensitivity, build-only bugs.
