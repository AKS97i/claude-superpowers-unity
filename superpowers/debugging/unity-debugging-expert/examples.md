# Unity Debugger — Example Sessions

Worked investigations demonstrating the skill's methodology across common Unity bug classes.

---

## 1. NullReferenceException — Health Component Missing on Enemy

**User input:**
```
NullReferenceException: Object reference not set to an instance of an object
EnemyAI.TakeDamage (UnityEngine.GameObject attacker) (at Assets/Scripts/EnemyAI.cs:47)
ProjectileController.OnTriggerEnter (UnityEngine.Collider other) (at Assets/Scripts/ProjectileController.cs:23)
```

**Output:**

### Symptom
`NullReferenceException` at `EnemyAI.TakeDamage` line 47 — a method on a component that should be present on every enemy.

### Reproduction
Not yet reproduced; single report. Likely consistent given projectile collision is a common path.

### Investigation
Stack trace (top-down):
- Throwing line: `EnemyAI.cs:47` — inside `TakeDamage`, something on line 47 is null
- Caller: `ProjectileController.OnTriggerEnter:23` — trigger overlap detected, called `TakeDamage` on `other.gameObject`

The call `other.GetComponent<EnemyAI>().TakeDamage(...)` (or similar) would throw if the colliding object has no `EnemyAI`, or if a field inside `TakeDamage` is null.

Line 47 is inside `TakeDamage`, so the null is **inside the method**, not the call to it. Most likely: a field like `healthComponent` that was never assigned.

### Hypotheses (ranked)
1. `healthComponent` (or similar) is a `[SerializeField]` reference that is unassigned on one or more enemy prefabs — **most likely**; evidence: line 47 inside the method, not at the call site
2. `GetComponent<HealthComponent>()` called at runtime returned null (component not present on this enemy variant)
3. `other.gameObject` carries a non-enemy collider that happened to have an `EnemyAI` component in the wrong state

### Root Cause  [Confidence: Medium]
A field accessed on line 47 of `TakeDamage` is null. Most likely an Inspector-assigned `[SerializeField]` reference that was never set on one enemy prefab variant.

Would be **High** with the source code of `EnemyAI.cs` around line 47.

### Fix
1. Read `EnemyAI.cs` line 47 — identify the null field.
2. If `[SerializeField]`: open the prefab in the Inspector, assign the reference. Add `Debug.Assert(healthComponent != null, "HealthComponent unassigned", this)` in `Awake` to catch it early.
3. If `GetComponent` result: add a null check and log a clear error:
   ```csharp
   var health = GetComponent<HealthComponent>();
   if (health == null) { Debug.LogError($"No HealthComponent on {name}", this); return; }
   health.ApplyDamage(amount);
   ```

### Verification
- Open each enemy prefab → Inspector shows the reference populated.
- Play the scene → no `NullReferenceException` on projectile impact.
- Remove the assignment from one prefab → `Assert` fires immediately in Awake.

### Prevention
Add `[field: SerializeField]` with `RequireComponent` or validate all references in `Awake` using `Debug.Assert`. **Why it happened:** the prefab was duplicated from a base and the new reference field was never assigned.

### Missing info
Source of `EnemyAI.cs` around line 47 would confirm which field and raise confidence to **High** or **Confirmed**.

---

## 2. WebGL Build Failure — Generics Stripped by IL2CPP

**User input:**
```
Unity 2022.3 LTS, WebGL, URP.
Game runs fine in the Editor but crashes immediately on the loading screen in the WebGL build.
Player.log shows:
  ExecutionEngineException: Attempting to call a virtual method on a non-boxed value type.
  at System.Collections.Generic.List`1[T].Add (T item)
