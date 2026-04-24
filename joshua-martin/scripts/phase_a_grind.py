"""
Phase A: Walk-forward holdout of grind predictors on Joshua's journal.

Target = the actual next grind he chose for the same coffee.
We measure how close each predictor lands; lower MAE wins.

The headline question: does the drift-based heuristic in AGENT_GUIDE
actually beat naive baselines on holdout?
"""
import math
from collections import defaultdict
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "entries.csv")

# Filter to the dominant Z1 era for clean drift comparison; Orea era has different scale.
zdf = df[df.brewer == "Z"].copy()
zdf = zdf[zdf.day.notna()].reset_index(drop=True)
# Drop Comandante-grinder rows (settings 24-27, incompatible with P100 scale).
zdf = zdf[zdf.grind < 10].reset_index(drop=True)

DRIFT_RATES = {
    "H&S": 0.020, "Hydrangea": 0.028, "September": 0.018,
    "Moonwake": 0.027, "Sey": 0.020, "Paix": 0.020,
    "Norena": 0.020,
}

# Build prediction tasks: for each entry (after the first for that coffee),
# predict its grind from prior history.
predictions = defaultdict(list)
truths = []

# Build per-coffee history dicts as we walk forward.
history = defaultdict(list)  # coffee -> list[(idx, day, grind, score)]
roaster_history = defaultdict(list)  # roaster -> list[(idx, day, grind, score, coffee)]
all_grinds = []

global_mean_running = []

for _, row in zdf.iterrows():
    coffee = row.coffee
    roaster = row.roaster
    day = row.day
    grind = row.grind
    score = row.score

    coff_hist = history[coffee]
    roast_hist = roaster_history.get(roaster, [])

    # Skip entries with no prior data at all
    if not all_grinds:
        all_grinds.append(grind)
        history[coffee].append((row.idx, day, grind, score))
        if roaster:
            roaster_history[roaster].append((row.idx, day, grind, score, coffee))
        continue

    truths.append(grind)
    drift = DRIFT_RATES.get(roaster, 0.020)

    # 1. global mean
    predictions["global_mean"].append(np.mean(all_grinds))

    # 2. roaster mean (using roaster history of *any* coffee)
    if roast_hist:
        predictions["roaster_mean"].append(np.mean([g for _, _, g, _, _ in roast_hist]))
    else:
        predictions["roaster_mean"].append(np.mean(all_grinds))

    # 3. last grind for this coffee (no drift)
    if coff_hist:
        predictions["last_grind"].append(coff_hist[-1][2])
    else:
        # Cold start: use roaster mean
        predictions["last_grind"].append(
            np.mean([g for _, _, g, _, _ in roast_hist]) if roast_hist
            else np.mean(all_grinds)
        )

    # 4. last grind + drift (the AGENT_GUIDE heuristic for same coffee)
    if coff_hist:
        last_idx, last_day, last_g, _ = coff_hist[-1]
        days = (day - last_day) if day and last_day else 1
        predictions["last_plus_drift"].append(last_g + drift * days)
    else:
        # Cold start fallback
        if roast_hist:
            # use freshest sibling at same age
            sibling = roast_hist[-1]
            sib_day, sib_g = sibling[1], sibling[2]
            days = (day - sib_day) if day and sib_day else 0
            predictions["last_plus_drift"].append(sib_g + drift * days)
        else:
            predictions["last_plus_drift"].append(np.mean(all_grinds))

    # 5. last sweet-spot grind (Score >= 4) for this coffee + drift
    sweet_prior = [(i, d, g, s) for i, d, g, s in coff_hist if s and s >= 4]
    if sweet_prior:
        last_i, last_d, last_g, _ = sweet_prior[-1]
        days = (day - last_d) if day and last_d else 1
        predictions["last_score4plus_plus_drift"].append(last_g + drift * days)
    elif coff_hist:
        last_i, last_d, last_g, _ = coff_hist[-1]
        days = (day - last_d) if day and last_d else 1
        predictions["last_score4plus_plus_drift"].append(last_g + drift * days)
    else:
        predictions["last_score4plus_plus_drift"].append(
            np.mean([g for _, _, g, _, _ in roast_hist]) if roast_hist
            else np.mean(all_grinds)
        )

    # 6. Sibling-anchored (most recent same-roaster brew, normalized to today's age)
    if roast_hist:
        # Find the most recent OTHER coffee from same roaster
        sibling_brews = [(i, d, g, s, c) for i, d, g, s, c in roast_hist if c != coffee]
        if sibling_brews:
            i, d, g, s, c = sibling_brews[-1]
            days = (day - d) if day and d else 0
            predictions["sibling_plus_drift"].append(g + drift * days)
        elif coff_hist:
            last_i, last_d, last_g, _ = coff_hist[-1]
            days = (day - last_d) if day and last_d else 1
            predictions["sibling_plus_drift"].append(last_g + drift * days)
        else:
            predictions["sibling_plus_drift"].append(np.mean(all_grinds))
    else:
        predictions["sibling_plus_drift"].append(np.mean(all_grinds))

    # 7. Best-scored prior grind for this coffee + drift to today
    if coff_hist:
        scored = [(i, d, g, s) for i, d, g, s in coff_hist if s is not None and not pd.isna(s)]
        if scored:
            best = max(scored, key=lambda x: (x[3], x[1]))  # tie-break by recency
            days = (day - best[1]) if day and best[1] else 1
            predictions["best_prior_plus_drift"].append(best[2] + drift * days)
        else:
            predictions["best_prior_plus_drift"].append(coff_hist[-1][2])
    else:
        predictions["best_prior_plus_drift"].append(
            np.mean([g for _, _, g, _, _ in roast_hist]) if roast_hist
            else np.mean(all_grinds)
        )

    # 8. Round-coarser bias: last_plus_drift snapped to nearest 0.025 then +0.025 if exactly between
    base = predictions["last_plus_drift"][-1]
    snapped = round(base / 0.025) * 0.025
    # If the raw was above the snap by > 0.012, bump up one click
    predictions["snap_coarser"].append(snapped + (0.025 if (base - snapped) > 0.0125 else 0))

    # 9. Bean rolling median
    if coff_hist:
        recent_grinds = [g for _, _, g, _ in coff_hist[-5:]]
        predictions["bean_median5"].append(float(np.median(recent_grinds)))
    else:
        predictions["bean_median5"].append(
            np.mean([g for _, _, g, _, _ in roast_hist]) if roast_hist
            else np.mean(all_grinds)
        )

    # Update history *after* prediction
    history[coffee].append((row.idx, day, grind, score))
    if roaster:
        roaster_history[roaster].append((row.idx, day, grind, score, coffee))
    all_grinds.append(grind)

