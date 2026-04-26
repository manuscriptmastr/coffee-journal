# Joshua Martin's Coffee Journal

A personal journal for dialing in specialty light-roast coffees on a Lagom P64 grinder and Z1 brewer.

Each entry tracks the grind setting, age, score, and tasting notes. Over time, patterns emerge — coffees from the same roaster age at the same rate, and the sweet spot drifts coarser by ~0.012–0.030/day depending on roast level and processing.

See [`profile.md`](./profile.md) for the calibration — roaster groupings, drift rates, correction bias, known failure modes, diagnosis accuracy per roaster. See [`Coffee Journal.md`](./Coffee%20Journal.md) for the raw entries.

For the universal methodology this profile builds on, see [`../AGENT_GUIDE.md`](../AGENT_GUIDE.md).

## Charts and tables

All charts are inlined as Mermaid (`xychart-beta`, flowchart) directly inside `profile.md`. They render natively on GitHub.com; in other markdown viewers (VS Code preview, Obsidian without plugin, terminal renderers) they may degrade to code blocks but the surrounding tables and prose carry the same information.

- **Drift curves** — see [`profile.md` § 7 Hydrangea narrative](./profile.md#7-roaster-groupings) for the inline Mermaid fit, and [§ 8 per-roaster Score-5 anchors](./profile.md#8-drift-rate-table-summary) for the other roasters' anchor tables and OLS fits.
- **Predictor MAE bar chart** — [`profile.md` § 15](./profile.md#15-holdout-validation).
- **Correction bias by score** — [`profile.md` § 9](./profile.md#9-correction-bias).
- **Score-5 follow-up Δ by gap** — [`profile.md` § 10](./profile.md#10-step-size-distribution).
- **Vocabulary → direction decision tree** — [`profile.md` § 13](./profile.md#13-vocabulary-map-joshua-specific-descriptor--direction).
