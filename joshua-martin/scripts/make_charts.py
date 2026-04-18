"""Generate validation charts from the Phase A/B holdout results."""
from pathlib import Path
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT.parent / "assets"
ASSETS.mkdir(exist_ok=True)
df = pd.read_csv(ROOT / "entries.csv")
zdf = df[(df.brewer == "Z") & (df.grind < 10) & (df.day.notna())].reset_index(drop=True)

# ---- Re-run minimal Phase A to compute MAE numbers ----
DRIFT = {"H&S":0.020,"Hydrangea":0.022,"September":0.018,"Moonwake":0.027,
         "Sey":0.020,"Paix":0.020,"Norena":0.020}

preds = defaultdict(list); truths = []
hist = defaultdict(list); rhist = defaultdict(list); allg = []
for _, row in zdf.iterrows():
    coffee, roaster, day, grind, score = row.coffee, row.roaster, row.day, row.grind, row.score
    if not allg:
        allg.append(grind); hist[coffee].append((day,grind,score))
        if roaster: rhist[roaster].append((day,grind,score,coffee))
        continue
    truths.append(grind)
    drift = DRIFT.get(roaster, 0.020)
    preds["global mean"].append(np.mean(allg))
    preds["roaster mean"].append(np.mean([g for _,g,_,_ in rhist.get(roaster,[])]) if rhist.get(roaster) else np.mean(allg))
    preds["last grind\n(no drift)"].append(hist[coffee][-1][1] if hist[coffee] else np.mean(allg))
    if hist[coffee]:
        ld, lg, _ = hist[coffee][-1]
        preds["last grind\n+ drift"].append(lg + drift * (day - ld))
    else:
        preds["last grind\n+ drift"].append(np.mean(allg))
    sib = [(d,g,s,c) for d,g,s,c in rhist.get(roaster,[]) if c != coffee]
    if sib:
        d,g,_,_ = sib[-1]
        preds["sibling\n+ drift"].append(g + drift*(day-d))
    elif hist[coffee]:
        ld, lg, _ = hist[coffee][-1]
        preds["sibling\n+ drift"].append(lg + drift*(day-ld))
    else:
        preds["sibling\n+ drift"].append(np.mean(allg))
    hist[coffee].append((day,grind,score))
    if roaster: rhist[roaster].append((day,grind,score,coffee))
    allg.append(grind)

truths = np.array(truths)
results = [(n, np.mean(np.abs(np.array(p)-truths)),
            np.mean(np.abs(np.array(p)-truths) <= 0.025) * 100)
           for n,p in preds.items()]
results.sort(key=lambda r: r[1], reverse=True)

# ---- Chart 1: Predictor MAE ----
fig, ax = plt.subplots(figsize=(10, 5.5))
names = [r[0] for r in results]
maes  = [r[1] for r in results]
hits  = [r[2] for r in results]
colors = ["#d96666" if "drift" not in n else ("#5b9b5b" if "+ drift" in n else "#d9a866") for n in names]
bars = ax.barh(names, maes, color=colors, edgecolor="black", linewidth=0.6)
for bar, mae, hit in zip(bars, maes, hits):
    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
            f"  MAE {mae:.3f}   ({hit:.0f}% within 1 click)",
            va="center", fontsize=9)
ax.axvline(0.025, color="#888", linestyle=":", linewidth=1)
ax.text(0.025, -0.7, " 1 click", color="#888", fontsize=8, ha="left")
ax.set_xlim(0, max(maes) * 1.55)
ax.set_xlabel("Mean Absolute Error in grind units (729 walk-forward predictions)")
ax.set_title("Grind predictor holdout — Joshua's Z brewer era\nDrift heuristic wins; no-drift baselines lose ~1 extra click of accuracy",
             fontsize=11, loc="left")
plt.tight_layout()
plt.savefig(ASSETS / "predictor_mae.png", dpi=140)
plt.close()
print("wrote predictor_mae.png")

# ---- Chart 2: Should-have-been direction by score ----
sb = zdf[zdf.should_be != "[]"].copy()
sb["should_be_list"] = sb.should_be.map(lambda s: eval(s) if isinstance(s, str) else [])
data_by_score = {}
for sc in [2, 3, 4, 5]:
    deltas = []
    for _, r in sb[sb.score == sc].iterrows():
        for v in r.should_be_list:
            deltas.append(v - r.grind)
    if deltas:
        data_by_score[sc] = deltas

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
# Stacked bar: % coarser/finer/same per score
scores = list(data_by_score.keys())
coarser_pct = [100*np.mean(np.array(d)>0.005) for d in data_by_score.values()]
same_pct    = [100*np.mean(np.abs(np.array(d))<=0.005) for d in data_by_score.values()]
finer_pct   = [100*np.mean(np.array(d)<-0.005) for d in data_by_score.values()]
ns          = [len(d) for d in data_by_score.values()]
x = np.arange(len(scores))
ax1.bar(x, coarser_pct, color="#5b9b5b", label="coarser", edgecolor="black", linewidth=0.6)
ax1.bar(x, same_pct, bottom=coarser_pct, color="#bbb", label="same", edgecolor="black", linewidth=0.6)
ax1.bar(x, finer_pct, bottom=np.array(coarser_pct)+np.array(same_pct), color="#d96666",
        label="finer", edgecolor="black", linewidth=0.6)
