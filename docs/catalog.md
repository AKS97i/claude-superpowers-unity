# Superpower Catalog

The complete index of planned and shipped Superpowers — **61 across 21 categories**.

- **Status:** ✅ Live · 🛠️ In progress · 🗓️ Planned
- **Value / Priority:** 1–5 (5 = highest). Priority `P0`–`P3` (`P0` = ship first).
- **Audience:** `A` = all · `I` = indie/solo · `S` = studio.

> This catalog is the single source of truth for scope and prioritization. New Superpowers are added here at proposal time. See [roadmap.md](roadmap.md) for sequencing and [philosophy.md](philosophy.md) for what qualifies as a Superpower.

---

## Debugging

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Unity Debugging Expert** | Systematically root-cause runtime errors, crashes & wrong behavior | A | error + stack, code, repro, version/platform, logs | ranked hypotheses, confidence-rated root cause, minimal fix, verification, regression guard | 5 | P0 | ✅ Live |
| Crash & Native-Stack Analyzer | Decode IL2CPP/native crashes, tombstones, managed-stack reconstruction | S/A | crash logs, symbols, device info | symbolicated cause + fix path | 4 | P1 | 🗓️ |
| Console & Log Forensics | Triage noisy console/Player.log; correlate errors to causes | A | logs, Editor/Player.log | prioritized error map + next steps | 4 | P1 | 🗓️ |

## Code Review

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Unity C# Code Review** | Review Unity code for correctness, lifecycle, allocations, conventions | A | diff/files, context | findings by severity + fixes | 5 | P0 | 🗓️ |
| MonoBehaviour Lifecycle Review | Audit Awake/OnEnable/Start/Update ordering & teardown bugs | A | scripts | lifecycle risk report | 3 | P2 | 🗓️ |
| Async/Coroutine Review | Find coroutine/async/UniTask pitfalls (cancellation, domain reload) | A | scripts | issues + safe patterns | 3 | P2 | 🗓️ |

## Architecture

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Unity Architecture Advisor** | Recommend structure/patterns for a feature/system | A | requirements, constraints | options + trade-offs + recommendation | 5 | P1 | 🗓️ |
| DI / Service Layer Designer | Design DI (VContainer/Zenject) or service locator | S | needs, scale | container design + wiring | 3 | P2 | 🗓️ |
| ScriptableObject Architecture Designer | Data-driven / SO-based design | A | data needs | SO schema + flow | 4 | P2 | 🗓️ |
| Save System Architect | Robust, versioned, migratable saves | A | data, platforms | save design + migration plan | 4 | P2 | 🗓️ |
| Scene Flow & Game-State Architect | Scene loading, state machines, bootstrapping | A | flow needs | state/scene architecture | 3 | P2 | 🗓️ |

## Performance

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Performance Optimization Strategist** | Diagnose & prioritize perf work end-to-end | A | profiler data, target, symptoms | bottleneck analysis + ranked plan | 5 | P0 | 🗓️ |
| Frame-Time / CPU Hotspot Hunter | Localize main-thread spikes | A | profiler capture | hotspot list + fixes | 4 | P1 | 🗓️ |
| Draw Call & Batching Optimizer | Reduce batches (SRP batcher, GPU instancing, atlasing) | A | frame debugger, stats | batching plan | 4 | P1 | 🗓️ |
| GC / Allocation Eliminator | Kill per-frame allocations & GC spikes | A | profiler allocations, code | allocation map + zero-alloc fixes | 5 | P1 | 🗓️ |

## Memory

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Memory Leak Investigator | Find leaks/retained refs/undisposed natives | A | memory profiler snapshots | leak source + fix | 4 | P1 | 🗓️ |
| Asset Memory Footprint Auditor | Audit texture/mesh/audio memory & import settings | A | build/memory report | footprint reductions | 4 | P1 | 🗓️ |

## Addressables

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Addressables System Designer | Group/label/load architecture | S/A | content needs, platforms | addressables design | 4 | P2 | 🗓️ |
| Resources→Addressables Migration Assistant | Plan & execute migration | A | current usage | migration plan + risks | 3 | P2 | 🗓️ |
| Remote Content & Catalog Strategist | CDN, remote catalogs, updates | S | delivery needs | content-delivery design | 3 | P3 | 🗓️ |

