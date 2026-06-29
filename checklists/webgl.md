# WebGL Debugging Checklist

WebGL-specific issues that do not appear in the Editor or on native platforms.

---

## 1. IL2CPP and stripping (WebGL always uses IL2CPP)

- [ ] `TypeLoadException` or `ExecutionEngineException` → stripping or AOT issue
  - [ ] Add `link.xml` entries for types accessed via reflection
  - [ ] Add static AOT hints for generic instantiations
  - [ ] Try `Managed Stripping Level = Minimal` to confirm; then add targeted entries
- [ ] Reflection (`Activator.CreateInstance`, `Type.GetType`, JSON deserialization) → all target types in `link.xml`

---

## 2. Memory

- [ ] WebGL memory is a fixed upfront allocation
  - Default: 256 MB — may be too small for some games
  - Player Settings → WebGL → Memory Size
- [ ] Out-of-memory crash (tab freezes or shows browser OOM error)?
  - [ ] Increase Memory Size
  - [ ] Profile in Chrome DevTools → Memory tab for allocation growth
- [ ] Texture compression: use DXT/S3TC for desktop WebGL; ETC2 for mobile browsers
  - Player Settings → WebGL → Texture Compression

---

## 3. Threading

- [ ] WebGL (non-SharedArrayBuffer) does not support threading
- [ ] Any `System.Threading.Thread` usage → will fail on WebGL
- [ ] `async/await` with `Task.Run` → moves to a thread; not supported without SharedArrayBuffer
- [ ] Use `UnityWebRequest`, `Addressables`, or coroutine-based async instead
- [ ] SharedArrayBuffer WebGL (Unity 2022.2+): requires COOP/COEP HTTP headers on the server

---

## 4. File system

- [ ] WebGL has no persistent file system by default — `Application.persistentDataPath` maps to IndexedDB
- [ ] `File.ReadAllText` / `System.IO` calls → not supported on WebGL
- [ ] Use `UnityWebRequest` for loading files from server
- [ ] Use `PlayerPrefs` or `IndexedDB` (via `Application.persistentDataPath`) for persistence

---

## 5. Native plugins

- [ ] Native C/C++ plugins must be compiled to WebAssembly (`.bc` / Emscripten)
- [ ] Native plugins for other platforms (`.dll`, `.so`, `.dylib`) are silently ignored on WebGL
- [ ] Check plugin's documentation for WebGL support
- [ ] Managed plugins (`.dll` C# libraries) work if they do not use unsupported APIs

---

## 6. Audio

- [ ] WebGL audio requires user interaction before the `AudioContext` is created (browser policy)
- [ ] First audio play must be triggered by a user gesture (button click, etc.)
- [ ] `AudioSource.Play()` called on `Start` → will be silent until user interaction
- [ ] Use `AudioContext.resume()` or a "click to start" screen

---

## 7. Networking

- [ ] `System.Net.Sockets` is not supported on WebGL
- [ ] Use `UnityWebRequest` for HTTP, or WebSocket for real-time connections
- [ ] CORS: the server must send appropriate `Access-Control-Allow-Origin` headers
- [ ] Mixed content: HTTPS pages cannot make HTTP requests

---

## 8. Build configuration

- [ ] **Development Build** enabled for debugging: allows source-mapped stack traces in browser
- [ ] **Code Optimization = Runtime Speed** for release builds
- [ ] Compression: `Gzip` requires server configuration; `Brotli` requires more server config; `Disabled` works everywhere
- [ ] Check browser console (F12 → Console) for JavaScript errors, not just Unity Console

---

## 9. Testing and diagnostics

- [ ] Test in multiple browsers (Chrome, Firefox, Safari behave differently)
- [ ] Use browser DevTools → Network tab to confirm all assets load
- [ ] Use browser DevTools → Console for JavaScript errors
- [ ] Enable `Debug Symbols` in WebGL Player Settings for readable stack traces
- [ ] Check `Player.log` at `Application.persistentDataPath` (mapped to IndexedDB)
