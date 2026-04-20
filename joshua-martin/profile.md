# Coffee Journal — Profile (Joshua)

Calibration file for Joshua's coffee journal. Pair with `AGENT_GUIDE.md` (universal methodology). The guide tells you how to predict; this file tells you the numbers and patterns specific to this journal.

## 1. Scope

- **Brew method**: Pour-over, primarily Z1 (Zerno) with Orea in earlier entries and occasional Aeropress.
- **Roast profile**: Specialty light-roast, often very light (H&S is among the lightest in the world).
- **Journal size**: ~1 year of daily entries, 3800+ lines of `Coffee Journal.md`.
- **Maintainer**: Joshua. Entries are top-to-bottom, earliest to most recent.

## 2. Equipment

- **Grinder**: **Lagom P64** (primary). Occasionally **Comandante C40** hand grinder (settings 24–27 range; incompatible scale with P64 — do not cross-compare numerically).
  - "Lagom" is the grinder brand, not a roaster.
- **Grinder step size (dial increment)**: **0.025** on the dial = 2.5 microns. **All predictions round to 0.025 increments** (e.g., 6.175, 6.200, 6.225).
- **Observed dial-value ranges**:
  - **Z1/Zerno brewer**: ~5.0–7.0+ (most entries fall here).
  - **Orea brewer**: ~6.6–7.3 (earlier entries).
- **Brewer shorthand codes** (appear in entry headers):
  - `O` = Orea
  - `Z` = Z1 (Zerno)
  - Accessories: `M` = Melodrip, `NK` = Negotiated Kalita filters

## 3. Recipe Baseline

- **12.5g coffee / 250g water** at **211°F**, 5-pour method with Melodrip.
- When not otherwise noted in an entry, assume this recipe.

## 4. Water

- **Default**: Custom mineralized water at **15KH / 35GH**. Very low-alkalinity, light on minerals — well below the SCA target of 68GH/40KH — which maximizes brightness and acidity for light roasts at the cost of some body.
- **Variants observed** (flagged explicitly in entries when used):
  - **Crystal Geyser spring water** (~50–72 GH, ~50–55 KH) — shifts sweet spot **~0.05–0.10 coarser** vs. custom. Confirmed: September batch shifted coarser on Crystal Geyser and back down when returning to custom.
  - **Reverse osmosis (RO)** — e.g., Whole Foods store RO. Requires **finer** settings, but the intercept shift is **inconsistent across refills** (TDS 5–50 depending on membrane state). Treat RO entries as **noisier** than custom-water entries — don't let apparent intercept shifts on RO override the consensus curve. One H&S batch 3 instance (Day 56–60) showed several Score 3s on RO that looked like an intercept shift, but a Score 5 at the same setting on the same water disproved it.
- **Rule of thumb**: A water change shifts the sweet spot baseline (intercept). It does **not** shift the drift rate (slope). Once dialed in to a new water, predictions proceed normally from the new anchor.

## 5. Rating Scale

1–5 scale, appended as `Score: X` in headers:

- **5** — Transcendent. Header adjectives that reliably proxy Score 5: "Stunning", "Magical", "Knockout", "Musical", "wow wow wow", "absolutely perfect", "one of the best", "shimmering".
- **4** — Solidly good. "Quite good", "really good", no major flaws.
- **3** — Enjoyable but with obvious flaws.
- **2** — Pretty unenjoyable.
- **1** — Gross/disgusting. Extremely rare.

When scoring is ambiguous or missing from the header, **read the notes** — sentiment in prose is a more reliable signal than the terse header.

## 6. Entry Format

Each entry header follows:

```
## CoffeeName, Brewer, GrindSetting @ Temp, Dose/Water Day X Sentiment, Score: X
Tasting notes and next-setting suggestions.
```

- **Sweet-spot markers**: Joshua typically marks dialed-in cups with `**Sweet spot**` in notes or glowing language ("dialed in", "musical", etc.).
- **"Should have been X"**: Joshua's retrospective corrected estimate of the true sweet spot for that day. Highly valuable for calibration.
- **Day X**: Days since roast date.
- **Same-day brews**: Joshua frequently brews the same coffee multiple times per day. Do not auto-increment Day X — always verify the current date and the latest journal entries before assuming a Day number.

