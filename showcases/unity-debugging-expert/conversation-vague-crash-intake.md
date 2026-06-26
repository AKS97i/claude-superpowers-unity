# Showcase conversation — "my game crashes sometimes, can you fix it?"

A redacted session showing the system's **honesty under insufficient information**:
it refuses to invent a cause, runs a tight intake tied to its methodology, and gives the
user a concrete way to capture the evidence — then diagnoses once the log arrives.

> **Setup:** Unity Debugging Expert active (via `SKILL.md`, or `prompt.md` pasted as system context).

---

**User**

> My game crashes sometimes. Can you fix it?

**Assistant**

I can — but I won't guess a cause from "crashes sometimes," because that's how you get a confident-sounding wrong answer. A crash has very different root causes depending on a few facts, so here's a short intake (this is Stage 0 of the method, not stalling):

1. **What does "crash" mean?** Editor freeze/hang, the player `.exe`/app closing, an exception in the Console, or an out-of-memory kill? Each points at a different layer.
2. **Platform + Unity version + render pipeline?** A native crash on Android is a different investigation from a managed exception in the Editor.
3. **Any log or message?** The single most useful artifact. Even "no message" is information.
4. **When does it happen?** Always at a certain action, after playing a while, on load? Frequency (1/10 runs vs. random)?

**Why I'm asking, not answering:** without a log or a repro I can only produce Speculative hypotheses, and a blind "fix" to a crash usually masks it rather than resolving it.

**To get the log** (this alone often makes the cause obvious):

- **Editor:** the Console + `Editor.log` (Help → "Open Editor Log Location" / `~/Library/Logs/Unity/Editor.log` on macOS, `%LOCALAPPDATA%\Unity\Editor\Editor.log` on Windows).
- **Windows build:** `Player.log` under `%USERPROFILE%\AppData\LocalLow\<Company>\<Product>\`.
- **Android:** `adb logcat` while reproducing — that captures native crashes the in-game console can't.

Paste whatever you can grab (and answers to 1–4) and I'll take it from there.

---

**User**

> It's the standalone Windows build closing instantly, no popup. Unity 2022.3, URP, PC. Happens a couple minutes into a level, not at a fixed moment. Here's the tail of Player.log:
>
> ```text
> ...
> Mono: successfully reloaded assembly
> Total: 12873.4 MB ... allocated
> Could not allocate memory: System out of memory!
> <RI.Hidden>
> Crash!!!
> ```

**Assistant**

## Symptom
The standalone Windows (URP, 2022.3) player closes with no dialog a couple of minutes into a level — `Player.log` ends with `Could not allocate memory: System out of memory!` then `Crash!!!`.

## Reproduction
Not reproduced here, but the log is decisive: this is an **out-of-memory crash**, not a logic exception (no managed stack trace; an explicit allocation failure with ~12.8 GB allocated). "A couple minutes in, not a fixed moment" fits a **leak/unbounded growth** rather than a single bad call.

## Investigation
- `System out of memory!` immediately before `Crash!!!` = the process died trying to allocate, i.e. memory exhaustion, not a NullRef/segfault in your code.
- 12.8 GB allocated is far past a normal level budget → something **accumulates without being released**: spawned objects not destroyed/pooled, growing collections, textures/RenderTextures/meshes created at runtime and never `Destroy`/`Release`d, or subscriptions/caches that never clear.
- Time-to-crash scaling with play time is the classic leak signature.

## Hypotheses (ranked)
1. **Runtime memory leak** — objects/assets allocated each frame or per spawn and never freed (managed or native). *For:* steady growth to 12.8 GB, time-dependent crash. *Against:* need the Memory Profiler to name the exact owner.
2. **Unbounded managed collection** (e.g. a log/event list that only ever grows). *For:* same growth pattern. *Against:* would usually be smaller than 12 GB unless it holds heavy objects.
3. A single huge allocation (giant texture/mesh) at a moment that happens to land "a couple minutes in." *Against:* less consistent with gradual timing.

## Root Cause  [Confidence: Medium]
**Most likely a runtime memory leak** — allocations that grow with play time until the OS refuses one. **Medium**, not higher, because the log proves *OOM* but not *which* allocations; the Memory Profiler will name the owner and move this to High/Confirmed. (Note: this is now drifting toward a **performance/memory** investigation — if it turns out to be pure optimization rather than a leak bug, the Memory Leak Investigator / Profiler Superpowers are the better tools; I'll get you to the cause first.)

## Fix
Find the leak before changing code:

1. Open **Window → Analysis → Memory Profiler**, take a snapshot early in the level and another after ~90s, and **diff** them — the object types that grew are your leak.
2. Likely culprits to check in that growth list: instantiated objects never `Destroy`d (pool them), runtime-created `Texture2D`/`RenderTexture`/`Mesh`/`Material` never `Destroy`/`Release`d, event handlers / static caches that only accumulate.
3. Fix the specific owner (destroy/release/unsubscribe; cap or evict caches).

## Verification
1. After the fix, watch allocated memory across a 10-minute session — it should plateau, not climb.
2. Re-diff two Memory Profiler snapshots far apart in time → the previously-growing type no longer grows.

## Prevention
- Add a lightweight memory watchdog/log during development (`Profiler.GetTotalAllocatedMemoryLong()`), and a soak test that plays a level for N minutes and asserts memory stays under budget.
- *Why it happened:* something allocated per-frame/per-spawn was never released, so memory grew until an allocation failed and the OS killed the process.

## Missing info (if any)
The **Memory Profiler snapshot diff** — that's the one artifact that turns "a leak" into "*this* type, allocated *here*." Share it and I'll pinpoint the owner.

---

**Why this is a good showcase:** the first reply produces **zero invented causes** — it runs a focused intake, explains *why* each input matters, and hands the user the exact commands to capture a log. The moment real evidence arrives, the diagnosis is specific and honestly rated (Medium, with the path to High) and it flags the handoff boundary to the memory/performance Superpowers. Mapped from [`evals/insufficient-info-vague-bug.md`](../../superpowers/debugging/unity-debugging-expert/evals/insufficient-info-vague-bug.md).
