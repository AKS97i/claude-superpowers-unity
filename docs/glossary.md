# Glossary

Shared vocabulary for the project. Kept short and precise.

| Term | Definition |
| --- | --- |
| **Superpower** | A single AI Engineering System in this collection — a structured, repeatable methodology that turns Claude into a Unity expert for one job. Lives in `superpowers/<category>/<name>/`. |
| **AI Engineering System** | Our framing for a Superpower: expert reasoning encoded as an investigation pipeline, decision framework, confidence model, and output format — not a one-off prompt. |
| **`DESIGN.md`** | The source-of-truth engineering spec for a Superpower (methodology, decision trees, confidence model, heuristics, edge cases). |
| **`SKILL.md`** | The production-ready [Claude Code](https://claude.com/claude-code) Skill rendering of a Superpower, using progressive disclosure. |
| **`prompt.md`** | The portable, self-contained Markdown rendering of a Superpower for Claude.ai, the API, or any LLM. |
| **Progressive disclosure** | Keeping `SKILL.md` lean and loading deep `references/` material only when relevant, so triggering stays reliable and context cost stays low. |
| **Triggering** | Claude Code's decision to invoke a skill based on its `description`. Reliable triggering is a primary design goal. |
| **Confidence model** | The named confidence levels (e.g. Confirmed / High / Medium / Low / Speculative) a Superpower uses, each with an explicit evidence threshold. |
| **Eval** | A test case: a realistic input plus a rubric of MUST / MUST NOT / confidence-disclosure checks. Lives in `evals/`. |
| **Rubric** | The checklist used to score a Superpower's behavior on an eval (pass/fail per item). |
| **Golden example** | A maintainer-reviewed, end-to-end worked session in `examples/`; documents the Superpower and anchors regressions. |
| **Stability tier** | A Superpower's maturity: `experimental` → `beta` → `stable`. Tracks *trust*, independent of version number. |
| **Showcase** | Screenshots, GIFs, or example conversations in `showcases/` demonstrating a Superpower on a real problem. |
| **Playbook** *(future)* | A composite workflow chaining several Superpowers for an end-to-end task. |
| **Ecosystem** | The family of sibling repositories (`claude-superpowers-{web,qa,…}`) sharing this architecture. See [ecosystem.md](ecosystem.md). |

## Unity terms used across Superpowers

| Term | Definition |
| --- | --- |
| **Domain reload** | Unity reinitializing the scripting domain (e.g. on script compile or entering Play Mode), which resets static state — a common source of bugs. |
| **Execution order** | The defined order in which Unity calls MonoBehaviour messages (`Awake` → `OnEnable` → `Start` → `Update` → …); a frequent root cause of timing bugs. |
| **IL2CPP** | Unity's ahead-of-time scripting backend; introduces code-stripping and AOT constraints that cause build-only bugs. |
| **Serialization** | How Unity persists fields (e.g. `[SerializeField]`) into scenes/prefabs/assets; misuse causes "lost reference" and inspector bugs. |
| **Render pipeline** | Built-in, URP, or HDRP — guidance flags differences rather than assuming one. |
| **Player.log / Editor.log** | Unity's runtime and editor log files; primary evidence sources for debugging. |
