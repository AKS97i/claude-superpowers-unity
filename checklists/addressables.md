# Addressables Debugging Checklist

Diagnosing issues with Unity's Addressable Asset System.

---

## 1. Works in Editor but not in build

The Editor falls back to `AssetDatabase.LoadAssetAtPath` for Addressable assets. If a build fails but the Editor works:

- [ ] Has the Addressables catalog been built? (**Window → Asset Management → Addressables → Groups → Build → New Build → Default Build Script**)
- [ ] Was the catalog rebuilt **after** the last asset was added or moved?
- [ ] Is the asset assigned to an Addressables group? (Not just in the project — must be in a group)
- [ ] Does the group's **Build Path** and **Load Path** match the expected runtime path?
  - Local assets: `LocalBuildPath` / `LocalLoadPath`
  - Remote assets: check remote URL is correct in the build profile
- [ ] Are the built bundles present in the build output?

---

## 2. Handle.Result is null / load fails silently

- [ ] Always check `handle.Status` before reading `handle.Result`:
  ```csharp
  if (handle.Status != AsyncOperationStatus.Succeeded) {
      Debug.LogError($"Load failed for '{key}': {handle.OperationException}");
      Addressables.Release(handle);
      return;
  }
  ```
- [ ] What is `handle.OperationException`? (log it — it describes the failure)
- [ ] Does the key (address string) exactly match the address set in the Addressables Groups window?
- [ ] Is the key case-sensitive? (Addressable addresses are case-sensitive)

---

## 3. Key not found

- [ ] Open **Window → Asset Management → Addressables → Groups** — find the asset and confirm its address string
- [ ] Is a label being used as a key? Confirm the label is assigned to the asset
- [ ] Using a `AssetReference` field? Confirm it is assigned in the Inspector
- [ ] Using `Addressables.LoadAssetsAsync` with a label? All assets with that label must be in a built group

---

## 4. Memory leaks — handles not released

- [ ] Every `LoadAssetAsync` or `LoadAssetsAsync` result must be released when done:
  ```csharp
  Addressables.Release(handle);
  // OR for instances:
  Addressables.ReleaseInstance(instance);
  ```
- [ ] Is `Instantiate` called via `Addressables.InstantiateAsync`? Use `Addressables.ReleaseInstance` to destroy
- [ ] Using `Addressables.LoadAssetAsync` and then `Instantiate` manually? Release the handle separately from destroying the instance

---

## 5. Remote catalog issues

- [ ] Is the catalog URL correct in Player Settings / Addressables Profiles?
- [ ] Can the device reach the URL? (Test with `UnityWebRequest` from device)
- [ ] Is the catalog version compatible with the built bundles?
- [ ] Is HTTPS certificate valid on the CDN? (iOS / Android strict certificate checking)
- [ ] Is `Addressables.UpdateCatalogs()` called before loading assets that require an updated catalog?

---

## 6. Async / timing issues

- [ ] Load operation awaited before accessing `Result`?
  ```csharp
  var handle = Addressables.LoadAssetAsync<GameObject>(key);
  await handle.Task;  // or yield return handle — do not skip this
  var result = handle.Result;
  ```
- [ ] Is the handle released while it is still loading? (Do not release before the operation completes)
- [ ] Multiple loads of the same key — is reference counting handled? (Addressables uses ref-counting; each load increments, each release decrements; bundle is unloaded at 0)

---

## 7. Profiling Addressables

- [ ] **Window → Asset Management → Addressables → Event Viewer**: shows load/release events, reference counts, and active handles
- [ ] Use **Profiler → Memory** to check for growing texture/bundle memory (unreleased handles)
- [ ] `Addressables.GetDownloadSizeAsync(key)` before loading — logs expected download size

---

## 8. Build groups configuration

| Setting | When to use |
|---|---|
| **Build Remote Catalog** | Required for remote (CDN) hosted bundles |
| **Content Update Restriction = Cannot Change Post Release** | Ensures content-update workflow; locks assets that cannot be patched |
| **Bundle Mode = Pack Separately** | One bundle per asset; fine-grained loading but more HTTP requests |
| **Bundle Mode = Pack Together** | One bundle per group; fewer requests but coarser granularity |
| **Compression = LZ4** | Best for runtime loading speed (default) |
| **Compression = LZMA** | Best for download size but slow decompression; use for archive/download bundles |
