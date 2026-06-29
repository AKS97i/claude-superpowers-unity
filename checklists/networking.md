# Networking Debugging Checklist

Diagnosing multiplayer issues in Unity. Covers Netcode for GameObjects (NGO), Mirror, Photon, and general patterns.

---

## 1. Establish the authority model

Before debugging any network issue:

- [ ] What is the authority model? (Server authoritative / client-authoritative / hybrid)
- [ ] Which machine owns each piece of state?
- [ ] Is the state being modified on the correct machine?
- [ ] Is an `[ServerRpc]` being called from the server instead of a client? (NGO: `[ServerRpc]` called from non-owning client fails silently by default)

---

## 2. State desync

When clients and host/server show different state:

- [ ] Is the state being modified on the **server/host only** and synced via `NetworkVariable` or `ClientRpc`?
- [ ] Is `NetworkVariable` set with the right read/write permissions?
  ```csharp
  new NetworkVariable<int>(0,
      NetworkVariableReadPermission.Everyone,
      NetworkVariableWritePermission.Server)
  ```
- [ ] Are `NetworkTransform` objects moving on non-owning clients directly? (Only the owner or server should set position)
- [ ] After a scene load: are `NetworkTransform` positions re-synced? (Use `Teleport` to force a baseline)
- [ ] Is latency/lag compensation needed for reconciliation?

---

## 3. Object lifecycle / spawning

- [ ] `NetworkObject` spawned only on the server/host:
  ```csharp
  if (IsServer) {
      var obj = Instantiate(prefab);
      obj.GetComponent<NetworkObject>().Spawn();
  }
  ```
- [ ] Prefab registered in the **NetworkManager's Network Prefab List**?
- [ ] `NetworkObject` component present on the prefab root?
- [ ] `Destroy` called on a `NetworkObject` — use `NetworkObject.Despawn(true)` from server instead
- [ ] Client tries to access a `NetworkObject` before it is spawned? (`OnNetworkSpawn` not yet called)

---

## 4. RPC issues (Netcode for GameObjects)

- [ ] `[ServerRpc]` called from the correct owner?
  - Default: only the **owning client** can call a `[ServerRpc]`
  - Use `[ServerRpc(RequireOwnership = false)]` to allow any client to call it
- [ ] `[ClientRpc]` called from the server? (ClientRpcs run on all clients; must be called from server)
- [ ] Parameters in RPCs are network-serializable? (primitives, `NetworkSerializable` types, `Vector3`, `Quaternion`, etc.)
- [ ] `[ServerRpc]` / `[ClientRpc]` method names end in `Rpc` suffix? (NGO 1.0+ requirement)

---

## 5. Disconnection / reconnection

- [ ] `OnClientDisconnectCallback` registered to clean up client state?
- [ ] Scene references rewired after a client reconnects?
- [ ] Player objects properly despawned on disconnect?
- [ ] Timeout settings appropriate for the target network conditions?

---

## 6. Scene management

- [ ] Using `NetworkManager.SceneManager.LoadScene` instead of `SceneManager.LoadScene` for networked scene loads?
- [ ] Clients waiting for `OnSceneLoaded` before trying to access networked objects in the new scene?
- [ ] Additive scene loads: references rewired via `SceneManager.sceneLoaded` callback after load?

---

## 7. Intermittent / timing issues

- [ ] Does the bug appear only at high latency? (Simulate with Network Emulator or `NetworkManager`'s simulated delay)
- [ ] Does the bug appear only with multiple clients but not host-only? (race condition in state sync)
- [ ] Is there a race between `OnNetworkSpawn` and other initialization? (`NetworkVariable` values not yet received when `Start` runs on client)
- [ ] Order-dependent: are you reading `NetworkVariable` values in `Awake`? (Values are not yet synced; use `OnNetworkSpawn` or `NetworkVariable.OnValueChanged`)

---

## 8. Diagnostics

- [ ] Enable **Network Log Level = Developer** in `NetworkManager` for verbose logs
- [ ] Use **Multiplayer Tools** package → **Network Stats** overlay for real-time bandwidth, RTT, packet loss
- [ ] Use **Multiplayer Tools** → **Network Scene Visualization** to confirm object spawning
- [ ] Log `IsServer`, `IsClient`, `IsHost`, `IsOwner` at the point of failure to confirm which machine is executing which path
- [ ] For NGO: `NetworkManager.Singleton.ConnectedClientsIds` to confirm client IDs in scope

---

## 9. Common gotchas by framework

| Framework | Common issue | Fix |
|---|---|---|
| **NGO** | `NetworkVariable` read before `OnNetworkSpawn` | Use `OnNetworkSpawn` or `OnValueChanged` |
| **NGO** | `[ServerRpc]` silently ignored from non-owner | Add `RequireOwnership = false` or check ownership |
| **NGO** | Scene management: use `NetworkManager.SceneManager` | Not `SceneManager` directly |
| **Mirror** | `[Command]` called from server instead of client | Check `isServer` / `isClient` guards |
| **Mirror** | `SyncVar` not updating on clients | Ensure modified on server; `[SyncVar(hook = ...)]` for callbacks |
| **Photon PUN** | `PhotonView.IsMine` not checked before modifying | Always guard with `if (!photonView.IsMine) return;` |
| **All** | Position set directly on non-owning client | Use authority-respecting sync (NetworkTransform, SyncVar, etc.) |
