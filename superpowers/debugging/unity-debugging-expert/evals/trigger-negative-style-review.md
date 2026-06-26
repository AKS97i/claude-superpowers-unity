# Eval: style/convention review should hand off, not trigger debugging

## Input

> Can you review this MonoBehaviour for code quality and tell me if it follows good Unity conventions? It works fine, I just want feedback on naming, structure, and whether I'm using `[SerializeField]` idiomatically.
>
> ```csharp
> public class playerController : MonoBehaviour {
>     public float Speed;
>     void Update() { /* movement */ }
> }
> ```

## Expected triggering
- should-fire: false
- Should be handled by **Unity C# Code Review**, not the Debugging Expert. The code works; the user wants style/convention feedback, which is review, not defect diagnosis.

## Rubric

### MUST
- [ ] Recognizes that the request is **code review for style/conventions**, explicitly out of scope for debugging, and says so.
- [ ] Recommends the Unity C# Code Review Superpower.
- [ ] Does not invent a bug in working code to justify a debugging session.

### MUST NOT
- [ ] Does **not** run the bug-diagnosis pipeline or emit a Symptom/Root Cause report.
- [ ] Does not claim a convention smell (e.g. lowercase class name, `public` field instead of `[SerializeField] private`) is a "defect" — it's a review note, not a bug.

### Confidence disclosure
- [ ] N/A — this is a scope/handoff decision, not a diagnosis.

## Notes
Boundary eval. The line: "find why this is broken" → Debugging Expert; "tell me if this is good code" → Code Review. If the user said "review this and also it sometimes crashes," the crash *is* in scope and the skill should engage on that part. Weak behavior: producing a debugging report, or doing the style review itself (that's another Superpower's job).
