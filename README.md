<div align="center">

# Unity Debugger Skill

### A structured debugging system for Unity — diagnoses any defect to a verified root cause.

**NullRefs · Lifecycle Bugs · Serialization · Editor vs Build · Coroutines · Platform Issues · Crashes**

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![Unity](https://img.shields.io/badge/Unity-2021_LTS_%E2%86%92_6-000.svg)](#compatibility)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)](superpowers/debugging/unity-debugging-expert/SKILL.md)

</div>

---

## What this is

A production-quality skill for diagnosing Unity bugs. It behaves as a Senior Unity Engineer with extensive experience debugging production games — gathering evidence, forming ranked hypotheses, and driving every defect to a verified root cause with an explicit confidence rating.

It never guesses. If the evidence is insufficient for a confident fix, it delivers an instrumentation plan instead.

---

## What it handles

- `NullReferenceException` and other runtime exceptions
- MonoBehaviour lifecycle and execution-order bugs
- Coroutine and async/await failures
- `[SerializeField]` / Inspector lost-reference issues
- Prefab reference loss and prefab override pitfalls
- Editor-only vs build-only divergence (IL2CPP stripping, AOT, path case-sensitivity)
- Platform-specific failures (iOS, Android, WebGL, console)
- Intermittent / timing / race-condition bugs
- Physics misbehavior
- Object-pool state bugs
- Input / event / callback failures
- Regressions introduced by a recent change

**Out of scope:** performance profiling, style review, and feature authoring.

---

## Repository structure

```
unity-debugger/
├── SKILL.md                    ← the skill (install this)
├── DESIGN.md                   ← engineering design spec
├── examples.md                 ← 9 worked debugging sessions
├── references.md               ← methodology, mental models, quick-lookup tables
├── references/
│   ├── null-reference-heuristics.md
│   ├── lifecycle-and-execution-order.md
│   ├── serialization-and-references.md
│   └── editor-vs-build-and-platform.md
├── examples/
│   ├── null-ref-on-additive-scene-load.md
│   ├── singleton-null-after-domain-reload-disabled.md
│   └── works-in-editor-not-in-build.md
└── evals/                      ← scenario + rubric test cases
```

At the repository root:
```
templates/
├── bug-report.md               ← bug report template
├── debug-session.md            ← working investigation log
├── reproduction-steps.md       ← minimal repro template
└── root-cause-analysis.md      ← post-mortem template

checklists/
├── general-debugging.md        ← step-by-step investigation checklist
├── build-failure.md            ← compilation and IL2CPP failures
├── webgl.md                    ← WebGL-specific issues
├── performance.md              ← performance triage (before deep profiling)
├── addressables.md             ← Addressable Asset System issues
└── networking.md               ← multiplayer and state sync issues
```

---

## Installation

### Option A — Skills directory (project-level)

```bash
git clone https://github.com/AKS97i/claude-superpowers-unity.git

mkdir -p .claude/skills
cp -R claude-superpowers-unity/superpowers/debugging/unity-debugging-expert \
      .claude/skills/unity-debugger
```

Describe your Unity bug in any session. The skill is invoked automatically when you share an error message, stack trace, or describe a Unity bug.

### Option B — Skills directory (user-level, all projects)

```bash
mkdir -p ~/.claude/skills
cp -R claude-superpowers-unity/superpowers/debugging/unity-debugging-expert \
      ~/.claude/skills/unity-debugger
```

### Option C — Paste as system prompt

Open `superpowers/debugging/unity-debugging-expert/SKILL.md` and paste it as the system prompt. No installation required.

---

## Usage

Share your bug. The skill structures its diagnosis automatically. You do not need to follow any special format — just provide what you have.

**Useful things to include:**
- The full error message and stack trace (do not truncate)
- Unity version, render pipeline, target platform
- Relevant code around the throwing site
- Reproduction steps and frequency
- Recent changes or git diff

**If you do not have a stack trace**, describe the behavior: what happens vs what should happen, when it occurs, and on which platform.

---

## Example sessions

Full worked investigations are in [`examples.md`](superpowers/debugging/unity-debugging-expert/examples.md). Brief overview:

### NullReferenceException — unassigned Inspector field
```
NullReferenceException: Object reference not set to an instance of an object
EnemyAI.TakeDamage (at Assets/Scripts/EnemyAI.cs:47)
ProjectileController.OnTriggerEnter (at Assets/Scripts/ProjectileController.cs:23)
```
→ Identified unassigned `[SerializeField]` on a prefab variant. Fix: assign in Inspector, add `Debug.Assert` in `Awake`. [Full session →](superpowers/debugging/unity-debugging-expert/examples.md#1-nullreferenceexception--health-component-missing-on-enemy)

---

### WebGL crash — IL2CPP generic stripping
```
ExecutionEngineException: Attempting to call a virtual method on a non-boxed value type.
at System.Collections.Generic.List`1[T].Add (T item)
```
→ Generic instantiation not traced by IL2CPP's static analysis. Fix: `link.xml` entry or AOT hint. [Full session →](superpowers/debugging/unity-debugging-expert/examples.md#2-webgl-build-failure--generics-stripped-by-il2cpp)

---

### Addressables — null result in build, works in Editor
→ Asset not included in a built Addressables group. Editor falls back to `AssetDatabase`; the build has no fallback. Fix: rebuild catalog, check group Build Path. [Full session →](superpowers/debugging/unity-debugging-expert/examples.md#3-addressables--asset-not-loaded-nullref-at-runtime)

---

### Memory leak — event subscription not unsubscribed
→ Static event accumulates subscriptions across scene loads; destroyed objects held by delegate list. Fix: symmetric `+=`/`-=` in `OnEnable`/`OnDisable`. [Full session →](superpowers/debugging/unity-debugging-expert/examples.md#4-memory-leak--event-subscription-not-unsubscribed)

---

### Physics tunneling — fast projectile through thin wall
→ `Discrete` collision detection skips geometry when per-step displacement exceeds wall thickness. Fix: switch to `Continuous` or use a raycast approach. [Full session →](superpowers/debugging/unity-debugging-expert/examples.md#5-physics-bug--rigidbody-tunneling-through-thin-walls)

---

### Coroutine stops unexpectedly — component disabled mid-execution
→ Unity halts all coroutines on a MonoBehaviour the moment it is disabled. Fix: persistent host or `OnEnable`/`OnDisable` restart. [Full session →](superpowers/debugging/unity-debugging-expert/examples.md#6-coroutine-stops-unexpectedly--component-disabled)

---

### Multiplayer desync after scene load
→ `NetworkTransform` sends deltas; if no movement occurred before the load, clients hold stale pre-load positions. Fix: force baseline sync post-load via `Teleport`. [Full session →](superpowers/debugging/unity-debugging-expert/examples.md#7-networking--client-state-desyncs-after-scene-load)

---

### Animator transition not firing
→ "Has Exit Time" enabled on the transition; looping animation must complete before the transition evaluates. Fix: uncheck "Has Exit Time". [Full session →](superpowers/debugging/unity-debugging-expert/examples.md#8-animator--state-transition-not-firing)

---

### Build failure — TypeLoadException on missing type
→ Type accessed only via reflection; IL2CPP stripped it. Fix: `link.xml` preservation entry. [Full session →](superpowers/debugging/unity-debugging-expert/examples.md#9-build-failure--missing-script-reference)

---

## Confidence model

Every diagnosis states a confidence level:

| Level | Meaning |
|---|---|
| **Confirmed** | Reproduced and fix verified |
| **High** | All evidence consistent; fix not yet user-verified |
| **Medium** | Consistent with evidence; alternatives not excluded |
| **Low** | Plausible; multiple live hypotheses |
| **Speculative** | Hypothesis pending missing information |

Low and Speculative findings are never presented as fact.

---

## Templates and checklists

For systematic debugging work:

| Resource | Use |
|---|---|
| [`templates/bug-report.md`](templates/bug-report.md) | Report a bug with all required fields |
| [`templates/debug-session.md`](templates/debug-session.md) | Track an active investigation |
| [`templates/reproduction-steps.md`](templates/reproduction-steps.md) | Write a minimal repro |
| [`templates/root-cause-analysis.md`](templates/root-cause-analysis.md) | Post-mortem after resolution |
| [`checklists/general-debugging.md`](checklists/general-debugging.md) | Step-by-step debugging checklist |
| [`checklists/build-failure.md`](checklists/build-failure.md) | Build and IL2CPP failure checklist |
| [`checklists/webgl.md`](checklists/webgl.md) | WebGL-specific issues |
| [`checklists/performance.md`](checklists/performance.md) | Performance triage |
| [`checklists/addressables.md`](checklists/addressables.md) | Addressables issues |
| [`checklists/networking.md`](checklists/networking.md) | Multiplayer and state sync |

---

## Compatibility

Designed to work across **Unity 2021 LTS through Unity 6**. Version-specific behavior is flagged inline. No render pipeline is assumed — Built-in, URP, and HDRP differences are noted where they matter.

---

## Contributing

Bug reports, new examples, and improved reference material are welcome. Open an issue or pull request.

---

## License

MIT. See [LICENSE](LICENSE).
