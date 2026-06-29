# Unity Debugger — References

Core reference material for the Unity Debugger skill. Detailed lookup tables are in the `references/` folder and loaded on demand.

---

## Debugging philosophy

**Gather evidence first, conclude second.** The most expensive mistake in debugging is committing to a fix before confirming the root cause. Every fix attempt that is wrong wastes time, adds risk, and can mask the real problem.

**Proximate vs root cause.** What threw is not always why the state was wrong. Fix the state, not just the symptom. A `NullReferenceException` at line 47 is the proximate cause; the field being unassigned in a prefab variant is the root cause.

**Confidence is not binary.** Every diagnosis has a confidence level. State it explicitly. Low confidence with a clear instrumentation plan is more valuable than high-confidence guessing.

**Reproducibility is everything.** If you cannot reproduce a bug, you cannot confirm a fix. An intermittent bug that you "fixed" but cannot confirm is a bug you have not fixed.

---

## Unity-specific mental models

### The Unity null trap

`UnityEngine.Object` overloads `==` and `!=`. A destroyed object returns `true` for `== null` but is **not** a C# null. Consequences:

- `?.` null-conditional operator does NOT catch a destroyed `UnityEngine.Object` — it calls the overloaded `==` which returns `true`, but the null-conditional only checks for actual C# null. Behavior: the `?.` branch IS taken (null-conditional fires) but the underlying object may throw if accessed directly.
- `ReferenceEquals(obj, null)` bypasses the overload and checks for true C# null.
- A destroyed object's `==` override fires in `if (obj == null)` checks — this works as intended for destroy checks.
- The `??` null-coalescing operator also bypasses the overload. Do not use `??` with `UnityEngine.Object`.

Use `if (obj != null)` for destroyed-object checks. Avoid `?.` and `??` on `UnityEngine.Object` references.

### MonoBehaviour lifecycle order

Within a single frame, execution order is:
1. `Awake` (all objects) → `OnEnable` → `Start` (all objects with Start not yet called)
2. Then per-frame: `FixedUpdate` (physics steps) → `Update` → `LateUpdate`
3. Rendering between `Update` and `LateUpdate`

Key ordering rules:
- `Awake` runs before `Start`, even across different objects in the same frame
- `Awake` order across objects is **not guaranteed** unless Script Execution Order is set
- `Start` runs on the first frame after the object is active
- A component's `Start` is called before any `Update` for that component

Coroutines:
- Coroutines run after `Update` in the same frame they are started
- A coroutine on a disabled MonoBehaviour or inactive GameObject does not run
- Domain reload (entering/exiting Play Mode, script recompile) stops all coroutines

### Serialization rules

Unity serializes:
- `public` fields of serializable types
- `private` fields with `[SerializeField]`
- Fields that are NOT `static`, NOT `readonly`, NOT `const`
- Types: primitives, `string`, `Vector2/3/4`, `Color`, `Rect`, `LayerMask`, `AnimationCurve`, `Gradient`, `GameObject`, `Component` subclasses, and `[Serializable]` classes/structs

Unity does **not** serialize:
- `Dictionary<K,V>` — use `[Serializable]` wrapper classes
- Properties (only fields)
- `null` for Unity Object types (stored as "missing" reference, not null)
- Generic types (except `List<T>`)
- Interfaces

Renamed fields lose their serialized data. Use `[FormerlySerializedAs("oldName")]` to migrate.

### IL2CPP and stripping

IL2CPP compiles C# to C++ before building. The managed code stripper removes types and methods not reachable from the build's entry points.

Types accessed only through:
- `System.Reflection`
- `Activator.CreateInstance`
- `JsonUtility.FromJson<T>` (generic type parameter not traced in some configurations)
- `Resources.Load<T>` with a runtime type string
- Dynamic invocation

...may be stripped. Preserve them via `link.xml` or by adding a direct static reference.

WebGL, iOS, and Switch always use IL2CPP. Android defaults to IL2CPP since Unity 2022.

---

## Quick-lookup tables

### NullReferenceException — top causes

| Cause | How to confirm | Fix |
|---|---|---|
| `[SerializeField]` ref unassigned | Open prefab in Inspector | Assign in Inspector; `Debug.Assert` in `Awake` |
| Ref lost on prefab/scene reload | Check prefab overrides; check scene serialization | Reassign; use `FindObjectOfType` fallback |
| `GetComponent` returned null | Add null check + log after call | Verify component is on the GameObject |
| Access after `Destroy` | Add log in `OnDestroy`; check caller | Check `!= null` before access; use events |
| Static/singleton cleared by domain reload | Check `[RuntimeInitializeOnLoadMethod]` | Initialize lazily; use `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]` |
| Additive scene ref not rewired | Check where ref is set vs when scene loads | Rewire in `SceneManager.sceneLoaded` callback |

Full table: [`references/null-reference-heuristics.md`](references/null-reference-heuristics.md)

---

### Lifecycle and execution order — common pitfalls

