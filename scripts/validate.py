#!/usr/bin/env python3
"""Structural validator for Superpowers.

Single source of truth for the structural (layer-4) checks described in
docs/testing-superpowers.md. Runs identically locally and in CI:

    python scripts/validate.py            # validate every Superpower
    python scripts/validate.py superpowers/debugging/unity-debugging-expert

Exits non-zero and prints every problem if anything fails. This checks *mechanics*
(files present, frontmatter, eval/trigger structure) so human reviewers and the
behavioral evals (layers 1-3) can focus on the quality of the reasoning encoded.
"""

from __future__ import annotations

import os
import re
import sys

ROOT = "superpowers"

REQUIRED_FILES = ["DESIGN.md", "SKILL.md", "prompt.md", "triggers.md"]
REQUIRED_FM = ["name", "description"]
REQUIRED_META = ["version", "stability", "category"]
REQUIRED_SKILL_SECTIONS = [
    "When to use this skill",
    "Methodology",
    "Confidence model",
    "Output format",
]
VALID_STABILITY = {"experimental", "beta", "stable", "deprecated"}

MIN_EXAMPLES = 1
MIN_EVALS = 2

# Sections every eval file must contain (see templates/eval.template.md).
REQUIRED_EVAL_SECTIONS = [
    "## Input",
    "## Expected triggering",
    "## Rubric",
    "### MUST",
    "### MUST NOT",
    "### Confidence disclosure",
]

# Headings + minimum entries for triggers.md (see templates/triggers.template.md).
TRIGGER_POS_HEADING = "## Should fire (positive triggers)"
TRIGGER_NEG_HEADING = "## Should not fire (negative triggers)"
MIN_POS_TRIGGERS = 3
MIN_NEG_TRIGGERS = 2


def find_superpowers(root: str) -> list[str]:
    found = []
    for dirpath, _, files in os.walk(root):
        if "SKILL.md" in files:
            found.append(dirpath)
    return sorted(found)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def count_bullets_after(text: str, heading: str) -> int:
    """Count top-level '- ' bullets in the block following a heading."""
    idx = text.find(heading)
    if idx == -1:
        return 0
    after = text[idx + len(heading):]
    # Stop at the next markdown heading.
    nxt = re.search(r"^#{1,6} ", after, re.M)
    block = after[: nxt.start()] if nxt else after
    return len(re.findall(r"^- ", block, re.M))


def validate_frontmatter(name: str, text: str, errors: list[str]) -> None:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{name}: SKILL.md missing YAML frontmatter")
        return
    fm = m.group(1)
    for key in REQUIRED_FM:
        if not re.search(rf"^{key}\s*:", fm, re.M):
            errors.append(f"{name}: SKILL.md frontmatter missing '{key}'")
    for key in REQUIRED_META:
        if not re.search(rf"^\s+{key}\s*:", fm, re.M):
            errors.append(f"{name}: SKILL.md metadata missing '{key}'")
    sm = re.search(r"^\s+stability\s*:\s*([A-Za-z]+)", fm, re.M)
    if sm and sm.group(1) not in VALID_STABILITY:
        errors.append(f"{name}: invalid stability '{sm.group(1)}'")


def validate_evals(name: str, ev_dir: str, errors: list[str]) -> int:
    if not os.path.isdir(ev_dir):
        return 0
    files = [x for x in sorted(os.listdir(ev_dir)) if x.endswith(".md")]
    for fn in files:
        text = read(os.path.join(ev_dir, fn))
        for sec in REQUIRED_EVAL_SECTIONS:
            if sec not in text:
                errors.append(f"{name}: evals/{fn} missing section '{sec}'")
        if not re.search(r"should-fire\s*:\s*(true|false)", text):
            errors.append(
                f"{name}: evals/{fn} missing 'should-fire: true|false' under Expected triggering"
            )
    return len(files)


def validate_triggers(name: str, sp: str, errors: list[str]) -> None:
    path = os.path.join(sp, "triggers.md")
    if not os.path.isfile(path):
        # Missing-file error already raised by the REQUIRED_FILES check.
        return
    text = read(path)
    if TRIGGER_POS_HEADING not in text:
        errors.append(f"{name}: triggers.md missing heading '{TRIGGER_POS_HEADING}'")
    elif count_bullets_after(text, TRIGGER_POS_HEADING) < MIN_POS_TRIGGERS:
        errors.append(
            f"{name}: triggers.md needs >={MIN_POS_TRIGGERS} positive triggers"
        )
    if TRIGGER_NEG_HEADING not in text:
        errors.append(f"{name}: triggers.md missing heading '{TRIGGER_NEG_HEADING}'")
    elif count_bullets_after(text, TRIGGER_NEG_HEADING) < MIN_NEG_TRIGGERS:
        errors.append(
            f"{name}: triggers.md needs >={MIN_NEG_TRIGGERS} negative triggers"
        )


def validate_superpower(sp: str, errors: list[str]) -> None:
    name = os.path.relpath(sp, ROOT)

    for f in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(sp, f)):
            errors.append(f"{name}: missing required file {f}")

    ex_dir = os.path.join(sp, "examples")
    ev_dir = os.path.join(sp, "evals")
    n_ex = (
        len([x for x in os.listdir(ex_dir) if x.endswith(".md")])
        if os.path.isdir(ex_dir)
        else 0
    )
    if n_ex < MIN_EXAMPLES:
        errors.append(f"{name}: needs >={MIN_EXAMPLES} example in examples/ (found {n_ex})")

    n_ev = validate_evals(name, ev_dir, errors)
    if n_ev < MIN_EVALS:
        errors.append(f"{name}: needs >={MIN_EVALS} evals in evals/ (found {n_ev})")

    skill_path = os.path.join(sp, "SKILL.md")
    if os.path.isfile(skill_path):
        text = read(skill_path)
        validate_frontmatter(name, text, errors)
        for sec in REQUIRED_SKILL_SECTIONS:
            if sec not in text:
                errors.append(f"{name}: SKILL.md missing section '{sec}'")

    validate_triggers(name, sp, errors)


def main(argv: list[str]) -> int:
    targets = argv[1:]
    if targets:
        superpowers = [t.rstrip("/") for t in targets]
    else:
        if not os.path.isdir(ROOT):
            print("No superpowers/ directory yet — nothing to validate.")
            return 0
        superpowers = find_superpowers(ROOT)

    if not superpowers:
        print("No Superpowers found under superpowers/.")
        return 0

    errors: list[str] = []
    for sp in superpowers:
        if not os.path.isfile(os.path.join(sp, "SKILL.md")):
            errors.append(f"{sp}: not a Superpower directory (no SKILL.md)")
            continue
        validate_superpower(sp, errors)

    if errors:
        print("Validation failed:\n")
        for e in errors:
            print(" -", e)
        return 1

    print(f"OK — {len(superpowers)} Superpower(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