```

**Output:**

### Symptom
`ExecutionEngineException` on WebGL build at `List<T>.Add` — game crashes on the loading screen. Works in Editor.

### Reproduction
Reproducible on WebGL build; does not occur in Editor. This is a **build-only** issue.

### Investigation
`ExecutionEngineException: Attempting to call a virtual method on a non-boxed value type` at `List<T>.Add` is a classic IL2CPP AOT (Ahead-of-Time compilation) generic instantiation failure. IL2CPP compiles C# to C++ at build time; if a generic type instantiation (`List<MyStruct>`) is only reached via reflection or late binding — never directly referenced in code — IL2CPP may not generate the concrete C++ for it, causing a runtime crash.

WebGL uses IL2CPP exclusively.

### Hypotheses (ranked)
1. A generic type (`List<T>`, `Dictionary<K,V>`, etc.) is instantiated only via reflection or a code path IL2CPP's static analysis does not trace — **most likely** given the exact error message
2. A `link.xml` stripping rule removed required type metadata
3. A third-party plugin relies on reflection-based generic invocation not covered by IL2CPP AOT tables

### Root Cause  [Confidence: High]
IL2CPP failed to generate the concrete `List<T>.Add` implementation for a specific `T` because that generic instantiation is never referenced statically — only through a reflected or dynamically-constructed code path. The AOT compiler skipped it; the runtime has no concrete code to call.

### Fix
Option A — add an AOT hint file (`link.xml` / `mcs.rsp`):
```xml
<!-- Assets/link.xml -->
<linker>
  <assembly fullname="mscorlib">
    <type fullname="System.Collections.Generic.List`1[[YourNamespace.YourStruct, Assembly-CSharp]]" preserve="all"/>
  </assembly>
</linker>
```

Option B — add a direct static reference so IL2CPP sees the instantiation:
```csharp
// In any class that is definitely compiled
#if !UNITY_EDITOR
[RuntimeInitializeOnLoadMethod]
static void AotWorkaround() {
    // Force IL2CPP to generate concrete code for these generics
    _ = new List<YourStruct>();
}
#endif
```

Use the stack trace to identify the exact `T` in `List<T>`.

### Verification
- Rebuild for WebGL.
- Load the game — loading screen should not crash.
- Check Player.log for the `ExecutionEngineException` — it should be absent.

### Prevention
Add a `WebGL` build step that runs `CheckStrippingLevel` in Unity Build Settings (set to `Minimal` or add `link.xml`). **Why it happened:** IL2CPP cannot trace generic instantiations that only appear at runtime through reflection.

---

## 3. Addressables — Asset Not Loaded, NullRef at Runtime

**User input:**
```
Unity 2021.3, PC, Built-in render pipeline.
I'm loading a prefab via Addressables: 
  var handle = Addressables.LoadAssetAsync<GameObject>(key);
  await handle.Task;
  var instance = Instantiate(handle.Result);