| Symptom | Likely cause | Fix |
|---|---|---|
| `NullRef` in `Awake` accessing another object's component | Awake order not guaranteed | Move to `Start`, or set Script Execution Order |
| Feature doesn't work until second frame | Logic in `Start` depends on another object's `Start` | Use events or explicit initialization order |
| Coroutine stops unexpectedly | MonoBehaviour or GameObject disabled | Use persistent host, or restart in `OnEnable` |
| Physics doesn't apply every frame | Using `Update` for physics changes | Move to `FixedUpdate` |
| Camera lag / jitter | Camera `Update` vs subject `LateUpdate` | Move camera to `LateUpdate` |
| `Time.deltaTime` gives fixed step value | Called from `FixedUpdate` | Use `Time.fixedDeltaTime` in `FixedUpdate`; `Time.deltaTime` in `Update` |

Full table: [`references/lifecycle-and-execution-order.md`](references/lifecycle-and-execution-order.md)

---

### Serialization — common pitfalls

| Symptom | Likely cause | Fix |
|---|---|---|
| Inspector value resets on play | Field not serializable (wrong type or missing `[SerializeField]`) | Check field type; add `[SerializeField]` |
| Renamed field loses data | Serialized name changed | Add `[FormerlySerializedAs("oldName")]` |
| Changes not saved in prefab | Editing prefab instance, not asset | Edit via prefab mode or apply override |
| Dictionary contents lost | `Dictionary` not Unity-serializable | Use `[Serializable]` key-value list wrapper |
| `[Serializable]` class not shown in Inspector | Missing no-arg constructor, or unsupported field type | Add default constructor; check field types |

Full table: [`references/serialization-and-references.md`](references/serialization-and-references.md)

---

### Editor-vs-build divergence — common causes

| Works in | Fails in | Cause | Fix |
|---|---|---|---|
| Editor | Build | IL2CPP type stripping | `link.xml`; direct static reference |
| Editor | Build | AOT generic instantiation | AOT hint; static reference to generic |
| Editor | Build | `AssetDatabase` call at runtime | Guard with `#if UNITY_EDITOR` |
| Editor | Build | Case-insensitive path (Windows → Linux/macOS) | Always match case in `Resources` paths |
| Editor | Build | Platform `#if` excludes runtime code | Review `#if` scopes |
| Build | Editor | `#if UNITY_EDITOR` wraps required runtime code | Move code out of `#if UNITY_EDITOR` |
| Editor | iOS/Switch/WebGL | Reflection-only type access | `link.xml` preservation |
| Editor | IL2CPP platforms | Generics accessed via reflection | AOT hint or static reference |

Full table: [`references/editor-vs-build-and-platform.md`](references/editor-vs-build-and-platform.md)

---

## Instrumentation patterns

When a bug cannot be reproduced, deliver an instrumentation plan rather than a blind fix.

### Targeted logging

```csharp
// Log state at the point of failure
void TakeDamage(float amount) {
    Debug.Log($"[TakeDamage] healthComponent={healthComponent}, amount={amount}", this);
    healthComponent.ApplyDamage(amount);
}
```

### Assert on assumptions

```csharp
void Awake() {
    Debug.Assert(healthComponent != null, "HealthComponent must be assigned", this);
    Debug.Assert(spawnPoint != null, "SpawnPoint must be assigned", this);
}
```

### Lifecycle breadcrumbs

```csharp
void OnEnable()  => Debug.Log($"[{name}] OnEnable  frame={Time.frameCount}");
void OnDisable() => Debug.Log($"[{name}] OnDisable frame={Time.frameCount}");
void OnDestroy() => Debug.Log($"[{name}] OnDestroy frame={Time.frameCount}");
```

### Frame-numbered logging for timing bugs

```csharp
Debug.Log($"[{GetType().Name}] {nameof(Start)} frame={Time.frameCount} scene={gameObject.scene.name}");
```

### Heisenbug-safe ring buffer

For timing-sensitive bugs where `Debug.Log` alters behavior, log to an in-memory buffer and dump on failure:

```csharp
static readonly Queue<string> _log = new(64);

static void RingLog(string msg) {
    if (_log.Count >= 64) _log.Dequeue();
    _log.Enqueue($"{Time.frameCount}: {msg}");
}

static void DumpLog() {
    foreach (var line in _log) Debug.Log(line);
}
```

---

## Version-specific gotchas

| Unity Version | Issue | Notes |
|---|---|---|
| ≤ 2021.x | `Physics.Raycast` GC allocation | Fixed in 2022+ |
| 2021.x | Enter Play Mode Options: Domain Reload disabled — singletons not reset | Check `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]` |
| 2022.x | `Animator.CrossFade` behavior change | Check Animator State Machine transition settings |
| 2022.3+ | Managed Stripping Level defaults more aggressive | Review `link.xml` on upgrade |
| Unity 6 | `FindObjectOfType` deprecated in some contexts | Use `FindFirstObjectByType` / `FindAnyObjectByType` |
| Unity 6 | `Physics.OverlapSphere` API changes | Review non-alloc variants |

Always check the Unity Issue Tracker for the exact patch version when a symptom matches a known regression.
