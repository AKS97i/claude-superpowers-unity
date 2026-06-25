# Worked example — Works in the Editor, fails in the Android build

Shows the editor-vs-build fork, honest confidence, and an instrumentation-first response when evidence is incomplete.

---

## User input

> My save system works perfectly in the Editor but crashes/does nothing on my Android build. I serialize save data with `JsonUtility`… actually no, I switched to Newtonsoft Json.NET to support polymorphic data. No error in the Editor. On device the save file is empty and the game resets. Unity 2022.3, IL2CPP, Android.

(No device log provided yet.)

---

## Response (using the Unity Debugging Expert)

## Symptom
Save/load works in the Editor but on Android (IL2CPP) the save file ends up empty and progress resets — observed only in the player build.

## Reproduction
Not reproduced here (no device log yet). The fork is clear though: **build-only / platform-only**, which points at the IL2CPP environment rather than the logic (the logic is identical and works under the Editor's Mono runtime).

## Investigation
- Editor uses Mono with full reflection; the Android build uses **IL2CPP with managed code stripping**.
- The user switched from `JsonUtility` to **Newtonsoft Json.NET specifically for polymorphic data**. Polymorphic (de)serialization relies heavily on **reflection and runtime type information** — exactly what IL2CPP stripping and AOT constraints break.
- "Empty file / silent reset" is consistent with serialization throwing (and being swallowed) or producing no output on device.

## Hypotheses (ranked)
1. **IL2CPP stripping removed the model types / their constructors**, so Json.NET can't (de)serialize them → empty/invalid output. *For:* classic Newtonsoft-on-IL2CPP failure; matches "works in Editor only." *Against:* unconfirmed without the device log.
2. **AOT / generic limitation** in Newtonsoft's reflection path throwing `ExecutionEngineException` on device. *For:* IL2CPP AOT is strict. *Against:* would usually log an exception — need the log.
3. A swallowed exception hides the real error (a `try/catch` writing empty data on failure). *For:* explains "silent". *Against:* secondary to 1/2.

## Root Cause  [Confidence: Medium]
**Most likely:** IL2CPP code stripping / AOT is breaking Newtonsoft's reflection-based polymorphic serialization, so save data isn't written/read on device. Confidence is **Medium** — this is the textbook cause and fits every symptom, but I haven't seen the device log confirming *which* exception fires. Here's how to raise it to High/Confirmed:

## Fix
Apply the standard mitigations, smallest-blast-radius first:
1. **Preserve your model types from stripping.** Add a `link.xml` listing the assembly/namespace of your save models (and Newtonsoft if needed), or annotate types with `[Preserve]`.
2. **Reduce reflection dependence:** configure Json.NET with explicit settings (`TypeNameHandling` only where required, custom `SerializationBinder`), and prefer the AOT-friendly Newtonsoft build for Unity if you're not already on it.
3. Temporarily set **Managed Stripping Level → Minimal/Disabled** in a test build to confirm the hypothesis (then re-enable with the proper `link.xml`).
Trade-off: `link.xml` is the precise fix; disabling stripping globally inflates build size and is only a diagnostic step.

## Verification
1. Make a **development build** (Script Debugging on) for Android.
2. Capture `adb logcat` while saving — look for `JsonSerializationException`, `TypeLoadException`, or `ExecutionEngineException`.
3. After adding `link.xml`/`[Preserve]`: confirm the save file contains data and progress persists across restarts.
4. Confirm the empty-file path also gets a logged error (no silent failures — see Prevention).

## Prevention
- Remove any `catch` that writes empty data without logging; surface serialization errors.
- Add a smoke test that round-trips a representative polymorphic save object and asserts equality.
- *Why it happened:* IL2CPP strips/AOT-restricts reflection-driven types; Newtonsoft polymorphic serialization needs those types preserved.

## Missing info (if any)
**The `adb logcat` output during a save on device** — that single artifact will confirm hypothesis 1 vs. 2 and move this from Medium to High/Confirmed. Also: which Newtonsoft package (the Unity-specific AOT build or the stock NuGet one)?
