"""
Phase B: Score prediction + heuristic validation on Joshua's journal.
"""
import re
from pathlib import Path
from collections import defaultdict
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "entries.csv")
zdf = df[(df.brewer == "Z") & (df.grind < 10)].reset_index(drop=True)

DRIFT_RATES = {
    "H&S": 0.020, "Hydrangea": 0.028, "September": 0.018,
    "Moonwake": 0.027, "Sey": 0.020, "Paix": 0.020, "Norena": 0.020,
}

# ---- Heuristic 1: "should have been" pointing coarser ----
# AGENT_GUIDE claim: "should have been" corrections point coarser 67% of the time.
print("=" * 70)
print("HEURISTIC 1: 'should-have-been' direction bias")
print("=" * 70)
sb = zdf[zdf.should_be != "[]"].copy()
sb["should_be_list"] = sb.should_be.map(lambda s: eval(s) if isinstance(s, str) else [])
coarser = finer = same = 0
deltas = []
for _, row in sb.iterrows():
    for v in row.should_be_list:
        d = v - row.grind
        deltas.append(d)
        if d > 0.005:
            coarser += 1
        elif d < -0.005:
            finer += 1
        else:
            same += 1
total = coarser + finer + same
print(f"  Total 'should be' suggestions: {total}")
print(f"  Coarser: {coarser} ({100*coarser/total:.1f}%)")
print(f"  Finer:   {finer} ({100*finer/total:.1f}%)")
print(f"  Same:    {same} ({100*same/total:.1f}%)")
print(f"  Mean delta: {np.mean(deltas):+.4f}")
print(f"  Median delta: {np.median(deltas):+.4f}")

# Per-score breakdown
print("\n  By score:")
for sc in [2, 3, 4, 5]:
    sub_deltas = []
    for _, row in sb[sb.score == sc].iterrows():
        for v in row.should_be_list:
            sub_deltas.append(v - row.grind)
    if sub_deltas:
        print(f"    Score {sc}: n={len(sub_deltas):3d}  coarser_pct={100*np.mean(np.array(sub_deltas)>0.005):.1f}%  mean={np.mean(sub_deltas):+.4f}")

# ---- Heuristic 2: Score-5 setting holds for 1-2 days? ----
print()
print("=" * 70)
print("HEURISTIC 2: Does a Score-5 setting hold for next-day brew?")
print("=" * 70)
# For each Score-5 entry, find the same coffee's NEXT entry within 3 days.
hits = misses = 0
gap_data = []
zdf_sorted = zdf.sort_values(["coffee", "idx"]).reset_index(drop=True)
for coffee, grp in zdf_sorted.groupby("coffee"):
    grp = grp.reset_index(drop=True)
    for i in range(len(grp) - 1):
        if grp.loc[i, "score"] == 5 and pd.notna(grp.loc[i, "day"]):
            # Find next entry
            for j in range(i + 1, len(grp)):
                if pd.notna(grp.loc[j, "day"]):
                    gap = grp.loc[j, "day"] - grp.loc[i, "day"]
                    if 0 < gap <= 3:
                        delta = grp.loc[j, "grind"] - grp.loc[i, "grind"]
                        next_score = grp.loc[j, "score"]
                        gap_data.append({
                            "coffee": coffee,
                            "gap_days": gap,
                            "grind_delta": delta,
                            "next_score": next_score,
                            "kept": abs(delta) < 0.001,
                        })
                    break
gap_df = pd.DataFrame(gap_data)
print(f"  Score-5 followed by within-3-day brew: n={len(gap_df)}")
print(f"  Stayed at same grind: {gap_df.kept.sum()} ({100*gap_df.kept.mean():.1f}%)")
print(f"  Went coarser: {(gap_df.grind_delta > 0.001).sum()}  ({100*(gap_df.grind_delta>0.001).mean():.1f}%)")
print(f"  Went finer:   {(gap_df.grind_delta < -0.001).sum()}  ({100*(gap_df.grind_delta<-0.001).mean():.1f}%)")
print(f"  Mean delta when changed: {gap_df[~gap_df.kept].grind_delta.mean():+.4f}")
print(f"  Mean delta per gap-day:")
for g in [1, 2, 3]:
    sub = gap_df[gap_df.gap_days == g]
    if len(sub):
        print(f"    gap={g} day(s): n={len(sub):3d}  mean_delta={sub.grind_delta.mean():+.4f}  kept_pct={100*sub.kept.mean():.0f}%")

# ---- Heuristic 3: Score-5 streaks (gradual refinement) ----
print()
print("=" * 70)
print("HEURISTIC 3: How are Score-5 brews preceded? (gradual vs jump)")
print("=" * 70)
streaks = {"5_after_5": 0, "5_after_4": 0, "5_after_3": 0, "5_after_lower": 0, "5_first": 0}
for coffee, grp in zdf_sorted.groupby("coffee"):
    grp = grp.reset_index(drop=True)
    for i, row in grp.iterrows():
        if row["score"] == 5:
            if i == 0:
                streaks["5_first"] += 1
                continue
            prev_score = grp.loc[i-1, "score"]
            if pd.isna(prev_score):
                streaks["5_first"] += 1
            elif prev_score == 5:
                streaks["5_after_5"] += 1
            elif prev_score == 4:
                streaks["5_after_4"] += 1
            elif prev_score == 3:
                streaks["5_after_3"] += 1
            else:
                streaks["5_after_lower"] += 1
