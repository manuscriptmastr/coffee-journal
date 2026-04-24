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

## Step 6: Ask the maintainer before inferring

A number of things about a journal cannot be read off the data without asking the maintainer directly. Inferring them from distribution shape or observational correlations will frequently mislead. Ask:

- **Exact score rubric.** What does each score level _mean_ to them? Modal scores from the distribution do not tell you whether "6" means "mediocre" or "safe default good." Bonus-point adjustments (cost, novelty, rarity) are also important — a rubric that mixes cup-quality and non-cup signals needs a flag.
- **Grinder model + scale orientation.** Higher-number-is-coarser is the common convention but not universal. Getting this wrong reverses every directional claim in the profile.
- **Storage protocol.** Freezing, degassing, resealing, room temperature vs. cellar — changes the aging curve entirely. "Days off roast" means different things under different protocols.
- **Conditions under which optional techniques are used.** For any lever the maintainer sometimes turns on and sometimes doesn't (alternate brewer, agitation tool, dilution, bypass), ask _when and why_ they reach for it. Observational averages on opt-in tools are often dominated by the selection rule, not the tool's effect. See "Pitfalls" below.
- **Notes / directive conventions.** What does a terse "finer next time" actually mean — a planned adjustment, a vague regret, or a note-to-self that was later overridden? Ask before parsing free-text for structured signal.
- **Brewer / recipe choice rules.** Is the brewer picked per-bean based on style, or rotated randomly? If bean-conditional, brewer choice is not an independent variable — treat it as a style prior rather than a quality lever.

Record the answers directly in §1–§6 of the profile, with a date and "(confirmed with maintainer)" annotation so later agents know the claim is source-of-truth rather than inferred.

## Step 7: Re-run sanity checks when new maintainer info arrives

Maintainer answers can change the assumptions behind earlier analyses. When a significant piece of information arrives (e.g., the storage protocol turns out to be different than assumed, a column turns out to conflate two instruments, a selection rule is disclosed), re-run the Step 3 drift-applicability checks and the affected holdout tests. Update the profile's verdict with fresh evidence rather than bolting a clarification onto the old analysis.

## Common pitfalls

- **Assuming a single maintainer's methodology transfers wholesale.** At least one journal in this repo is a counter-example: same guide, same analysis framework, but drift-based prediction disabled on empirical grounds.
- **Skipping the holdout test.** Without it you'll deploy a drift model that could be worse than the trivial baseline.
- **Over-engineering the profile on day one.** Fill §1–§8 with real data; scaffold the rest with TODOs. The profile grows with the journal.
- **Forgetting to exclude execution-failure brews.** If the raw data has a flag column for these, use it. Keep them in the dataset but exclude from calibration.
- **Confusing observation with causation on opt-in techniques.** If a lever (an alternate brewer, a rescue tool, a non-default water) is used only under specific conditions, its observational effect reflects _the conditions that triggered its use_, not the lever's own influence. "Technique X shows a −0.47 point average delta" is often explained entirely by "technique X is used only when the brew is already in trouble." Always ask the maintainer: _under what conditions do you use this?_ Do not model opt-in techniques as independent variables without a controlled comparison.
- **Treating bean-conditional choices as independent variables.** Related pitfall: if the maintainer picks brewer / recipe / water based on bean style, within-bean comparisons of those choices partially measure the selection rule, not the choice itself. Treat as a style prior.
- **Inferring a rubric from distribution shape.** Score distributions tell you nothing about what the scores _mean_ to the maintainer. Ask.
- **Treating an inferred storage protocol as confirmed.** "Maintainer probably freezes because the age curve peaks late" is a hypothesis, not a fact. Ask.
