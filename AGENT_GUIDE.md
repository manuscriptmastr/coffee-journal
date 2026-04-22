# Coffee Journal — Agent Guide (Universal)

This is the **universal** half of the agent methodology for predicting grind settings from a coffee dial-in journal. It applies to any pour-over, specialty-coffee journal, regardless of whose.

The **calibration** half — equipment, roasters, drift rates, personal vocabulary, scoring, biases — lives in a companion file (`profile.md` by default). Agents should always load both together.

## How to Read This Guide + Your Profile

- **This guide** gives you the physics, the vocabulary, the methodology, and the traps. It never names a specific grinder, roaster, or coffee.
- **The profile** gives you the numeric parameters and personal patterns for _this_ journal: grinder step size, typical grind range, roaster groups with observed drift rates, the user's personal vocabulary quirks, correction bias, and known failure modes.
- When the guide says "apply the drift rate from your profile," the profile has the table.
- When the guide says "round to the user's grinder step size," the profile tells you what that is.

If a field is missing from the profile, ask the user a concise clarifying question. Never block prediction on missing data — fall back to conservative defaults, note the assumption, and flag it.

## The Goal

Predict the **sweet spot** grind setting for a given coffee at a given age (days since roast). The sweet spot is the extraction level where acidity, sweetness, complexity, and mouthfeel all come together harmoniously.

## Agent Quick-Start: Predicting in Under a Minute

When asked to predict a setting:

0. **Check the current date first** (your `current_datetime` or equivalent). Then determine the correct Day number by comparing to the most recent entries in the journal — do **not** assume today is one day after the last entry, and do **not** increment Day X blindly. Multiple brews happen on the same calendar day, and days can be skipped. If the journal's latest batch-mate entries are dated today and already at Day N, the coffee you're predicting is also Day N (not N+1).
1. **Find the 1–3 most recent entries for this coffee.** If any are Score 5 or "Sweet spot" marked, that's your anchor.
2. **Find the most recent entry for any sibling from the same roaster/batch at a comparable age.** A sibling cup from yesterday beats an older anchor from this coffee. A sibling cup from **today** at the same Day number is the strongest anchor of all — use its setting directly (accounting for any diagnosis).
3. **Add drift × days elapsed** using your profile's drift table. If the roaster isn't listed, fall back to the profile's default drift rate (or ~0.020/day if the profile doesn't specify). If days elapsed is 0, don't add drift. **If the profile disables drift prediction** (see "Does drift-based prediction apply to this journal?" below), skip this step and use the profile's static-grind strategy instead.
4. **Round to the user's grinder step size.** When two options are equally defensible, **pick the coarser one** (most journals' corrections skew coarser; the user's step-size distribution in the profile confirms whether a single-step miss is meaningful or below noise). A one-click miss is usually inside the sweet-spot window.
5. **Sanity checks before replying:**
   - Consult the profile's "Known failure modes" section — does this coffee / roaster group have a cautionary pattern?
   - Is this a low-Score-5-history coffee or roaster? Still chase the 5 via grind — don't settle preemptively. Historical distributions reflect past dial-ins, not coffee ceilings.
   - Is this Day < 14? Fresh coffees are noisy. Trust backtracking from older dialed-in entries more than first-cup impressions.
   - Did the user recently note "finer side of sweet spot"? Add one more click coarser than the raw drift math says.

## Reading a Journal

Entries typically follow a header-plus-notes pattern:

```
## CoffeeName, Brewer, GrindSetting @ Temp, Dose/Water Day X Sentiment, Score: X
Tasting notes and next-setting suggestions.
```

The exact format is journal-specific — the profile documents this user's header template and abbreviations. Universal conventions:

