# Eval: coroutine silently stops when the GameObject is disabled

## Input

> My respawn logic just stops working sometimes. I start a coroutine that waits 3 seconds then respawns the player, but occasionally the player never respawns. No errors in the console. Unity 2021.3, Built-in pipeline, PC.
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

## Expected triggering
- should-fire: true

## Rubric

### MUST
- [ ] Identifies that `StartCoroutine` is called on a MonoBehaviour that is being **disabled in the same method** (`SetActive(false)` immediately before `StartCoroutine`), so the coroutine never runs (or stops immediately).
- [ ] Explains that a coroutine stops when its owning GameObject/component is disabled and does not resume on re-enable.
- [ ] Proposes a fix that runs the coroutine on a still-active owner (e.g. a persistent manager / spawner), or restructures so the object isn't disabled before/while the coroutine must run (e.g. use a separate manager, or `Invoke`/timer on an active object, or disable renderer/collider instead of the whole GameObject).
- [ ] Produces the required output format (Symptom / Reproduction / Investigation / Hypotheses / Root Cause / Fix / Verification / Prevention).
- [ ] States a confidence level.

### MUST NOT
- [ ] Does not attribute it to a generic "race condition" without identifying the disable-then-coroutine cause.
- [ ] Does not claim "Confirmed" (the fix isn't verified within the session).
- [ ] Does not invent console errors that the user said don't exist.

### Confidence disclosure
- [ ] States what would raise confidence (e.g. confirming `OnDeath` is the only place respawn starts; reproducing).

## Notes
Strong response: root cause at **High** confidence (the bug is evident from the code), proximate ("coroutine never advances") vs. root ("owner disabled in the same frame the coroutine is started") distinguished, and a prevention note (don't disable an object you need to run logic on; use a manager). Weak response: suggests increasing the wait time, or blames `WaitForSeconds`/`timeScale` without spotting the `SetActive(false)`.
