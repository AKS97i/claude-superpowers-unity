# Showcase — Unity Debugging Expert

Demonstrations of the [Unity Debugging Expert](../../superpowers/debugging/unity-debugging-expert/) driving real Unity bugs to a verified root cause.

## Featured conversations

Full, redacted end-to-end sessions — the textual showcase. They stand on their own today.

| Conversation | What it shows |
| --- | --- |
| [Coroutine respawn never fires](conversation-coroutine-respawn.md) | Rejects the obvious-but-wrong fix ("increase the wait / race condition"); reads code ordering; separates proximate vs. root cause; prevention rule |
| [Vague "crashes sometimes"](conversation-vague-crash-intake.md) | Honesty under insufficient info: no invented cause, a focused intake with rationale, exact log-capture commands, then a specific OOM/leak diagnosis once evidence arrives |

## Worked examples

Maintainer-reviewed reference transcripts (also serve as eval anchors).

| Scenario | What it shows | Source |
| --- | --- | --- |
| NullReferenceException on additive scene load | Methodology in action: intake → localize (execution order) → ranked hypotheses → High-confidence root cause → minimal fix → regression guard | [worked example](../../superpowers/debugging/unity-debugging-expert/examples/null-ref-on-additive-scene-load.md) |
| Works in Editor, NullRef in Android build | Editor-vs-build divergence; IL2CPP code stripping; honest confidence + verification plan | [worked example](../../superpowers/debugging/unity-debugging-expert/examples/works-in-editor-not-in-build.md) |
| Singleton null on second Play (Domain Reload off) | Non-obvious cause: stale statics under Enter Play Mode Options; `RuntimeInitializeOnLoadMethod` fix | [worked example](../../superpowers/debugging/unity-debugging-expert/examples/singleton-null-after-domain-reload-disabled.md) |

## Media — to capture for `stable`

The transcripts above are the textual showcase. Captured screen media is the remaining gate
for promoting this Superpower to `stable` (see the [testing strategy](../../docs/testing-superpowers.md#what-passing-means-by-tier)).
Drop files in `media/` and embed them above as they're recorded.

Suggested shot-list (each ~10–30s, trimmed, under ~3 MB):

- [ ] **GIF** — the coroutine-respawn session end to end: messy prompt → structured, confidence-rated report.
- [ ] **GIF** — the vague-crash intake: the model asking for the log instead of guessing, then diagnosing from `Player.log`.
- [ ] **Screenshot** — a real Unity Console error + the resulting diagnosis report side by side (before → after).
- [ ] **Screenshot** — a confidence rating + "what would raise it" line, to make the honesty visible at a glance.

> Want to contribute a recording? See the [showcase guide](../README.md).