Works in Editor, NullRef in build on handle.Result.
```

**Output:**

### Symptom
`handle.Result` is null after `await handle.Task` in a build — asset not loaded despite no thrown exception. Works in Editor.

### Reproduction
Reproducible in build; Editor works. Editor-vs-build divergence.

### Investigation
When `LoadAssetAsync` completes without throwing but `Result` is null, the operation status is `Failed`. Common causes in builds but not Editor:
- The asset is not included in an Addressables group that is bundled into the build (Editor falls back to direct asset database access)
- The Addressable key does not match any built catalog entry (key mismatch, remote catalog not loaded)
- The remote catalog URL is wrong in the build profile

Checking `handle.Status == AsyncOperationStatus.Succeeded` before reading `handle.Result` would surface the actual error.

### Hypotheses (ranked)
1. Asset is not included in any built Addressables group — only available via AssetDatabase in Editor — **most likely** given Editor-vs-build divergence
2. The catalog was built with a different key (e.g., address string changed, label mismatch)
3. Remote catalog fetch failed in the build environment (wrong URL, no network)

### Root Cause  [Confidence: High]
The Addressables asset is in a group that is not marked for build inclusion, or the group was never rebuilt after the asset was added. The Editor's `EditorAddressablesImpl` falls back to `AssetDatabase.LoadAssetAtPath`, masking the missing bundle; the player has no such fallback.

### Fix
1. Check the operation result before using it:
   ```csharp
   var handle = Addressables.LoadAssetAsync<GameObject>(key);
   await handle.Task;
   if (handle.Status != AsyncOperationStatus.Succeeded) {
       Debug.LogError($"Addressables load failed for '{key}': {handle.OperationException}");
       return;
   }
   var instance = Instantiate(handle.Result);
   ```
2. Open **Window → Asset Management → Addressables → Groups** — confirm the asset's group has **Build Path** and **Load Path** set to the target (e.g., `LocalBuildPath` / `LocalLoadPath` for local bundles).
3. Run **Build → New Build → Default Build Script** (not just Play mode).
4. Use **Window → Asset Management → Addressables → Event Viewer** during play to confirm load events.

### Verification
- Build and run → no NullRef.
- The `handle.Status` check path never fires.
- Removing the asset from its group → the error log fires immediately with a clear message.

### Prevention
Always check `handle.Status` on Addressables results. Add an integration test that loads each key in a standalone player. **Why it happened:** the asset was added to the project after the last Addressables build; the catalog was stale.

---

## 4. Memory Leak — Event Subscription Not Unsubscribed

**User input:**
```
Unity 2022.3, Android, URP.
After playing through several levels, the game becomes progressively slower and eventually crashes.
The Profiler shows GC allocations growing continuously even on scenes with no new object creation.
No specific exception.
```

**Output:**

### Symptom
Progressive memory growth across scene loads → crash on Android. GC allocations grow even on "empty" scenes.

### Reproduction
Reproducible: play several levels, observe memory growth in Profiler.

### Investigation
Continuous GC allocation growth across scenes when no new objects are intentionally created is a classic **leaked event subscription** or **static reference** pattern:
- A MonoBehaviour subscribes to a `static` event or `UnityEvent` in `OnEnable`/`Awake`/`Start` but never unsubscribes in `OnDisable`/`OnDestroy`.
- The destroyed (but referenced) object's GC root is held by the event delegate list.
- As scenes reload, new instances subscribe but old ones are never collected.

Android crashes earlier because of tighter memory limits.

### Hypotheses (ranked)
1. MonoBehaviour subscribes to a `static` C# event and never unsubscribes — each scene load adds another subscription, old objects stay in memory — **most likely**
2. A `static` list or dictionary accumulates scene-local objects that are never cleared on scene unload
3. A coroutine or `async` task holds a reference to destroyed objects, preventing GC

### Root Cause  [Confidence: High]
A static event (or a long-lived object's event) has accumulated dangling subscriptions from destroyed MonoBehaviours. Each scene load registers new handlers; none deregister on scene unload. The delegate list holds strong references to the subscribers, preventing GC.

### Fix
For every `+= EventHandler` in `OnEnable` or `Start`, add a matching `-= EventHandler` in `OnDisable` or `OnDestroy`:
```csharp
void OnEnable() {
    GameEvents.OnLevelComplete += HandleLevelComplete;
}