## Build Systems

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Build Pipeline Engineer | Design/repair build scripts & automation | S/A | platforms, requirements | pipeline design | 4 | P2 | 🗓️ |
| Build Size Reducer | Shrink app / IPA / APK / AAB size | A | build report | size-reduction plan | 4 | P1 | 🗓️ |
| **Platform Build Troubleshooter** | Fix iOS/Android/console build & signing failures | A | build errors, platform | diagnosis + fix steps | 5 | P1 | 🗓️ |

## Rendering

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Render Pipeline Advisor | Choose/configure URP/HDRP/Built-in | A | project goals, platforms | pipeline recommendation + config | 4 | P2 | 🗓️ |
| Lighting & GI Optimization Expert | Bake / realtime / GI tuning | A | scene, target | lighting plan | 3 | P2 | 🗓️ |
| Render Feature / Custom Pass Engineer | Build SRP render features/passes | S | effect needs | pass design / code guidance | 3 | P3 | 🗓️ |

## Shader Development

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Shader Author & Debugger | Write/debug HLSL/ShaderLab/Shader Graph | A | shader, symptoms | working shader + explanation | 4 | P2 | 🗓️ |
| Shader Performance Optimizer | Reduce shader cost / variants | S/A | shader, GPU profile | optimization plan | 3 | P3 | 🗓️ |

## Mobile Optimization

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mobile Performance Optimizer** | End-to-end mobile performance | A | device, profiler | mobile perf plan | 5 | P1 | 🗓️ |
| Thermal & Battery Budget Advisor | Sustain framerate under thermal limits | I/A | device behavior | thermal budget plan | 3 | P3 | 🗓️ |
| Device Tiering & Compatibility Strategist | Quality tiers across devices | S/A | device matrix | tiering strategy | 3 | P3 | 🗓️ |

## Multiplayer

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Multiplayer Architecture Advisor | Topology, authority, transport choice | S/A | game type, scale | netcode architecture | 4 | P2 | 🗓️ |
| Network Authority & Ownership Designer | Server-auth vs client-auth design | S | gameplay needs | authority model | 3 | P3 | 🗓️ |

## Netcode

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Netcode for GameObjects Expert | NGO setup, RPCs, NetworkVariables | A | feature, code | NGO implementation guidance | 4 | P2 | 🗓️ |
| Net Sync & Interpolation Debugger | Fix jitter / desync / snapping | S/A | symptoms, code | sync diagnosis + fix | 4 | P2 | 🗓️ |
| Prediction & Lag Compensation Designer | Client prediction / reconciliation | S | gameplay | prediction design | 3 | P3 | 🗓️ |

## AI Gameplay

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Game AI Behavior Designer | FSM/BT/GOAP/utility AI design | A | behavior goals | AI architecture | 3 | P2 | 🗓️ |
| NavMesh & Pathfinding Troubleshooter | Fix nav / pathing issues | A | symptoms, setup | nav fix plan | 3 | P2 | 🗓️ |

## Animation

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Animation System Architect | Animator / Playables / state design | A | needs | animation architecture | 3 | P2 | 🗓️ |
| Animation Performance Optimizer | Reduce rig / animation cost | S/A | profiler, rigs | optimization plan | 3 | P3 | 🗓️ |

## Physics

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Physics Debugging & Tuning Expert | Fix jitter, tunneling, instability | A | symptoms, setup | physics diagnosis + tuning | 4 | P2 | 🗓️ |
| Deterministic / Rollback Physics Advisor | Determinism for rollback netcode | S | requirements | determinism plan | 2 | P3 | 🗓️ |

## UI

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UI Architecture Advisor | UGUI vs UI Toolkit + structure | A | UI needs | UI architecture | 4 | P2 | 🗓️ |
| UI Performance Optimizer | Fix canvas rebuilds / overdraw / batching | A | profiler, hierarchy | UI perf plan | 4 | P2 | 🗓️ |
| Responsive / Multi-Resolution UI Designer | Scale across aspect ratios / safe areas | A | targets | responsive layout plan | 3 | P3 | 🗓️ |

## Editor Tooling

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Editor Tool Builder | Custom inspectors / EditorWindows / UI Toolkit editors | S/A | tool goal | tool design + code guidance | 4 | P2 | 🗓️ |
| Workflow Automation Scripter | Asset post-processors / menu items / batch ops | S/A | workflow pain | automation script guidance | 4 | P2 | 🗓️ |
| Property Drawer & Attribute Designer | Custom drawers / attributes | S/A | data display needs | drawer design | 2 | P3 | 🗓️ |

