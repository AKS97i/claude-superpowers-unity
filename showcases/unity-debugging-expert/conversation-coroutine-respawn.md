# Showcase conversation — "my respawn coroutine sometimes never fires"

A redacted end-to-end session. Messy real-world input → a structured, confidence-rated
diagnosis that finds the root cause instead of the obvious-but-wrong one.

> **Setup:** Unity Debugging Expert active (via `SKILL.md`, or `prompt.md` pasted as system context).

---

**User**

> My respawn logic just stops working sometimes. I start a coroutine that waits 3 seconds then respawns the player, but occasionally the player never respawns. No errors in the console. I've tried increasing the wait time but it didn't help.

**Assistant**

Before I dig in, two quick essentials so I diagnose the right runtime, not a guess:

- **Unity version + render pipeline + platform?**
- Can you share the **method that starts the coroutine** and where it lives? "Sometimes never fires, no errors" is the signature of a coroutine whose owner stops running — the surrounding code matters more than the wait itself.

(Heads-up: increasing the wait time not helping is already a useful clue — it points away from "the timer is wrong" and toward "the coroutine isn't running at all.")

---

**User**

> Unity 2021.3, Built-in, PC. Here's the code:
>
> ```csharp
> public class Enemy : MonoBehaviour {
>     void OnDeath() {
>         gameObject.SetActive(false);          // hide the enemy
>         StartCoroutine(RespawnAfterDelay());
>     }
>     IEnumerator RespawnAfterDelay() {
>         yield return new WaitForSeconds(3f);
>         Respawn();
>     }
> }
> ```

**Assistant**

## Symptom
A respawn coroutine started in `OnDeath()` sometimes never completes — the player/enemy never respawns, with no console errors.

## Reproduction
Reproduced from the code: `OnDeath()` disables the GameObject and *then* starts the coroutine on that same object. Deterministic — it will fail every time this path runs (not actually intermittent; see below).

## Investigation
- `StartCoroutine` is called on the `Enemy` MonoBehaviour **immediately after `gameObject.SetActive(false)`** — i.e. on a component whose GameObject is now inactive.
- Coroutines are driven by the MonoBehaviour's runner, which **only ticks while the GameObject is active and the component enabled**. Disabling the object stops its coroutines, and they do **not** resume on re-enable.
- "No errors" fits: this isn't an exception — the coroutine just never advances. "Sometimes" is likely "every time `OnDeath` runs this way," with other respawns coming from a code path that doesn't disable first.
- Increasing `WaitForSeconds` had no effect — consistent with the coroutine never running at all, not with a too-short timer.

## Hypotheses (ranked)
1. **Coroutine stopped because its owner was disabled in the same method** (strong). *For:* `SetActive(false)` precedes `StartCoroutine` on the same object; matches "no error, never completes, longer wait doesn't help." *Against:* none.
2. `Respawn()` is failing silently (weak). *Against:* you'd typically see *some* effect or error, and the timer change wouldn't be irrelevant.
3. A genuine race/timing issue (weakest). *Against:* the behavior is fully explained by the disable-then-start ordering; no timing needed.

## Root Cause  [Confidence: High]
**Proximate:** `RespawnAfterDelay` never advances past the yield. **Root:** the coroutine is started on a GameObject that was just **deactivated in the same method**, so Unity never ticks it. High confidence — the cause is evident in the code; **Confirmed** once you verify the fix below.

## Fix
Run the timed logic on an object that **stays active**. Smallest options first:

```csharp
// Option A — let a persistent manager own the respawn timer.
void OnDeath() {
    gameObject.SetActive(false);
    RespawnManager.Instance.RespawnAfter(3f, transform.position, prefab);
}
```

```csharp
// Option B — keep the object active; hide only the visuals/collider.
void OnDeath() {
    _renderer.enabled = false;
    _collider.enabled = false;
    StartCoroutine(RespawnAfterDelay());   // owner stays active, coroutine ticks
}
```

Trade-off: Option A centralizes respawn timing (cleanest if you pool enemies); Option B is a one-file change but you must re-enable everything you disabled. Avoid "just don't disable the object" if disabling is what you actually want gameplay-wise — use a manager.

## Verification
1. Trigger `OnDeath`; confirm respawn fires after ~3s every time.
2. Add a temporary `Debug.Log` at the top of `RespawnAfterDelay` — with the bug it never logs; after the fix it always does.

## Prevention
- Never start a coroutine on an object you're about to disable; own timed logic on a persistent manager.
- *Why it happened:* a coroutine stops when its owning GameObject/component is disabled and does not resume on re-enable.

## Missing info (if any)
None blocking. If respawn *also* fails on a path that doesn't call `SetActive(false)`, share that path — that would point at `Respawn()` itself (hypothesis 2).

---

**Why this is a good showcase:** the obvious fix ("increase the wait" / "it's a race condition") is wrong; the system reads the *ordering* in the code, separates proximate from root cause, rates confidence honestly, and leaves a prevention rule. Mapped from [`evals/coroutine-stops-on-disable.md`](../../superpowers/debugging/unity-debugging-expert/evals/coroutine-stops-on-disable.md).