void OnDisable() {
    GameEvents.OnLevelComplete -= HandleLevelComplete;
}
```

To find all unbalanced subscriptions:
1. In the Profiler, use the **Memory** module → **All Objects** filter → look for `System.Action` or delegate objects growing per scene.
2. Grep for `+=` in scripts that have `OnEnable`/`Start` and check that each has a matching `-=` in `OnDisable`/`OnDestroy`.

### Verification
- Profile across 3 level loads → GC allocation in the Memory module stays flat.
- Android build no longer crashes.

### Prevention
Use `IDisposable` wrappers for subscriptions, or require a lint rule that flags `+=` without a corresponding `-=` in the same class. **Why it happened:** event subscriptions were added during feature development without adding the symmetric unsubscription.

---

## 5. Physics Bug — Rigidbody Tunneling Through Thin Walls

**User input:**
```
Unity 2021.3, PC, Built-in.
Fast-moving projectile (Rigidbody) passes through thin walls. Collision detection = Discrete.
The wall is a standard Box Collider, ~0.1 units thick.
```

**Output:**

### Symptom
Fast projectile passes through a thin wall — tunneling. Discrete collision detection misses the wall.

### Reproduction
Reproducible: fire projectile at sufficient speed toward a 0.1-unit wall.

### Investigation
Tunneling occurs when a Rigidbody moves more than its own collider thickness in a single physics step. With `Discrete` collision detection, Unity only checks overlap at each fixed step — if the projectile's per-step displacement exceeds the wall thickness, it skips through.

At 60 Hz `FixedUpdate`, a projectile at 50 units/second moves ~0.83 units per step — eight times the wall thickness.

### Hypotheses (ranked)
1. Discrete collision detection + fast velocity + thin wall → physics step skips the geometry — **confirmed by geometry and settings**
2. Collider layer not included in the projectile's collision matrix
3. Rigidbody `Is Kinematic` bypasses physics resolution

### Root Cause  [Confidence: High]
`Discrete` collision detection does not perform sweep tests between physics steps. At the projectile's velocity, the per-step displacement exceeds the wall's 0.1-unit thickness, so the projectile begins one step on one side of the wall and ends the next step on the other side — no overlap is ever detected.

### Fix
Change the projectile Rigidbody's **Collision Detection** to `Continuous` (or `Continuous Dynamic` if both objects move):

In Inspector: Rigidbody → Collision Detection → **Continuous**

For very high-speed projectiles, consider a raycast approach instead:
```csharp
void FixedUpdate() {
    if (Physics.Raycast(transform.position, rb.velocity.normalized,
                        out var hit, rb.velocity.magnitude * Time.fixedDeltaTime)) {
        HandleHit(hit);
        Destroy(gameObject);
    }
}
```

The raycast approach is cheaper than `Continuous Dynamic` and handles extreme speeds.

### Verification
- Fire the projectile at the same speed → it stops on the wall.
- Increase speed 10× → still no tunneling.

### Prevention
Set all fast-moving Rigidbodies to `Continuous` collision detection by default. Add a validation script that warns when a Rigidbody is `Discrete` and its speed exceeds a threshold relative to the thinnest collider it could hit. **Why it happened:** the default `Discrete` mode is suitable for most objects but not for fast projectiles against thin geometry.

---

## 6. Coroutine Stops Unexpectedly — Component Disabled

**User input:**
```
Unity 2022.3. I start a coroutine on a MonoBehaviour and it stops partway through for no reason.
The object is not destroyed. There's no exception. It just stops.
```

**Output:**

### Symptom
Coroutine halts mid-execution without exception or object destruction.

### Reproduction
Not yet reproduced precisely; behavior is described as "stops partway through for no reason."

### Investigation
Unity coroutines are tied to the MonoBehaviour that starts them. A coroutine stops under any of these conditions (no exception required):
1. The MonoBehaviour is **disabled** (`enabled = false`)
2. The GameObject is **deactivated** (`SetActive(false)`)
3. The MonoBehaviour is **destroyed**
4. `StopCoroutine` / `StopAllCoroutines` is called
5. A `domain reload` occurred (Enter Play Mode, script recompile)

Because there is no exception, condition 1 or 2 is most likely — something in the code path disables the component or deactivates the GameObject while the coroutine is yielding.

### Hypotheses (ranked)
1. The MonoBehaviour or its GameObject is disabled mid-coroutine by another script — **most likely** given no exception
2. `StopAllCoroutines()` called from another context
3. Domain reload (unlikely in a shipping build, possible in Editor)

### Root Cause  [Confidence: Medium]
The MonoBehaviour hosting the coroutine is being disabled (or its GameObject deactivated) while the coroutine is in a `yield` suspension. Unity halts all coroutines on a MonoBehaviour the moment it becomes disabled.

Would be **High** with the coroutine source and evidence of what triggers the disable.

### Fix
Option A — run the coroutine on a persistent host:
```csharp
// Start the coroutine on a GameObject that will not be disabled
CoroutineRunner.Instance.StartCoroutine(MyCoroutine());
```

Option B — use `OnDisable`/`OnEnable` to restart:
```csharp
IEnumerator _activeCoroutine;

void OnEnable() {
    _activeCoroutine = MyCoroutine();
    StartCoroutine(_activeCoroutine);
}

