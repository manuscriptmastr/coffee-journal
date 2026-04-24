"""Generate the two Hydrangea drift charts referenced in README.md.

Framing (per profile §8): the current batch is a single slow, noisy drift trend
around ~0.025/day, NOT a three-regime accelerating curve. Day-to-day windowed
slopes wiggle between ~0.013 and ~0.035 but converge on one rate when fit
linearly across all Score-5 anchors. Batch-to-batch behaviour is expected to
look similar — drift is slow and generally predictable.
"""
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT.parent / "assets"
ASSETS.mkdir(exist_ok=True)

df = pd.read_csv(ROOT / "entries.csv")
zh = df[(df.roaster == "Hydrangea") & (df.brewer == "Z") & df.day.notna()].copy()
zh = zh.sort_values("idx").reset_index(drop=True)

# Segment the two batches. The current (Mar 29 2026) batch comprises Pena,
# La Isabela, Monteblanco, Paraiso at idx >= 880. Everything prior on Z is the
# earlier Z1 Hydrangea batch (Pena, Paraiso at Day 14-57 range).
current = zh[zh.idx >= 880].copy()
earlier = zh[zh.idx < 880].copy()

COFFEE_COLORS = {
    "Pena": "#2e7d32",
    "La Isabela": "#c62828",
    "Monteblanco": "#1565c0",
    "Paraiso": "#ef6c00",
}


def _fit_and_plot(ax, data, title, subtitle):
    """Plot per-coffee points with Score encoding + one shared linear fit."""
    # Fit a single linear trend across Score-5 anchors (the best SS estimates)
    anchors = data[data.score == 5]
    if len(anchors) >= 2:
        slope, intercept = np.polyfit(anchors.day, anchors.grind, 1)
    else:
        slope, intercept = np.polyfit(data.day, data.grind, 1)

    # Trend line across full day range with a ±1-click corridor
    day_range = np.array([data.day.min() - 0.5, data.day.max() + 0.5])
    trend = slope * day_range + intercept
    ax.fill_between(
        day_range,
        trend - 0.025,
        trend + 0.025,
        color="#888",
        alpha=0.15,
        label="±1 click (grinder resolution)",
    )
    ax.plot(
        day_range,
        trend,
        color="#555",
        linewidth=1.8,
        linestyle="--",
        label=f"linear fit: {slope:+.3f}/day",
    )

    # Per-coffee points, score-coded by marker
    for coffee, color in COFFEE_COLORS.items():
        sub = data[data.coffee == coffee]
        if sub.empty:
            continue
        for score, marker, size in [
            (5, "o", 80),
            (4, "s", 55),
            (3, "x", 70),
            (2, "v", 60),
        ]:
            pts = sub[sub.score == score]
            if not pts.empty:
                ax.scatter(
                    pts.day,
                    pts.grind,
                    c=color,
                    marker=marker,
                    s=size,
                    edgecolors="black" if marker != "x" else color,
                    linewidths=0.6,
                    label=f"{coffee} S{score}" if score == 5 else None,
                    zorder=3,
                )

    ax.set_xlabel("Day since roast")
    ax.set_ylabel("Lagom P64 grind setting")
    ax.set_title(title, fontsize=12, loc="left", fontweight="bold", pad=38)
    # Wrap subtitle manually to avoid clipping
    import textwrap

    wrapped = "\n".join(textwrap.wrap(subtitle, width=110))
    ax.text(
        0.0,
        1.015,
        wrapped,
        transform=ax.transAxes,
        fontsize=9,
        color="#555",
        va="bottom",
    )
    ax.grid(True, alpha=0.25)

    # Legend: coffees + trend, deduplicated
    handles, labels = ax.get_legend_handles_labels()
    seen = set()
    unique = [
        (h, l) for h, l in zip(handles, labels) if not (l in seen or seen.add(l))
    ]
    ax.legend(
        [h for h, _ in unique],
        [l for _, l in unique],
        loc="lower right",
        fontsize=8,
        framealpha=0.9,
    )
    return slope, intercept


# ---- Chart 1: current batch ----
fig, ax = plt.subplots(figsize=(11, 6.5))
slope, intercept = _fit_and_plot(
    ax,
    current,
    "Hydrangea current batch (Mar 29 roast) — Z1, Day 8 onward",
    (
        "Single slow drift trend. Score-5 anchors fit one line within ±1 click; "
        "daily windowed slopes wiggle ~0.013–0.035/day around the overall rate "
        "but there is no distinct regime change. All four coffees share the "
        "same trajectory; they differ in coarse/fine-edge failure vocabulary, "
        "not in drift rate."
    ),
)
n_anchors = (current.score == 5).sum()
ax.annotate(
    f"linear fit across {n_anchors} Score-5 anchors:  grind = {slope:.4f}·day + {intercept:.3f}",
    xy=(0.02, 0.96),
    xycoords="axes fraction",
    fontsize=9,
    color="#333",
    va="top",
)
plt.tight_layout()
plt.savefig(ASSETS / "hydrangea_current_drift.png", dpi=140)
plt.close()
print(
    f"wrote hydrangea_current_drift.png — fit slope={slope:.4f}/day intercept={intercept:.3f}"
)

# ---- Chart 2: earlier Z1 batch ----
fig, ax = plt.subplots(figsize=(11, 6.5))
slope2, intercept2 = _fit_and_plot(
    ax,
    earlier,
    "Hydrangea earlier Z1 batch (Pena, Paraiso)",
    (
        "Single slow drift trend across the full ~50-day window. Same ~0.02/day "
        "family as the current batch; scatter widens later as per-coffee "
        "coarse-tolerance fingerprints become visible."
    ),
)
plt.tight_layout()
plt.savefig(ASSETS / "hydrangea_z1_drift.png", dpi=140)
plt.close()
print(
    f"wrote hydrangea_z1_drift.png — fit slope={slope2:.4f}/day intercept={intercept2:.3f}"
)
