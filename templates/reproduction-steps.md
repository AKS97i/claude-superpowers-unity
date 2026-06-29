# Reproduction Steps Template

Use when creating a minimal reproduction case for a Unity bug.

---

## Bug being reproduced

<!-- Reference the bug report or a brief description. -->

## Reproduction status

- [ ] Always reproducible with these steps
- [ ] Intermittent — triggers approximately X% of attempts
- [ ] Steps pending validation

---

## Minimal scene setup

<!-- Describe the minimum scene state required to trigger the bug. -->
<!-- Remove everything not necessary for reproduction. -->

**GameObjects required:**

**Components required:**

**Inspector values required:**

---

## Steps to reproduce

1. Open Unity version **[x.x.xxxx]**
2. Open scene **[scene name]**
3. 
4. 
5. 
6. **Observe:** [what happens]

## Expected result

<!-- What should happen at step 6. -->

## Actual result

<!-- What actually happens at step 6. -->

---

## Minimal code

<!-- If the bug is code-dependent, include the smallest script that triggers it. -->

```csharp
// MinimalRepro.cs
using UnityEngine;

public class MinimalRepro : MonoBehaviour {
    void Start() {
        // Minimal code that triggers the bug
    }
}
```

---

## What was ruled out during minimization

<!-- List things you removed that did not affect whether the bug appears. -->
<!-- This helps future investigators narrow faster. -->

- Removed X — bug still present
- Removed Y — bug still present
- Removed Z — bug disappeared (Z may be relevant)

---

## Attachments

- [ ] Minimal project (zip)
- [ ] Screenshot / recording
- [ ] Editor.log / Player.log
- [ ] Profiler snapshot
