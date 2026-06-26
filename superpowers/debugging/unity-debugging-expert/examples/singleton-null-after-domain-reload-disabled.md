# Worked example — Singleton null on the second Play (Domain Reload disabled)

A redacted session showing the methodology catch a non-obvious cause: stale statics
when **Enter Play Mode Options** disables Domain Reload.

---

## User input

> `GameManager.Instance` works the first time I press Play, but if I stop and Play again *without* changing any code, `Instance` is null and everything NullRefs. The moment I edit a script (forcing a recompile) it works again for one run. Unity 2022.3, URP, Editor. I enabled "Enter Play Mode Options" recently to speed up iteration.
>
> ```csharp
> public class GameManager : MonoBehaviour {
>     public static GameManager Instance;
>     void Awake() => Instance = this;
> }
> ```

---

## Response (using the Unity Debugging Expert)

## Symptom
`GameManager.Instance` is null on the **second and later** Play sessions of an Editor session, but fine on the first run and fine again immediately after any recompile.

## Reproduction
Reproduced conceptually and deterministic from the description: Play (works) → Stop → Play again without recompiling (null). Recompile resets it for one run. This precise signature is the key evidence.

## Investigation
- `Instance` is a **static** field assigned in `Awake`. Statics live in the **managed domain**, not in the scene.
- The "works first time, breaks on re-Play, recompile fixes it for one run" pattern points directly at **domain lifetime**, not at scene/order/logic.
- The user enabled **Enter Play Mode Options**. With **Reload Domain disabled**, Unity does *not* tear down and rebuild the scripting domain when entering Play Mode — so static fields **keep their values from the previous session**.
- On the second Play, `Instance` still references the **previous session's `GameManager`**, which was destroyed when Play stopped. A recompile forces a domain reload, which reinitializes statics — masking the bug for exactly one run.

## Hypotheses (ranked)
1. **Stale static across Play sessions due to disabled Domain Reload** (strong). *For:* the exact "first run OK, re-Play null, recompile fixes one run" signature; the user just enabled Enter Play Mode Options. *Against:* none — every symptom fits.
2. Awake not running / wrong object (weak). *Against:* it works on the first run and after recompile with no code change, so `Awake` and wiring are fine.
3. Script Execution Order (weakest). *Against:* order wouldn't explain the dependence on recompile vs. re-Play.

## Root Cause  [Confidence: High]
**Proximate:** `Instance` is null (or points at a destroyed object) on re-Play. **Root:** with **Domain Reload disabled**, the static `Instance` is **not reset** between Play sessions; it holds the previous (now destroyed) instance, and `Awake` reassigning it isn't enough because the stale value is observed before/around teardown assumptions. The code silently relied on a domain reload zeroing statics. **High** — the signature is diagnostic; it becomes **Confirmed** by the verification below.

## Fix
Make statics correct **regardless** of the Domain Reload setting — don't disable the iteration-speed option. Reset the static explicitly when the game subsystems initialize:

```csharp
public class GameManager : MonoBehaviour {
    public static GameManager Instance;

    // Runs on entering Play Mode even when Domain Reload is disabled.
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    static void ResetStatics() => Instance = null;

    void Awake() {
        // Optional: guard against a duplicate surviving a fast Play cycle.
        if (Instance != null && Instance != this) { Destroy(gameObject); return; }
        Instance = this;
    }
}
```

Trade-off: a `RuntimeInitializeOnLoadMethod(SubsystemRegistration)` reset is the precise, low-blast-radius fix and keeps your faster iteration. Turning Domain Reload back on also "fixes" it but discards the iteration-speed benefit you turned the option on for — and leaves the latent assumption in the code for the next person.

## Verification
1. Keep Enter Play Mode Options on (Domain Reload disabled). Play → Stop → Play again **without** recompiling → confirm `Instance` is non-null and no NullRefs.
2. As a control, temporarily re-enable Domain Reload → the bug also disappears (confirms the cause).
3. Confirm no duplicate `GameManager` survives across a stop/Play cycle (the `Awake` guard).

## Prevention
- Reset any mutable **static / singleton** state via `[RuntimeInitializeOnLoadMethod]` so it never depends on a domain reload.
- Add a quick check (a debug overlay or assert) that `Instance` is freshly assigned each session.
- *Why it happened:* disabling Domain Reload skips the static-field reset; code that assumed statics start null breaks on the second Play.

## Missing info (if any)
None blocking. If you also disabled **Reload Scene**, tell me — scene-level static caches (e.g. cached `FindObjectOfType` results) need the same `RuntimeInitializeOnLoadMethod` treatment.
