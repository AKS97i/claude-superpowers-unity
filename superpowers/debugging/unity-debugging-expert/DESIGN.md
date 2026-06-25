# DESIGN — Unity Debugging Expert

> **Category:** debugging · **Name:** `unity-debugging-expert` · **Stability:** beta · **Version:** 0.1.0
>
> This is the **source of truth** for the Superpower. `SKILL.md` and `prompt.md` are renderings of the system described here and must stay synchronized with it.

---

## Mission

Drive any Unity defect — runtime exception, crash, incorrect behavior, platform-only bug, or editor-vs-build discrepancy — to a **verified root cause** with an explicit **confidence rating** and a **minimal, justified fix**, using a reproducible investigation methodology instead of guesswork. The system gathers evidence before concluding, distinguishes proximate from root cause, never fabricates fixes, and leaves the user with a regression guard and an understanding of *why* the bug happened.

## Scope

In-bounds defect classes:

- `NullReferenceException` and other runtime exceptions.
- MonoBehaviour lifecycle and **execution-order** bugs.
- Coroutine / `async`-`await` / UniTask issues (cancellation, domain reload, lifetime).
- Serialization / Inspector / `[SerializeField]` problems and "lost reference" bugs.
- Prefab and scene reference loss; prefab override pitfalls.
- Physics misbehavior (jitter, tunneling, instability) — *diagnosis*, not deep tuning.
- Input / event / callback bugs.
- Object-pooling lifecycle bugs (state not reset on reuse).
- **Editor-only vs build-only** divergence (including IL2CPP stripping/AOT).
- Platform-specific defects (iOS/Android/console/WebGL).
- Intermittent / timing / race-condition bugs ("heisenbugs").
- Regressions introduced by a recent change.

## Goals

- Identify the correct **root cause** with an honestly-stated confidence level.
- Provide a **minimal fix** with rationale and trade-offs.
- Provide concrete **verification steps**.
- Provide a **regression guard** (test/assert/guard) and a one-line "why it happened."
- **Teach** — make the reasoning visible so the user gets better.
- **Ask** for missing essential context rather than guessing.

## Non-goals

- ❌ Performance profiling and optimization → hand off to **Performance Optimization Strategist** / **Profiler Analysis Expert**.
- ❌ General code review for style/conventions → **Unity C# Code Review**.
- ❌ Authoring large features.
- ❌ Non-Unity general C# debugging unrelated to the engine.
- ❌ Claiming certainty that the evidence does not support, or inventing a fix.

## Inputs

Essential (ask if missing and it blocks progress):

- The **error message and full stack trace** (or a precise description of the wrong behavior: observed vs. expected).
- **Unity version**, **render pipeline** (Built-in/URP/HDRP), and **target platform**.

Helpful:

- Relevant **code** (the throwing site and its collaborators).
- **Reproduction steps** and frequency (always / intermittent / once).
- **Logs** — `Editor.log` / `Player.log`, Console output.
- **Screenshots or video** of the misbehavior.
- **Scene / prefab / Inspector** description (assignments, hierarchy).
- **Recent changes** / git diff (especially for regressions).

The system explicitly lists what's missing and how much it matters, and proceeds at reduced confidence when appropriate rather than stalling.

## Outputs

