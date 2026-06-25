# Reference — Serialization & references

Unity's serialization rules cause a whole family of "lost reference", "value reverted", and "Inspector not showing my field" bugs.

## What Unity serializes

A field is serialized (and shown in the Inspector) when it is:

- `public`, **or** marked `[SerializeField]`; **and**
- not marked `[NonSerialized]`; **and**
- of a serializable type.

Serializable types include: primitives, `string`, enums, `UnityEngine.Object` references, structs/classes marked `[System.Serializable]`, and arrays/`List<T>` of the above.

**Not serialized by default:** `Dictionary<,>`, multidimensional/jagged arrays, properties (auto or otherwise), `static`/`const`/`readonly` fields, generic-typed fields (pre-2020 limitations), and interfaces (no native interface serialization).

## Common bugs and causes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Field doesn't appear in Inspector | `private` without `[SerializeField]`, or non-serializable type | Add `[SerializeField]`, or make the type `[System.Serializable]` |
| Value resets to default after rename | Field renamed → Unity sees a new field, drops old data | Add `[FormerlySerializedAs("oldName")]` |
| Reference shows `None` after pulling changes | Bad scene/prefab YAML merge or changed GUID/fileID | Inspect `.meta` GUID + scene YAML `fileID`; re-assign; fix merge with a Unity-aware merge tool |
| Value "reverts" on a prefab instance | Prefab override confusion | Check whether the instance has an override; "Apply"/"Revert" as intended |
| `Dictionary` is empty after reload | Dictionaries aren't serialized | Use a serializable wrapper (`ISerializationCallbackReceiver` with parallel lists) or a known serialized-dictionary utility |
| Cross-scene reference is null | Unity doesn't serialize references across scenes | Resolve at runtime via a registry/locator after additive load |
| Polymorphic field loses subtype | Default serializer doesn't store managed type | ⚠️ Unity 2019.3+: use `[SerializeReference]` for polymorphic/managed references |

## Prefab pitfalls

- An **instance override** silently shadows the prefab value — the prefab can change while the instance keeps the old value (or vice versa). Use the override indicators / context menu to reason about it.
- **Nested prefabs / variants** add layers of overrides; a value may be set on the variant, the base, or the instance.
- Applying an accidental override propagates it to all instances — check before "Apply All".

## Meta files & version control

- Every asset has a `.meta` with a **GUID**; references are stored by GUID + fileID. **Losing/regenerating a `.meta` breaks every reference to that asset.**
- Commit `.meta` files. Use a Unity-aware `.gitignore`, enable **Visible Meta Files** + **Force Text** serialization, and consider Smart Merge (UnityYAMLMerge) for scene/prefab merges. (This is the domain of the future *Version Control Hygiene Advisor* Superpower.)

## Confirmation tactics

- Diff the scene/prefab `.yaml` to see whether a `fileID`/GUID changed.
- Log the field's value in `Awake` to confirm it deserialized as expected.
- For "reverts after rename", check git history for the rename and whether `[FormerlySerializedAs]` was added.