void OnDisable() {
    if (_activeCoroutine != null) StopCoroutine(_activeCoroutine);
}
```

Option C — switch to `async/await` with a `CancellationToken` if the logic can tolerate it (not tied to component lifecycle).

### Verification
- Add `Debug.Log` at the end of the coroutine — confirm it reaches completion.
- Add `Debug.Log` in `OnDisable` of the hosting MonoBehaviour — confirm disable is or is not called.

### Prevention
Document which components host long-running coroutines and ensure they are not disabled externally. Consider using a dedicated coroutine-runner singleton for global coroutines. **Why it happened:** Unity's coroutine lifetime is coupled to the MonoBehaviour's enabled state, which is easy to forget when the disable is caused by another system.

### Missing info
The coroutine source code and which GameObject/component hosts it would raise confidence to **High**.

---

## 7. Networking — Client State Desyncs After Scene Load

**User input:**
```
Unity 2022.3, Netcode for GameObjects (NGO) 1.7, PC multiplayer.
After loading a new scene additively, client-side objects appear in the wrong position.
Host sees correct positions. Clients see stale pre-load positions.
```

**Output:**

### Symptom
After additive scene load in NGO, client objects are at pre-load positions; host is correct.

### Reproduction
Reproducible: trigger additive scene load → clients see wrong positions.

### Investigation
In NGO, `NetworkObject` positions are not automatically re-synced after a scene load unless the host explicitly sends updated state. Common causes:
- `NetworkTransform` reconciles only on delta; if no movement occurs post-load, clients never receive an update
- `OnSceneLoaded` on clients fires before the host has finished spawning objects in the new scene context
- `NetworkObject` references are rewired per-scene; if a client's scene reference points to the old scene's instance, it reads the pre-load transform

### Hypotheses (ranked)
1. `NetworkTransform` delta sync skips objects that haven't moved since before the load — client state is stale — **most likely**
2. Client `OnSceneLoaded` callback fires before the host sends post-load spawn messages
3. Object pooling across scenes reuses a `NetworkObject` without resetting its `NetworkTransform` baseline

### Root Cause  [Confidence: Medium]
`NetworkTransform` sends deltas; if an object did not move between the last sync and the scene load, clients receive no update and hold the pre-load position. The host's local Transform is correct; it never sends a redundant full-state update.

### Fix
Force a full state sync post-load on the host:
```csharp
// On Host, after additive scene load completes
void OnSceneLoaded(Scene scene, LoadSceneMode mode) {
    if (!IsServer) return;
    foreach (var netObj in FindObjectsOfType<NetworkObject>()) {
        if (netObj.TryGetComponent<NetworkTransform>(out var nt)) {
            nt.Teleport(netObj.transform.position, netObj.transform.rotation,
                        netObj.transform.localScale);
        }
    }
}
```

Alternatively, use a `ClientRpc` to force clients to snap to the authoritative position immediately after load.

### Verification
- Load the additive scene → client positions match host within one frame.
- Artificially delay the client's scene-loaded callback → positions still sync correctly.

### Prevention
Add a post-scene-load sync step to the scene management system for all `NetworkTransform` objects. **Why it happened:** `NetworkTransform` optimizes bandwidth by sending only deltas; a scene load does not trigger a baseline resync.

### Missing info
NGO version and whether `NetworkTransform` interpolation is enabled would refine the fix approach.

---

## 8. Animator — State Transition Not Firing

**User input:**
```
Unity 2021.3, PC, URP.
My Animator has a transition from "Idle" to "Run" triggered by a bool parameter "IsRunning".
Setting Animator.SetBool("IsRunning", true) does nothing. The character stays in Idle.
```

**Output:**

### Symptom
`Animator.SetBool("IsRunning", true)` does not trigger "Idle → Run" transition.

### Reproduction
Reproducible.

### Investigation
When `SetBool` has no visible effect, the most common causes are:
1. **"Has Exit Time" is enabled** on the transition — the Idle animation must complete its current loop before the transition is evaluated
2. **Transition conditions** are misconfigured — the trigger is set but the condition logic doesn't match
3. The parameter name is wrong (typo — `SetBool` with a wrong name silently does nothing)
4. The Animator Controller is not the one assigned on this GameObject
5. The Animator is in a Sub-State Machine and the transition exists in the parent but not the sub-machine

### Hypotheses (ranked)
1. "Has Exit Time" is checked on the transition — **most likely** for a simple Idle→Run on a looping animation
2. Parameter name typo — `SetBool` fails silently
3. The transition's condition is checking the parameter in the wrong direction (IsRunning == false)

### Root Cause  [Confidence: Medium]
The "Idle → Run" transition has **Has Exit Time** enabled. The Idle animation loops and the exit time is near the end of the clip, so the transition is queued but only fires once the current loop completes — creating apparent lag or appearing not to fire at all on short clips.

### Fix
1. Select the "Idle → Run" transition in the Animator window.
2. In the Inspector: **uncheck "Has Exit Time"** (for immediate response to input).
3. Set **Transition Duration** to 0.1–0.25 s for a smooth blend.
4. Verify the **Condition** is `IsRunning` → `true`.

To catch name mismatches at compile time:
```csharp
static readonly int IsRunningHash = Animator.StringToHash("IsRunning");
animator.SetBool(IsRunningHash, true);
```

### Verification
- Enter Play Mode → setting `IsRunning = true` transitions immediately.
- Setting `IsRunning = false` returns to Idle without waiting for the Run animation to complete.

### Prevention
Use `Animator.StringToHash` for all parameter references to catch typos at compile time. Disable "Has Exit Time" by default on any transition driven by gameplay input. **Why it happened:** Unity's default transition settings include "Has Exit Time", which is appropriate for cinematic cutscenes but wrong for responsive character controllers.

---

## 9. Build Failure — Missing Script Reference

**User input:**
```
Unity 2022.3, Android.
Build fails with:
  Error building Player: Exception: Error: TypeLoadException: Could not load type
  'MyGame.InventorySystem.ItemDatabase' from assembly 'Assembly-CSharp'.