for i, (cp, n) in enumerate(zip(coarser_pct, ns)):
    ax1.text(i, cp/2, f"{cp:.0f}%", ha="center", va="center", fontweight="bold", color="white")
    ax1.text(i, 102, f"n={n}", ha="center", va="bottom", fontsize=9, color="#555")
ax1.set_xticks(x); ax1.set_xticklabels([f"Score {s}" for s in scores])
ax1.set_ylabel("% of 'should have been' suggestions"); ax1.set_ylim(0, 110)
ax1.legend(loc="upper right", framealpha=0.9, fontsize=9)
ax1.set_title("Direction of correction by score of brew", fontsize=10)
ax1.axhline(67, color="#a44", linestyle="--", linewidth=1, alpha=0.6)
ax1.text(len(scores)-0.5, 68, "previously claimed 67%", color="#a44", fontsize=8, ha="right")

# Mean delta per score
means = [np.mean(d) for d in data_by_score.values()]
ax2.bar(x, means, color=["#d96666" if m < 0.005 else "#5b9b5b" for m in means],
        edgecolor="black", linewidth=0.6)
for i, m in enumerate(means):
    ax2.text(i, m + 0.001, f"{m:+.4f}", ha="center", va="bottom", fontsize=9)
ax2.set_xticks(x); ax2.set_xticklabels([f"Score {s}" for s in scores])
ax2.axhline(0, color="black", linewidth=0.8)
ax2.set_ylabel("Mean Δ (suggested grind − actual grind)")
ax2.set_title("Mean correction magnitude by score", fontsize=10)

fig.suptitle("Correction bias is score-conditional — it's not a flat 67%", fontsize=12)
plt.tight_layout()
plt.savefig(ASSETS / "correction_bias_by_score.png", dpi=140)
plt.close()
print("wrote correction_bias_by_score.png")

# ---- Chart 3: Score-5 follow-up grind change ----
gap_data = []
zdf_sorted = zdf.sort_values(["coffee", "idx"]).reset_index(drop=True)
for coffee, grp in zdf_sorted.groupby("coffee"):
    grp = grp.reset_index(drop=True)
    for i in range(len(grp) - 1):
        if grp.loc[i, "score"] == 5 and pd.notna(grp.loc[i, "day"]):
            for j in range(i + 1, len(grp)):
                if pd.notna(grp.loc[j, "day"]):
                    gap = grp.loc[j, "day"] - grp.loc[i, "day"]
                    if 0 < gap <= 3:
                        gap_data.append({
                            "gap": gap,
                            "delta": grp.loc[j, "grind"] - grp.loc[i, "grind"],
                            "next_score": grp.loc[j, "score"],
                        })
                    break
gap_df = pd.DataFrame(gap_data)

fig, (axA, axB) = plt.subplots(1, 2, figsize=(12, 5))
# Histogram of deltas
bins = np.arange(-0.075, 0.151, 0.025) - 0.0125
axA.hist(gap_df.delta, bins=bins, color="#5b9b5b", edgecolor="black")
axA.axvline(0, color="black", linewidth=1, linestyle="--")
axA.set_xlabel("Grind change (next brew − Score 5 brew)")
axA.set_ylabel("Number of follow-ups")
axA.set_title(f"Grind change after a Score 5 (n = {len(gap_df)} follow-ups within 3 days)\n"
              f"86% go coarser, 0% finer", fontsize=10)
axA.set_xticks(np.arange(-0.05, 0.151, 0.025))

# Mean delta vs gap days
gap_summary = gap_df.groupby("gap").agg(n=("delta","size"),
                                         mean_delta=("delta","mean"),
                                         kept_pct=("delta", lambda d: 100*np.mean(np.abs(d)<0.001)))
ax_b2 = axB.twinx()
axB.bar(gap_summary.index, gap_summary.mean_delta, color="#5b9b5b", alpha=0.85,
        edgecolor="black", linewidth=0.6, label="mean Δ grind")
ax_b2.plot(gap_summary.index, gap_summary.kept_pct, "ko-", label="% kept setting", linewidth=2)
axB.set_xlabel("Days between Score-5 brew and next brew")
axB.set_ylabel("Mean Δ grind", color="#3a6e3a")
ax_b2.set_ylabel("% of follow-ups that kept the same grind", color="black")
axB.set_xticks([1, 2, 3])
ax_b2.set_ylim(0, 100)
for x, n in zip(gap_summary.index, gap_summary.n):
    axB.text(x, gap_summary.loc[x, "mean_delta"] + 0.003, f"n={n}",
             ha="center", va="bottom", fontsize=9)
axB.set_title("Realised drift after Score 5 ≈ documented per-roaster rate", fontsize=10)

fig.suptitle("A Score-5 setting is a snapshot, not a steady state", fontsize=12)
plt.tight_layout()
plt.savefig(ASSETS / "score5_followup.png", dpi=140)
plt.close()
print("wrote score5_followup.png")
