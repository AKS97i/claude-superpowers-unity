# Root Cause Analysis Template

A post-mortem document for a resolved Unity bug. Captures what happened and how to prevent recurrence.

---

## Bug summary

**Title:**

**Severity:** Critical / High / Medium / Low

**Date found:**

**Date resolved:**

**Time to resolve:**

---

## Impact

**Who was affected:**

**What was broken:**

**Scope:** Single scene / Multiple scenes / All platforms / Specific platform only

---

## Timeline

| Time | Event |
|---|---|
| | Bug first reported / observed |
| | Investigation started |
| | Root cause identified |
| | Fix developed |
| | Fix verified |
| | Deployed / merged |

---

## Symptom

**Observed behavior:**

**Expected behavior:**

**Error message / stack trace:**

```
Paste here
```

---

## Investigation summary

**Evidence gathered:**

**Hypotheses considered:**

| Hypothesis | Ruled out by |
|---|---|
| | |
| | |

---

## Root cause

**Confidence at resolution:** Confirmed / High

**Proximate cause:**
<!-- What threw / what was wrong at the point of failure -->

**Root cause:**
<!-- Why the state was wrong in the first place -->

**Contributing factors:**
<!-- Process, tooling, or code patterns that made this possible -->

---

## Fix

**Change description:**

**Files changed:**

```csharp
// Key change
```

**Why this fix is correct:**

**Alternatives considered and why they were rejected:**

---

## Verification

**How the fix was verified:**

**Test added:**

---

## Prevention

### Immediate actions

- [ ] 

### Process improvements

- [ ] 

### Code guard added

```csharp
// Guard / assert / test
```

**Why it happened (one sentence for the team):**

---

## Lessons learned

<!-- What would have caught this earlier? -->
<!-- What debugging technique was most useful? -->
<!-- What should be added to the onboarding or code review checklist? -->
