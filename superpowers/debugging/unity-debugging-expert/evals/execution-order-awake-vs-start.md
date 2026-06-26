# Eval: NullRef from reading another script's reference in Awake

## Input

> Sometimes my `Player` script throws a NullReferenceException on the very first frame, sometimes it doesn't — same scene, no code changes between runs. The line is `_inventory.AddStarterItems();`. `_inventory` is set up by an `Inventory` component on the same GameObject. Unity 2021.3, Built-in, PC.
>
> ```csharp
> public class Player : MonoBehaviour {
>     private Inventory _inventory;
>     void Awake() {
>         _inventory = GetComponent<Inventory>();
>         _inventory.AddStarterItems();   // NullRef here, intermittently
>     }
> }
> public class Inventory : MonoBehaviour {
>     private List<Item> _items;
>     void Awake() => _items = new List<Item>();
> }
> ```

## Expected triggering
- should-fire: true

## Rubric

### MUST
- [ ] Identifies that `GetComponent<Inventory>()` returns the component fine, but `Inventory._items` is initialized in **`Inventory.Awake()`**, and `Player.Awake()` may run **first** — so `AddStarterItems()` touches a null `_items`.
- [ ] Explains that **Awake order across components/GameObjects is not guaranteed** (unless set via Script Execution Order), which is why it's intermittent / machine-dependent.
- [ ] Distinguishes proximate (`_items` null inside `AddStarterItems`) from root (cross-component initialization-order dependency). Note the throw is likely *inside* `Inventory`, not because `_inventory` itself is null.
- [ ] Proposes a robust fix: initialize `_items` at declaration or in the field initializer (so it doesn't depend on Awake timing), and/or move cross-object setup to `Start` (all Awakes complete before any Start), and/or set explicit Script Execution Order as a last resort.
- [ ] Produces the required output format and states a confidence level.

### MUST NOT
- [ ] Does not assume `GetComponent` returned null without considering that the inner `_items` is what's null.
- [ ] Does not recommend Script Execution Order as the *first* fix when initializing the list at declaration is simpler and removes the ordering dependency entirely.
- [ ] Does not claim "Confirmed" without a verified repro/fix.

### Confidence disclosure
- [ ] States confidence (High — the intermittent-on-same-scene + cross-Awake pattern is diagnostic) and notes the one ambiguity worth confirming: whether the NullRef is `_inventory` itself or `_items` inside it (ask for the full stack trace to be certain).

## Notes
Tests the lifecycle/execution-order lens and the Awake-vs-Start rule (all Awake() run before any Start()). Strong response leads with "initialize at declaration to remove the timing dependency," explains the non-determinism, and only mentions Execution Order as a fallback. Weak response: "add a null check before AddStarterItems" (hides the ordering bug) or blames `GetComponent`.