## 7. Roaster Groupings

Coffees are named after producers / farms / creative names. Multiple coffees from the same roaster age similarly and often share the same sweet spot at the same age.

### H&S Roasters

- **Orea era**: Pineda, Vista, Pena, Lasso Mejorado\*, Lopez, San Antonio (decaf)
- **Z1 batch 1**: La Esperanza 2, La Esperanza, Gatomboya, Karani, Iridescence, Kiamwangi, Banko Taratu, Placer
  - Drift **~0.015/day during Day 28–50**, then **accelerates to ~0.035–0.050/day past Day 50** (Placer went from 6.25 at Day 53 to 6.75 at Day 63)
- **Z1 batch 2**: Birthday Cake, Rumudamo (natural + washed)
- **Z1 batch 3 (most recent)**: Trujillo, Lasso, Ninco, Chelbessa
- **Likely H&S**: Karianini, later Paraiso
- Drift rates vary by batch: batch 1 ~0.015/day, batch 3 ~0.023/day
- **H&S batch 3 showed acceleration past Day 58** (~0.033–0.042/day), matching batch 1's late-age pattern. Earlier entries at 6.2–6.25 on Day 59–61 that appeared underextracted were actually overextracted — the overextraction spiral mimicked underextraction with "small, watery" flavors. Going coarser (6.275, then 6.3) improved scores, confirming the acceleration. By Day 63, the sweet spot may be at 6.4+. At this acceleration rate, **use bigger jumps (0.05–0.075) rather than single 0.025 increments** to keep up. The late-age spiral (Day 58–68) cost 24 entries before a Score 5 was achieved again via the bracketing strategy — a cautionary example of how chasing with conservative increments during acceleration wastes brews.

_\*Lasso Mejorado is roasted by Paix, a separate roaster._

### Hydrangea Coffee Roasters

- Uberrimo, Bolanos, Paraiso, Elida, Pena (most recent), La Isabela (natural), Monteblanco (co-ferment)
- Thermal shock processing is a Hydrangea method.
- Z1 sweet spot **~6.0–6.1 around Day 34–40**, earlier-batch drift ~0.022/day.
- Elida was the standout (multiple Score 5 entries); Uberrimo and Bolanos were subtler and harder to dial in.
- Hydrangea coffees were notably forgiving early (Uberrimo scored 5 on Day 8 on the Orea).
- **Most recent batch** (Pena washed, La Isabela natural, Paraiso thermal shock, Monteblanco co-ferment, all roasted ~March 29): sweet spot converged on **5.45 at Day 9–10** regardless of processing method. Drift is very slow early (~0.008/day through Day 14, matching the original Hydrangea batch on Orea), **accelerating as the coffees age**. The roaster's approach dominates over processing method for baseline setting. Sweet spot held at **5.5 for Day 13–14** (Paraiso Score 5 Day 13, Monteblanco Score 5 Day 14). By Day 15, drift accelerated — Pena at 5.5 read as slightly overextracted, sweet spot shifted to 5.525. The **CO2 phase appears to end around Day 14–15** for this batch, after which drift picks up. By Day 17, drift reached ~0.025/day (5.575 confirmed by Pena and Monteblanco Score 5s). By Day 17–18, all four coffees converged to identical settings regardless of processing — max spread was 0.075 (3 clicks), and by Day 17 spread was zero. Tightest processing-method convergence in the journal. The batch has a **70% Score 5 rate with zero Score 3s across 17 entries** — the best-performing batch in the journal by a wide margin.
- **Post-Day-15 drift rate**: **0.0300/day** (empirically fit across Pena, La Isabela, Paraiso, Monteblanco).
- **Day 19 sweet spot confirmed at 5.65** (A/B tested; Monteblanco, Pena, La Isabela correction, Paraiso on finer edge all agree).
- **Day 20**: Sweet spot at **5.675** (La Isabela Score 5 _"more voluminous"_, Monteblanco Score 5 Sweet Spot). Paraiso Score 4 at 5.675 (_"funky peach gummy isn't quite as developed"_) — Paraiso was the first coffee to show the batch beginning to differentiate.
- **Day 21**: The batch visibly split. All three coffees scored ≤4 at 5.7, but **in opposite extraction directions**:
  - **Pena**: mild over at 5.7 (_"nothing shining / sweetness not sugary / acidity not genuine / cocoa a little off"_) — looks like under by vocabulary, confirmed as over by tiebreaker brew at 5.675 which came out Score 3 with mouth rubbing + heavy cocoa. Pena wants **5.725+**.
  - **La Isabela**: genuinely under at 5.7 (Score 3, _"watery / hollow / little substance or development"_). Step back to **5.675** (last Score 5).
  - **Paraiso**: truly ambiguous — _"unfocused / dulled / missing crisp/bright/sweet edge and definition"_ with no mouthfeel issue. No tiebreaker yet; could be either side.