Works in Editor.
```

**Output:**

### Symptom
Android build fails: `TypeLoadException` for `ItemDatabase` in `Assembly-CSharp`. Works in Editor.

### Reproduction
Reproducible on Android build; Editor runs fine.

### Investigation
`TypeLoadException: Could not load type` on IL2CPP (Android) when the Editor works means one of:
1. The class is conditionally excluded by a `#if` platform define that excludes Android
2. IL2CPP stripping removed the type because no static reference to it survives the linker pass
3. The class inherits from or uses a type that was stripped
4. The type is in a separate assembly or package that is not referenced in the Android build's assembly list

Editor uses Mono, which resolves types lazily at runtime; IL2CPP resolves them at build time.

### Hypotheses (ranked)
1. `ItemDatabase` or a type it depends on is being stripped by IL2CPP's managed code stripping — **most likely** for a `TypeLoadException` that only occurs in an IL2CPP build
2. `#if !UNITY_ANDROID` (or similar) wraps the class definition
3. The class is only instantiated via reflection (e.g., `Activator.CreateInstance`, `JsonUtility.FromJson`) and IL2CPP doesn't trace it

### Root Cause  [Confidence: High]
`ItemDatabase` is instantiated or referenced only through reflection (e.g., `JsonUtility`, `Resources.Load<ScriptableObject>`, or a serialization library) and never through a direct code reference that IL2CPP's static analysis can trace. The type is stripped during the IL2CPP build.

### Fix
Add `ItemDatabase` to `link.xml` to preserve it:
```xml
<!-- Assets/link.xml -->
<linker>
  <assembly fullname="Assembly-CSharp">
    <type fullname="MyGame.InventorySystem.ItemDatabase" preserve="all"/>
  </assembly>
</linker>
```

Or set **Edit → Project Settings → Player → Other Settings → Managed Stripping Level** to `Minimal` (less targeted, larger build).

### Verification
- Rebuild for Android → no `TypeLoadException`.
- Confirm `link.xml` is in `Assets/` and has no syntax errors.

### Prevention
Any type only ever reached through reflection, `Resources.Load`, or a serialization system needs a `link.xml` entry. Set up a build validation step that runs the stripped build in a simulator before shipping. **Why it happened:** IL2CPP performs static analysis to determine which types are reachable; reflection-only code paths are invisible to the linker.
