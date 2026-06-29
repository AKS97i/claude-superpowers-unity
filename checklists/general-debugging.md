# General Debugging Checklist

A structured checklist for working any Unity bug. Work top-to-bottom; skip sections that don't apply.

---

## 1. Information gathering

- [ ] I have the full error message and complete stack trace (not truncated)
- [ ] I know the Unity version, render pipeline, and target platform
- [ ] I have observed vs. expected behavior written down
- [ ] I know whether this is always / intermittent / once
- [ ] I know what recently changed (git log / diff)

---

## 2. Stack trace analysis

- [ ] I have read the stack trace top-to-bottom
- [ ] I have identified the **throwing line** (top frame)
- [ ] I have identified the **call path** (how execution reached the throw)
- [ ] I have scanned the log for the **first** error (it may be different from the last)
- [ ] I have noted any warnings preceding the error

---

## 3. Reproduction

- [ ] I can reproduce the bug reliably
  - If yes: proceed to hypothesis testing
  - If intermittent: characterize the trigger (timing / platform / data / frame-order)
  - If no repro: create an instrumentation plan instead of guessing

---

## 4. Unity-specific checks

### Object lifecycle
- [ ] Is any accessed object destroyed? (Check `!= null` — Unity overloads `==`)
- [ ] Is there an Awake/Start ordering dependency?
- [ ] Is a coroutine stopped by a disabled component?
- [ ] Is a singleton null after domain reload?

### Serialization
- [ ] Are all `[SerializeField]` references assigned in the Inspector?
- [ ] Were any fields renamed recently? (Check `[FormerlySerializedAs]`)
- [ ] Is the field type serializable by Unity?

### Scene/prefab
- [ ] Is the right prefab instance in the scene?
- [ ] Were any prefab references lost after a scene reload?
- [ ] Is this additive-scene and references need rewiring?

---

## 5. Hypothesis ranking

- [ ] I have listed at least 2 candidate causes
- [ ] Each candidate has evidence for AND against
- [ ] I have a rule-out set (alternatives I am actively excluding)
- [ ] I have ranked them by likelihood

---

## 6. Testing (cheapest first)

- [ ] Added targeted `Debug.Log` / `Debug.Assert` at the relevant site
- [ ] Added lifecycle breadcrumbs (`OnEnable`/`OnDisable`/`OnDestroy`)
- [ ] Isolated the suspect component (disabled others)
- [ ] Reduced to a minimal repro scene
- [ ] (For regressions) Used `git bisect` to find the introducing commit

---

## 7. Root cause confirmation

- [ ] I can distinguish proximate cause ("what threw") from root cause ("why the state was wrong")
- [ ] My confidence level is stated: Confirmed / High / Medium / Low / Speculative
- [ ] I know what evidence would raise my confidence

---

## 8. Fix

- [ ] The fix is the **smallest correct change** — no extra refactoring
- [ ] I have considered and noted trade-offs
- [ ] The fix addresses the root cause, not just the symptom

---

## 9. Verification

- [ ] The original error no longer occurs
- [ ] Related paths have been tested (edge cases, other platforms)
- [ ] No new errors were introduced

---

## 10. Prevention

- [ ] A regression guard is in place (assert / test / guard clause)
- [ ] The team has a one-line "why it happened" note
- [ ] The bug report template or checklist has been updated if a new pattern was found