- **End of the 70% Score-5 streak**: Day 21 is the first day with zero Score 5s in this batch. Signals the end of the batch's unusually forgiving early period — coffees are now drifting at individual rates and require per-coffee settings, not a single batch cadence.
- **Calibration lesson** (Day 21): Same-day parallel drops with overlapping off-peak vocabulary can hide opposite-sign diagnoses. See §11 "Stalled-drift false alarm."
- **Day 22**: Both Paraiso and La Isabela Score 4 at 5.75. La Isabela probed at 5.775 same day — acidity _brightened further_ ("even more brilliant sweet-tart grape candy") and texture _loosened further_ ("even looser"), without volume recovering. Falsifies "mild over" on La Isabela; confirms she was inside an SS-window with varietal acidity headroom. Paraiso's "loose funky flimsy" at 5.75 reads the same way — probably fine-edge SS, not over. **"Small flavor volume" on Day 22 is likely reference-anchor bias vs. Day 9's peak-perfuminess cup** ("one of the best of the year"), not an extraction deficit. Stop chasing volume; characterize the new window.
- **Day 22 Monteblanco**: Score 4 at 5.75 with _"soft first sip, small volume, limp, fantastic clarity, could be brighter, juicy/loose in cooldown, fantastic flavors"_ — Joshua called **5.725** (finer). Inflection is opposite La Isabela's: where La Isabela was bright-but-loose, Monteblanco reads soft/muted. **Updated batch-level read**: Pena (5.725+), Monteblanco (5.725) and likely Paraiso + La Isabela all share a **~5.725 SS center** on Day 22. The four coffees differ in **coarse-tolerance**, not in drift rate: La Isabela and Paraiso tolerate 5.75 with just structural looseness (bright-side deficit); Monteblanco and Pena don't — past SS they read muted/limp (muted-side deficit). Earlier §8 note about "per-coffee divergence" is partially wrong: centers are still shared; only coarse-side failure modes differ. See §13 "per-coffee coarse-tolerance."

### September Coffee

- **Core washed batch**: Pena (Z1), Morena, Bermudez, Velasco, Lasso (Sep), Castillo, Cuenca, Ortega, Pintado, Danche, Chelbesa
- **Creative/processed**: White Honey, Gingerbread, Putushio, Tamana/Tamama
- **Producer-named other**: Buttercream, Sudan Rume, Fajardo, Martinez, Rojas
- Three distinct drift tiers:
  - **Core washed**: **~0.015/day** — very tight clustering, 11 coffees within ~0.1 of each other.
  - **Creative/processed**: **~0.027/day linear**, but **decelerates** from ~0.036 to ~0.020/day — converges with washed rate by Day 40. Likely honey/natural/anaerobic processing → more soluble compounds → faster early aging. Peaked early (Score 5s only through Day 25).
  - **Producer-named other**: **~0.013/day** — slowest, noisiest, hardest to diagnose. Most overextraction-spiral incidents came from this group. Only 1 Score 5 across ~90 entries (Buttercream Day 26). Diagnosis accuracy ~50–55% — lean heavily on sibling data for these coffees.

### Moonwake Coffee Roasters

- Serrato, Gomez, Ramirez, Benitez
- Drift: **~0.025–0.029/day**
- Sweet spots are notably **higher** than other roasters at the same age (~6.6–6.7 at Day 50).
- Tightest convergence of any roaster batch — all four within 0.05 of each other at key ages.
- Benitez is the most stable/distinct (vivid raspberry, almost never misdiagnosed); Serrato the most polarizing ("not my favorite profile" but well-executed).