- **Grind direction**: "Coarser" = larger particles = less extraction. "Finer" = smaller particles = more extraction. Underextracted → go finer. Overextracted → go coarser. Most grinder dials use higher numbers for coarser, but verify in the profile.
- **Ratings**: Typically a 1–5 scale appended as `Score: X`. **5** = transcendent; **4** = solidly good; **3** = enjoyable with obvious flaws; **2** = unenjoyable; **1** = gross (rare). When scoring is ambiguous, read the notes — sentiment in prose is a more reliable signal than a terse header. Recurring glowing adjectives (e.g., "Stunning", "Knockout", "Magical", "Musical" — the profile lists this user's set) reliably proxy Score 5 even when the explicit score was omitted.
- **Sweet-spot markers**: Users flag dialed-in cups with their own convention (`**Sweet spot**`, "dialed in", etc. — profile records theirs).
- **"Should have been X"**: A correction — the user's retrospective estimate of the true sweet spot for that day. These are gold for calibration.
- **Day X**: Days since roast date.

## Core Concept: Sweet Spot Drift

As coffee ages, its sweet spot shifts **coarser** (toward less extraction). A coffee dialed in at setting S today will be slightly overextracted at S tomorrow — it needs a small bump coarser.

The drift is approximately linear within a coffee's active window (roughly Day 15–60, but light roasts can extend much longer), though it can curve. Within a given roaster's batch, drift can **decelerate** with age or **accelerate** past some threshold. Acceleration is the more dangerous pattern — it causes chasing with conservative steps to fall behind the curve.

**Linear vs. quadratic**: For short-range predictions (a few days out), a linear model works as well as a quadratic one. The quadratic term is typically small (~0.0001–0.0003/day²) and matters only over 10+ day gaps. **Use linear for day-to-day predictions.** If recent entries consistently overshoot or undershoot by one click in the same direction, the drift rate has shifted — adjust the slope rather than fitting a curve.

**Why drift happens** ([Gagné](https://coffeeadastra.com), _The Physics of Filter Coffee_; [Hoffmann](https://www.youtube.com/@jameshoffmann), _The World Atlas of Coffee_): As coffee ages, CO2 escapes and the cellular structure becomes more porous, making the coffee easier to extract. The same grind setting extracts more from older coffee → overextraction → must go coarser to compensate. Early erratic behavior (Day 1–14) is largely from CO2 disrupting the brew bed and repelling water, causing uneven extraction regardless of setting. Processed coffees (honey, natural, anaerobic) tend to drift faster than washed because their more developed sugars and soluble compounds make the extractability shift more pronounced.

**Drift rate correlates with longevity.** Slower-drifting coffees maintain quality longer; faster-drifting coffees have narrower active windows and are harder to track at older ages.

### Drift-tracking vs. correction: two different moves

A grind-setting change between entries can mean two very different things, and conflating them is the easiest reasoning error to make:

1. **Drift-tracking**: Bumping coarser by the day's drift amount to stay on the moving sweet spot. The cup is expected to taste ~the same across days — same profile, same score — if drift is tracked correctly.
2. **Correction**: Moving further than drift predicts (or against drift) to change the _extraction profile_ of the cup — to fix an under or over.

**The two look identical in the data but mean opposite things.** If yesterday's setting scored 3 and today's setting (one click coarser) scores 5, you **cannot** conclude yesterday was overextracted. You only know today tracked the curve. Yesterday's Score 3 could have been a genuine overextraction, a normal drift-tracking cup that was off for unrelated reasons (brew variance, palate, water), or anything between.

**What counts as evidence of a profile change (vs. drift-tracking):**

- A **same-day A/B** at two settings.
- A **sibling at the same setting** scoring differently on the same day (batch-level dial-in signal).
- A setting that **fell behind the curve** (under-tracked by 2+ days) reading as _smaller/focused_ rather than _watery/fragile_ — that falsifies the overextraction explanation.
- A setting more than ~2 drift-units away from expectation where the score still landed well — implies the window is wider or the drift rate is off.

**What does NOT count as evidence:**

- A one-click bump matching daily drift producing a Score 5. That's the prediction working, nothing more.
- "Going coarser restored the X quality" over a 1–2 day gap. Drift alone would have done that.

**For sensation-based diagnosis** ("smaller + more focused", "bright but thin", etc.): these are only actionable when you can rule out **natural batch aging** as the cause. Volatile aromatics deplete as coffee ages — the cup can legitimately become _smaller and more focused_ at the sweet spot as a property of the aging arc, not a grind miss. Before treating "smaller + focused" as evidence of mild overextraction, ask: has the _score_ dropped, or has only the _character_ shifted? A Score 5 that "feels smaller" than it did a week ago is usually the batch evolving, not the setting drifting.

### Does drift-based prediction apply to this journal?

The drift framework above is the core methodology of this guide, but it is **not** universally applicable. Before using it on a new journal, verify the hypothesis holds on this user's data. If it doesn't, predictions based on drift will be worse than a trivial baseline — sometimes much worse.

**Sanity checks, in order:**

1. **Grinder step resolution.** Drift is typically ~0.01–0.03 per day. If the user's grinder steps in 0.1 or coarser, a day's drift is below one click and the drift signal will be invisible in their data. Drift still physically happens — the user just can't act on it. In this case, predictions should rely on bean/roaster-conditional priors and ignore day-number.
2. **Brew cadence.** Drift fitting requires multiple brews of the same coffee at different days-off-roast. A user who brews a given bag ~3 times across 2 days has no drift signal to fit. Rule of thumb: need ≥ 4 brews of a bean spanning ≥ 7 days.
3. **Dial-in behavior.** Look at consecutive same-bean brews. Does the user actually adjust grind as coffee ages, or hold it constant and vary other things (water, ratio, brewer, temperature)? If ≥ 30 % of follow-up brews use the identical grind, drift is not a dimension the user is exploring; other covariates dominate.
4. **Holdout test before deploying.** For each bean with ≥ 6 brews, train three models on the first 3 brews: `drift` (linear slope), `last` (most recent grind), `mean` (average grind). Predict remaining brews. Compare MAE. **If `drift` is not the clear winner — and especially if it loses to `mean` — fall back to `mean`- or `last`-grind prediction.** This takes ~50 lines of Python to run and saves weeks of wrong predictions.
5. **Score-variance decomposition.** For reference, Joshua's journal shows ~20 % of score variance attributable to time/drift. A journal where roaster + bean explain > 70 % of variance and brewer explains < 5 % will benefit little from time-based modeling.

**If drift does not apply:** the rest of this guide still matters — water chemistry, taste vocabulary (if the user records notes), under-vs-over diagnosis, sibling logic — but the prediction method in the next section must be swapped for a static prior (bean-conditional mean → roaster-conditional mean → population mode). The profile should explicitly disable drift-based prediction and note which fallback is in use.

**Signs drift does apply:** users with fine-step grinders (≤ 0.05 / click), entry cadence of ≥ 1 brew/day during active dial-in, a habit of recording "should have been X" corrections, and prose tasting notes describing extraction direction. When these are present, the full framework below is the highest-accuracy prediction method we have.

## Water Chemistry

Water composition has a first-order effect on where the sweet spot sits on the grind dial. It doesn't change the _shape_ of drift — it shifts the _baseline_ (the intercept). When a user switches waters, predictions should re-anchor to the first dialed-in entry on the new water and proceed normally from there; drift rate (slope) is preserved.

**How water affects extraction** ([Colonna-Dashwood](https://maxwelldashwood.com)/[Hendon](https://pubs.acs.org/doi/10.1021/jf501687c), _Water for Coffee_; [Gagné](https://coffeeadastra.com/2018/12/16/water-for-coffee-extraction/); [Rao](https://www.scottrao.com/blog/2023/6/4/demystifying-water-for-coffee)):

- **General Hardness (GH — calcium and magnesium)** is the extraction engine. These ions penetrate coffee cell walls and bind to flavor compounds. More GH = more extraction at the same grind setting.
- **Alkalinity (KH — bicarbonate)** is a buffer that neutralizes acids post-extraction. More KH = less perceived acidity, smoother but potentially flatter cup. [Rao](https://www.scottrao.com) calls alkalinity "the single most important factor in how water will affect coffee flavor."
- **Magnesium vs. calcium** ([Hendon et al. 2014](https://pubs.acs.org/doi/10.1021/jf501687c), _J. Agric. Food Chem._): Mg²⁺ binds more strongly to desirable acids (citric, malic, lactic) than Ca²⁺. Magnesium-forward water produces brighter, more acidic cups; calcium-forward water produces more body and creaminess.

**Why water changes shift grind setting**: Higher-GH water extracts more → same grind tastes more extracted → must grind coarser. Lower-GH water extracts less → must grind finer.

**RO water caution**: Store-bought RO water is unreliable as a baseline. Output TDS varies widely (5–50+) depending on source water, membrane age, and servicing schedule. The remaining minerals are disproportionately sodium (low extraction power) vs. the calcium/magnesium that drive extraction. The same store's RO water can change between refills, making calibration unstable. Treat RO water entries as noisier than mineralized-water entries — the intercept shift may not be consistent across refills. Don't let noisy RO entries override the consensus curve; look for Score 5s on the same water at the same setting to disprove an apparent intercept shift before acting on it.

**Brewing-temperature vs. drinking-temperature**: Temperature is secondary to grind size for pour-over ([Batali et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7536440/); [Rao](https://www.scottrao.com); [Gagné](https://coffeeadastra.com/2018/11/30/brewing-better-coffee/)). At fixed extraction yield, 87°C and 93°C coffee is sensorially indistinguishable. Fix temperature high (near boiling for light roasts), adjust grind only. Slurry temperature is 5–15°C below kettle temperature and falls across multi-pour recipes ([Gagné](https://coffeeadastra.com/2019/09/06/an-investigation-of-kettle-temperature-stability/)). Drinking-temperature matters more than brewing-temperature for perception: sweetness peaks ~44°C, acidity ~25°C, maximum flavor complexity 31–37°C. Light roasts taste _better_ as they cool — "musical, shimmering" qualities are most perceptible in cooldown.

## Prediction Method

### 1. Find the coffee's recent data

Read the most recent entries for that coffee. Identify:

- The last confirmed sweet spot (or "should have been" correction)
- The grind setting and day number
- Any qualifiers ("finer side", "barely underextracted") that shift the true sweet spot by roughly one grinder step

### 2. Check sibling coffees from the same roaster

Coffees from the same roaster at similar ages tend to converge on the same grind setting. If Coffee A hit sweet spot at setting S on Day N, and you're predicting Coffee B from the same roaster on Day N+1, that's strong evidence for S + one drift-unit.

**A recent near-miss from a sibling is more predictive than an older confirmed sweet spot.** If Coffee A scored 5 two days ago at S, but Coffee B scored 4 (barely under) yesterday at S + one drift-unit, use Coffee B's data as the anchor — it's fresher.

**When in doubt, assume coffees from the same batch track together.** Even genuine outliers within a batch rarely diverge more than ~0.05–0.1 from siblings at the same age. This prior is especially strong for noisy coffees where a single data point would mislead.

When comparing siblings, always **normalize to the same age**. If Coffee A (roasted Day 0) was sweet spot S on Day 60, and Coffee B (roasted 2 days later) is being brewed on the same calendar date, Coffee B is Day 58 — two days younger. At drift D/day, Coffee B's sweet spot is S − 2D. Equal trajectories; the difference is just age.

### 3. Estimate drift rate

Use the **local (recent) drift rate** rather than a full-regression slope, especially for older coffees where drift may decelerate or accelerate. The profile's drift table should give per-roaster-group rates, often with age-window caveats (e.g., "accelerates past Day 58", "decelerates after Day 40"). Typical pour-over light-roast drift rates span roughly **0.010–0.035/day** across roasters; if the profile doesn't list this roaster, default to ~0.020/day and flag the assumption.

**Drift is a curve, not a single rate.** For a given coffee or batch, drift commonly passes through three regimes:

1. **CO₂ phase** (~Days 8–14, sometimes extending to Day 17 for dense light roasts): drift is very slow (~0.005–0.015/day). Fresh-coffee perfuminess and CO₂ lift dominate perceived cup quality; sweet-spot settings barely move.
2. **Mid-life ramp** (~Days 14–20): drift settles into the roaster's "textbook" rate (~0.020–0.030/day for most light-roast pour-over profiles). This is the stablest, most-predictable phase.
3. **Late-life acceleration** (~Day 20+): drift _increases_ past the mid-life rate, commonly to 0.035–0.050/day, as volatile compounds deplete and extraction kinetics shift. Score 5s become harder to land because a click of grinder resolution no longer reliably covers a day of drift.

When predicting, identify which regime the coffee is in before applying a rate. A Day-10 coffee and a Day-22 coffee from the same batch can have drift rates that differ by **3–5×**. Using a batch-wide average across regimes will systematically mispredict at both ends. The **marker for entering late-life acceleration** is a drop in Score 5 frequency without a corresponding vocabulary change — the coffees still taste fine, but the "right" setting moves faster than one click a day, so most brews land a half-click off center.

### 4. Predict and round

```
predicted = last_sweet_spot + (drift_rate × days_elapsed)
```

Round to the user's grinder step size. **When ambiguous, round coarser** — overextraction triggers the spiral (costly multi-brew recovery), while underextraction just produces a mediocre cup (one-brew correction). Most journals' "should have been" corrections point coarser the majority of the time; the profile records the specific percentage for this user.

**When lost (2+ consecutive Score 3s), make bigger jumps (2–3 grinder steps) rather than conservative single-step increments.** Chasing with single clicks while drift accelerates produces a string of Score 3s. A single large correction (even if it overshoots slightly into underextraction) is more informative and recoverable than multiple small ones landing on the wrong side. The goal is to **establish a bracket** — one setting confirmed over, one confirmed under — then split the difference. Bracketing is faster than incremental crawling in one direction.

**On surprise (Score 3 where you expected 4+), probe coarser first.** Don't trust the extraction diagnosis — it's typically only ~55–70% accurate (see § Diagnosis reliability). Brewing one click coarser is the safer test: if it improves, drift was faster than expected. If it worsens, go two clicks finer from the original. This two-step recovery avoids the spiral.

### 5. Sanity check

- The sweet spot window is typically ~2–3 grinder steps wide. Being one click off is almost always fine.
- Fresh coffees (Day < 14–21) are unreliable — "wait" is often the right answer.
  - The first cup from a newly opened bag often tastes disproportionately good regardless of setting ("first cup magic"), then the coffee quickly shifts to its true sweet spot. Early entries are useful signal but noisy — don't anchor too heavily on them.
  - For fresh coffees from a known roaster, backtracking from later dialed-in entries (using drift rate in reverse) often gives a better early-day prediction than trusting the first few cups.
- The active window is roughly Day 17–60 for most coffees, but light roasts can peak much longer — 3+ months easily. When a coffee seems "off" at older ages, **blame the setting, not the coffee.** The sweet spot is still there; it's just harder to find as drift accumulates small errors. Treat "ceiling coffees" and "floor coffees" as artifacts of incomplete dial-in, not intrinsic properties — historical score distributions should not lower prediction ambition.
- When one coffee's trajectory diverges from its siblings, prefer the consensus unless there's strong evidence. Noisy data from a single coffee shouldn't override the batch trend.
- Watch for the **overextraction spiral** — going past the sweet spot finer makes symptoms mimic underextraction, tempting you to go even finer. See § Distinguishing under vs. over when flavors are small.
- Verify day numbers by calculating from roast dates when available — journal day numbers can have errors.
- **"Finer side of sweet spot" / "coarser side" qualifiers reveal micro drift.** If a coffee lands on the finer side today, tomorrow it may need a one-step bump coarser. If drift is slower than one step/day, a setting may hold for two days before needing a bump.
- **Sentiment outweighs diagnosis.** The user's descriptors (what the cup tasted and felt like) are more reliable than their extraction-direction call, which is often wrong. When diagnosis conflicts with descriptors, trust the descriptors and form your own read on direction.
- Diagnoses are most reliable for coffees with vivid, repeatable flavor profiles. Subtle or vague coffees produce noisier diagnoses — lean more on sibling data.
- **Score 5 cups are convergence results, not correction results.** In the data, the large majority of Score 5 entries follow a Score 4 or another Score 5 for the same coffee — not a "should have been" correction. The path to a Score 5 is gradual refinement (3→4→5), not a lucky correction. When a coffee has been at Score 4 for 2–3 entries, the setting is very close — a single-step adjustment may unlock the 5.
- **A Score 5 setting is a snapshot, not a steady state.** Holdout on one journal (n=42 follow-ups within 3 days) shows ~86% of next brews go coarser and 0% finer, with the realised step closely tracking the documented per-roaster drift rate. Default to "tomorrow ≈ today + one drift-step coarser" rather than repeating the winning grind. Verify on your journal — if the "kept-setting" rate after Score 5 is high, the user's drift rate is slower than one step/day and the rule weakens.

### Diagnosis reliability

**User extraction-direction diagnoses are typically right about 55–70% of the time**, depending on roaster and the user's calibration. Reliability is highest for roasters whose coffees have vivid, repeatable flavor profiles, and lowest for roasters whose profiles are subtle or heterogeneous. The most common misdiagnosis is attributing **scratchiness/roughness to underextraction when it's actually overextraction** — the signature of the spiral.

These numbers are partially confounded by drift-tracking: a coarser move between days is often the correct prediction regardless of diagnosis, so next-entry improvement doesn't cleanly isolate diagnosis accuracy. Still, the empirical near-equivalence of finer-vs-coarser moves after a lone "underextracted" call (both land roughly 55–65% improvement in most journals) supports the conclusion that **a lone direction diagnosis barely distinguishes direction**. Weight sibling data and the coarser-bias rule over the user's direction call when they disagree. **The diagnosis is a hint, not a verdict.**

## Taste Vocabulary → Extraction Direction

### Overextracted (go coarser)

- "Dull", "flat", "pungent finish", "brown", "staling"
- Heavy/dominant black tea (not the pleasant kind)
- "Gravy-like" finish
- Loss of distinct acidity — flavors become homogeneous
- Roughness, tightness, scratchiness in mouth
- "Acidic but missing florals" (counter-intuitive but widely confirmed)
- "Concentrated", "heavily focused", "introverted" flavors (vs. loose and bright) — subtle overextraction sign

### Sweet spot

- "Musical", "shimmering", "melded", "glowing"
- "Plump", "mouthfilling", "expansive", "loose"
- "Crystal clear", "effortless"
- Recognizable flavors integrated with sweetness
- Defined, lasting finish without heaviness
- Scientifically, this is the point where complex late-extracting aromatics (fruity/floral compounds like beta-damascenone) have fully dissolved while [harsh phenolics haven't yet overwhelmed them](https://www.sciencedirect.com/science/article/pii/S1387380616000440). Aromatic compounds extract in order of polarity: bright/buttery notes first, complex fruity/floral depth mid-extraction, harsh/smoky phenolics last.
- **Acidity timing in the sip** distinguishes extraction levels: at the sweet spot, acidity is **immediate and integrated** — bright from the first sip, woven into sweetness. When underextracted, acidity is **far-off and searching** — you sense it could be there but it never fully arrives. When overextracted, acidity is **delayed to the finish** — heavy late-extracting compounds (phenolics, melanoidins) mask the acids upfront, but the acids emerge as a "warm glow" in the finish once the heavier compounds clear the palate. This last signal is easy to mistake for a positive quality, but if acidity only appears in the finish and not immediately, the cup may be over.

### Edges of the sweet-spot window (still Score 5, but trending)

The sweet spot is a window ~2–3 grinder steps wide, not a point. Two distinct signatures mark its edges — both can still earn Score 5, but they tell you which direction the coffee is headed:

- **Coarser edge (mild under, no roughness):** "soft", "gentle", "barely out of focus", "mouthfilling but diffuse", "may be fully focused by next cup". Big volume, bright qualities present, no astringency or scratchiness — just slightly unresolved. Drift will catch up within a day; **no corrective action needed.**
- **Finer edge (mild over, slight roughness):** "barely smaller flavor volume", "slight roughness, localized", "focused / resolved / introverted", "black tea forward", "pleasant perfuminess, edges softening". **Bump coarser next brew** — ignoring this signature lets it accumulate into the spiral.

The tiebreaker between the two: **mouthfeel**. Coarser edge = loose and diffuse. Finer edge = any hint of scratch/rough/tight, even subtle.

### Underextracted (go finer)

- "Watery", "fragile", "toyish", "small flavor volume"
- "Hollow" — aromatics and dynamics present in the surroundings of the cup, but no substance or development in the actual flavor. Strongly underextracted signal when it appears.
- Far-off flavors, "searching" for tasting notes
- Flavors present but not "focused in"
- "Unfocused", "dulled", "missing edge / definition", "nothing shining" — **ambiguous**; can appear on either side. If accompanied by "acidity not genuine / cocoa off / balanced but flat" or any mouthfeel rubbing, suspect mild over. Confirm with a tiebreaker brew before committing.
- Can also show tight astringency (overlaps with overextraction — context matters, see § Astringency)
- "Salty" or "saline" quality (a reliable under signal per [Perger](https://www.baristahustle.com))
- On low-mineral water (RO), underextraction can be more pronounced — the water lacks the ionic "grip" to extract flavor compounds, so even a correct grind setting may read as underextracted. Finer grind compensates, but the cup character may differ from mineralized water.

### Distinguishing under vs. over when flavors are small

Both under and overextraction can produce small, underwhelming cups. The key difference:

- **Under**: Flavors are honest but small — "I liked what was there and wanted more." Improves in cooldown as complex aromatics ([beta-damascenone](https://pmc.ncbi.nlm.nih.gov/articles/PMC8230519/) and similar quality markers) become more perceptible at lower temperatures.
- **Over**: Flavors are dishonest — dull, collapsed, homogeneous. "Gravy-like." Harsh phenolic compounds have overwhelmed the delicate aromatics. Mouthfeel rough/scratchy.
- **Mouthfeel is the tiebreaker**: scratchiness/roughness = over, almost always. Loose/genuine texture with small flavors = under. This works because [retronasal olfaction shares processing circuitry with the gustatory (taste) cortex](https://pmc.ncbi.nlm.nih.gov/articles/PMC6604050/) — mouthfeel and flavor perception are neurologically intertwined.

**The spiral's signature:** "small/watery/fragile" flavors + any mouthfeel discomfort (scratchy, rubbing, tight, stiff). When both signals appear together, **overextraction is substantially more likely than underextraction** in most journals' data — going finer from this pattern fails the majority of the time. **When in doubt, go coarser.**

**Distinguishing over from under when both "small" and "mouthfeel" are present:**

- **Suspect over:** flavors are dull, concentrated/focused, or "introspective"; mouth is stiff without brightness; acidity delayed to finish rather than immediate; no improvement in cooldown.
- **Suspect under:** flavors are bright and honest but need more; improves notably in cooldown; texture is loose/genuine despite being small; acidity is immediate but thin.

### Distinguishing under vs. over when astringency is present

Astringency can appear on both sides of the extraction curve (confirmed by [Perger](https://www.baristahustle.com), [Hoffmann](https://www.youtube.com/@jameshoffmann), [Hedrick](https://www.youtube.com/@LanceHedrick)). The character differs:

- **Underextracted astringency**: "Green", "papery", "dry-sour" — a tannic, tea-bag-steeped-too-long quality. Often accompanied by sourness and quick finish. **Whole-mouth clenching/puckering with stiff lips** is a sourness/underextraction tell — the entire mouth reacts to the acid.
- **Overextracted astringency**: "Rough", "scratchy", "raspy", "powdery" — a sandpaper-on-tongue quality, typically localized (tongue, roof of mouth) **without** the full-mouth clenching. Often accompanied by dullness and collapsed flavors.
- If astringency appears alongside **sour + bitter simultaneously**, the issue may be **uneven extraction** (channeling/bypass) rather than grind setting — the bed has both over- and under-extracted zones ([Rao](https://www.scottrao.com), _Everything but Espresso_; [Perger](https://www.baristahustle.com)).

### Three calibration laws (derived across journals)

These are the highest-leverage heuristics, surfacing counter-intuitively in most journals' data:

1. **Loose and expansive and voluminous is more indicatory of the sweet spot than defined acidity.** Bright acidity alone can coexist with overextraction.
2. **"Acidic but missing florals" is overextracted, not underextracted.** The florals are the first casualty of crossing the line.
3. **Any roughness, tightness, dryness, or scratchiness in mouth is likely overextraction.** This is the #1 source of misdiagnosis — the reflex to call it "under" and grind finer is the spiral's front door.

### Multi-coffee ambiguity: probe before committing to a direction

When **two or more unrelated coffees** on the same day all lose a point at the same incremental step with overlapping "off-peak but not clearly wrong" vocabulary ("unfocused", "dulled", "missing edge / definition", "nothing shining", "watery", "hollow"), it's tempting to read this as a systemic signal — e.g., stalled drift pushing every coffee past its coarse edge at once. **Resist the urge to commit to a direction from vocabulary alone.**

The trap: coffees at the same setting can sit on opposite sides of their own sweet spots, and the same off-peak language ("dulled", "missing edge", "nothing shining") can come from either mild under OR mild over. Homogeneous/introverted phrasing especially — "balanced but nothing shining", "acidity not genuine", "cocoa a little off" — reads like under but is frequently **mild over**. Only a few descriptors are reliably one-sided: "watery" (under), "hollow" (under), and anything with mouthfeel discomfort (over).

The reliable move is to **probe with a tiebreaker brew** on whichever coffee has the most ambiguous signal: brew it one step in either direction the same day and compare.

- If the probe cup **improves** → the earlier cup was past the coarse edge; step the others back toward their last Score-5 or hold.
- If the probe cup **degrades with mouthfeel discomfort** (rubbing, rasp, heavy/stinky finish, "cocoa off") → the earlier cup was mild over; step **coarser** beyond the earlier setting.
- If neither direction clears it → the coffees are on different sides of their individual windows, and each needs its own probe.

One unambiguous tiebreaker cup is worth more than any amount of cross-coffee vocabulary pattern-matching.

### Brilliant acidity + small volume: coarser-probe test

When a cup presents **defined, peaking acidity** ("brilliant", "effervescent", "grape candy", "sharp") alongside **small flavor volume** and **clean mouthfeel** (no rubbing/rasp), two diagnoses compete:

- **Mild over**: acidity is peaking because aromatic complexity has collapsed around it; phenolics haven't built enough for rubbing yet but are compressing volume.
- **Sweet-spot window with varietal acidity that has headroom**: the coffee's acidity keeps unlocking further as you go coarser; "small volume" may be a reference artifact (see below).

The probe is diagnostic: **brew one step coarser the same day**.

- **If coarsening softens the acidity** (integrates it, or shifts brightness → warm-glow finish) and **volume returns** → confirmed mild over; step finer from the original setting.
- **If coarsening makes the acidity _even brighter_** and the texture **"even looser"** without volume recovering → **not over**. The coffee was inside or near its sweet-spot window; acidity has headroom at coarser settings, and the "small volume" symptom is either fine-edge character or a reference-anchor artifact.

Over-extraction's bright acidity is _fragile_: it does not unlock further under coarsening. Acidity that intensifies when you coarsen is sweet-spot acidity with room to open up, not compressed acidity being relieved.

### The reference-anchor bias

"Small flavor volume" evaluated against a recent peak cup from the **young-coffee period** (Days 8–14, fresh CO₂ perfuminess still dominant) can be a **reference-bias artifact rather than a real compression signal**. Fresh coffee contributes perceived flavor volume through perfuminess and CO₂ lift that fades regardless of grind — by Day 20+ the same coffee genuinely cannot produce the same "big first impression," even at peak extraction.

Symptoms of reference-anchor bias:

- Cup reads "small" or "delicate" alongside otherwise-sweet-spot markers (loose, defined acidity, honest flavors, clean mouthfeel)
- The mental comparison is to a specific early-days cup (often explicitly remembered as "one of the best" or "peak perfuminess")
- Coarsening probe does not recover the "volume" — because there's nothing to recover; the deficit is temporal, not extraction-based

When the bias is in play, stop chasing volume and characterize the _new_ window the coffee is in. Score 4s that aren't missing anything extraction-addressable are the signature of a coffee past its young-peak; they represent the best that setting can produce and shouldn't be treated as near-misses.

### Per-coffee coarse-tolerance (same-setting, same-day, opposite inflection)

When sibling coffees from the same batch all land Score 4 at the same setting on the same day but show **different deficit inflections**, the likely explanation is _not_ that the batch entered a narrow window or that drift stalled — it's that each coffee's **coarse-tolerance** differs. The sweet-spot center is roughly shared; how far past it each coffee can go before registering under-signs is not.

How it presents:

- Same roaster, same batch, all at grind setting G on day D, all Score 4
- Coffee A: **brilliant / effervescent / loose** with small volume — bright-side deficit
- Coffee B: **soft / limp / could be brighter / fantastic clarity** — muted-side deficit
- A coarsening probe on A unlocks _more_ brightness (SS-window with varietal headroom)
- The journal-keeper's own instinct on B is to go _finer_ (correctly reads it as under-leaning)

What it means:

- The SS center for the day is probably finer than G (B's instinct is right)
- A is **coarse-tolerant** for its variety — its acidity/character structure doesn't collapse past SS, it just goes looser
- B is **coarse-intolerant** — past SS, it reads muted or limp rather than bright-but-loose
- Drift rate per coffee has _not_ diverged; what differs is how each coffee _fails_ when you pass SS

Action: set next-brew for B at the finer setting (the SS center). For A, either match B's setting to confirm the shared center, or stay coarse and accept the coarse-edge-SS trade-off. Don't infer per-coffee drift divergence from this pattern alone — that requires at least two data points per coffee showing different cadences.

### Score-rate collapse as a drift-regime signal

A sudden drop in Score-5 frequency across a batch, **without** a corresponding shift in vocabulary or apparent extraction direction, is a strong signal that drift has entered late-life acceleration. The diagnostic chain:

- The batch was landing Score 5s reliably at some cadence (e.g., ~70% S5 rate in its mid-life window)
- Over 2–3 days, every coffee starts coming in Score 4 — not Score 3 — with sweet-spot-adjacent vocabulary ("loose", "bright", "nice flavors but could use X")
- The grinder clicks the user is making are the same size as before
- The "right" setting now moves faster than one click per day, so most brews land a half-click off center regardless of which direction the correction was

This is **not** a recipe problem, a diagnosis problem, or a stalled drift. It's a signal that the coffee has passed from the mid-life ramp into late-life acceleration. Reactions:

- Widen correction step size to 2 clicks per day instead of 1 (or alternate day-to-day bracketing)
- Expect an S4 ceiling to persist — don't chase Score 5 with finer corrections
- Do _not_ infer per-coffee divergence from parallel S4s (see "Per-coffee coarse-tolerance")
- Watch for the actual spiral signals (mouthfeel discomfort, "small + stiff" patterns). If those are absent, the batch is fine; the drift rate is just outrunning the grinder's resolution.
