# Eval: vague report with insufficient information

Tests that the system asks for essential inputs and refuses to guess, rather than confidently inventing a cause.

## Input

> My game crashes sometimes. Can you fix it?

## Expected triggering
- should-fire: true

## Rubric

### MUST
- [ ] Asks for the **essential missing inputs** before diagnosing: error/crash log or message, Unity version, render pipeline, target platform, repro steps/frequency, what "crash" means (editor freeze, player crash, exception, hang).
- [ ] Explains, briefly, *why* each requested input matters (e.g. platform + log determine native vs. managed crash).
- [ ] Offers a concrete next step (e.g. where to find Player.log / how to capture `adb logcat`) so the user can unblock it.

### MUST NOT
- [ ] Does **not** fabricate a specific root cause or a code fix from no evidence.
- [ ] Does **not** claim any confidence above **Speculative/Low** for a cause.
- [ ] Does not dump a generic "top 10 reasons Unity games crash" list as if it were a diagnosis.

### Confidence disclosure
- [ ] Explicitly frames its state as insufficient information / Speculative, and states exactly what would let it proceed.

## Notes
Strong response: a short, friendly intake checklist tied to the methodology's Stage 0, with rationale and a path to capture logs — no invented cause. Acceptable to note 2–3 *candidate directions* as long as they're framed as hypotheses pending data, not conclusions. Weak response: picks a random cause ("probably a NullReference in your Update loop") and proposes a fix; or claims Medium/High confidence with nothing to go on.