total5 = sum(streaks.values())
for k, v in streaks.items():
    print(f"  {k:<18} {v:3d}  ({100*v/total5:.1f}%)")
print(f"  → After 4 or 5: {100*(streaks['5_after_4']+streaks['5_after_5'])/total5:.1f}%")

# ---- Heuristic 4: Score predictor — distance to per-coffee best grind predicts score ----
print()
print("=" * 70)
print("HEURISTIC 4: Score vs grind-distance from coffee's median Score>=4 grind")
print("=" * 70)
# For each coffee, compute median grind across Score>=4 entries (their "good zone")
good_grind = (zdf[zdf.score >= 4].groupby("coffee").grind.agg(['median', 'count']))
zdf2 = zdf.merge(good_grind, left_on="coffee", right_index=True, how="left")
zdf2 = zdf2[zdf2["count"] >= 3]  # need enough good brews to define zone
zdf2["dist_from_good"] = (zdf2.grind - zdf2["median"]).abs()
zdf2["dist_bin"] = pd.cut(
    zdf2.dist_from_good,
    bins=[-0.001, 0.025, 0.075, 0.15, 0.3, 10],
    labels=["≤0.025", "0.025-0.075", "0.075-0.15", "0.15-0.30", ">0.30"],
)
print("  Score by distance from coffee's good-grind median:")
print(zdf2.groupby("dist_bin", observed=True).agg(
    n=("score", "count"),
    mean_score=("score", "mean"),
    median_score=("score", "median"),
    pct_score5=("score", lambda s: 100 * (s == 5).mean()),
    pct_score4plus=("score", lambda s: 100 * (s >= 4).mean()),
).round(2))

# ---- Heuristic 5: Score-3 spiral risk: probe coarser first? ----
print()
print("=" * 70)
print("HEURISTIC 5: After Score-3, going coarser vs finer — which recovers?")
print("=" * 70)
recovery = {"coarser_5": 0, "coarser_4": 0, "coarser_3": 0, "coarser_low": 0,
            "finer_5": 0, "finer_4": 0, "finer_3": 0, "finer_low": 0}
for coffee, grp in zdf_sorted.groupby("coffee"):
    grp = grp.reset_index(drop=True)
    for i in range(len(grp) - 1):
        if grp.loc[i, "score"] == 3 and pd.notna(grp.loc[i+1, "score"]):
            delta = grp.loc[i+1, "grind"] - grp.loc[i, "grind"]
            ns = grp.loc[i+1, "score"]
            direction = "coarser" if delta > 0.005 else ("finer" if delta < -0.005 else None)
            if direction is None:
                continue
            bucket = "low" if ns < 3 else int(ns)
            recovery[f"{direction}_{bucket}"] += 1
print(f"  After Score-3 → coarser:")
total_c = recovery["coarser_5"] + recovery["coarser_4"] + recovery["coarser_3"] + recovery["coarser_low"]
print(f"    Score 5: {recovery['coarser_5']}  4: {recovery['coarser_4']}  3: {recovery['coarser_3']}  <3: {recovery['coarser_low']}  (n={total_c})")
if total_c:
    pct_recov = 100 * (recovery["coarser_5"] + recovery["coarser_4"]) / total_c
    print(f"    Recovered to ≥4: {pct_recov:.1f}%")
print(f"  After Score-3 → finer:")
total_f = recovery["finer_5"] + recovery["finer_4"] + recovery["finer_3"] + recovery["finer_low"]
print(f"    Score 5: {recovery['finer_5']}  4: {recovery['finer_4']}  3: {recovery['finer_3']}  <3: {recovery['finer_low']}  (n={total_f})")
if total_f:
    pct_recov = 100 * (recovery["finer_5"] + recovery["finer_4"]) / total_f
    print(f"    Recovered to ≥4: {pct_recov:.1f}%")

# ---- Heuristic 6: Sibling convergence at same age ----
print()
print("=" * 70)
print("HEURISTIC 6: Sibling convergence within same roaster at similar age")
print("=" * 70)
# For each Score-5, look at OTHER same-roaster brews within 2 days that also scored.
# Check |grind_diff| distribution.
spreads = []
for _, row in zdf[zdf.score == 5].iterrows():
    if pd.isna(row.day):
        continue
    siblings = zdf[
        (zdf.roaster == row.roaster) &
        (zdf.coffee != row.coffee) &
        ((zdf.day - row.day).abs() <= 2) &
        (zdf.score >= 4) &
        (zdf.idx != row.idx)
    ]
    for _, sib in siblings.iterrows():
        spreads.append(abs(sib.grind - row.grind))
if spreads:
    arr = np.array(spreads)
    print(f"  Score-5 vs same-roaster sibling (Score≥4, within 2 days), n={len(arr)}")
    print(f"    Median grind spread: {np.median(arr):.4f}")
    print(f"    Mean:                {arr.mean():.4f}")
    print(f"    Within 1 click (≤0.025): {100*(arr<=0.025).mean():.1f}%")
    print(f"    Within 2 clicks (≤0.05): {100*(arr<=0.050).mean():.1f}%")
    print(f"    Within 3 clicks (≤0.075): {100*(arr<=0.075).mean():.1f}%")
