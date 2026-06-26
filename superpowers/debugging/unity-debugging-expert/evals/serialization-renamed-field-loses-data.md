# Eval: renaming a serialized field silently loses Inspector data

## Input

> I refactored a script and renamed a field from `speed` to `moveSpeed`. Now every enemy in my scene moves at 0 — all the values I'd tuned in the Inspector are gone and reset to default. I didn't touch the prefabs otherwise. Unity 2022.3, Built-in, PC.
>
> ```csharp
> public class EnemyMover : MonoBehaviour {
>     [SerializeField] private float moveSpeed = 0f; // was: private float speed
> }
> ```

## Expected triggering
- should-fire: true

## Rubric

### MUST
- [ ] Identifies that Unity serializes by **field name**, so renaming `speed` → `moveSpeed` makes the old serialized data orphaned and the new field falls back to its **default (0)**.
- [ ] Recommends `[FormerlySerializedAs("speed")]` (from `UnityEngine.Serialization`) on the renamed field to migrate existing data.
- [ ] Notes that this is data-loss, not a code bug — the values exist nowhere if already overwritten/saved, so recovery depends on whether the scene/prefab was re-saved after the rename.
- [ ] Produces the required output format (Symptom / Reproduction / Investigation / Hypotheses / Root Cause / Fix / Verification / Prevention).
- [ ] States a confidence level.

### MUST NOT
- [ ] Does not blame the `= 0f` initializer as the root cause (it is a symptom — the field is default because the serialized data didn't carry over).
- [ ] Does not claim the data is definitely recoverable without knowing whether the asset was re-saved.
- [ ] Does not propose hand-re-entering values as the *first/only* fix when `[FormerlySerializedAs]` would migrate them automatically (if not yet re-saved).

### Confidence disclosure
- [ ] States confidence (High for the cause — this is documented Unity behavior) and what would confirm it (e.g. checking version control for the pre-rename scene/prefab, or whether values reappear after adding `[FormerlySerializedAs]` and reverting the asset).

## Notes
Strong response: distinguishes the **mechanism** (name-based serialization) from the **recovery question** (was the asset re-saved since the rename?), gives `[FormerlySerializedAs]` with the correct namespace, and a prevention note (rename via the attribute, or use the IDE/Unity rename that preserves serialization; commit before refactors). Weak response: tells the user to just re-enter the numbers, or attributes the 0 to the field initializer without explaining serialization-by-name.