### SEY

- Muhito, Dota, Gotiti, Botina (Bonita)
- "SEY grassy/spicy quality", "SEY citric spiciness"
- Drift: **~0.020/day**
- These coffees were erratic and hard to dial in on the Z1.
- **Narrow sweet spot window** (~0.35 range vs. ~0.5+ for Hydrangea) and **misleading astringency** — they read as underextracted (tight mouth, green qualities) even when overextracted, leading to repeated finer adjustments that made things worse.
- **Highest overextraction spiral vulnerability of any roaster** (~15% of entries hit the "small + mouthfeel" dual pattern).

### Other

- **Paix**: Lasso Mejorado only.
- **Norena**: Roaster unknown.

**Important naming clash**: "Lasso", "Pena", and "Paraiso" each appear under multiple roasters at different points in the journal. Use journal position and context to determine which is which. A "Lasso" entry early in the journal (Orea, Paix) is a completely different coffee than one later (September Coffee Z1) or the most recent (H&S Z1).

## 8. Drift-Rate Table (Summary)

| Roaster / Batch                | Drift/Day      | Notes                                                                                                                                                                                                                                                |
| ------------------------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| September (core washed)        | ~0.015         | Very consistent across coffees                                                                                                                                                                                                                       |
| September (creative/processed) | ~0.027 avg     | Gingerbread, White Honey; decelerates from ~0.036 to ~0.020                                                                                                                                                                                          |
| September (producer other)     | ~0.013         | Fajardo, Martinez, Rojas, Sudan Rume, Buttercream; slow, noisy                                                                                                                                                                                       |
| H&S batch 1                    | ~0.015         | Karani, Gatomboya, Iridescence; **accelerates to 0.035–0.050 past Day 50**                                                                                                                                                                           |
| H&S batch 3                    | ~0.023         | Trujillo, Lasso, Ninco, Chelbessa; **accelerates to ~0.033+ past Day 58**                                                                                                                                                                            |
| Hydrangea (most recent batch)  | ~0.008 → 0.030 | Pre-Day-15 CO2 phase very slow; **post-Day-15 ~0.030/day** through Day 20. Day 22 SS center converges to ~5.725 for all four coffees. **Per-coffee divergence is in _coarse-tolerance_, not drift rate** — La Isabela + Paraiso tolerate +0.025 coarse (stay bright + loose); Pena + Monteblanco don't (read muted/limp past SS). See §7, §13. |
| Moonwake                       | ~0.025–0.029   | Serrato, Gomez, Ramirez, Benitez                                                                                                                                                                                                                     |
| SEY                            | ~0.020         | Muhito, Dota; narrow window, spiral-prone                                                                                                                                                                                                            |

## 9. Correction Bias

Holdout count of "should have been X" annotations across the journal (n = 452):

| Score of brew | Coarser         | Finer | Same | Mean Δ     |
| ------------- | --------------- | ----- | ---- | ---------- |
| 2             | 39 %            | 57 %  | 4 %  | +0.005     |
| 3             | 49 %            | 49 %  | 2 %  | +0.011     |
| 4             | **62 %**        | 36 %  | 2 %  | +0.022     |
| 5             | **100 %** (n=8) | 0 %   | 0 %  | +0.047     |
| **All**       | **52 %**        | 46 %  | 2 %  | **+0.014** |

![Correction bias by score](assets/correction_bias_by_score.png)

The previously-cited "67 % coarser" figure was wrong — overall the corrections are essentially symmetric (52 / 46). The coarser bias is **score-conditional**: it only emerges once the cup is already close (Score 4+), where it represents drift-tracking, not error-correction.

**Implication:** "When ambiguous, round coarser" applies after a Score-4-or-better brew. After a Score-2-or-3 brew, the direction is genuinely uncertain — diagnosis matters more than a default bias.

## 10. Step-Size Distribution

Between consecutive entries of the same coffee, Joshua's grind adjustments:

| Step  | % of adjustments |
| ----- | ---------------- |
| 0.050 | 34%              |
| 0.000 | 20%              |
| 0.025 | 15%              |
| 0.100 | 12%              |
| other | 19%              |

