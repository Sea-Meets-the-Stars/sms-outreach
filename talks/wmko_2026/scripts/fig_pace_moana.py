"""Created by JXP and Claude.

Figure for the slide "Ocean satellites: color" (WMKO 2026 public lecture,
Sea meets the stars): who lives where in the ocean, as seen by NASA's PACE
satellite.

PACE's OCI instrument measures the colour of the sea in hundreds of
wavelengths; the MOANA algorithm (Lange et al. 2020) turns that spectrum
into cell counts for three groups of picophytoplankton.  The figure shows
two of them side by side, as large as the slide allows, on a log colour
scale for one day (1 July 2025) over the Atlantic -- the region held by
the local data file:

    Synechococcus    -- a slightly larger cyanobacterium, cooler water
    Picoeukaryotes   -- small algae with a nucleus, nutrient-rich water

(Prochlorococcus, the tiniest and most numerous group, is left out so that
each map is bigger and easier to read from the back of the room.)  The
figure uses the taller slide size (style.FULL_TALL, no sub-line), each
panel has a one-line "Name: tagline" heading, and the latitude range is
trimmed to -45..60 so the maps take nearly the full figure height.

Land is charcoal; grey is "no data" on that day (clouds, between orbits).
The data file stores land as the fill value 254 cells/mL in all fields;
it is masked before plotting.

Run from the repo root (conda run does not pass stdin; the script writes
the PNG and updates figures/sources.json, or the manifest named by the
SOURCES_JSON environment variable):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_pace_moana.py

Input : /Users/xavier/data/Color/PACE/PACE_OCI.20250701.L4m.DAY.MOANA.V3_2.0p1deg.nc
Output: talks/wmko_2026/figures/pace_moana.png
"""
import os
import sys
import warnings
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.offsetbox import AnnotationBbox, HPacker, TextArea
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from sms_outreach.slides import style
from sms_outreach.slides.style import INK, MUTED

FIGS = Path(__file__).resolve().parents[1] / "figures"
DATA = Path("/Users/xavier/data/Color/PACE/"
            "PACE_OCI.20250701.L4m.DAY.MOANA.V3_2.0p1deg.nc")

LAND_FILL = 254.0          # value the L4m file stores over land (all fields)
LAND = "#3a3a3a"           # charcoal land
GAP = "#d4d4d4"            # light grey: no data (clouds, between orbits)
CMAP = "viridis"
# lon0, lon1, lat0, lat1 shown (file: -85..25, -70..70).  The latitude range
# is trimmed to -45..60 so the map is nearly square and fills the height;
# each 5-degree band dropped holds ~3% of the day's valid pixels.
EXTENT = [-85, 25, -45, 60]
# Figure-fraction layout of the two map boxes (left edges, bottom, size).
# Each box is anchored at its left edge; the map keeps its aspect ratio, so
# the box height sets the map size and the colour bar + tick labels fall in
# the rest of the box.  The left edges centre map + colour bar in each half.
PANEL_X0 = (0.035, 0.535)
PANEL_Y0, PANEL_W, PANEL_H = 0.105, 0.46, 0.80
# Colour bar: gap from the map and width, as fractions of the map width;
# TITLE_X is the centre of map + colour bar + tick labels in axes fraction,
# so the one-line heading sits over the whole group.
CBAR_X0, CBAR_W = 1.035, 0.05
TITLE_X = 0.68

# (variable, display name, one-line tagline, colour-scale floor, ceiling)
GROUPS = [
    ("syncoccus_moana", "Synechococcus", "a bigger cyanobacterium", 1e2, 5e4),
    ("picoeuk_moana", "Picoeukaryotes", "small algae, richer waters", 1e2, 2e4),
]

SOURCE = ("NASA PACE OCI, MOANA picophytoplankton (Lange et al. 2020), "
          "L3 mapped daily, 1 July 2025 (NASA/GSFC/OBPG)")


