# Eval: MissingReferenceException / NullRef accessing a destroyed object

## Input

> I get `MissingReferenceException: The object of type 'Transform' has been destroyed but you are still trying to access it.` My enemy manager keeps a list of enemies and moves them toward the player every frame. It happens a few frames after an enemy dies. Unity 6, URP, PC.
>
> ```csharp
> public class EnemyManager : MonoBehaviour {
>     readonly List<Enemy> enemies = new();
>     void Update() {
>         foreach (var e in enemies)
>             e.transform.position = Vector3.MoveTowards(e.transform.position, target, speed * Time.deltaTime);
>     }
> }
> // Enemy.Die() calls Destroy(gameObject);
> ```

## Expected triggering
- should-fire: true

## Rubric

### MUST
- [ ] Identifies that `Destroy(gameObject)` destroys the enemy but its entry **remains in the `enemies` list**, so `Update` later dereferences a destroyed object.
- [ ] Explains the **Unity `== null` overload**: a destroyed `UnityEngine.Object` compares equal to `null` even though the C# reference is non-null — so a plain `if (e != null)` *does* catch it, but the manager never checks at all (or the list still holds the reference).
- [ ] Proposes removing the enemy from the list on death (e.g. raise an event / manager-owned despawn) rather than only calling `Destroy`, and/or null-checking via Unity's overloaded `==` and pruning.
- [ ] Notes that mutating the list during a `foreach` (if removal is added naïvely) throws `InvalidOperationException` — recommend a safe removal pattern (iterate backwards over an indexed list, or `RemoveAll`, or a removal queue).
- [ ] Produces the required output format and states a confidence level.

### MUST NOT
- [ ] Does not claim a generic "race condition" — this is deterministic given the list-not-pruned cause.
- [ ] Does not recommend `?.` (null-conditional) as a fix on a `UnityEngine.Object`, since `?.` bypasses Unity's overloaded `==` and will *not* treat a destroyed object as null (a known trap).
- [ ] Does not claim "Confirmed" without the fix being verified.

### Confidence disclosure
- [ ] States confidence (High — message + code clearly show the cause) and what would confirm it (reproduce: kill an enemy, observe the throw next frames; verify list pruning removes it).

## Notes
Strong response: nails both the lifecycle bug (destroyed object still referenced) **and** the two Unity-specific traps (`==` overload, and `?.`/`is null` bypassing it), plus the safe-removal-during-iteration concern. Prevention: manager owns spawn/despawn; enemies notify on death. Weak response: suggests wrapping in `try/catch`, or uses `enemy?.transform` and declares it fixed.
