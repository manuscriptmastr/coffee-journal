# Skill: onboard-journal

**Trigger**: User asks to add a new maintainer's journal to the repo, set up a new profile, or validate whether this repo's drift methodology applies to a new dataset.

Adds a new maintainer's journal to the repo and calibrates it.

## Step 1: Create the folder shape

Duplicate the structure of an existing journal folder (e.g., `joshua-martin/`):

```
<maintainer-slug>/
├── profile.md          — calibration parameters (required)
├── README.md           — one-screen intro + drift charts (optional but recommended)
├── <raw journal>       — prose Markdown, CSV export, or whatever the maintainer uses
├── scripts/            — ingestion / analysis / chart-making
└── assets/             — drift charts, validation plots
```

Then add a line to the root `README.md` and `CLAUDE.md` / `AGENTS.md` pointing at the new folder.

## Step 2: Scaffold profile.md

Use the 15-section template that Joshua's profile follows (see `joshua-martin/profile.md`):

1. Scope
2. Equipment (grinder, step size, brewer, shorthand codes)
3. Recipe baseline
4. Water
5. Rating scale
6. Entry format
7. Roaster groupings (with drift/day per group)
8. Drift-rate table
9. Correction bias (coarser/finer percentages by score)
10. Step-size distribution
11. Known failure modes
12. Diagnosis accuracy by roaster
13. Vocabulary map (maintainer-specific descriptor → direction)
14. Open questions / TODO
15. Holdout validation

Not all sections will be populated on day one — scaffold them with "TODO" and fill in as the journal grows.

## Step 3: Run the drift-applicability sanity checks

Before committing to drift-based prediction for this journal, run the checks in `AGENT_GUIDE.md` §"Does drift-based prediction apply to this journal?":

1. **Grinder step resolution.** Drift is ~0.01–0.03/day. If the grinder steps in ≥0.1, a day's drift is below one click → invisible in the data. Still record drift; just don't predict with it.
2. **Brew cadence.** Need ≥ 4 brews of a bean spanning ≥ 7 days to fit drift.
3. **Dial-in behavior.** If ≥ 30% of follow-up brews use the identical grind, drift isn't a dimension the user is exploring.
4. **Holdout MAE test.** For each bean with ≥ 6 brews, train three models on the first 3 brews: `drift` (linear slope), `last` (most recent grind), `mean` (average grind). Predict the rest. Compare MAE. If `drift` doesn't clearly win — and especially if it loses to `mean` — fall back to static prediction.
5. **Score-variance decomposition.** If roaster + bean explain >70% of variance and brewer <5%, time-based modeling has little room.

## Step 4: Document the verdict explicitly

In profile.md §8, state whether drift-based prediction applies, and which fallback is in use if not. See `tim-hwang/profile.md` §8 for an example of a profile that explicitly **disables** drift with full evidence.

## Step 5: Walk-forward validation

Once profile.md has drift rates documented, run a walk-forward holdout:

- Each prediction sees only prior history.
- Compare `last+drift`, `sibling+drift`, `last`, `bean_median`, `roaster_mean`, `global_mean`.
- Record MAE, RMSE, ≤1-click hit rate, ≤2-click hit rate.
- Add the table to profile.md §15. See `joshua-martin/profile.md` §15 for format.

## Common pitfalls

- **Assuming Joshua's methodology transfers wholesale.** Tim's journal is a counter-example: same repo, same guide, but drift disabled.
- **Skipping the holdout test.** Without it you'll deploy a drift model that could be worse than the trivial baseline (as it is for Tim).
- **Over-engineering the profile on day one.** Fill §1–§8 with real data; scaffold the rest with TODOs. The profile grows with the journal.
- **Forgetting to exclude skill-issue / execution-failure brews.** If the raw data has a flag column for these, use it. Tim's profile §10 documents 67 such brews excluded from calibration.
