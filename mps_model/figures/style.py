"""Shared colors and chart styling."""
import logging

import matplotlib

matplotlib.use("Agg")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # quiet "font weight not found" notes  # draw to files, no window
import matplotlib.pyplot as plt  # noqa: E402

BLUE, ORANGE, AQUA, VIOLET, RED, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7", "#e34948", "#eda100"
LIGHT_BLUE = "#a9c7ee"
INK, INK2, GRID, GAP_GREY = "#0b0b0b", "#52514e", "#e4e3df", "#c9c7c0"
M = 1e6  # dollars per million

# Inter is the deck typeface; DejaVu Sans (bundled with matplotlib) is the fallback.
SANS = ["Inter", "DejaVu Sans"]


def use_style(font_size=11, family=SANS):
    plt.rcParams.update({"font.family": family, "font.size": font_size, "axes.edgecolor": INK2,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})


def remove_spines(ax, sides=("top", "right")):
    for side in sides:
        ax.spines[side].set_visible(False)


def light_grid(ax, axis="y", color=GRID):
    ax.grid(axis=axis, color=color, lw=0.8)
    ax.set_axisbelow(True)
