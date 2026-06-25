# Reference — Lifecycle & execution order

Timing bugs are among the hardest Unity defects because the code is "correct" but runs at the wrong moment.

## MonoBehaviour message order (per object, simplified)

```
Awake            # once, when the object is created (even if disabled later). All Awakes run before any Start.
OnEnable         # each time the object/component becomes enabled
Start            # once, before the first Update, only if the component is enabled
FixedUpdate      # physics step (may run 0..n times per frame)
Update           # once per frame
LateUpdate       # once per frame, after all Updates
OnDisable        # when disabled
OnDestroy        # when destroyed
```

Key consequences:

- **All `Awake()` calls complete before any `Start()`.** So `Start` is the safe place to read *other* objects' state initialized in their `Awake`. Reading cross-object state in `Awake` is the classic order-of-initialization NullRef.
- **Order between different objects' `Awake`/`Start` is undefined** unless you set **Script Execution Order** (Project Settings → Script Execution Order) or initialize lazily.
- `OnEnable` runs *after* `Awake` but can run *many* times; don't put one-time setup there.

## Update vs FixedUpdate

| Put here | What |
| --- | --- |
| `FixedUpdate` | Rigidbody forces/velocity, physics queries that must align with the physics step |
| `Update` | Input polling, frame-rate-dependent logic, non-physics movement (using `Time.deltaTime`) |
| `LateUpdate` | Camera follow, anything that must read final transforms of the frame |

- Mixing physics writes into `Update` causes **jitter and nondeterminism** (variable timing vs. fixed step).
- `FixedUpdate` may run zero or multiple times per rendered frame — don't assume 1:1 with `Update`.
- Use `Time.deltaTime` in `Update`, `Time.fixedDeltaTime` in `FixedUpdate`.

## Coroutines

- A coroutine started via `StartCoroutine` is owned by the MonoBehaviour; it **stops when the component/GameObject is disabled or destroyed** and does **not** auto-resume on re-enable.
- A coroutine on a soon-to-be-disabled object is a common "my logic just stops" bug. Run long-lived coroutines on a persistent manager, or use `async`/UniTask with explicit cancellation.
- `yield return null` waits one frame; `WaitForSeconds` is affected by `Time.timeScale`; `WaitForSecondsRealtime` is not.

## async/await & domain reload

- `async` tasks are **not** tied to MonoBehaviour lifetime by default — they can keep running after Play Mode exits or the object is destroyed, touching dead objects. Use `CancellationToken`s (UniTask's `GetCancellationTokenOnDestroy()` is ideal).
- ⚠️ **Unity 6+ / Enter Play Mode Options:** with domain reload disabled, static state and lingering tasks may **survive** between Play sessions. Guard static initialization and cancel tasks on teardown.

## Confirmation tactics

- Log `Time.frameCount` + method name to see the actual call order.
- Temporarily set Script Execution Order to test an ordering hypothesis (then prefer a code-level fix).
- For "logic stopped" bugs, log in `OnDisable` to see whether the owner was disabled when the coroutine died.