# Score predictors
truths = np.array(truths)
print(f"Holdout: {len(truths)} grind predictions across {zdf.coffee.nunique()} coffees on Z brewer.\n")

results = []
for name, preds in predictions.items():
    preds = np.array(preds)
    err = preds - truths
    mae = np.mean(np.abs(err))
    bias = np.mean(err)
    within_click = np.mean(np.abs(err) <= 0.025) * 100
    within_2 = np.mean(np.abs(err) <= 0.05) * 100
    rmse = np.sqrt(np.mean(err ** 2))
    results.append((name, mae, bias, rmse, within_click, within_2))

results.sort(key=lambda r: r[1])
print(f"{'Predictor':<28} {'MAE':>6} {'Bias':>7} {'RMSE':>6} {'≤1clk%':>7} {'≤2clk%':>7}")
print("-" * 70)
for name, mae, bias, rmse, w1, w2 in results:
    print(f"{name:<28} {mae:.4f} {bias:+.4f} {rmse:.4f} {w1:6.1f} {w2:6.1f}")

# Per-roaster breakdown of the top-2 predictors
print("\n--- MAE by roaster (top-2 predictors) ---")
top2 = [r[0] for r in results[:2]]
zdf_pred = zdf.iloc[1:].copy().reset_index(drop=True)
zdf_pred = zdf_pred.iloc[:len(truths)]
zdf_pred["truth"] = truths
for name in top2:
    zdf_pred[name] = predictions[name]
agg = zdf_pred.groupby("roaster").apply(
    lambda g: pd.Series({
        f"{n}_MAE": np.mean(np.abs(g[n] - g["truth"])) for n in top2
    } | {"n": len(g)})
)
print(agg.round(4))

# Drift validation: per-roaster realized drift
print("\n--- Realized drift rate per roaster (Score >= 4 entries only, OLS slope of grind vs day) ---")
sweet = zdf[(zdf.score >= 4) & (zdf.day.notna())].copy()
for r in sweet.roaster.dropna().unique():
    sub = sweet[sweet.roaster == r]
    if len(sub) < 10:
        continue
    # OLS: g = a + b*day
    x = sub.day.values
    y = sub.grind.values
    b, a = np.polyfit(x, y, 1)
    print(f"  {r:<12} n={len(sub):3d}  slope={b:+.4f}/day  intercept={a:.3f}  documented={DRIFT_RATES.get(r, '?')}")
