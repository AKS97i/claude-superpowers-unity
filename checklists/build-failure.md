# Build Failure Checklist

Structured checklist for diagnosing Unity build failures. Covers compilation errors, linker errors, and platform-specific failures.

---

## 1. Identify failure type

- [ ] Compilation error (C# compile-time)
- [ ] Linker / IL2CPP error
- [ ] TypeLoadException / MissingMethodException at runtime (after build succeeds)
- [ ] Asset / resource missing in build
- [ ] Build toolchain error (Gradle, Xcode, etc.)

---

## 2. Compilation errors

- [ ] Read the full error message — find the **first** error (later ones are often cascading)
- [ ] Check if `#if` platform defines exclude required code on this target
- [ ] Check for Editor-only types (`UnityEditor.*`) used outside `#if UNITY_EDITOR`
- [ ] Check for `asmdef` / assembly reference issues (type visible in Editor, missing in build assembly)
- [ ] Check for `unsafe` code without the `Allow unsafe code` player setting

---

## 3. IL2CPP / stripping failures

- [ ] Error is `TypeLoadException` or `MissingMethodException` at runtime
  - [ ] Type may be stripped — add to `link.xml`
  - [ ] Type accessed only via reflection → `link.xml` or static reference
  - [ ] Generic type instantiation not traced → add AOT hint or static reference
- [ ] Error is `ExecutionEngineException: Attempting to call a virtual method on a non-boxed value type`
  - [ ] Generic instantiation (e.g., `List<MyStruct>`) reached via reflection
  - [ ] Add `link.xml` entry for the specific generic instantiation
- [ ] Current `Managed Stripping Level` (Player Settings → Other Settings):
  - `Minimal` — strip nothing; use for diagnostics
  - `Low` / `Medium` / `High` — progressively more aggressive
  - [ ] Try `Minimal` to confirm stripping is the cause; then add targeted `link.xml` entries

---

## 4. Reflection and serialization

- [ ] Any class instantiated only via `Activator.CreateInstance` or JSON deserialization?
- [ ] Any type passed to `JsonUtility.FromJson<T>` only at runtime?
- [ ] Any `Resources.Load<T>` where `T` is resolved at runtime from a string?
- [ ] These types need `link.xml` preservation

---

## 5. Platform-specific checks

### Android
- [ ] Gradle version is compatible with Unity version
- [ ] Minimum API level matches target devices
- [ ] `AndroidManifest.xml` does not conflict with Unity's generated manifest
- [ ] Native plugin `.so` files are present for all target ABIs

### iOS
- [ ] Xcode version is compatible
- [ ] Bitcode setting matches (Unity 2022+ defaults to disabled)
- [ ] `Info.plist` permissions are set for any used hardware (camera, microphone, location)
- [ ] Framework dependencies are linked

### WebGL
- [ ] IL2CPP stripping is checked (WebGL always uses IL2CPP)
- [ ] Memory settings are appropriate (default 256 MB may be too low)
- [ ] `link.xml` covers all reflection-accessed types

---

## 6. Asset / resource issues

- [ ] All assets referenced in code are included in a build group (Addressables) or `Resources/` folder
- [ ] Asset paths match case-sensitively (Windows editor → Linux/macOS/Android build)
- [ ] No missing script components on prefabs (shown as `Missing (Mono Script)` in Inspector)
- [ ] Addressables catalog has been rebuilt after adding assets

---

## 7. Diagnostics steps

- [ ] Set Stripping Level to `Minimal` → rebuild → does the error disappear?
  - Yes → stripping is the cause; add `link.xml` entries
  - No → stripping is not the cause
- [ ] Enable **Development Build** + **Script Debugging** → rebuild → more detailed stack trace?
- [ ] Check **Window → Console** in Editor for any warnings about missing references before building
- [ ] Check the full build log (not just the Console) for earlier errors

---

## 8. Common link.xml entry patterns

```xml
<linker>
  <!-- Preserve a specific type -->
  <assembly fullname="Assembly-CSharp">
    <type fullname="MyNamespace.MyClass" preserve="all"/>
  </assembly>

  <!-- Preserve an entire namespace -->
  <assembly fullname="Assembly-CSharp">
    <namespace fullname="MyNamespace" preserve="all"/>
  </assembly>

  <!-- Preserve a system type -->
  <assembly fullname="mscorlib">
    <type fullname="System.Collections.Generic.List`1[[MyNamespace.MyStruct, Assembly-CSharp]]"
          preserve="all"/>
  </assembly>
</linker>
```

Place `link.xml` in any `Assets/` subfolder (it is picked up automatically).
