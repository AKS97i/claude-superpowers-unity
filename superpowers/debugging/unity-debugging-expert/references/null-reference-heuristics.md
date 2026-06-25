# Reference — NullReferenceException heuristics

The most common Unity runtime error. Work the causes in roughly this order; each row gives the tell and how to confirm.

> **Unity `null` caveat:** `UnityEngine.Object` overloads `operator ==`, so a *destroyed* object compares `== null` even though it isn't a real C# null reference. A `?.` (null-conditional) **bypasses** this overload and will NOT treat a destroyed object as null — a frequent source of "but I null-checked it!" bugs.

| # | Cause | Tell-tale | How to confirm |
| --- | --- | --- | --- |
| 1 | Unassigned Inspector reference (`[SerializeField]`/public) | Field is null at first use; works on one instance but not another | Select the object; check the field is assigned in the Inspector. Compare prefab vs. instance overrides. |
| 2 | Reference lost on prefab/scene reload or re-import | "It was assigned, now it's None" after a domain reload, merge, or re-import | Check the `.meta`/scene YAML for a broken GUID/fileID; re-assign and check version control for a bad merge. |
| 3 | `GetComponent<T>()` returned null | NullRef immediately after a `GetComponent` call | The component isn't on that GameObject (maybe on a child/parent). Use `GetComponentInChildren/Parent`, or `TryGetComponent`. |
| 4 | Accessed too early (execution order) | NullRef in `Awake`/`Start` referencing another object's state | The dependency's `Awake` hasn't run yet. Move the read to `Start`, or set Script Execution Order, or initialize lazily. See `lifecycle-and-execution-order.md`. |
| 5 | Static/singleton cleared | NullRef on a singleton `Instance` after entering Play Mode again | Domain reload / Enter-Play-Mode Options reset it (⚠️ Unity 6+ defaults to fast enter-play-mode). Guard with explicit init; don't rely on static state surviving. |
| 6 | Access after `Destroy()` | Intermittent NullRef on an object you destroyed/pooled | Object was destroyed but a reference lingers. Null-check with `==` (not `?.`), null the reference on destroy, or fix pool lifecycle. |
| 7 | Additive scene reference not rewired | NullRef after `LoadScene(..., Additive)` | The reference points to the wrong scene's instance or wasn't reconnected. Resolve via a registry/locator after load, not a serialized cross-scene ref. |
| 8 | Collection/element null | NullRef indexing an array/list | Element never assigned, or list resized; check element initialization. |
| 9 | Event/callback after teardown | NullRef in a delegate firing after the subscriber was destroyed | Unsubscribe in `OnDisable`/`OnDestroy`. |

## Reading the stack trace

- The **top frame** is usually the throwing line — start there.
- A NullRef message in Unity often doesn't name the variable; identify *which* dereference on that line could be null (there may be several).
- If the trace points into engine/third-party code, find the **last frame in user code** and inspect what it passed in.

## Fast confirmation tactics

- Add a `Debug.Log` / `Debug.Assert` immediately before the throwing line printing each candidate reference.
- For "assigned in Inspector?" doubts, log `name` of the owning object and the field together.
- For lifetime bugs, log in `OnDestroy`/`OnDisable` to see whether teardown precedes the access.
