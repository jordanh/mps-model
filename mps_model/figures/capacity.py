"""Figure 11: how full each Middle Ground receiving building gets, and its average class size, before
and after the moves (from capacity_class_size_impacts.csv)."""
import matplotlib.ticker
import pandas as pd

from .style import BLUE, INK, INK2, LIGHT_BLUE, plt

GRID = "#e4e2dc"
ELEMENTARY_CLASS_CAP = 26


def dumbbell(ax, df, before, after, fmt, ref=None, ref_label=None, xmax=None):
    """One row per school: hollow dot today, filled dot after the move."""
    y = range(len(df))
    for i, (b, a) in enumerate(zip(df[before], df[after])):
        ax.plot([b, a], [i, i], color=LIGHT_BLUE, lw=3, solid_capstyle="round", zorder=1)
    ax.scatter(df[before], y, s=110, color="white", edgecolor=BLUE, linewidth=2.2, zorder=3, label="Today")
    ax.scatter(df[after], y, s=130, color=BLUE, edgecolor="white", linewidth=2, zorder=4, label="After the move")
    pad = (xmax or max(df[after].max(), df[before].max())) * 0.025
    for i, (b, a) in enumerate(zip(df[before], df[after])):
        ax.text(max(a, b) + pad, i, f"{fmt(b)} → {fmt(a)}", ha="left", va="center", fontsize=12.5, color=INK,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"), zorder=5)
    if ref is not None:
        ax.axvline(ref, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=0)
        ax.text(ref, len(df) - 0.35, ref_label, ha="center", va="bottom", fontsize=12, color=INK2)
    ax.set_yticks(list(y))
    ax.set_yticklabels(df.label, fontsize=13, color=INK)
    ax.set_ylim(-0.6, len(df) - 0.1)
    if xmax:
        ax.set_xlim(0, xmax)
    ax.grid(axis="x", color=GRID, lw=1)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(INK2)
    ax.tick_params(length=0, pad=6, colors=INK2)


def draw(results):
    plt.rcParams.update({"font.family": ["Inter", "DejaVu Sans"], "font.size": 15})
    d = pd.read_csv(results.table("capacity_class_size_impacts.csv"))
    mg = d[(d.plan == "Middle Ground") & (d.role == "receives")].copy()
    mg["label"] = mg.school + "\n(from " + mg.receives_from.str.replace("; ", " + ") + ")"
    mg["u_before"] = mg.util_2024_design_before.fillna(mg.utilization_before)
    mg["u_after"] = mg.util_2024_design_after.fillna(mg.utilization_after)
    mg = mg.sort_values("u_after")
    elementary = mg[mg.class_size_cap == ELEMENTARY_CLASS_CAP].sort_values("class_size_after")

    fig, (left, right) = plt.subplots(1, 2, figsize=(15, 6.2), dpi=200, gridspec_kw=dict(width_ratios=[1.15, 1]))
    fig.subplots_adjust(left=0.15, right=0.98, top=0.83, bottom=0.15, wspace=0.6)
    dumbbell(left, mg, "u_before", "u_after", lambda v: f"{v:.0%}", 1.0, "Design enrollment", 1.2)
    left.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    left.set_title("Share of the building's design enrollment in use", loc="left", fontsize=15, fontweight="semibold",
                   color=INK, pad=24)
    dumbbell(right, elementary, "class_size_before", "class_size_after", lambda v: f"{v:.0f}",
             ELEMENTARY_CLASS_CAP, f"Class-size cap ({ELEMENTARY_CLASS_CAP})", 36)
    right.set_title("Average elementary class size", loc="left", fontsize=15, fontweight="semibold", color=INK, pad=24)
    handles, labels = left.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.15, 0.995), ncol=2, frameon=False, fontsize=13)
    fig.text(0.15, 0.015, "Middle Ground plan, receiving schools. Design enrollment from MPS's 2024 Physical Space Study. "
             "Counts every moved student, before any family leaves.\n"
             "Class sizes are modeled sections at a cap of 26; high school programs move with their own teachers.",
             fontsize=11.5, color=INK2)
    fig.savefig(results.figure("fig11_capacity_class_size.png"), facecolor="white")
    plt.close(fig)