A **one-click (0.025) miss is meaningful but not large** — it's inside the sweet-spot window most of the time. A 0.05 miss is the typical "noticeable" adjustment. 20% of consecutive entries keep the setting the same (drift-tracking at the window's center, or a re-brew for confirmation).

**After a Score 5, the setting almost never holds.** Across 42 cases where Joshua brewed the same coffee within 3 days of a Score 5:

| Gap    | n   | Kept setting | Mean Δ |
| ------ | --- | ------------ | ------ |
| 1 day  | 14  | 21 %         | +0.025 |
| 2 days | 20  | 10 %         | +0.041 |
| 3 days | 8   | 12 %         | +0.050 |

86 % went coarser, 0 % went finer. The realized per-day slope (~0.025) closely matches the documented per-roaster drift rates (§ 8). **Treat a Score 5 as a "today's setting" anchor, not a "this week's setting" anchor** — predict tomorrow at one click coarser by default.

![Score-5 follow-up](assets/score5_followup.png)

## 11. Known Failure Modes

- **La Esperanza 2 spiral**: Score 4 at 5.85 degraded to Score 2 by 6.0 as Joshua kept going finer thinking the cup was underextracted. Clearest journal example of the spiral; use as a teaching case.
- **SEY misleading astringency**: SEY's natural "tight mouth + green qualities" read as under even when over. Finer adjustments made things worse across many entries. Trust coarser when SEY shows "small + mouthfeel" pattern.
- **September producer-named coffees** (Fajardo, Martinez, Rojas, Sudan Rume): Subtle/vague flavor profiles → diagnosis accuracy ~50–55%. Most overextraction-spiral incidents came from this group. **Lean heavily on sibling data; distrust the direction call.**
- **H&S batch 3 late-age acceleration** (Day 58–68): Drift accelerated past 0.033/day; conservative 0.025 increments fell behind, producing a 24-entry string of Score 3s before bracketing restored a Score 5. When consecutive Score 3s appear at older ages in this roaster, **jump 0.05–0.075** and bracket.
- **RO water noise**: Several Score 3s on RO during H&S batch 3 Day 56–60 looked like an intercept shift but were brew variability. One Score 5 on the same RO at the same setting disproved the shift hypothesis. Don't over-correct for RO.
- **Stalled-drift false alarm** (Hydrangea batch, Day 21): Three coffees (Paraiso, Pena, La Isabela) all scored 4 at 5.7 with off-peak but ambiguous vocabulary — "unfocused / dulled / missing edge" (Paraiso), "nothing shining / sweetness not sugary / acidity not genuine / cocoa a little off" (Pena), "watery / hollow" (La Isabela, Score 3). Initial reading: parallel underextraction overshoot from stalled drift, all three step back to last Score-5. **Falsified by tiebreaker brew**: Pena at 5.675 (finer than 5.7) came out Score 3 with mouth rubbing, heavy cocoa, no acidity, "cocoa off in a stinky way" — unambiguous overextraction. If 5.7 had been under, 5.675 should have been closer to peak; instead it was more over. Correct reading: Pena was **mild over** at 5.7 (wanted 5.725+); La Isabela was genuinely under (watery/hollow is one-sided); Paraiso was truly ambiguous. **Lesson**: Multi-coffee same-day drops with overlapping "dulled / missing edge / nothing shining" language look systemic but can hide opposite-sign diagnoses. Always probe one of the ambiguous coffees with a tiebreaker brew (finer or coarser) before committing to a shared direction.

## 12. Diagnosis Accuracy (by Roaster)

Overall Joshua direction-call accuracy: **~60–65%.** Breakdown:

- **Moonwake**: ~70–75% (vivid flavor profiles)
- **September washed core**: ~70–75%
- **H&S**: ~65% overall
- **Hydrangea**: ~65%
- **September creative/processed**: ~60%
- **September producer-named other**: ~50–55%
- **SEY**: ~45–50% (misleading astringency)

#1 source of misdiagnosis: **attributing scratchiness/roughness to underextraction when it's actually overextraction.**

## 13. Vocabulary Map (Joshua-specific descriptor → direction)

