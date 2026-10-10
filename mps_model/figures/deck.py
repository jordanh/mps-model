"""Images sized for the image frames of our presentation deck (optional: `--deck-images`).

Maps are cropped to the district (title band removed, legend kept) and padded with white to each
frame's aspect ratio. Slide numbers refer to our designed deck. Also draws the growth map with the
protected communities ringed (slide 22).
"""
import shutil

from PIL import Image, ImageDraw

from .. import paths
from .style import BLUE, GAP_GREY, INK, INK2, plt

MAP_CROP = (60, 240, 1010, 1660)  # district outline + legend, in map figure pixels
FRAME_HEIGHT = 2000

# (source figure, deck image, frame width / height measured from the designed PDF)
DECK_MAPS = [
    ("fig8_map_family_trust_plan.png", "slide10_family_trust_map.png", 0.87),
    ("figA1_map_district_option1.png", "slide11_footprint_first_thumbnail.png", 0.60),
    ("fig3_map_optimum_plan.png", "slide12_middle_ground_map.png", 0.71),
    ("fig3_map_optimum_plan.png", "slide27_middle_ground_map.png", 1.60),
    ("figA1_map_district_option1.png", "slide28_footprint_first_option1_map.png", 1.59),
    ("figA1_map_district_option1.png", "slide50_district_option1_map.png", 1.58),
    ("figA2_map_district_option2.png", "slide51_district_option2_map.png", 1.58),
    ("figA3_map_district_option3.png", "slide52_district_option3_map.png", 1.58),
]
DECK_COPIES = [  # figures and tables used as they are
    ("fig9_kenwood_pathway.png", "new_slide_kenwood_pathway.png"),
    ("fig1_net_savings_vs_closures.png", "slide25_net_savings_curve.png"),
    ("fig10_glide_path.png", "slide14_glide_path.png"),
    ("fig7_lever_tradeoff.png", "slide07_lever_tradeoff.png"),
    ("fig11_capacity_class_size.png", "slide27b_capacity_class_size.png"),
    ("fig12_recruit_value_capacity.png", "slide07b_recruit_value_capacity.png"),
]
DECK_TABLES = [
    ("lever_tradeoff_by_closures.csv", "slide07_lever_tradeoff_data.csv"),
    ("three_plans_levers.csv", "slide07b_recruit_value_data.csv"),
    ("capacity_class_size_impacts.csv", "slide27b_capacity_data.csv"),
]

# Projected 10-year change by community, as printed on the district's growth map, and where each
# protected community's label box sits on that image (pixels in the 803 x 1076 source).
GROWTH_LABELS = [("Central", 58.7), ("Phillips", 35.5), ("University", 34.5), ("Longfellow", 22.1),
                 ("Near North", 21.4), ("Northeast", 15.7), ("Camden", 12.1), ("Nokomis", -1.1),
                 ("Powderhorn", -3.4), ("Southwest", -6.9), ("Bde Maka Ska", -7.9)]
LABEL_BOXES = {"Northeast": (375, 142, 617, 216), "Near North": (12, 265, 255, 340),
               "University": (497, 348, 742, 423), "Central": (132, 515, 375, 590),
               "Phillips": (400, 521, 643, 596), "Longfellow": (542, 702, 785, 777)}
PROTECTED_PCT = 15


def fit_to_frame(im, aspect, height=FRAME_HEIGHT):
    """Scale an image to fit a frame of the given width:height, padded with white."""
    w, h = round(height * aspect), height
    scale = min(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), (255, 255, 255))
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas


def growth_slide(out_dir):
    src = Image.open(paths.GROWTH_MAP).convert("RGB")
    draw = ImageDraw.Draw(src)
    for x0, y0, x1, y1 in LABEL_BOXES.values():
        draw.rounded_rectangle((x0 - 7, y0 - 7, x1 + 7, y1 + 7), radius=26, outline=BLUE, width=7)

    plt.rcParams.update({"font.family": ["Inter", "DejaVu Sans"], "font.size": 15})
    fig = plt.figure(figsize=(18.5, 10), dpi=110)
    map_ax = fig.add_axes([0.0, 0.02, 0.40, 0.96])
    map_ax.imshow(src)
    map_ax.axis("off")
    ax = fig.add_axes([0.53, 0.12, 0.44, 0.76])
    names = [g[0] for g in GROWTH_LABELS][::-1]
    values = [g[1] for g in GROWTH_LABELS][::-1]
    ax.barh(names, values, color=[BLUE if v >= PROTECTED_PCT else GAP_GREY for v in values], height=0.68)
    for i, v in enumerate(values):
        protected = v >= PROTECTED_PCT
        ax.text(v + (1 if v >= 0 else -1), i, f"{v:+.1f}%", va="center", ha="left" if v >= 0 else "right",
                fontsize=14, color=INK if protected else INK2, fontweight="semibold" if protected else "normal")
    ax.axvline(PROTECTED_PCT, color=BLUE, lw=1.6, ls=(0, (4, 3)))
    ax.text(PROTECTED_PCT + 1.5, len(values) - 0.3, f"Protected: +{PROTECTED_PCT}% or more", color=BLUE, fontsize=14,
            fontweight="semibold", va="bottom")
    ax.axvline(0, color=INK2, lw=1)
    ax.set_xlim(-14, 68)
    ax.set_xticks([])
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=15, colors=INK)
    ax.set_title("Projected 10-year change in enrollment, by community", loc="left", fontsize=18,
                 fontweight="semibold", color=INK, pad=16)
    fig.text(0.53, 0.04, "Blue rings mark the six protected communities.\n"
             "Source: MPS, 10-year projected change in where students attend MPS schools.",
             fontsize=12, color=INK2, linespacing=1.5)
    fig.savefig(out_dir / "slide22_growth_map_protected.png", facecolor="white")
    plt.close(fig)


def draw(results):
    out = results.deck
    out.mkdir(parents=True, exist_ok=True)
    for src, dst, aspect in DECK_MAPS:
        im = Image.open(results.figure(src)).convert("RGB").crop(MAP_CROP)
        fit_to_frame(im, aspect).save(out / dst, optimize=True)
    for src, dst in DECK_COPIES:
        shutil.copy(results.figure(src), out / dst)
    for src, dst in DECK_TABLES:
        shutil.copy(results.table(src), out / dst)
    growth_slide(out)
