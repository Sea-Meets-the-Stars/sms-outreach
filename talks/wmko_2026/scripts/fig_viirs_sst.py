"""Created by JXP and Claude.

Global sea-surface-temperature map for the slide "Ocean satellites:
temperature" (WMKO 2026 public lecture, Sea meets the stars).

Data: NOAA Geo-Polar Blended SST analysis (Level 4, gap-free, 5 km,
day+night), ERDDAP dataset ``noaacwBLENDEDsstDNDaily`` on NOAA CoastWatch.
Its polar-orbiter input is VIIRS on NOAA-20 and NOAA-21 (plus AVHRR on
Metop-B/C and the geostationary imagers GOES ABI, Himawari AHI and
Meteosat SEVIRI), so it is a VIIRS-based product, not pure VIIRS.  One day
of ``analysed_sst`` is fetched with an ERDDAP stride of 2 (0.1 deg,
1800 x 3600 points, ~25 MB) and cached as netCDF under ~/data/SST/VIIRS/;
later runs read the cache.

The figure is a Pacific-centred Robinson map (Hawai'i near the middle),
charcoal land, a thermal-style sequential colormap and a slim vertical
colour bar in degrees C.  No in-figure title (the slide title does that).

Run from the repo root (conda run does not pass stdin; the script writes
the PNG and updates figures/sources.json, or the manifest named by the
SOURCES_JSON environment variable):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_viirs_sst.py

Output: talks/wmko_2026/figures/viirs_sst.png
"""
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import requests
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patheffects import withStroke
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from sms_outreach.slides import style
from sms_outreach.slides.style import INK, MUTED

FIGS = Path(__file__).resolve().parents[1] / "figures"
CACHE = Path.home() / "data" / "SST" / "VIIRS"

ERDDAP = "https://coastwatch.noaa.gov/erddap/griddap"
DATASET = "noaacwBLENDEDsstDNDaily"
DATE = "2026-10-04"            # latest day available when the figure was made
STRIDE = 2                     # native grid is 0.05 deg; 2 -> 0.1 deg
RETRIES = 3                    # download attempts (server 502s are transient)
SOURCE = ("NOAA Geo-Polar Blended SST analysis (L4, 5 km; VIIRS NOAA-20/21 "
          "+ AVHRR + geostationary), NOAA CoastWatch ERDDAP "
          f"{DATASET}, {DATE}")

CENTRAL_LON = 180.0            # Pacific-centred: Hawai'i near the middle
HAWAII = (-155.5, 19.6)        # lon, lat of the Island of Hawai'i
LAND = "#3d3d3d"               # charcoal land
VMIN, VMAX = -2.0, 32.0        # colour range, deg C

# Thermal-style sequential colormap (cmocean 'thermal' is not installed):
# lightness rises monotonically from near-black navy through violet,
# magenta and orange to pale yellow, so warm = bright, cold = dark.
THERMAL_STOPS = ["#032333", "#0d3a6b", "#3b3f98", "#6b3f9c", "#9a3d8b",
                 "#c54372", "#e45a52", "#f58034", "#fbad2a", "#f6d94f",
                 "#e9fa5b"]


def thermal_cmap():
    """Created by JXP and Claude. Build the thermal-like colormap from the
    stops above (evenly spaced, linearly interpolated in RGB)."""
    return LinearSegmentedColormap.from_list("sms_thermal", THERMAL_STOPS,
                                             N=256)


def layout(fig, proj, height_frac=0.97, gap_in=0.22, bar_in=0.16,
           label_in=0.62):
    """Created by JXP and Claude. Axes rectangles (figure fractions) for a
    full-globe map plus a colour bar hugging its right edge, the pair
    centred in the figure.  The map axes is sized to the projection's
    aspect so the globe fills it exactly."""
    fig_w, fig_h = fig.get_size_inches()
    x0, x1 = proj.x_limits
    y0, y1 = proj.y_limits
    map_h = height_frac * fig_h
    map_w = map_h * (x1 - x0) / (y1 - y0)
    group_w = map_w + gap_in + bar_in + label_in
    left = 0.5 * (fig_w - group_w)
    map_rect = [left / fig_w, 0.5 * (1 - height_frac), map_w / fig_w,
                height_frac]
    bar_rect = [(left + map_w + gap_in) / fig_w, 0.12, bar_in / fig_w, 0.76]
    return map_rect, bar_rect


def cache_path():
    """Created by JXP and Claude. Path of the cached netCDF subset."""
    deg = 0.05 * STRIDE
    return CACHE / f"geopolar_blended_dn_{DATE}_{deg:.2f}deg.nc"


