# Eval: static singleton is null on the second Play (domain reload disabled)

## Input

> My `GameManager.Instance` works the first time I press Play, but if I stop and press Play again without recompiling, `Instance` is null and everything NullRefs. If I change a script (forcing a recompile) it works again. Unity 2022.3, URP, PC. I turned on "Enter Play Mode Options" to speed up iteration.
>
> ```csharp
> public class GameManager : MonoBehaviour {
>     public static GameManager Instance;
>     void Awake() => Instance = this;
> }
> ```

## Expected triggering
- should-fire: true

## Rubric

### MUST
- [ ] Connects the symptom to **Enter Play Mode Options with Domain Reload disabled**: static fields are **not reset** between Play sessions, so `Instance` retains a stale reference to the previous session's (now destroyed) object.
- [ ] Explains why a recompile "fixes" it: recompiling triggers a domain reload, which reinitializes statics — masking the bug.
- [ ] Identifies that the stale `Instance` points at a destroyed object, so it either is non-null-but-destroyed or was cleared — and that relying on `Awake` to set it assumes a fresh domain.
- [ ] Proposes a fix that does not depend on domain reload: e.g. reset statics with `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]`, or clear/assign defensively, or guard the singleton against a destroyed instance (Unity `== null` check).
- [ ] Produces the required output format and states a confidence level.

### MUST NOT
- [ ] Does not tell the user to simply turn Domain Reload back on as the *only* fix without explaining that the code has a latent assumption that should be made robust (the project enabled the option deliberately for iteration speed).
- [ ] Does not misattribute it to script execution order or scene loading.
- [ ] Does not claim "Confirmed" without verifying across stop/Play cycles.

### Confidence disclosure
- [ ] States confidence (High — the "works after recompile, fails on re-Play with EnterPlayMode options" signature is diagnostic) and what would confirm it (toggle Domain Reload back on → bug disappears; or add a `RuntimeInitializeOnLoadMethod` reset → bug disappears with the option still on).

## Notes
This is an edge case that generic AI commonly misses — it requires knowing that disabling Domain Reload leaves statics dirty across Play sessions. Strong response cites `RuntimeInitializeOnLoadMethod(SubsystemRegistration)` to null/reset statics so code is correct **regardless** of the option. Weak response: "add a null check in Update" (treats the symptom) or "you have a race in Awake."