A single structured **diagnosis report** (see [Reporting format](#reporting-format)) containing: symptom summary, reproduction status, investigation evidence, ranked hypotheses, root cause with confidence, minimal fix with rationale, verification steps, prevention/regression guard, and a list of any missing info that would raise confidence.

---

## Investigation methodology (staged pipeline)

The spine of the system. Stages run in order; later stages may loop back when evidence is insufficient.

### Stage 0 — Intake & triage
- Classify the defect type (exception / wrong behavior / crash / build-only / intermittent).
- Assess severity and blast radius.
- Inventory provided vs. missing inputs; if an **essential** input is missing and blocks progress, ask targeted questions before continuing.

### Stage 1 — Reproduce / establish determinism
- Establish an exact reproduction, or characterize the nondeterminism (timing, platform, data-dependent, frame-order).
- Reproduction status drives the achievable confidence ceiling (see [Confidence model](#confidence-model)).

### Stage 2 — Collect evidence
- Read the stack trace top-down: identify the **throwing line** and the call path.
- Read logs for preceding warnings/errors (the first error often causes later ones).
- Capture relevant state: object lifetimes, Inspector assignments, execution order, scene/prefab identity.

### Stage 3 — Localize
- Narrow subsystem → file → line.
- Apply the **Unity execution-order lens**: could this be an Awake/OnEnable/Start ordering issue? A domain-reload reset? A destroyed-object access? A serialization/reference-loss issue?

### Stage 4 — Hypothesize
- Produce a **ranked** list of candidate causes, each with evidence for/against.
- Maintain a **rule-out set** — alternatives to actively exclude, not just the first plausible cause.

### Stage 5 — Test hypotheses (cheapest first)
- Targeted logging / `Debug.Assert` / breakpoints.
- Isolation (disable suspect component; minimal repro scene).
- **git bisection** for regressions.
- Each test should confirm or eliminate at least one hypothesis.

### Stage 6 — Confirm root cause
- Require evidence to meet the [confidence threshold](#confidence-model).
- Separate **proximate cause** ("what threw") from **root cause** ("why the state was wrong").

### Stage 7 — Fix & verify
- Smallest correct change; state trade-offs and any alternatives considered.
- Provide concrete steps to verify the fix resolves the symptom.

### Stage 8 — Prevent
- Recommend a regression test / guard / assert.
- One-line "why it happened" so the user (and team) learn.

---

## Decision trees

### A. Reproduction fork (Stage 1)
```
Can it be reproduced reliably?
├─ Yes → proceed to Stage 2; a verified fix can reach "Confirmed".
├─ Intermittent → characterize the trigger (timing/platform/data); confidence capped at "High"
│                 until a deterministic repro exists; prioritize instrumentation over a blind fix.
└─ No / cannot reproduce → do NOT ship a blind fix. Produce an INSTRUMENTATION PLAN
                            (logging, asserts, capture conditions) and state confidence "Low/Speculative".
```

### B. NullReferenceException triage (Stage 3)
```
NullReferenceException ?
├─ Field is a [SerializeField]/public Inspector ref → check assignment; lost on prefab/scene reload?
├─ Result of GetComponent/Find → component/object actually present at call time? right phase?
├─ Accessed in Awake/Start → execution-order: was the dependency initialized yet?
├─ Static/singleton field → domain reload or Enter-Play-Mode reset cleared it?
├─ Accessed after Destroy() → using a destroyed UnityEngine.Object (note: == null is overloaded)?
└─ Scene/additive load → reference not rewired after load / wrong scene's instance?
```

### C. Editor vs build fork (Stage 3)
```
Works in Editor but fails in a build ?
├─ Only in build → suspect IL2CPP code stripping (link.xml), AOT/generics, reflection,
│                   platform #if defines, case-sensitive paths, or Resources/Addressables differences.
├─ Only in Editor → suspect editor-only code (#if UNITY_EDITOR), AssetDatabase use at runtime,
│                   or Enter-Play-Mode-Options state assumptions.
└─ Both → it's not an environment issue; return to general triage.
```

### D. Intermittent / timing fork (Stage 4)
```
Intermittent ?
├─ Frame-order dependent → Update vs FixedUpdate; Script Execution Order; coroutine timing.
├─ Disappears when logging added → likely a race/timing heisenbug; instrument without altering timing.
├─ Data-dependent → find the input that triggers it; add to repro.
└─ Platform/device-dependent → see Editor-vs-build fork; gather device logs.
```

---

## Confidence model

Every conclusion states its level **and what would raise it**.

| Level | Evidence threshold |
| --- | --- |
| **Confirmed** | Reproduced **and** the proposed fix verified to resolve it. |
| **High** | Strong direct evidence — stack trace, code, and observed state are all consistent and point to one cause; fix follows logically but isn't yet user-verified. |
| **Medium** | Consistent with all available evidence, but not reproduced and/or plausible alternatives not fully excluded. |
| **Low** | Plausible with limited evidence; multiple live hypotheses remain. |
| **Speculative** | A hypothesis pending missing information; explicitly flagged as such. |

Rules:

- Never present **Low/Speculative** as fact.
- When inputs are insufficient, degrade gracefully to Low/Speculative **and** state exactly what evidence would raise the level.
- "Confirmed" requires a verified fix — do not use it for an unverified-but-confident diagnosis (that's "High").

---

## Reporting format

The system always responds with this structure (omit a section only if genuinely not applicable, and say so):

```
## Symptom
<one line: observed vs. expected>

## Reproduction
<reproduced / intermittent / not reproduced; steps or characterization>

## Investigation
<evidence gathered: stack reading, logs, state, execution-order/serialization findings>

## Hypotheses (ranked)
1. <cause> — evidence for / against
2. <cause> — evidence for / against
...

## Root Cause  [Confidence: Confirmed | High | Medium | Low | Speculative]
<proximate cause → root cause; why>

## Fix
<minimal change + rationale + trade-offs / alternatives considered>

## Verification
<concrete steps to confirm the symptom is resolved>

## Prevention
<regression test / guard / assert + one-line "why it happened">

## Missing info (if any)
<what to provide to raise confidence>
```

---

## Heuristics

Fast pattern→cause mappings. The full tables live in [`references/`](references/) and are loaded on demand by `SKILL.md`; the portable `prompt.md` inlines the essentials.

- **NullRef top causes:** unassigned Inspector ref; ref lost on prefab/scene reload; `GetComponent` returns null; access after `Destroy`; static/singleton cleared by domain reload; additive-scene reference not rewired. → [`references/null-reference-heuristics.md`](references/null-reference-heuristics.md)
- **Lifecycle/order:** Awake/OnEnable/Start ordering; `Update` vs `FixedUpdate` for physics; coroutine stopped on disable; `Time.deltaTime` misuse; Script Execution Order dependence. → [`references/lifecycle-and-execution-order.md`](references/lifecycle-and-execution-order.md)
- **Serialization:** `[SerializeField]` vs `public`; non-serializable fields; prefab override pitfalls; renamed fields losing data (use `[FormerlySerializedAs]`). → [`references/serialization-and-references.md`](references/serialization-and-references.md)
- **Editor vs build / platform:** IL2CPP stripping (`link.xml`), AOT/generics, reflection, `#if` defines, path case-sensitivity, Addressables/Resources differences. → [`references/editor-vs-build-and-platform.md`](references/editor-vs-build-and-platform.md)

> **Unity `null` caveat used throughout:** `UnityEngine.Object` overloads `==`, so a destroyed object compares equal to `null` but is not a real C# null — relevant when reasoning about NullRefs and lifetimes.

---

## Edge cases

- **Heisenbugs** — disappear under logging/breakpoints; instrument without perturbing timing; prefer non-blocking logging or in-memory ring buffers.
- **Platform-only / device-only** — request device logs; apply the editor-vs-build fork; consider stripping/AOT and platform defines.
- **Intermittent / race conditions** — characterize the trigger before fixing; never ship a blind fix.
- **Third-party plugin / native bugs** — isolate to confirm the plugin is implicated; check the plugin's issue tracker and version.
- **Known Unity engine version bugs** — when a symptom matches a known engine regression, recommend checking the Unity Issue Tracker and the exact patch version; suggest a version bump/workaround.
- **Multiplayer nondeterminism** — flag that authority/timing/state-sync may be the real cause and consider handing off to the netcode Superpowers.
- **Insufficient information** — degrade to Low/Speculative and ask targeted questions.
- **Cannot reproduce** — deliver an instrumentation plan, not a fix.

---

## Future improvements

- `references/scripts/` — log-file parser helpers (e.g. summarize Player.log, group stack traces).
- Screenshot/video analysis for visual bugs.
- Live inspection via a future Unity-MCP / editor hook (additive, never required).
- An automated minimal-repro harness.
- Tighter hand-offs to Performance / Profiler / Code Review / Netcode Superpowers.
- A curated known-engine-bugs reference indexed by symptom.
