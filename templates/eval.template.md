<!--
eval.template.md — copy to superpowers/<category>/<name>/evals/<scenario>.md
One eval per file. See docs/testing-superpowers.md. Delete comments before committing.
-->

# Eval: <scenario name>

## Input
<The exact user message(s) and any provided artifacts — stack trace, logs, code,
Unity version, platform, repro steps. Make it realistic and redacted.>

## Expected triggering
- should-fire: true | false
- <if false: which sibling skill should handle it instead, and why>

## Rubric

### MUST
- [ ] <e.g. asks for Unity version/platform if not provided>
- [ ] <e.g. produces the required output format>
- [ ] <e.g. identifies the correct root cause / cause family>

### MUST NOT
- [ ] <e.g. does not fabricate a fix without evidence>
- [ ] <e.g. does not claim "Confirmed" without a verified reproduction>

### Confidence disclosure
- [ ] <e.g. states a confidence level>
- [ ] <e.g. states what additional evidence would raise confidence>

## Notes
<What a strong vs. weak response looks like; edge cases; known traps.>
