"""Figure 12: what each added student is worth as the open buildings fill up, and where each plan's
recruiting starts and ends on that curve."""
import matplotlib.ticker
import numpy as np
import pandas as pd

from ..recruitment import Recruitment
from .style import AQUA, BLUE, INK, INK2, plt

GRID, PURPLE = "#e4e2dc", "#4f3aa8"
ROWS = [("Family Trust plan", "Family Trust", AQUA), ("Middle Ground plan", "Middle Ground", BLUE),
        ("Footprint-First plan (District Option 1)", "Option 1", PURPLE),
        ("Footprint-First plan (District Option 3)", "Option 3", PURPLE)]


def draw(results, assumptions):
    plt.rcParams.update({"font.family": ["Inter", "DejaVu Sans"], "font.size": 12})
    recruitment = Recruitment(assumptions)
    levers = pd.read_csv(results.table("three_plans_levers.csv")).set_index("plan")
    full_until = assumptions.recruitment_capacity("full_benefit_until_util")
    taper_end = assumptions.recruitment_capacity("taper_end_util")
    utilization = np.linspace(0.5, 1.0, 500)
    value = [recruitment.value_of_recruit(u) for u in utilization]

    fig, ax = plt.subplots(figsize=(12, 5.4), dpi=200)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.86, bottom=0.2)
    ax.axhline(0, color=INK2, lw=1)
    ax.plot(utilization, value, color=INK, lw=2.5)
    for x, label in [(full_until, f"{full_until:.0%}: busing costs start\nto eat the benefit"),
                     (taper_end, f"{taper_end:.0%}: new classrooms or\nreopened buildings needed")]:
        ax.axvline(x, color=INK2, lw=1, ls=(0, (4, 3)))
        ax.text(x + 0.004, 7300, label, fontsize=10, color=INK2, va="top")
    for i, (key, label, color) in enumerate(ROWS):
        r = levers.loc[key]
        y = -2900 - i * 620
        start, end = r.utilization_before_recruiting, r.utilization_after_recruiting
        ax.annotate("", xy=(end, y), xytext=(start, y), arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2))
        ax.plot([start], [y], "o", color=color, ms=6)
        ax.text(start - 0.005, y, label, ha="right", va="center", fontsize=10.5, color=color, fontweight="semibold")
        ax.text(end + 0.005, y, f"{start:.0%} → {end:.0%}  ({r.recruits_needed_to_balance:,.0f} recruits)", ha="left",
                va="center", fontsize=10, color=INK, bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"), zorder=5)
    ax.set_xlim(0.5, 1.0)
    ax.set_ylim(-5200, 7600)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v:,.0f}" if v >= 0 else f"-${-v:,.0f}"))
    ax.set_yticks([value[-1], 0, 2000, 4000, recruitment.net_revenue])
    ax.text(taper_end + 0.005, value[-1] + 250, "Each added student\nnow costs money", fontsize=10, color=INK2, va="bottom")
    ax.set_xlabel("Students as a share of design enrollment in the buildings left open (district average)")
    ax.set_title("What MPS keeps from each added student, per year", loc="left", fontsize=14, fontweight="bold", color=INK, pad=12)
    ax.grid(axis="y", color=GRID)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.text(0.09, 0.03, "Our estimates. $11,500 revenue per student, half kept (MPS FY27 budget). Busing $3,850 per rider "
             "(MPS $73M for about 19,000 riders).\nNew seats about $3,800 per student a year (staffing and running a "
             "reopened 450-seat building). Arrows show each plan's recruiting, start to finish.", fontsize=9.5, color=INK2)
    fig.savefig(results.figure("fig12_recruit_value_capacity.png"), facecolor="white")
    plt.close(fig)
