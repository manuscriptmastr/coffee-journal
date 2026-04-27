# Agent Instructions

_A vendor-neutral entry point for coding agents working in this repo (Codex, Cursor, Aider, Copilot, OpenCode, Claude Code, etc.)._

This repo contains a universal coffee-prediction methodology plus one or more maintainers' calibrated journals. To work effectively here, load these files:

1. **[`AGENT_GUIDE.md`](./AGENT_GUIDE.md)** — Universal methodology: drift physics, water chemistry, extraction vocabulary, prediction method, sweet-spot window edges, spiral diagnosis. Applicable to any pour-over journal.
2. **The `profile.md` from the relevant journal folder** — that journal's numeric calibration: equipment, recipe baseline, water, roaster groupings with drift rates, correction bias, vocabulary quirks, known failure modes.

Journal folders currently in this repo:

- [`joshua-martin/`](./joshua-martin/) — Joshua's journal (~1 year of daily entries, Lagom P64 + Z1/Orea, specialty light roast).
- [`tim-hwang/`](./tim-hwang/) — Tim's journal (~1900 brews, coarser-step grinder, drift-based prediction **disabled** — see that profile's §8 for the walked-through sanity checks). _Gitignored._
- [`pal/`](./pal/) — Pal's pour-over journal (~560 V60 brews + ~320 D27 brews, JX-Pro / A4z / ZP6 grinders, no score/date columns; drift-based prediction **disabled**; uses a five-axis taste card + composite quality proxy — see that profile's §5, §8, and §15). _Gitignored._

The guide is the method; the profile is the parameters. Read the guide first for context, then consult the profile whenever the guide says "your profile's drift table" or "the user's grinder step size."

## Skills (task-triggered procedures)

Vendor-neutral skill documents live in [`skills/`](./skills/). Load the matching file when the user's request fits its trigger:

- **[`skills/predict-grind.md`](./skills/predict-grind.md)** — user asks for a grind prediction for a specific coffee.
- **[`skills/new-journal-entry.md`](./skills/new-journal-entry.md)** — user asks to create a new entry in a journal. Enforces header-only, blank-body convention (reasoning goes in chat, not in the file).
- **[`skills/onboard-journal.md`](./skills/onboard-journal.md)** — user adds a new maintainer's journal; walks through folder shape, profile scaffolding, drift-applicability checks, and walk-forward validation.
- **[`skills/diagnose-spiral.md`](./skills/diagnose-spiral.md)** — user describes "small + mouthfeel discomfort" or a run of Score 3s; runs the under-vs-over decision tree and probe-coarser / bracketing rules.

## How to adapt this setup to another journal

Duplicate the journal-folder shape, populate a new `profile.md`, and run the walk-forward calibration loop described in `skills/onboard-journal.md`. The universal guide stays untouched.
