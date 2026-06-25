# Showcases

Visual proof that the Superpowers solve real Unity engineering problems.

This directory holds **screenshots, GIFs, and example conversations** demonstrating each Superpower in action. Showcases make the value obvious at a glance and are part of how a Superpower earns the `stable` tier.

## Structure

```
showcases/
└── <superpower-name>/
    ├── README.md            # short narrative + embedded media
    ├── conversation-*.md    # full example conversations (redacted)
    └── media/               # screenshots (.png) and GIFs (.gif)
```

## What makes a good showcase

- **Real problem, real fix.** Use an actual (redacted) bug or task, not a toy.
- **Before → after.** Show the messy input and the structured, confidence-rated output.
- **Honest.** If the Superpower asked for more info or hedged confidence, show that — it's a feature.
- **Lightweight media.** Prefer GIFs/screenshots under ~3 MB; trim to the relevant moment.

## How showcases relate to evals

A showcase conversation often starts life as a [worked example](../docs/authoring-guide.md#step-6--add-examples-1) or an [eval](../docs/testing-superpowers.md) case. Reuse them — a strong worked example is also a strong showcase.

## Contributing a showcase

1. Create `showcases/<superpower-name>/`.
2. Add a short `README.md` narrating the scenario and embedding media.
3. Drop screenshots/GIFs in `media/`.
4. Link it from the Superpower and, if notable, from the root README.

> Media files are added when captured. We keep the directory structure in place so contributions have an obvious home.
