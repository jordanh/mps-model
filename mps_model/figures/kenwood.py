"""Figure 9: Kenwood's middle and high school pathway under our plans, since 2021, and in the district
options."""
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from PIL import Image

from .. import paths
from .style import BLUE, INK, INK2, VIOLET, plt

WEST_SIDE_CROP = (130, 640, 560, 1560)   # x0, y0, x1, y1 in map pixels: Camden edge to Southwest
LEGEND_HEIGHT = 170


def _road_miles(a, b):
    """Routed road miles from the drive-time matrix (data/compiled/school_drive_matrix.csv)."""
    m = pd.read_csv(paths.DRIVE_MATRIX).set_index(["from_school", "to_school"])
    return m.loc[(a, b), "road_miles"]


def draw(results):
    plt.rcParams.update({"font.family": ["Inter", "DejaVu Sans"]})
    pos = pd.read_csv(paths.SCHOOL_CONTEXT).set_index("school")
    base = Image.open(results.basemaps / "base_ours.png").convert("RGB")   # Kenwood shaded as Southwest
    x0, y0, x1, y1 = WEST_SIDE_CROP
    crop = base.crop(WEST_SIDE_CROP)
    w, h = crop.size
    fig = plt.figure(figsize=(w / 60, (h + LEGEND_HEIGHT) / 60), dpi=150)
    ax = fig.add_axes([0, LEGEND_HEIGHT / (h + LEGEND_HEIGHT), 1, h / (h + LEGEND_HEIGHT)])
    ax.imshow(crop, extent=(x0, x1, y1, y0))
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)
    ax.axis("off")

    def at(school):
        return pos.loc[school, "map_x"], pos.loc[school, "map_y"]

    def arrow(a, b, color, lw, ls="-", rad=0.0, z=5):
        ax.add_patch(FancyArrowPatch(at(a), at(b), arrowstyle="-|>", mutation_scale=22, lw=lw, color=color,
                                     linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=z, shrinkA=8, shrinkB=10))

    dashed, dotted = (0, (5, 4)), (0, (2, 3))
    arrow("Anwatin", "North", INK2, 2.5, ls=dashed, rad=-0.2)          # since 2021
    arrow("Kenwood", "Franklin", VIOLET, 2.5, ls=dotted, rad=-0.25)    # district Option 1
    arrow("Franklin", "North", VIOLET, 2.5, ls=dotted, rad=0.2)
    arrow("Kenwood", "Anthony", VIOLET, 2.5, ls=dotted, rad=-0.15)     # district Options 2-3
    arrow("Anthony", "Southwest", VIOLET, 2.5, ls=dotted, rad=-0.25)
    arrow("Kenwood", "Anwatin", BLUE, 6, rad=0.25, z=7)                # our plans
    arrow("Anwatin", "Southwest", BLUE, 6, rad=-0.12, z=7)

    for school, label, dx, dy in [("Kenwood", "Kenwood K-5", 14, 6), ("Anwatin", "Anwatin 6-8", -96, 30),
                                  ("Southwest", "Southwest High", 14, -8), ("North", "North High", -10, -26),
                                  ("Franklin", "Franklin 6-8", 12, 22), ("Anthony", "Anthony 6-8", 10, -18)]:
        x, y = at(school)
        ax.plot(x, y, "o", ms=11, color=INK, mec="white", mew=2, zorder=9)
        ax.text(x + dx, y + dy, label, fontsize=13, fontweight="semibold", color=INK, zorder=10,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.92))
    ax.text(282, 930, f"{_road_miles('Kenwood', 'Anwatin'):.1f} road mi", fontsize=12, color=BLUE,
            fontweight="semibold", zorder=10,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9))
    ax.text(250, 1150, "Grades 9-12\nat Southwest", fontsize=11.5, color=BLUE, fontweight="semibold", zorder=10,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9))

    legend_ax = fig.add_axes([0.04, 0.0, 0.92, (LEGEND_HEIGHT - 10) / (h + LEGEND_HEIGHT)])
    legend_ax.axis("off")
    items = [(BLUE, "-", 6, "Our plans: Kenwood, Anwatin (kept open), Southwest"),
             (INK2, dashed, 2.5, "Since 2021: Kenwood, Anwatin, North"),
             (VIOLET, dotted, 2.5, "District options: Option 1 via Franklin to North;\n"
                                    f"Options 2-3 via Anthony (about {_road_miles('Kenwood', 'Anthony'):.1f} road mi)")]
    legend_ax.legend([Line2D([0], [0], color=c, ls=ls, lw=lw) for c, ls, lw, _ in items], [t for *_, t in items],
                     loc="center left", frameon=False, fontsize=12.5, handlelength=3)
    fig.savefig(results.figure("fig9_kenwood_pathway.png"), facecolor="white")
    plt.close(fig)