def fetch_sst():
    """Created by JXP and Claude. Return (lon, lat, sst) for DATE, downloading
    the ERDDAP subset to the cache the first time.

    sst is a 2-D float array in deg C with NaN over land; lon is -180..180.
    """
    path = cache_path()
    if not path.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        query = (f"analysed_sst[({DATE}T12:00:00Z)]"
                 f"[(-89.975):{STRIDE}:(89.975)]"
                 f"[(-179.975):{STRIDE}:(179.975)]")
        url = f"{ERDDAP}/{DATASET}.nc?{query}"
        print(f"downloading {url}")
        tmp = path.with_suffix(".part")
        for attempt in range(1, RETRIES + 1):      # ERDDAP gives transient 502s
            try:
                with requests.get(url, stream=True, timeout=600) as r:
                    r.raise_for_status()
                    with open(tmp, "wb") as f:
                        for chunk in r.iter_content(chunk_size=1 << 20):
                            f.write(chunk)
                break
            except requests.exceptions.HTTPError as err:
                if attempt == RETRIES:
                    raise
                print(f"  attempt {attempt} failed ({err}); retrying")
                time.sleep(15 * attempt)
        tmp.rename(path)
        print(f"cached {path} ({path.stat().st_size / 1e6:.1f} MB)")
    ds = xr.open_dataset(path)
    sst = ds["analysed_sst"].squeeze().values.astype(float)
    sst[sst < -300] = np.nan                     # ERDDAP fill value
    lon = ds["longitude"].values
    lat = ds["latitude"].values
    ds.close()
    print(f"SST {DATE}: {np.nanmin(sst):.1f} to {np.nanmax(sst):.1f} degC, "
          f"grid {sst.shape}")
    return lon, lat, sst


def pacific_order(lon, sst):
    """Created by JXP and Claude. Roll the longitude axis so it runs 0..360,
    which keeps every grid cell away from the seam of a map centred on
    180 deg (no wrapped polygons in pcolormesh)."""
    lon360 = np.where(lon < 0, lon + 360, lon)
    order = np.argsort(lon360)
    return lon360[order], sst[:, order]


def draw_map(ax, lon, lat, sst):
    """Created by JXP and Claude. SST image, land, globe outline and the
    Hawai'i marker on a Robinson axes."""
    pc = ccrs.PlateCarree()
    # Globe background in the land colour: missing cells (ice shelves, lakes
    # the two land masks disagree on) then show as land, not white holes.
    ax.set_facecolor(LAND)
    lon360, sst360 = pacific_order(lon, sst)
    mesh = ax.pcolormesh(lon360, lat, sst360, transform=pc,
                         cmap=thermal_cmap(), vmin=VMIN, vmax=VMAX,
                         shading="nearest", rasterized=True, zorder=1)
    ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor=LAND,
                   edgecolor="none", zorder=2)
    ax.spines["geo"].set_edgecolor("#999999")
    ax.spines["geo"].set_linewidth(0.8)
    ax.set_global()

    # Hawai'i: small white ring with a label, so the audience finds home.
    ax.plot(*HAWAII, "o", transform=pc, ms=9, mfc="none", mec="white",
            mew=1.8, zorder=4)
    ax.text(HAWAII[0] + 4.0, HAWAII[1] + 3.0, "Hawaiʻi", transform=pc,
            fontsize=16, color="white", ha="left", va="bottom", zorder=4,
            path_effects=[withStroke(linewidth=3.0, foreground="#000000",
                                     alpha=0.65)])
    return mesh


def make_figure():
    """Created by JXP and Claude. Build and save the SST map."""
    style.apply_style()
    lon, lat, sst = fetch_sst()

    fig = plt.figure(figsize=style.FULL)
    proj = ccrs.Robinson(central_longitude=CENTRAL_LON)
    map_rect, bar_rect = layout(fig, proj)
    ax = fig.add_axes(map_rect, projection=proj)
    mesh = draw_map(ax, lon, lat, sst)

    cax = fig.add_axes(bar_rect)
    cb = fig.colorbar(mesh, cax=cax, orientation="vertical", extend="max")
    cb.set_ticks([0, 10, 20, 30])
    cb.ax.tick_params(labelsize=14, length=4, width=1, color=MUTED)
    cb.outline.set_edgecolor("#999999")
    cb.outline.set_linewidth(0.8)
    cax.set_title("°C", fontsize=16, color=INK, pad=8)
    ax.set_title("")

    return style.save(fig, FIGS, "viirs_sst.png", source=SOURCE,
                      slide="Ocean satellites: temperature",
                      sources_json=os.environ.get("SOURCES_JSON"))


if __name__ == "__main__":
    make_figure()