Descriptors with strong directional signal in Joshua's journal beyond the universal set:

- **Coarser edge of sweet spot (Score 5 leaning under)**: "big in mouth, not quite focused initially", "soft", "gentle", "mouthfilling but diffuse", "may be fully focused by next cup". Prototype: **Pena Day 19 @ 5.65** (most recent Hydrangea batch).
- **Finer edge of sweet spot (Score 5 leaning over)**: "barely smaller flavor volume", "slight roughness, localized", "pleasant perfuminess, edges softening", "black tea forward". Prototype: **Paraiso Day 19 @ 5.625**.
- **Overextraction spiral signature**: "small" + any mouth discomfort ("scratchy", "tight", "rubbing", "stiff"). Joshua's journal: going finer from this fails 67% of the time.
- **"Hollow" / "watery" / "little substance or development in the flavor"**: Reliable underextraction signal. Prototype: **La Isabela Day 21 @ 5.7**.
- **"Nothing shining / sweetness not sugary / acidity not genuine / cocoa a little off / balanced but flat"**: **Ambiguous — lean mild over.** Looks like under ("nothing shining") but often resolves as mild over in Joshua's journal. Prototype: **Pena Day 21 @ 5.7** — finer tiebreaker at 5.675 came out with mouth rubbing + heavy cocoa, confirming mild over. When this vocabulary appears, brew a tiebreaker in either direction before committing.
- **"Brilliant / effervescent / peaking acidity" + "small flavor volume" + clean mouthfeel**: **Ambiguous — probe coarser to distinguish.** Joshua's formulated heuristic was "this equals barely overextracted," but the coarser probe disambiguates. If acidity _softens_ under coarsening → confirmed mild over. If acidity _unlocks further_ (brightens, texture opens up) → not over; the coffee is inside a sweet-spot window with varietal acidity that has headroom, and the "small volume" symptom is likely a reference-anchor artifact (see below). Prototype: **La Isabela Day 22** — 5.75 "brilliant grape soda + small volume" → 5.775 "even more brilliant, even looser" = not over, SS-window with headroom.
- **"Small flavor volume" when compared to a Day 8–14 peak cup**: Suspect **reference-anchor bias**, not compression. Fresh-coffee perfuminess and CO₂ lift fade regardless of grind; late-life cups cannot reproduce the young-coffee "big first impression" even at peak extraction. Check whether the mental anchor is a specific early-days cup ("one of the best of the year"-class memory). If other markers are sweet-spot-coded (loose, defined acidity, honest flavors, clean mouthfeel), the cup is probably peaking for its age and doesn't need adjustment. Prototype: **La Isabela Day 9 @ 5.45** anchors Day 22's "small volume" perception.
- **Per-coffee coarse-tolerance (same setting, same day, opposite inflection)**: When sibling coffees all Score 4 at the same setting but with differently-coded deficits — one reads _bright-but-loose_ (coarse-edge SS), another reads _soft/limp/could-be-brighter_ (under-leaning) — the SS center is probably shared, and the coffees differ in how they _fail_ past SS. Act on the under-leaning coffee's instinct (finer); don't infer divergent drift rates. Prototype: **Hydrangea batch Day 22** — La Isabela/Paraiso at 5.75 bright-but-loose, Monteblanco at 5.75 soft/limp with Joshua calling 5.725; all four share a ~5.725 SS center.

(This section is a stub — planned to be populated more systematically by a `vocab_infer.py` script across all Score-3-then-corrected pairs.)

## 14. Open Questions / TODO

- Cross-water transfer: working hypothesis is that water shifts intercept but not slope. Needs more A/B data on custom ↔ Crystal Geyser and custom ↔ RO to confirm.
- Hydrangea batch: does post-Day-15 drift continue accelerating past Day 25, or stabilize at 0.030?
- Does the coarser-edge "may be fully focused by next cup" observation hold across roasters, or is it specific to Hydrangea's gentler profile?
- Step-size distribution was computed months ago; re-run periodically to see if adjustment habits are tightening as calibration improves.

## 15. Holdout Validation

Walk-forward holdout on **729 same-coffee grind predictions** from the Z brewer era (P100 grinder only; Comandante entries excluded). Each predictor sees only prior history and predicts the next grind Joshua actually used.

