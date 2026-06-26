# Eval: pooled object reuses stale state on respawn

## Input

> I pool my bullets to avoid GC. After a while, some bullets spawn already "dead" or moving in the wrong direction — like they remember their last life. Fresh (non-pooled) bullets are always fine. Unity 2021.3, Built-in, PC.
>
> ```csharp
> public class Bullet : MonoBehaviour {
>     public Vector3 velocity;
>     int hitsRemaining = 3;
>     void OnEnable() { /* nothing */ }
>     void Update() {
>         transform.position += velocity * Time.deltaTime;
>         if (hitsRemaining <= 0) Pool.Return(this);
>     }
>     void OnHit() { if (--hitsRemaining <= 0) Pool.Return(this); }
> }
> ```

## Expected triggering
- should-fire: true

## Rubric

### MUST
- [ ] Identifies the **pooling lifecycle bug**: a pooled object is *reused*, not recreated, so fields like `hitsRemaining` and `velocity` retain their values from the previous life; `OnEnable` doesn't reset them.
- [ ] Explains why fresh (`Instantiate`d) bullets are fine — a new object gets field initializers / a fresh `hitsRemaining = 3`, whereas a returned-to-pool object kept `hitsRemaining` at 0.
- [ ] Proposes resetting all per-life state on acquisition — in `OnEnable` or a dedicated `ResetState()`/`OnSpawn()` the pool calls — (`hitsRemaining = 3`, `velocity` set by the spawner, clear any timers/trails/coroutines).
- [ ] Notes the broader pooling principle: anything mutated during an object's life must be re-initialized on reuse (including disabling/re-enabling trails, stopping coroutines, resetting Rigidbody velocity).
- [ ] Produces the required output format and states a confidence level.

### MUST NOT
- [ ] Does not blame GC or suggest abandoning pooling (the user pooled deliberately).
- [ ] Does not propose only fixing `velocity` while missing `hitsRemaining` (or vice-versa) — both are stale state.
- [ ] Does not claim "Confirmed" without verifying the reset resolves it.

### Confidence disclosure
- [ ] States confidence (High — "remembers its last life" + pooling + no reset is diagnostic) and what would confirm it (log `hitsRemaining` on spawn → see it start at 0 for reused bullets; after adding the reset → always 3).

## Notes
Strong response generalizes to "reset all per-life state on acquire" and lists the usual suspects (counters, velocity, coroutines, trails, Rigidbody). Prevention: a pool that calls a single `OnSpawn`/`IPoolable.Reset` contract so new state can't be forgotten. Weak response: "set hitsRemaining in OnEnable" only, ignoring velocity and the general principle.
