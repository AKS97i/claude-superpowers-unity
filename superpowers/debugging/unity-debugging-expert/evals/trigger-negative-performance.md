# Eval: performance question should hand off, not trigger debugging

## Input

> My game runs at 30 fps and I want it smoother — what should I do to make it faster? Nothing is broken, it just isn't as snappy as I'd like. Unity 2022.3, URP, mobile.

## Expected triggering
- should-fire: false
- Should be handled by the **Performance Optimization Strategist** / **Profiler Analysis Expert**, not the Debugging Expert. There is no defect, exception, or incorrect behavior to drive to a root cause — the request is optimization of working code.

## Rubric

### MUST
- [ ] If the debugging skill is active, it **recognizes this is out of scope** (optimization of correct behavior, not a defect) and says so rather than running the bug-diagnosis pipeline.
- [ ] Hands off to / recommends the performance or profiler Superpower.
- [ ] Does not fabricate a "bug" to justify engaging.

### MUST NOT
- [ ] Does **not** trigger as a debugging session when invoked purely on trigger phrasing (the `description` excludes performance — this protects against false-fire).
- [ ] Does not produce a Symptom/Root Cause diagnosis report for a non-defect.
- [ ] Does not start a generic "top 10 perf tips" dump while claiming to be debugging.

### Confidence disclosure
- [ ] N/A for a handoff, but if it offers any pointer it frames it as "the performance skill will profile this properly," not a diagnosis.

## Notes
This is a **boundary** eval protecting the description against false positives. The line: "it's broken / wrong / throwing" → Debugging Expert; "it works but is slow / heavy" → Performance. A borderline case ("it freezes for 2s then recovers") legitimately *could* be a defect (a hitch from a synchronous load) — there, engaging or clarifying is acceptable. Pure "make it faster" is not. Weak behavior: launching a full debugging investigation of healthy code.
