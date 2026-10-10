"""Figure 1: net savings by number of closures. Figure 1b: the curve past 16 closures.
Figure 2: gross savings, costs and net savings by plan."""
import json

import pandas as pd

from ..plans import optimum_tolerance

from .style import AQUA, BLUE, GRID, INK, INK2, M, ORANGE, RED, VIOLET, light_grid, plt, remove_spines, use_style

REQUESTED_RANGE = 16   # closures range the analysis was asked to cover


def net_savings_curve(results, curve, comparison, n_opt, assumptions):
    core = curve[curve.N <= REQUESTED_RANGE]
    # the plateau: closure counts whose net savings are within the selection tolerance of the peak
    tolerance = optimum_tolerance(core.net_savings.max(), assumptions)
    plateau = core[core.net_savings >= core.net_savings.max() - tolerance].N
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=200)
    remove_spines(ax)
    light_grid(ax)
    ax.axhline(0, color=INK2, lw=1)
    ax.axvspan(plateau.min() - 0.4, plateau.max() + 0.4, color=BLUE, alpha=0.08, lw=0, zorder=0)
    ax.text((plateau.min() + plateau.max()) / 2, core.total_costs.max() / M * 0.97,
            f"{plateau.min()}-{plateau.max()} closures: net savings within ${tolerance / M:.1f}M of the best.\nThe plan takes the fewest.",
            ha="center", va="top", fontsize=10, color=INK2)
    ax.plot(core.N, core.gross_savings / M, color=AQUA, lw=2, marker="o", ms=5, label="Gross savings (closures + specialist sharing)")
    ax.plot(core.N, core.total_costs / M, color=ORANGE, lw=2, marker="o", ms=5, label="Costs (families leaving + bussing + one-time)")
    ax.plot(core.N, core.net_savings / M, color=BLUE, lw=3, marker="o", ms=7, label="Net savings")
    top = core.gross_savings.max() / M
    opt = core[core.N == n_opt].iloc[0]
    family_trust = core[core.N == 2].iloc[0]
    ax.annotate(f"Middle Ground: {n_opt} closures\nnet ${opt.net_savings / M:.1f}M/yr", (n_opt, opt.net_savings / M),
                xytext=(n_opt + 0.3, opt.net_savings / M - top * 0.22), color=INK,
                arrowprops=dict(arrowstyle="-", color=INK2), fontsize=11, fontweight="bold")
    ax.annotate(f"Family Trust: 2 HS program merges\nnet ${family_trust.net_savings / M:.1f}M/yr", (2, family_trust.net_savings / M),
                xytext=(2.4, family_trust.net_savings / M - top * 0.2), color=INK,
                arrowprops=dict(arrowstyle="-", color=INK2), fontsize=10)
    for _, r in comparison[comparison.plan.str.startswith("District")].iterrows():
        ax.scatter([r.schools_closed], [r.net_savings / M], s=70, marker="D", color=VIOLET, zorder=5, edgecolor="white", lw=1.5)
        ax.annotate(r.plan.replace("District ", ""), (r.schools_closed, r.net_savings / M), xytext=(-18, 10),
                    textcoords="offset points", fontsize=9, color=INK2)
    ax.scatter([], [], s=70, marker="D", color=VIOLET, label="District Options 1-3 (same model; they also close schools in growth areas)")
    unconstrained = results.root / "unconstrained" / "net_savings_by_closures.csv"
    if unconstrained.exists():
        u = pd.read_csv(unconstrained)
        u = u[u.N <= REQUESTED_RANGE]
        ax.plot(u.N, u.net_savings / M, color=INK2, lw=1.5, ls="--", label="Net savings if growth areas were NOT protected")
    ax.set_xticks(range(0, REQUESTED_RANGE + 1))
    ax.set_xlabel("Number of schools closed")
    ax.set_ylabel("Annual savings ($ millions)")
    ax.set_title(f"Net savings are nearly flat from {plateau.min()} to {plateau.max()} closures, then fall", loc="left",
                 fontsize=14, color=INK, fontweight="bold")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=2, fontsize=9.5)
    fig.tight_layout()
    fig.savefig(results.figure("fig1_net_savings_vs_closures.png"))
    plt.close(fig)


def extended_stress_test(results, curve):
    if curve.N.max() <= REQUESTED_RANGE:
        return
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=200)
    remove_spines(ax)
    light_grid(ax)
    ax.axhline(0, color=INK2, lw=1)
    ax.plot(curve.N, curve.net_savings / M, color=BLUE, lw=2.5, marker="o", ms=5, label="Net savings")
    ax.plot(curve.N, -curve.bus_cost / M, color=ORANGE, lw=2, ls="--", label="Bussing cost (shown negative)")
    ax.plot(curve.N, -curve.lost_family_cost / M, color=RED, lw=2, ls=":", label="Cost of families leaving (shown negative)")
    ax.axvspan(REQUESTED_RANGE + 0.5, curve.N.max() + 0.5, color=GRID, alpha=0.5, lw=0)
    ax.text(REQUESTED_RANGE + 1, ax.get_ylim()[1] * 0.85, "Beyond the 16-closure range\nrequested (stress test)", color=INK2, fontsize=9)
    ax.set_xlabel("Number of schools closed")
    ax.set_ylabel("Annual $ millions")
    ax.set_title("Stress test: closing more than 16 schools", loc="left", fontsize=14, color=INK, fontweight="bold")
    ax.legend(frameon=False, loc="lower left", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(results.figure("fig1b_extended_stress_test.png"))
    plt.close(fig)


def plan_comparison_bars(results, comparison):
    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=200)
    remove_spines(ax)
    light_grid(ax)
    x = range(len(comparison))
    w = 0.26
    ax.bar([i - w for i in x], comparison.gross_savings / M, w - 0.02, color=AQUA, label="Gross savings")
    ax.bar(list(x), comparison.total_costs / M, w - 0.02, color=ORANGE, label="Costs")
    ax.bar([i + w for i in x], comparison.net_savings / M, w - 0.02, color=BLUE, label="Net savings")
    for i, r in comparison.iterrows():
        ax.text(i + w, r.net_savings / M + (0.6 if r.net_savings >= 0 else -1.6), f"${r.net_savings / M:.1f}M",
                ha="center", fontsize=9, color=INK)
    ax.axhline(0, color=INK2, lw=1)
    ax.set_xticks(list(x))
    ax.set_xticklabels([p.replace("Optimum plan", "Middle Ground").replace(" (", "\n(") for p in comparison.plan], fontsize=9.5)
    ax.set_ylabel("Annual $ millions")
    ax.set_title("Gross savings, costs and net savings by plan", loc="left", fontsize=14, color=INK, fontweight="bold")
    ax.legend(frameon=False, ncol=3, loc="upper right", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(results.figure("fig2_plan_comparison.png"))
    plt.close(fig)


def draw(results, assumptions):
    use_style(11, family="DejaVu Sans")
    curve = pd.read_csv(results.table("net_savings_by_closures.csv"))
    comparison = pd.read_csv(results.table("plan_comparison.csv"))
    n_opt = json.loads(results.table("plans.json").read_text())["optimum_N"]
    net_savings_curve(results, curve, comparison, n_opt, assumptions)
    extended_stress_test(results, curve)
    plan_comparison_bars(results, comparison)
