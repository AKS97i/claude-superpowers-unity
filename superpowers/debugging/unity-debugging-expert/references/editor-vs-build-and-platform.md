# Reference — Editor vs build & platform-specific bugs

"It works in the Editor but breaks in the build" (or on one platform) means the *environment* changed, not the logic. The Editor runs Mono with full reflection and all assets present; a player build may run IL2CPP with code stripping, AOT constraints, and platform quirks.

## Build-only bugs (works in Editor, fails in build)

| Cause | Why it only happens in the build | Confirm / fix |
| --- | --- | --- |
| **IL2CPP code stripping** | Managed Stripping Level removes types/members only reached via reflection or serialization | Symptom: `TypeLoadException`, missing method, JSON fails to populate. Preserve via `link.xml` or `[Preserve]`; lower stripping level to test the hypothesis. |
| **AOT / generic limitations** | IL2CPP is ahead-of-time; some runtime-generated generics throw `ExecutionEngineException` | Avoid problematic generic virtual calls; provide concrete usages so the AOT compiler emits them. |
| **Reflection assumptions** | Types/assemblies present in Editor may be stripped or differently named | Avoid string-based type lookup, or preserve the types. |
| **`#if UNITY_EDITOR` divergence** | Code compiled only in the Editor is absent in the build | Ensure runtime paths don't depend on editor-only code/data. |
| **`AssetDatabase` at runtime** | `AssetDatabase` is editor-only; returns nothing in a build | Use `Resources`/Addressables/direct references instead. |
| **Path case-sensitivity** | Windows/macOS Editor are case-insensitive; Android/Linux/iOS file systems may not be | Match exact case for file/Resource paths. |
| **Resources vs Addressables differences** | Load paths/availability differ between Editor and packaged build | Verify the asset is actually included; check Addressables groups/build. |
| **Platform `#if` defines** | `UNITY_ANDROID`, `UNITY_IOS`, etc. gate different code | Audit conditional compilation for the failing platform. |
| **Shader/variant stripping** | Variants used only at runtime get stripped | Add to an "always included" list or a shader variant collection. |

## Editor-only bugs (works in build, fails in Editor)

- Enter Play Mode Options assumptions: with domain/scene reload disabled (⚠️ Unity 6+ default), static state persists between Play sessions — initialize explicitly.
- Editor-only tooling/Gizmos throwing in `OnDrawGizmos`/`OnValidate`.
- Asset post-processors or editor scripts interfering.

## Platform-specific bugs

- **Get the device logs.** Android: `adb logcat`; iOS: Xcode device console / Organizer; consoles: platform tooling. The Player.log is the primary evidence.
- **Architecture/ABI:** wrong native plugin ABI (arm64 vs armv7) → `DllNotFoundException`/load failure.
- **Permissions / sandbox:** file paths must use `Application.persistentDataPath`; `dataPath` may be read-only.
- **Precision/float behavior** can differ subtly across GPUs/CPUs — relevant for visual or physics determinism.
- **Memory limits** are far tighter on mobile/console — an Editor that "works" may OOM on device (consider handing off to the memory/performance Superpowers).

## Methodology for this class

1. Confirm the fork: build-only, editor-only, or both (if both, it's not an environment issue).
2. Reproduce in a **development build** with **script debugging** and full stack traces enabled.
3. Get the **Player.log / device log** — it usually names the missing type/method/path.
4. Form the hypothesis from the table; test by toggling the suspected setting (e.g. stripping level) in an isolated build.
5. Fix at the right layer (preserve types, fix paths, adjust defines) — prefer a targeted `link.xml`/`[Preserve]` over disabling stripping globally.
