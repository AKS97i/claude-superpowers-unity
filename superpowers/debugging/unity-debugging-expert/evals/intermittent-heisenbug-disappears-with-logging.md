# Eval: bug disappears when logging is added (heisenbug)

## Input

> I have a rare bug where a projectile occasionally passes through a wall instead of hitting it. It happens maybe 1 in 50 shots. The weird part: when I add `Debug.Log` calls in the movement and collision code to investigate, it stops happening entirely. I'm using `transform.position +=` in `Update` to move the projectile and `OnCollisionEnter` to detect hits. Unity 2022.3, Built-in, PC.

## Expected triggering
- should-fire: true

## Rubric

### MUST
- [ ] Recognizes the **heisenbug signature** (disappears under logging) and treats "logging changes timing/perf, masking a race or frame-dependent issue" as the working frame — not a reason to dismiss it.
- [ ] Identifies the most likely **proximate cause family**: fast-moving object **tunneling** through a collider because discrete `Update`-based movement steps over the wall between physics ticks (and physics should use `FixedUpdate` / Rigidbody motion, with Continuous collision detection for fast objects).
- [ ] Explains *why* logging hides it: the added overhead slows the frame / changes step size, reducing the per-frame travel distance enough to avoid tunneling — confirming it's timing/step-size dependent.
- [ ] Recommends an **instrumentation-first** approach that does not perturb timing (e.g. record positions into an in-memory ring buffer and dump after the miss, or enable Continuous collision detection and test) rather than shipping a blind fix.
- [ ] Proposes the real fix direction: move via `Rigidbody.MovePosition` in `FixedUpdate`, set **Collision Detection = Continuous (Dynamic)**, or raycast along the travel path between frames for fast projectiles.
- [ ] Produces the required output format and states a confidence level.

### MUST NOT
- [ ] Does **not** ship a confident "here's the fix" as Confirmed/High when it hasn't reproduced the intermittent bug — confidence must be capped (Medium at most) per the intermittent fork.
- [ ] Does not advise leaving the `Debug.Log` calls in "since it works now" — that masks the bug, not fixes it.
- [ ] Does not attribute it to a generic null/logic error with no link to the timing/step-size evidence.

### Confidence disclosure
- [ ] Explicitly states confidence is capped because the bug is intermittent and unreproduced, and that a deterministic repro (or confirming Continuous collision detection eliminates it) would raise it. States what to capture without altering timing.

## Notes
Edge-case eval: tests the intermittent/heisenbug fork and the discipline of instrument-don't-perturb + capped confidence. Strong response names tunneling + FixedUpdate/Continuous detection, explains the logging-masks-timing mechanism, and proposes non-perturbing capture. Weak response: declares a fix as High confidence, or tells the user to keep the logs because "it works now."
