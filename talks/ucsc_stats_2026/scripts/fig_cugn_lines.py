"""Created by JXP and Claude.

Map of the California Underwater Glider Network (CUGN) standard lines for
the UCSC Statistics talk (2026): the four CalCOFI/CUGN cross-shore lines
56.0, 66.7, 80.0 and 90.0 plus the alongshore leg between lines 80 and 90,
over a Natural Earth coastline, with a few coastal cities for orientation.

Used on two slides: "A model ocean constrained by data" (half-width cell
next to a ROMS SST map) and "Optimize the robot placement" (about 6" wide
beside bullets).  The figure is drawn roughly square so it works in both.

Line end points
---------------
Inshore / offshore ends of the gridded 2026-beta CUGN climatology products
(cugn-climatology/context/initial_exploration.md, section 2 "Grids and
geometry": 56 -> 300 km, 66.7 -> 400 km, 80 -> 365 km, 90 -> 530 km,
alongshore -> 220 km), i.e. the geometry plotted in
cugn-climatology/context/figs/fig01_line_geometry.png.  Cross-checked
against cugn/cugn/utils.py:line_endpoints, which agrees at the inshore ends
(the full CalCOFI lines 66.7 and 90 extend further offshore than the
gridded products).

Run from the repo root:

    conda run -n ocean14 python talks/ucsc_stats_2026/scripts/fig_cugn_lines.py

Output: talks/ucsc_stats_2026/figures/cugn_lines.png
Requires cartopy (downloads the Natural Earth 50m land/coastline on first use).
"""
import sys
import warnings
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from sms_outreach.slides import style

OUT_DIR = REPO / "talks" / "ucsc_stats_2026" / "figures"
MANIFEST = OUT_DIR / "sources.json"
SOURCE = ("CUGN lines 56.0, 66.7, 80.0, 90.0 (Rudnick et al. 2017, J. Geophys. "
          "Res. Oceans); coastline: Natural Earth; drawn by J. X. Prochaska & Claude")
SLIDE = "A model ocean constrained by data; Optimize the robot placement"

# (lon, lat) inshore -> offshore, degrees E / N
LINES = {
    "56":   ((-123.27, 38.53), (-126.23, 37.17)),
    "66.7": ((-121.84, 36.89), (-125.71, 35.09)),
    "80":   ((-120.48, 34.47), (-123.89, 32.83)),
    "90":   ((-117.75, 33.50), (-122.61, 31.11)),
}
# alongshore leg, south (line 90) -> north (line 80)
ALONGSHORE = ((-119.96, 32.42), (-121.14, 34.13))
LINE_COLORS = {"56": style.SEA, "66.7": style.SEA_LIGHT,
               "80": style.TEAL, "90": style.STARS}

# city: (lon, lat), label offset in degrees, horizontal alignment
CITIES = {
    "San Francisco":    ((-122.42, 37.77), (0.25, 0.05), "left"),
    "Monterey":         ((-121.89, 36.60), (0.25, -0.15), "left"),
    "Point Conception": ((-120.47, 34.45), (0.2, 0.2), "left"),
    "Los Angeles":      ((-118.24, 34.05), (0.2, 0.1), "left"),
    "San Diego":        ((-117.16, 32.72), (0.0, -0.33), "center"),
}

EXTENT = (-127.0, -115.6, 30.5, 39.5)   # lon_min, lon_max, lat_min, lat_max
LAND = "#d9d9d9"
COAST = "#8a8a8a"
SEA_BG = "#f2f7fc"
LABEL_FS = 14
CITY_FS = 11


def _text_angle(ax, p0, p1):
    """Created by JXP and Claude. Angle (deg) in display space of the
    segment p0 -> p1 (data coords), for text rotated along a line."""
    x0, y0 = ax.transData.transform(p0)
    x1, y1 = ax.transData.transform(p1)
    return np.degrees(np.arctan2(y1 - y0, x1 - x0))


def main():
    """Created by JXP and Claude. Draw the CUGN line map and save it."""
    style.apply_style()
    plt.rcParams["axes.grid"] = False   # cartopy draws its own gridlines
    # style.save calls tight_layout, which only warns on GeoAxes
    warnings.filterwarnings("ignore", message=".*not compatible with tight_layout.*")

    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize=(4.3, 3.4))
    ax = fig.add_axes([0.14, 0.09, 0.84, 0.89], projection=proj)
    ax.set_extent(EXTENT, crs=proj)
    ax.set_facecolor(SEA_BG)
    ax.add_feature(cfeature.NaturalEarthFeature("physical", "land", "50m"),
                   facecolor=LAND, edgecolor="none", zorder=1)
    ax.add_feature(cfeature.NaturalEarthFeature("physical", "coastline", "50m"),
                   facecolor="none", edgecolor=COAST, linewidth=0.7, zorder=2)
    ax.spines["geo"].set_edgecolor("#444444")

    gl = ax.gridlines(crs=proj, draw_labels=True, linewidth=0.5,
                      color="#999999", alpha=0.4, linestyle="-")
    gl.top_labels = False
    gl.right_labels = False
    gl.xlocator = mticker.FixedLocator([-126, -124, -122, -120, -118])
    gl.ylocator = mticker.FixedLocator([32, 34, 36, 38])
    gl.xlabel_style = {"size": 12, "color": style.INK}
    gl.ylabel_style = {"size": 12, "color": style.INK}

    # alongshore leg (grey, drawn under the lines)
    (x0, y0), (x1, y1) = ALONGSHORE
    ax.plot([x0, x1], [y0, y1], color=style.GRAY, lw=2.2, transform=proj,
            zorder=3, solid_capstyle="round")

    # the four cross-shore lines with a filled circle at the inshore end
    for name, (ins, off) in LINES.items():
        c = LINE_COLORS[name]
        ax.plot([ins[0], off[0]], [ins[1], off[1]], color=c, lw=2.8,
                transform=proj, zorder=4, solid_capstyle="round")
        ax.plot(ins[0], ins[1], "o", ms=7, color=c, mec="white", mew=0.8,
                transform=proj, zorder=6)

    # cities: small dark dots with labels on land
    for name, ((lon, lat), (dx, dy), ha) in CITIES.items():
        ax.plot(lon, lat, "o", ms=3.5, color=style.INK, transform=proj, zorder=7)
        ax.text(lon + dx, lat + dy, name, fontsize=CITY_FS, color=style.INK,
                ha=ha, va="center", transform=proj, zorder=8)

    # line labels: rotated along each line, just above its offshore half
    fig.canvas.draw()   # transforms need the final axes geometry
    for name, (ins, off) in LINES.items():
        ang = _text_angle(ax, off, ins)
        f = 0.72                       # fraction of the way to the offshore end
        lon = ins[0] + f * (off[0] - ins[0])
        lat = ins[1] + f * (off[1] - ins[1])
        ax.text(lon, lat + 0.22, f"Line {name}", fontsize=LABEL_FS,
                color=LINE_COLORS[name], rotation=ang,
                rotation_mode="anchor", ha="center", va="bottom",
                transform=proj, zorder=8)

    style.save(fig, OUT_DIR, "cugn_lines.png", SOURCE, SLIDE, sources_json=MANIFEST)


if __name__ == "__main__":
    main()