![Predictor MAE](assets/predictor_mae.png)

| Predictor               | MAE       | RMSE  | ≤ 1 click | ≤ 2 clicks |
| ----------------------- | --------- | ----- | --------- | ---------- |
| `last_grind + drift`    | **0.065** | 0.166 | **42 %**  | **70 %**   |
| `sibling_plus_drift`    | 0.065     | 0.144 | 43 %      | 66 %       |
| `last_grind` (no drift) | 0.092     | 0.194 | 22 %      | 56 %       |
| `bean_median5`          | 0.158     | 0.235 | 6 %       | 18 %       |
| `roaster_mean`          | 0.228     | 0.306 | 8 %       | 17 %       |
| `global_mean`           | 0.237     | 0.319 | 10 %      | 17 %       |

**Headline:** The simple drift heuristic from § 8 (last grind + per-roaster rate × days elapsed) **wins** at MAE ≈ 0.065 — that's about 1.3 clicks of error, well inside the ~2-click sweet-spot window. Adding drift over a no-drift baseline cuts MAE from 0.092 → 0.065 (29 % improvement) and doubles the within-1-click hit rate (22 % → 42 %). **Drift is real and worth modeling.**

Sibling-anchored prediction is statistically tied with last-coffee+drift on MAE but achieves slightly better RMSE — useful when the same-coffee history is sparse or when the user wants to challenge a noisy prior with batch consensus.

Realised drift slopes (Score ≥ 4 entries, OLS) vs documented:

| Roaster                    | Documented | Realised | Verdict     |
| -------------------------- | ---------- | -------- | ----------- |
| Hydrangea                  | 0.022      | +0.018   | ✓           |
| H&S                        | 0.020      | +0.022   | ✓           |
| Moonwake                   | 0.027      | +0.024   | ✓           |
| Sey                        | 0.020      | +0.020   | ✓ (small n) |
| September (washed)         | 0.015      | +0.017   | ✓           |
| September (creative)       | 0.027      | +0.029   | ✓           |
| September (producer-other) | 0.013      | +0.012   | ✓           |

All documented drift rates from § 8 hold up against the empirical fit. The pooled September slope of ~0.008 was misleading because it averaged across three tiers of very different rates.

### Heuristic stress-tests

- **Score-3 recovery (n=274 follow-up brews).** Going coarser after a Score 3 recovered to ≥ 4 in **38 %** of cases (n=215); going finer recovered in **42 %** (n=59). Joshua defaults to coarser 78 % of the time, but the data does _not_ show coarser as the higher-recovery move from a fresh Score 3 — it just reflects that drift-tracking dominates. **Treat the "round coarser" rule as drift-tracking advice, not as a recovery move.** When the prior cup was clearly bad, weigh the descriptors and don't default-bias the direction.
- **Score 5 → next brew (n=42 within 3 days).** 86 % of follow-ups went coarser, 0 % finer. Mean coarsening per day ≈ 0.025. **A Score-5 setting almost never holds.**
- **Score 5 lineage (n=64).** 66 % of Score 5 brews followed a Score 4 or Score 5 (matching the 64 % figure cited in the AGENT_GUIDE). Convergence-by-refinement is the dominant path; "lucky correction" is rare.
- **Distance-to-good-grind vs score (n=690).** Median grind within ± 0.025 of the coffee's good-grind median scores 4.0; 0.025–0.075 also scores 4.0; 0.075–0.15 scores 3.5; 0.15–0.30 scores 3.0; > 0.30 scores 3.0. The sweet-spot window is **roughly 3 clicks wide** (-0.075 to +0.075 from the median good grind), confirming the AGENT_GUIDE's 2–3-click width claim.
- **Sibling convergence (n=515 Score-5 vs same-roaster Score-≥4 sibling within 2 days).** Median grind spread = 0.050 (2 clicks), mean = 0.13. Only 22 % of pairs agree within 1 click; 49 % within 2 clicks; 55 % within 3 clicks. Siblings are useful priors but **noisier than previously claimed** ("rarely > 0.05–0.1"). Use sibling consensus as a tiebreaker when within 2–3 clicks of own-history prediction; distrust it when it disagrees by more.
