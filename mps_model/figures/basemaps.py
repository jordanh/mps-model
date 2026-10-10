"""Base maps for the closure maps, all in the pixel frame of the district's current pathway map, so the
school positions in data/compiled/map_positions_and_context.csv land correctly on every one of them.

  base_option{1,2,3}.png  the district's own Option 1-3 high school pathway maps (Sept. 15, 2026
                          Transformation Proposal, slide 24), with their new attendance boundaries
  base_ours.png           the current map with Kenwood's attendance area moved to the Southwest pathway
                          (our plans' only boundary change, policy.pathway_overrides)

The option maps in data/district/option_maps/ were extracted from slide 24 with pdfimages (alpha masks
applied). They are registered to the current map by scale and offset, from each map's bounding box.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .. import paths

DISTRICT_BOX = (172, 264, 952, 1562)   # district outline bounding box in the current map
OPTION_BOX = {"option1": (109, 83, 1239, 1958),
              "option2": (87, 64, 1208, 1942),
              "option3": (87, 64, 1208, 1942)}   # the same outline in each option map
MAP_INTERIOR = (56, 200, 1012, 1640)   # inside the card frame, below the title band

# Recoloring Kenwood's area (pixel rules tuned by eye on these specific images)
WEST_SIDE = (slice(860, 1200), slice(170, 530))      # rows, columns between Bryn Mawr and Lake Harriet
OLD_BOUNDARY_BAND = (slice(1166, 1200), slice(182, 284))
HIGHWAY_SHIELD = (slice(880, 915), slice(170, 230))  # I-394 shield, left untouched
BOUNDARY_COLOR = (82, 96, 172)
SOUTHWEST_TINT = np.array([25, -12, -23])            # shifts North-pathway purple to Southwest pink
MERGED_AREA_COLOR = (245, 210, 212)


def current_map():
    return Image.open(paths.CURRENT_PATHWAY_MAP).convert("RGB")


def registered_option_map(name, current):
    """A district option map resampled into the current map's frame (white outside the map)."""
    src = Image.open(paths.DISTRICT_OPTION_MAPS_DIR / f"{name}.png").convert("RGB")
    x0, y0, x1, y1 = OPTION_BOX[name]
    c = DISTRICT_BOX
    sx, sy = (c[2] - c[0]) / (x1 - x0), (c[3] - c[1]) / (y1 - y0)
    im = src.resize((round(src.width * sx), round(src.height * sy)), Image.LANCZOS)
    canvas = Image.new("RGB", current.size, "white")
    canvas.paste(im, (round(c[0] - x0 * sx), round(c[1] - y0 * sy)))
    return canvas


def in_current_frame(map_img, current):
    """Keep the current map's card frame and title band, replace the map inside it."""
    out = current.copy()
    out.paste(map_img.crop(MAP_INTERIOR), MAP_INTERIOR[:2])
    return out


def _filled(mask):
    """Close small gaps, then fill holes (lakes, labels) by flood-filling from outside."""
    img = Image.fromarray((mask * 255).astype("uint8"))
    img = img.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.MinFilter(11))
    ImageDraw.floodfill(img, (0, 0), 128)
    return np.asarray(img) != 128


def map_with_kenwood_in_southwest(current, option2):
    """Kenwood's area is purple (North pathway) on the current map and pink (Southwest) on Option 2,
    which moves exactly that area. Recolor it on the current map, erase the old Kenwood / Lake Harriet
    boundary and draw the new Kenwood / Bryn Mawr boundary."""
    a, b = np.asarray(current).astype(int), np.asarray(option2).astype(int)
    west = np.zeros(a.shape[:2], bool)
    west[WEST_SIDE] = True
    purple = (a[..., 2] - a[..., 0] > 6) & (a[..., 2] > 200) & west
    pink = (b[..., 0] - b[..., 2] > 20) & (b[..., 0] > 200) & west
    kenwood = _filled(purple) & _filled(pink)

    out = a.copy()
    tint = kenwood & (a[..., 2] - a[..., 0] > 5) & (a[..., 2] - a[..., 0] < 45) & (a[..., 0] > 140)
    out[tint] = np.clip(a[tint] + SOUTHWEST_TINT, 0, 255)

    band = np.zeros(kenwood.shape, bool)
    band[OLD_BOUNDARY_BAND] = True
    old_line = band & (a[..., 2] - a[..., 0] > 25) & (a[..., 1] - a[..., 0] < 25) & (a[..., 0] < 200)
    out[old_line] = MERGED_AREA_COLOR

    grown = np.asarray(Image.fromarray((kenwood * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9))) > 0
    rest_of_north = ((a[..., 2] - a[..., 0] > 6) & (a[..., 2] > 200) & (a[..., 0] > 150)
                     & (a[..., 1] - a[..., 0] < 15) & west & ~kenwood)
    above_row_1000 = np.arange(a.shape[0])[:, None] < 1000
    new_line = grown & above_row_1000 & ~kenwood & (rest_of_north | (a.sum(-1) < 600))
    new_line[HIGHWAY_SHIELD] = False
    out[new_line] = BOUNDARY_COLOR
    return Image.fromarray(out.astype("uint8"))


def build_basemaps(results):
    current = current_map()
    for k in (1, 2, 3):
        in_current_frame(registered_option_map(f"option{k}", current), current).save(results.basemaps / f"base_option{k}.png")
    option2 = registered_option_map("option2", current)
    map_with_kenwood_in_southwest(current, option2).save(results.basemaps / "base_ours.png")
