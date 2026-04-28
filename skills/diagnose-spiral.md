# Skill: diagnose-spiral

**Trigger**: User describes a cup with small/watery/fragile flavors combined with any mouthfeel discomfort (scratchy, tight, rubbing, stiff, rough), or reports 2+ consecutive Score 3s while chasing finer.

The single most common and costly misdiagnosis in pour-over dial-in: calling overextracted cups underextracted and grinding finer, which makes the problem worse. This skill runs the decision tree for the ambiguous "small + mouthfeel" pattern.

## Trigger signatures

Apply this skill when the user reports any of:

- "Small / watery / fragile / thin" flavors **+** any mouthfeel discomfort (scratchy, rough, rubbing, tight, stiff, powdery)
- 2+ consecutive Score 3s while repeatedly grinding finer
- Astringency that reads as "green / papery / dry-sour" but with localized (not whole-mouth) texture — this is over-astringency, not under
- A cup that "seems underextracted but tastes dishonest / dull / collapsed / gravy-like"
- Acidity that only appears in the finish as a "warm glow," never immediate

## Pre-check: is the coffee under-rested?

Before running the under-vs-over decision tree, check the coffee's age. Cups brewed in the **first ~10 days off roast** can mimic the spiral signature (small flavors + mouthfeel discomfort) even at a correct grind setting — the cause is CO₂-blocked extraction and unsettled volatiles, not extraction direction. See AGENT_GUIDE §"Under-rested coffee (Day 1–14)".

Apply the under-rested cross-checks before grinding finer or coarser:

1. **Same off-flavor across two different beans from the same roaster** at similar days off roast → roast freshness, not grind miss.
2. **Same off-flavor across two different brewing waters** → not a water-mineralization issue.
3. **Same off-flavor on dry aroma + wet aroma + taste** → in the bean, not the brew.
4. **No improvement in cooldown** despite reading underextracted → CO₂-blocked, not honestly under.

If 2 of 4 hold and the coffee is < Day 14, **stop the spiral diagnosis**. The intervention is **time** (wait until Day 14–21), not grind. If the user must brew, La Cabra's <3-week recipe is finer + cooler (~194 °F) + shorter contact — opposite to "go coarser."

## Decision tree

For the canonical spiral signature (small flavors + mouthfeel discomfort), the guide's empirical finding is: **in most journals, overextraction is substantially more likely than underextraction**, and going finer fails the majority of the time.

Run the tiebreaker:

1. **Is mouthfeel scratchy / rubbing / rough / tight / powdery?** → Suspect over. Phenolics have built up. Go **coarser**.
2. **Is mouthfeel loose / clean / genuine, and flavors improve in cooldown?** → Suspect under. Complex aromatics come through as the cup cools. Go finer cautiously.
3. **Is acidity delayed to the finish as a warm glow, with no immediate brightness?** → Suspect over. Heavy late-extracting compounds are masking the acids upfront.
4. **Is acidity immediate but thin, and you "wanted more of what was there"?** → Suspect under.
5. **Whole-mouth clenching with stiff lips?** → Under (sourness tell).
6. **Localized scratchiness on tongue/roof without full-mouth clench?** → Over.
7. **Both sour AND bitter together?** → Possibly uneven extraction / channeling, not a grind issue.

## The probe-coarser rule

On surprise (Score 3 where you expected 4+), brew **one click coarser first** before trusting the extraction diagnosis:

- **If the coarser probe improves** → drift was faster than expected, hold coarser.
- **If the coarser probe worsens** → go two clicks finer from the original.

This two-step recovery avoids the spiral even when the initial diagnosis is wrong.

## The bracketing rule

When lost (2+ consecutive Score 3s), stop making single-click adjustments. Instead:

- Jump 2–3 grinder steps in one direction to **establish a bracket**.
- Confirm one setting clearly too coarse and one clearly too fine.
- Split the difference.

A single large correction that overshoots is more informative and recoverable than multiple small ones landing on the wrong side. The cautionary example is Joshua's H&S batch 3 Day 58–68 spiral: 24 entries of Score 3s before bracketing restored a Score 5.

## Reference-anchor check

Before concluding a cup is over, check for **reference-anchor bias**:

- Is "small flavor volume" being compared to a Day 8–14 peak cup with CO₂-driven perfuminess?
- Is the cup otherwise sweet-spot-coded (loose, defined acidity, honest flavors, clean mouthfeel)?
- Does a coarser probe fail to recover volume?

If yes, the cup is likely peaking for its age, not compressed. Stop chasing volume.

## Brilliant-acidity + small-volume probe

For cups with **defined, peaking acidity** ("brilliant", "effervescent", "grape candy") alongside **small volume** and **clean mouthfeel**:

- Brew one step coarser same day.
- **Coarsening softens the acidity / volume returns** → confirmed mild over; step finer.
- **Coarsening brightens acidity further / texture loosens further** → **not over**; varietal acidity has headroom, small volume is fine-edge character or reference-anchor artifact.

## Related profile sections

When diagnosing in Joshua's journal: see `joshua-martin/profile.md` §11 "Known failure modes" (La Esperanza 2 spiral, SEY misleading astringency, H&S batch 3 acceleration) and §13 "Vocabulary map" for per-descriptor direction.

When diagnosing in Tim's journal: per-brew tasting notes exist in `tim-hwang/brews_with_notes.csv`; see profile §12 for vocabulary patterns. Bitter is monotonic (cleanest negative); astringency is U-shaped (can appear at Score 8+ as bright-acidic, not rough-over).