def load_fields(path=DATA):
    """Created by JXP and Claude. Read the plotted MOANA abundance fields.

    Returns (lon, lat, fields) with fields a dict name -> 2-D array in
    cells/mL; land (fill value 254) and missing pixels are NaN.
    """
    ds = xr.open_dataset(path)
    fields = {}
    for var, *_ in GROUPS:
        a = ds[var].values.astype(float)
        a[a == LAND_FILL] = np.nan
        fields[var] = a
    return ds.lon.values, ds.lat.values, fields


def nice_ticks(lo, hi):
    """Created by JXP and Claude. Decade ticks within [lo, hi] with
    comma-separated labels (1,000 rather than 10^3) for a lay audience."""
    ticks = [10.0 ** k for k in range(int(np.ceil(np.log10(lo))),
                                     int(np.floor(np.log10(hi))) + 1)]
    return ticks, [f"{t:,.0f}" for t in ticks]


def draw_panel(ax, lon, lat, data, name, tagline, lo, hi):
    """Created by JXP and Claude. One group's map: log colour scale over
    [lo, hi] cells/mL, charcoal land, grey gaps, slim colour bar at right."""
    ax.set_extent(EXTENT, crs=ccrs.PlateCarree())
    ax.set_facecolor(GAP)
    im = ax.pcolormesh(lon, lat, np.clip(data, lo, hi),
                       transform=ccrs.PlateCarree(), shading="auto",
                       cmap=CMAP, norm=LogNorm(lo, hi), rasterized=True)
    ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor=LAND,
                   edgecolor="none", zorder=3)
    ax.spines["geo"].set_edgecolor("#9a9a9a")
    ax.spines["geo"].set_linewidth(0.8)
    # One-line heading, "Name: tagline", centred over map + colour bar so
    # the map can take the full height (two stacked lines cost ~0.5 in).
    heading = HPacker(children=[
        TextArea(name + ":", textprops=dict(fontsize=18, color=INK)),
        TextArea(tagline, textprops=dict(fontsize=15, color=MUTED)),
    ], align="baseline", pad=0, sep=5)
    ax.add_artist(AnnotationBbox(heading, (TITLE_X, 1.0), xycoords="axes fraction",
                                 box_alignment=(0.5, 0.0), frameon=False,
                                 pad=0.25))

    cax = ax.inset_axes([CBAR_X0, 0.0, CBAR_W, 1.0])
    cb = plt.colorbar(im, cax=cax, orientation="vertical")
    ticks, labels = nice_ticks(lo, hi)
    cb.set_ticks(ticks)
    cb.set_ticklabels(labels)
    cb.ax.tick_params(labelsize=15, length=3, pad=2)
    cb.ax.minorticks_off()
    cb.outline.set_linewidth(0.5)
    return im


def make_figure():
    """Created by JXP and Claude. Build and save the two-panel figure.

    Axes are placed by hand (style.save's tight_layout leaves add_axes
    axes alone); each map box is anchored at its left edge so the colour
    bar and labels fall in the gap before the next panel.
    """
    style.apply_style()
    plt.rcParams["axes.grid"] = False
    lon, lat, fields = load_fields()

    proj = ccrs.Robinson(central_longitude=0.5 * (EXTENT[0] + EXTENT[1]))
    fig = plt.figure(figsize=style.FULL_TALL)
    for x0, (var, name, tagline, lo, hi) in zip(PANEL_X0, GROUPS):
        ax = fig.add_axes([x0, PANEL_Y0, PANEL_W, PANEL_H], projection=proj,
                          anchor="W")
        draw_panel(ax, lon, lat, fields[var], name, tagline, lo, hi)

    fig.text(0.5, 0.008, "Cells per millilitre of seawater  \u00b7  "
             "grey = no data that day (clouds, between orbits)",
             ha="center", va="bottom", fontsize=15, color=MUTED)
    with warnings.catch_warnings():       # tight_layout ignores add_axes axes
        warnings.simplefilter("ignore", UserWarning)
        return style.save(fig, FIGS, "pace_moana.png", source=SOURCE,
                          slide="Ocean satellites: color",
                          sources_json=os.environ.get("SOURCES_JSON"))


if __name__ == "__main__":
    make_figure()
