"""Figure 10: the glide path. Each school year's shortfall that bridge funding must cover, for Family
Trust and Middle Ground, as stepped areas that fall to zero (from glide_path.csv)."""
import pandas as pd

from .style import AQUA, BLUE, INK, INK2, plt

GRID = "#e4e2dc"
SERIES = [("Family Trust plan", "Family Trust", AQUA, "o"), ("Middle Ground plan", "Middle Ground", BLUE, "s")]


def draw(results):
    plt.rcParams.update({"font.family": ["Inter", "DejaVu Sans"], "font.size": 15})
    levers = pd.read_csv(results.table("three_plans_levers.csv")).set_index("plan")
    glide = pd.read_csv(results.table("glide_path.csv"))
    years = list(dict.fromkeys(glide.school_year))
    schedules = {label: glide[glide.plan == label].shortfall_m.tolist() for _, label, _, _ in SERIES}
    top = max(s[0] for s in schedules.values()) * 1.18

    fig, ax = plt.subplots(figsize=(14, 5.6), dpi=200)
    fig.subplots_adjust(left=0.06, right=0.76, top=0.88, bottom=0.16)
    x = list(range(len(years)))
    for plan, label, color, marker in SERIES:
        gaps = schedules[label]
        total = levers.loc[plan, "bridge_funding_evidence_pace"] / 1e6
        years_to_balance = levers.loc[plan, "years_to_balance_evidence_pace"]
        edges = [i - 0.5 for i in x] + [x[-1] + 0.5]
        values = gaps + [gaps[-1]]
        ax.fill_between(edges, values, step="post", color=color, alpha=0.13, lw=0)
        ax.step(edges, values, where="post", color=color, lw=2.6)
        live = [i for i, g in enumerate(gaps) if g > 0]
        ax.plot(live, [gaps[i] for i in live], marker, color=color, ms=9, mec="white", mew=2, zorder=5)
        for i in live:
            ax.text(i, gaps[i] + top * 0.03, f"${gaps[i]:.1f}M", ha="center", va="bottom", fontsize=13, color=INK2)
        label_y = top * (0.80 if label == "Family Trust" else 0.47)
        ax.plot([len(years) - 0.2], [label_y], marker, color=color, ms=12, mec="white", mew=2, clip_on=False)
        ax.text(len(years) - 0.05, label_y, label, fontsize=15, fontweight="semibold", color=INK, va="center")
        ax.text(len(years) - 0.05, label_y - top * 0.06,
                f"${total:.0f}M bridge in total\nbalanced in about {years_to_balance:g} years",
                fontsize=13, color=INK2, va="top", linespacing=1.4)
    ax.text(len(years) - 1, top * 0.035, "Balanced", ha="center", va="bottom", fontsize=14, fontweight="semibold", color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=14, color=INK2)
    ax.set_xlim(-0.6, len(years) - 0.5)
    ax.set_ylim(0, top)
    ticks = list(range(0, int(top) + 1, 5))
    ax.set_yticks(ticks)
    ax.set_yticklabels(["$0"] + [f"${t}M" for t in ticks[1:]], fontsize=13, color=INK2)
    ax.grid(axis="y", color=GRID, lw=1)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(INK2)
    ax.tick_params(length=0, pad=8)
    fig.text(0.06, 0.95, "Shortfall that bridge funding must cover, by school year", fontsize=16, fontweight="semibold",
             color=INK, va="top")
    fig.text(0.06, 0.04, "The shaded area under each line is the total bridge. Recruits counted each October, "
             "at the evidence-based pace of 2% enrollment growth a year.", fontsize=12, color=INK2)
    fig.savefig(results.figure("fig10_glide_path.png"), facecolor="white")
    plt.close(fig)
