# Performance Debugging Checklist

A starting checklist for diagnosing Unity performance issues before deep profiling. For full profiling analysis, use the Profiler Analysis skill.

---

## 1. Define the problem precisely

- [ ] Frame rate: what is the target? What is actual?
- [ ] Which scene / moment / action causes the drop?
- [ ] Is it CPU-bound or GPU-bound?
  - In Profiler: if `Gfx.WaitForPresent` is large → GPU-bound
  - If `PlayerLoop` is large with little `Gfx.WaitForPresent` → CPU-bound
- [ ] Is it a one-time spike or a continuous drop?
- [ ] Does it happen on all platforms or a specific one?

---

## 2. Profile before fixing

- [ ] Use the Unity Profiler (Window → Analysis → Profiler) — do not guess
- [ ] Profile a **development build**, not in-editor Play mode
- [ ] Profile on the **target device** (not a powerful dev machine)
- [ ] Capture at least 100 frames during the problem moment
- [ ] Identify the top-consuming call in the CPU Profiler hierarchy

---

## 3. CPU — common culprits

### GC allocations (managed memory)
- [ ] Profiler → CPU → GC.Alloc column shows allocation in hot paths
- [ ] Common sources: string concatenation, LINQ, `foreach` on non-array collections, `new` in `Update`
- [ ] Fix: cache allocations; use `StringBuilder`; use `for` instead of `foreach` for arrays; pool objects

### Physics
- [ ] `FixedUpdate` running too many times per frame? (lower `Fixed Timestep` in Time settings)
- [ ] Too many colliders, triggers, or `OverlapSphere` calls per frame?
- [ ] Complex mesh colliders? (replace with primitive colliders where possible)

### Rendering — CPU side
- [ ] High draw call count? (Profiler → Rendering statistics)
- [ ] GPU instancing / static batching / dynamic batching enabled?
- [ ] Too many `Camera.Render` calls? (multiple cameras, reflection probes)

### Scripting
- [ ] `Find`, `FindObjectOfType`, `GetComponent` in `Update`? (cache in `Awake`/`Start`)
- [ ] Heavy `Debug.Log` calls in production build? (strip logs in release)
- [ ] Expensive operations on every frame that could run on a timer?

---

## 4. GPU — common culprits

- [ ] Overdraw: many transparent objects layered on top of each other
- [ ] Shader complexity: expensive fragment shaders on large screen-space quads
- [ ] Shadow casting: too many shadow-casting lights or high shadow distance
- [ ] Texture resolution: uncompressed or oversized textures
- [ ] Post-processing: expensive effects on lower-end hardware

---

## 5. Memory — GC pressure

- [ ] Profiler → Memory → GC Allocated shows spikes?
- [ ] Recurring GC.Collect calls? (memory allocations triggering full collection)
- [ ] Object pooling missing for frequently created/destroyed objects?
- [ ] Large arrays created and abandoned each frame?

---

## 6. Load time

- [ ] Scene load is slow? Profile with `LoadScene` timing
- [ ] Assets loaded synchronously on the main thread?
  - Use `LoadSceneAsync` / `Addressables.LoadAssetAsync`
- [ ] Audio clips set to `Load Type = Decompress on Load`? (large clips → use `Streaming`)
- [ ] Texture mipmaps generated at load time? (import with mipmaps pre-generated)

---

## 7. Mobile-specific

- [ ] Thermal throttling? (device gets hot, GPU/CPU clock down)
  - Test with consistent temperature; use device profiler tools
- [ ] Battery mode reducing performance on iOS?
- [ ] Vsync enabled? (may cap at 30 fps on some devices)
  - `Application.targetFrameRate = 60` / `QualitySettings.vSyncCount = 0`
- [ ] Texture format: use ETC2 (Android) / ASTC (Android/iOS) for compressed mobile textures

---

## 8. Quick wins (check before deep profiling)

- [ ] `Physics.autoSyncTransforms = false` if not needed
- [ ] Reduce `Shadow Distance` in Quality Settings
- [ ] Cull small objects at distance (LOD groups)
- [ ] Reduce `Pixel Light Count` in Quality Settings
- [ ] Disable real-time GI if not required
- [ ] Set `Audio Sample Rate Setting` appropriately for mobile

---

## Handoff note

This checklist covers initial triage. For deep profiling, CPU flame-graph analysis, memory allocation tracking, or GPU frame capture: use the **Profiler Analysis** or **Performance Optimization** skills.
