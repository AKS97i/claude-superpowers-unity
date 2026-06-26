# Trigger tests — Unity Debugging Expert

Phrasings that **should** invoke this skill and phrasings that **should not**. This is the
behavioral contract for the `description` — the single most failure-prone string. Run these
with the [`skill-creator`](../../../docs/testing-superpowers.md#how-to-run-evals) tooling or by
inspection; every entry is one user message.

Format is machine-checked by [`scripts/validate.py`](../../../scripts/validate.py): each bullet
is a quoted phrasing under the matching heading.

## Should fire (positive triggers)

- "Unity throws NullReferenceException on scene load, here's the stack trace"
- "My game works in the Editor but crashes on my Android build"
- "This coroutine sometimes just stops and I get no error"
- "Values I set in the Inspector reset to 0 after I renamed a field"
- "MissingReferenceException: the object has been destroyed but you're still trying to access it"
- "My singleton Instance is null on the second time I press Play"
- "A projectile occasionally passes through walls, about 1 in 50 shots"
- "Pooled bullets spawn with stale state from their previous life"
- "Here's my Player.log — the build closes with no error a few minutes in"
- "Physics behaves differently in the build than in the editor"

## Should not fire (negative triggers)

- "How do I make my game run faster?" — Performance Optimization Strategist
- "My game runs at 30 fps, how do I improve it?" — Performance / Profiler
- "Review this MonoBehaviour for code quality and naming conventions" — Unity C# Code Review
- "What's the best architecture for my inventory system?" — Architecture Advisor
- "How do I reduce my build size?" — Build Size Reducer
- "Write unit tests for this class" — Test Authoring Expert

## Borderline (clarify or engage on the defect part)

- "It freezes for two seconds then recovers" — could be a hitch (defect) or perf; clarify whether it's a hang/exception vs. just heavy.
- "Review my code and also it sometimes crashes" — the crash is in scope; defer the style review to Code Review.

## Notes

The line: **broken / wrong / throwing / crashing** → Debugging Expert; **works but slow / heavy** →
Performance; **works, is it good code?** → Code Review. Negative triggers protect against
false-fire; see [`evals/trigger-negative-performance.md`](evals/trigger-negative-performance.md)
and [`evals/trigger-negative-style-review.md`](evals/trigger-negative-style-review.md) for the
scored versions.
