# Agent Instructions

This repo contains a universal coffee-prediction methodology plus one or more maintainers' calibrated journals. **Agents should load two files to predict a setting:**

1. **[`AGENT_GUIDE.md`](./AGENT_GUIDE.md)** — Universal methodology: drift physics, water chemistry, extraction vocabulary, prediction method, sweet-spot window edges, spiral diagnosis. Applicable to any pour-over journal.
2. **The `profile.md` from the relevant journal folder** — that journal's calibration: equipment, recipe baseline, water, roaster groupings with drift rates, correction bias, vocabulary quirks, known failure modes.

Journal folders currently in this repo:

- [`joshua-martin/`](./joshua-martin/) — Joshua's journal (~1 year of daily entries, Lagom P64 + Z1/Orea, specialty light roast).
- _(more maintainers can be added as sibling folders with the same shape)_

The guide is the method; the profile is the parameters. Read the guide first for context, then consult the profile whenever the guide says "your profile's drift table" or "the user's grinder step size."

To adapt this setup to another journal: duplicate the journal-folder shape, populate a new `profile.md`, and run the walk-forward calibration loop described in the plan. The universal guide stays untouched.
