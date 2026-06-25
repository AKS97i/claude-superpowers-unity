# Worked example — NullReferenceException on additive scene load

A canonical, redacted session showing the methodology end-to-end.

---

## User input

> Getting a NullReferenceException when I load my UI scene additively. The `GameManager` reference on my `HUDController` is null but it's assigned in the Inspector. Unity 6, URP, running in the Editor.
>
> ```
> NullReferenceException: Object reference not set to an instance of an object
>   at HUDController.Start () [0x00012] in HUDController.cs:24
> ```
>
> ```csharp
> public class HUDController : MonoBehaviour {
>     [SerializeField] private GameManager gameManager; // assigned in Inspector
>     void Start() {
>         _score = gameManager.Score; // line 24
>     }
> }
> ```
> The HUD scene is loaded with `SceneManager.LoadScene("HUD", LoadSceneMode.Additive)` from the main scene at runtime. `GameManager` lives in the main scene.

---

## Response (using the Unity Debugging Expert)

## Symptom
`HUDController.Start()` throws `NullReferenceException` at line 24 because `gameManager` is null, even though the field is assigned in the Inspector.

## Reproduction
Reproduced conceptually from the description: load the HUD scene additively at runtime → `Start` runs → `gameManager` is null. (Reliable, deterministic.)

## Investigation
- The throwing line dereferences `gameManager` — that's the only candidate on line 24.
- The field *is* assigned in the Inspector, so this isn't a "forgot to drag it in" case.
- Critical detail: `GameManager` is in the **main scene**, `HUDController` is in the **HUD scene**, loaded **additively at runtime**. Unity does **not** serialize references *across scenes* — a serialized reference can only point within the same scene/prefab. So the Inspector assignment is either a stale/broken cross-scene link or was never truly persisted across the scene boundary.

## Hypotheses (ranked)
1. **Cross-scene reference not resolved** (strong). The serialized `gameManager` cannot legitimately point at an object in another scene; at runtime in the loaded HUD scene it deserializes to null. *Evidence for:* the two objects live in different scenes loaded separately; Unity's documented behavior. *Evidence against:* none.
2. Execution order (weaker). If both were in one scene, `Start` reading another object's `Awake`-initialized state could be an issue — but here the field itself is null, so ordering isn't the proximate cause.
3. Field genuinely unassigned (weakest). User states it's assigned; and cross-scene assignment wouldn't survive anyway.

## Root Cause  [Confidence: High]
**Proximate:** `gameManager` is null at line 24. **Root:** the reference is a **cross-scene reference**, which Unity cannot serialize; when the HUD scene loads additively, the field deserializes to null. Confidence is High (consistent with documented Unity behavior and the scene layout); it would be **Confirmed** by reproducing and verifying the fix resolves it.

## Fix
Resolve the dependency **at runtime** instead of via a serialized cross-scene field. Minimal options, smallest first:

```csharp
// Option A: a simple service locator / singleton lookup
void Start() {
    gameManager = GameManager.Instance;          // resolved at runtime
    if (gameManager == null) {
        Debug.LogError("GameManager not found — is the main scene loaded?", this);
        return;
    }
    _score = gameManager.Score;
}
```
Trade-off: introduces a singleton/locator. If you already use a DI container (VContainer/Zenject), inject `GameManager` instead. Avoid `FindObjectOfType` in hot paths, but it's acceptable for one-time `Start` resolution if you don't want a singleton.

## Verification
1. Enter Play Mode, load the HUD scene additively as in production.
2. Confirm no NullRef and that `_score` reflects `GameManager.Score`.
3. Test the failure path: load the HUD scene *without* the main scene → expect the logged error, not a crash.

## Prevention
- Add a guard + clear error (above) so a missing manager is diagnosable, not a bare NullRef.
- Add a PlayMode test that loads the HUD scene additively and asserts `HUDController` initializes.
- *Why it happened:* Unity cannot serialize references across separately-loaded scenes; cross-scene wiring must be resolved at runtime.

## Missing info (if any)
None blocking. If you use a DI framework, share it and I'll give the injection-based fix instead of the singleton.