## Asset Management

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Asset Pipeline & Import Settings Auditor | Audit import settings at scale | A | project/import report | import-settings fixes | 4 | P2 | 🗓️ |
| Project Organization & Convention Enforcer | Folder/naming/asset structure | A | project layout | reorg + convention plan | 3 | P3 | 🗓️ |
| **Version Control Hygiene Advisor** | .gitignore, LFS, meta files, YAML merge, smart-merge | A | repo setup, symptoms | VCS hygiene plan | 5 | P1 | 🗓️ |

## Profiling

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Profiler Analysis Expert** | Interpret Unity Profiler captures | A | profiler capture | bottleneck readout | 5 | P1 | 🗓️ |
| Frame Debugger Analyst | Diagnose draw-order/state from Frame Debugger | S/A | frame capture | render-path analysis | 3 | P3 | 🗓️ |

## CI/CD

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CI/CD Pipeline Architect | GameCI / Cloud Build / test pipelines | S | platforms, repo | CI/CD design | 4 | P2 | 🗓️ |
| Automated Test Pipeline Builder | Wire Unity Test Framework into CI | S/A | repo, tests | test-automation plan | 3 | P2 | 🗓️ |

## Technical Leadership

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unity Tech-Debt Auditor | Identify/prioritize Unity-specific debt | S | codebase signals | debt register + plan | 4 | P2 | 🗓️ |
| Code Standards & Convention Author | Generate team C#/Unity standards | S | team context | standards doc | 3 | P3 | 🗓️ |
| Technical Design Doc Writer | Draft Unity TDDs | S/A | feature brief | structured TDD | 3 | P2 | 🗓️ |
| Estimation & Sprint Planning Advisor | Break down / estimate Unity work | S | scope | task breakdown + estimates | 2 | P3 | 🗓️ |
| Onboarding & Knowledge-Base Builder | Onboarding docs for a Unity project | S | project | onboarding guide | 3 | P3 | 🗓️ |

## Testing (cross-cutting)

| Superpower | Purpose | Aud. | Typical inputs | Expected outputs | Val | Prio | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unity Test Authoring Expert | Write EditMode/PlayMode tests, mocking, harnesses | A | code, behavior | test plan + tests | 4 | P2 | 🗓️ |

---

## Ranking by real-world impact

We rank by:

> **impact ≈ frequency of need × audience breadth × severity of the pain × how poorly generic AI handles it unaided**

### Tier 1 — ship first

| # | Superpower | Why it ranks here |
| --- | --- | --- |
| 1 | **Unity Debugging Expert** | Debugging is the most universal, time-draining task; every developer hits it daily, and generic AI guesses badly at Unity-specific causes. |
| 2 | **Performance Optimization Strategist** | Perf problems are near-universal and high-stakes for shipping/ratings; needs methodology generic AI lacks. |
| 3 | **Unity C# Code Review** | Applies to every code change; compounding quality value across a team. |
| 4 | **Profiler Analysis Expert** | Unlocks #2; reading captures is a skill most devs lack and AI rarely does well. |
| 5 | **GC / Allocation Eliminator** | The single most common Unity perf killer; concrete, teachable, high-frequency wins. |
| 6 | **Mobile Performance Optimizer** | Mobile is Unity's largest market; the pain is acute and constant. |
| 7 | **Platform Build Troubleshooter** | Build failures block shipping entirely; urgent and frequent, with deterministic fixes. |
| 8 | **Version Control Hygiene Advisor** | Cheap to build, prevents catastrophic team-wide pain (meta-file/merge disasters). Punches far above its weight. |

### Tier 2 — broad value, slightly narrower or dependent
Architecture Advisor · Build Size Reducer · UI Performance Optimizer · Memory Leak Investigator · Asset Import Auditor · Netcode for GameObjects Expert · Editor Tool Builder · Unity Test Authoring Expert.

### Tier 3 — specialist, high ceiling, narrower audience
Shader Author/Optimizer · Render Feature Engineer · HDRP/lighting deep-dives · Prediction & Lag Compensation · Deterministic Physics · Remote Catalog Strategist · Estimation & Onboarding systems.

**Why this shape:** the top of the list maximizes *breadth × frequency × severity* while targeting exactly where unaided AI is weakest (Unity-specific reasoning). Specialist rendering/netcode systems have high ceilings but serve fewer developers per release, so they follow once the broad-impact core is solid. Build and version-control systems rank surprisingly high because their failures are *blocking* and their fixes are deterministic and teachable — high value per unit of effort.
