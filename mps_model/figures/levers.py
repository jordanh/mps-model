"""Figure 6: how each plan closes the gap, lever by lever. Figure 7: families lost and recruits
needed for every number of closures."""
import matplotlib.ticker
import pandas as pd

from .style import AQUA, BLUE, GAP_GREY, GRID, INK, INK2, M, VIOLET, YELLOW, plt, remove_spines, use_style

OPTION_LABELS = [("Footprint-First plan (District Option 1)", "Opt. 1"),
                 ("Footprint-First plan (District Option 2)", "Opt. 2"),
                 ("Footprint-First plan (District Option 3)", "Opt. 3")]


def lever_mix(results, plans, gap):
    n_mg = int(plans.loc["Middle Ground plan", "schools_closed"])
    option1 = plans.loc["Footprint-First plan (District Option 1)"]
    show = [("Family Trust plan", "Family Trust\n2 program merges"),
            ("Middle Ground plan", f"Middle Ground\n{n_mg} closures"),
            ("Footprint-First plan (District Option 1)", f"Footprint-First\n(District Option 1)\n{int(option1.schools_closed)} closures")]
    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=200)
    for i, (key, label) in enumerate(show):
        r = plans.loc[key]
        segments = [(r.sharing_savings / M, AQUA, "Specialist sharing"),
                    (max(0, r.closure_net_savings) / M, BLUE, "Closures (net of bussing, families leaving, moving)"),
                    (r.recruitment_net_annual / M, YELLOW, "Recruitment (net of campaign cost)"),
                    (max(0, r.gap_left_if_recruitment_as_planned) / M, GAP_GREY, "Gap left unclosed")]
        left = 0
        for value, color, name in segments:
            if value <= 0.05:
                continue
            ax.barh(i, value, left=left, color=color, height=0.6, edgecolor="white", lw=2,
                    label=name if i == 0 or name == "Gap left unclosed" else None, hatch="//" if color == GAP_GREY else None)
            if value > 1.6:
                ax.text(left + value / 2, i, f"${value:.1f}M", ha="center", va="center", fontsize=10,
                        color="white" if color == BLUE else INK)
            left += value
    gap_m = gap / M
    ax.axvline(gap_m, color=INK, lw=1.2, ls="--")
    ax.text(gap_m + 0.2, 2.42, f"${gap_m:.0f}M FY28 gap (estimate)", fontsize=9, color=INK2, va="bottom")
    ax.set_yticks(range(len(show)))
    ax.set_yticklabels([s[1] for s in show], fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(0, 40)
    ax.set_xlabel("Annual $ millions")
    remove_spines(ax)
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    handles = {}
    for h, label in zip(*ax.get_legend_handles_labels()):
        handles.setdefault(label, h)
    ax.legend(handles.values(), handles.keys(), frameon=False, fontsize=9, loc="lower center",
              bbox_to_anchor=(0.5, -0.42), ncol=2)
    ax.set_title("Three ways to close the gap: the levers trade off against each other", loc="left", fontsize=14,
                 color=INK, fontweight="bold")
    fig.tight_layout()
    fig.savefig(results.figure("fig6_three_plans_lever_mix.png"))
    plt.close(fig)


def tradeoff(results, plans, by_n):
    n_ft = int(plans.loc["Family Trust plan", "schools_closed"])
    n_mg = int(plans.loc["Middle Ground plan", "schools_closed"])
    marks = {"Family Trust": n_ft, "Middle Ground": n_mg}
    plan_color = {n_ft: AQUA, n_mg: BLUE}
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=200)
    for ax, column, title, fmt in [(axes[0], "families_lost", "Families who leave MPS", "{:,.0f}"),
                                   (axes[1], "recruits_needed", "New students needed to balance the budget", "{:,.0f}")]:
        ax.bar(by_n.N, by_n[column], color=[plan_color.get(n, GAP_GREY) for n in by_n.N], width=0.7, edgecolor="white")
        if column == "recruits_needed":  # past ~14 closures recruits hit the 90% capacity line and never balance
            for n in by_n.loc[~by_n.can_balance.astype(bool), "N"]:
                ax.text(n, by_n[column].max() * 0.04, "Can't\nbalance", ha="center", va="bottom", fontsize=7.5,
                        color=INK2, rotation=90)
        for name, n in marks.items():
            v = by_n.loc[by_n.N == n, column].iloc[0]
            ax.annotate(f"{name}\n" + fmt.format(v), (n, v), xytext=(0, 8), textcoords="offset points",
                        ha="center", fontsize=9.5, color=INK, fontweight="semibold")
        for key, label in OPTION_LABELS:
            r = plans.loc[key]
            v = r.families_lost if column == "families_lost" else r.recruits_needed_to_balance
            ax.scatter([r.schools_closed], [v], marker="D", s=60, color=VIOLET, zorder=5, edgecolor="white", lw=1.5)
            ax.annotate(label, (r.schools_closed, v), xytext=(0, 7), textcoords="offset points", ha="center",
                        fontsize=8, color=VIOLET)
        ax.scatter([], [], marker="D", s=60, color=VIOLET, label="Footprint-First (district options)")
        ax.legend(frameon=False, fontsize=8.5, loc="upper left")
        ax.set_title(title, loc="left", fontsize=12, color=INK, fontweight="bold")
        ax.set_xlabel("Number of schools closed")
        ax.set_xticks(range(0, 17, 2))
        remove_spines(ax, ("top", "right", "left"))
        ax.grid(axis="y", color=GRID)
        ax.set_axisbelow(True)
        ax.set_ylim(0, by_n[column].max() * 1.22)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
        ax.tick_params(length=0)
    fig.tight_layout()
    fig.savefig(results.figure("fig7_lever_tradeoff.png"), facecolor="white")
    plt.close(fig)


def draw(results, assumptions):
    use_style(11)
    plans = pd.read_csv(results.table("three_plans_levers.csv")).set_index("plan")
    by_n = pd.read_csv(results.table("lever_tradeoff_by_closures.csv"))
    lever_mix(results, plans, assumptions.get("budget", "structural_gap"))
    tradeoff(results, plans, by_n)
