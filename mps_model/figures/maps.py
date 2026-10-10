"""Closure maps: red X on each closed building, blue arrows for students moving (width by count),
dashed aqua lines for specialist-sharing pairs.

Our plans are drawn on the current map with Kenwood moved to Southwest (base_ours.png). Each district
option is drawn on the district's own map for that option, with its new boundaries.
"""
import json

import pandas as pd
from matplotlib.patches import FancyArrowPatch
from PIL import Image

from .. import paths
from .style import AQUA, BLUE, INK, RED, plt

TITLE_BAND = (55, 40, 960, 140)   # x, y, width, height of the white title box, in map pixels
LEGEND_BAND = (60, 1590, 950, 75)


class MapContext:
    def __init__(self, results):
        self.results = results
        self.plans = json.loads(results.table("plans.json").read_text())
        self.moves = pd.read_csv(results.table("plan_reassignments.csv"))
        self.pairs = pd.read_csv(results.table("plan_specialist_pairs.csv"))
        self.position = pd.read_csv(paths.SCHOOL_CONTEXT).set_index("school")
        self.bases = {k: Image.open(results.basemaps / f"base_{k}.png").convert("RGB")
                      for k in ("ours", "option1", "option2", "option3")}


def _draw_x(ax, x, y, half=15, lw=4.5):
    ax.plot([x - half, x + half], [y - half, y + half], color=RED, lw=lw, zorder=6, solid_capstyle="round")
    ax.plot([x - half, x + half], [y + half, y - half], color=RED, lw=lw, zorder=6, solid_capstyle="round")


def closure_map(ctx, plan_name, filename, title, show_pairs=False, base="ours"):
    image = ctx.bases[base]
    pos = ctx.position
    fig = plt.figure(figsize=(image.width / 150, image.height / 150), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(image)
    ax.axis("off")
    x, y, w, h = TITLE_BAND
    ax.add_patch(plt.Rectangle((x, y), w, h, color="white", zorder=3))
    ax.text(535, 95, title, ha="center", va="center", fontsize=17, fontweight="bold", color=INK, zorder=4)

    moves = ctx.moves[ctx.moves.plan == plan_name]
    totals = moves.groupby(["closed_school", "receiving_school"]).students.sum().reset_index()
    for _, r in totals.iterrows():
        a, b = pos.loc[r.closed_school], pos.loc[r.receiving_school]
        ax.add_patch(FancyArrowPatch((a.map_x, a.map_y), (b.map_x, b.map_y), arrowstyle="-|>", mutation_scale=18,
                                     lw=1.5 + r.students / 90, color=BLUE, alpha=0.9, connectionstyle="arc3,rad=0.18", zorder=5))
        ax.text((a.map_x + b.map_x) / 2 + 6, (a.map_y + b.map_y) / 2, f"{int(r.students)}", fontsize=8, color=BLUE,
                fontweight="bold", zorder=7, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
    for school in ctx.plans["plans"][plan_name]:
        p = pos.loc[school]
        _draw_x(ax, p.map_x, p.map_y)
        ax.text(p.map_x + 18, p.map_y + 22, school, fontsize=8.5, color="white", fontweight="bold", zorder=8,
                bbox=dict(boxstyle="round,pad=0.2", fc=RED, ec="none"))
    if show_pairs:
        for _, r in ctx.pairs[ctx.pairs.plan == plan_name].iterrows():
            a, b = pos.loc[r.school_a], pos.loc[r.school_b]
            ax.plot([a.map_x, b.map_x], [a.map_y, b.map_y], color=AQUA, lw=3, ls=(0, (3, 2)), zorder=5)

    x, y, w, h = LEGEND_BAND
    ax.add_patch(plt.Rectangle((x, y), w, h, color="white", zorder=3))
    ax.plot([90, 110], [1615, 1635], color=RED, lw=4, zorder=6)
    ax.plot([90, 110], [1635, 1615], color=RED, lw=4, zorder=6)
    ax.text(122, 1626, "School building closed", va="center", fontsize=10, zorder=6)
    ax.add_patch(FancyArrowPatch((390, 1626), (450, 1626), arrowstyle="-|>", mutation_scale=15, lw=2.5, color=BLUE, zorder=6))
    ax.text(460, 1626, "Students move (n)", va="center", fontsize=10, zorder=6)
    if show_pairs:
        ax.plot([700, 740], [1626, 1626], color=AQUA, lw=3, ls=(0, (3, 2)), zorder=6)
        ax.text(748, 1626, "Shared specialists", va="center", fontsize=10, zorder=6)
    fig.savefig(ctx.results.figure(filename), dpi=150)
    plt.close(fig)


def draw(results):
    plt.rcParams.update({"font.family": "DejaVu Sans"})
    ctx = MapContext(results)
    n_opt = ctx.plans["optimum_N"]
    middle_ground = next(p for p in ctx.plans["plans"] if p.startswith("Optimum"))
    closure_map(ctx, middle_ground, "fig3_map_optimum_plan.png", f"Middle Ground plan: {n_opt} closures")
    closure_map(ctx, "3-closure plan", "fig4_map_three_closure_plan.png", "Variant: 3-closure plan")
    closure_map(ctx, middle_ground, "fig5_map_optimum_with_specialist_sharing.png",
                "Middle Ground plan + shared specialists", show_pairs=True)
    closure_map(ctx, "Family Trust plan", "fig8_map_family_trust_plan.png",
                "Family Trust plan: 2 high school program merges", show_pairs=True)
    for k in (1, 2, 3):
        closure_map(ctx, f"District Option {k}", f"figA{k}_map_district_option{k}.png",
                    f"Footprint-First: District Option {k} (modeled)", base=f"option{k}")
