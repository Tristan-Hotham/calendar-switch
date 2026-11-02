"""House style for static figures: fonts (static instances cut from the variable Fraunces in /home/claude/ref/fonts,
written to WORK), the palette, the ramps used on the page, and Natural Earth outlines in the Equal Earth projection."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Polygon as MPoly
import numpy as np
from pyproj import Transformer
from common import *

FD = os.path.join(WORK, "fonts"); os.makedirs(FD, exist_ok=True)
if not os.path.exists(f"{FD}/Fraunces-Black.ttf"):
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    for w, nm in ((900, "Black"), (700, "Bold")):
        instancer.instantiateVariableFont(TTFont(f"{FONTS}/FrauncesVar.ttf"), {"wght": w, "opsz": 144, "SOFT": 0, "WONK": 0}).save(f"{FD}/Fraunces-{nm}.ttf")
DISP = fm.FontProperties(fname=f"{FD}/Fraunces-Black.ttf")
DISPB = fm.FontProperties(fname=f"{FD}/Fraunces-Bold.ttf")
SERP = fm.FontProperties(fname=f"{FONTS}/SourceSerif4-Regular.ttf")
SERB = fm.FontProperties(fname=f"{FONTS}/SourceSerif4-Semibold.ttf")
for f in ("IBMPlexMono-Regular.ttf", "IBMPlexMono-Medium.ttf"):
    fm.fontManager.addfont(f"{FONTS}/{f}")
MONO = "IBM Plex Mono"
plt.rcParams.update({"font.family": MONO, "font.size": 12, "axes.edgecolor": "#636A72", "axes.labelcolor": "#1D2128",
                     "xtick.color": "#636A72", "ytick.color": "#636A72"})
BG, FG, MUT, RULE, SEA = "#F6F4EF", "#1D2128", "#636A72", "#DDD8CC", "#E3EAEC"
NOTYET, UNDATED, NEVER = "#F2EEE5", "#C9C4BA", "#4B5059"
CALC, ROADC, METC, VOTEC, LEFTC, MIXC, SWEC = "#B4432F", "#2F5FA7", "#2E8A6E", "#7A4FA0", "#D08A2E", "#9A8FB0", "#C9A227"
RAMP = {   # same bins and colours as the page
    "cal": ([1600, 1752, 1800, 1900, 1950], ["1582 to 1599", "1600 to 1751", "1752 to 1799", "1800s", "1900 to 1949", "1950 on"], ["#6E1F14", "#9A3322", "#C25A38", "#DB8B57", "#E9B47F", "#F3D7B4"]),
    "metric": ([1850, 1875, 1900, 1950, 1970], ["1795 to 1849", "1850 to 1874", "1875 to 1899", "1900 to 1949", "1950 to 1969", "1970 on"], ["#0F4D3B", "#1F6E55", "#2E8A6E", "#5AAE8D", "#91CDB3", "#C9E7D9"]),
    "vote": ([1915, 1930, 1945, 1960, 1980], ["1893 to 1914", "1915 to 1929", "1930 to 1944", "1945 to 1959", "1960 to 1979", "1980 on"], ["#2E1747", "#4F2B74", "#7A4FA0", "#9C7BC0", "#BFA6DA", "#E2D6EF"]),
}


def ramp(k, y):
    e, _, c = RAMP[k]
    return c[sum(y >= x for x in e)]


def tint(hex_, t):
    h = hex_.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#" + "".join(f"{round(v + (255 - v) * t):02x}" for v in (r, g, b))


EE = Transformer.from_crs(4326, 8857, always_xy=True)
W = jload(f"{DATA}/world.json")
SU = jload(f"{DATA}/subunits.json")


def rings(geom):
    cs = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in cs:
        yield np.array(poly[0])


def project_feats(F, key):
    out = []
    for f in F["features"]:
        for ring in rings(f["geometry"]):
            x, y = EE.transform(np.clip(ring[:, 0], -179.9, 179.9), np.clip(ring[:, 1], -89.5, 89.5))
            out.append((f["properties"][key], np.column_stack([x, y])))
    return out


SHAPES = project_feats(W, "iso")
SUBSHAPES = project_feats(SU, "code")
WORLD_EXT = (-17.1e6, 17.1e6, -6.7e6, 8.75e6)     # Antarctica is not drawn


def world(ax, colour=lambda iso: NOTYET, lw=.3, ext=WORLD_EXT, ec="#FFFFFF", z=1, sub=None, hatch=None):
    """Countries filled by colour(iso); sub: {code: colour} drawn on top; hatch: {iso: True} drawn with a dashed outline."""
    for iso, p in SHAPES:
        ax.add_patch(MPoly(p, closed=True, fc=colour(iso), ec=ec, lw=lw, zorder=z))
    if sub:
        for code, p in SUBSHAPES:
            if code in sub:
                ax.add_patch(MPoly(p, closed=True, fc=sub[code], ec=ec, lw=lw * .6, zorder=z + .1))
    if hatch:
        for iso, p in SHAPES:
            if iso in hatch:
                ax.add_patch(MPoly(p, closed=True, fc="none", ec=FG, lw=.7, ls=(0, (2.5, 1.6)), zorder=z + .2))
    ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_aspect("equal"); ax.axis("off")


def outline(ax, fc=None, lw=.8, ec=MUT, z=0):
    """Equal Earth globe outline."""
    lat = np.linspace(-90, 90, 181)
    xl, yl = EE.transform(np.full_like(lat, -180), lat); xr, yr = EE.transform(np.full_like(lat, 180), lat[::-1])
    ax.add_patch(MPoly(np.column_stack([np.r_[xl, xr], np.r_[yl, yr]]), closed=True, fc=fc or "none", ec=ec, lw=lw, zorder=z))


def proj(lon, lat):
    return EE.transform(np.asarray(lon), np.asarray(lat))


def spines(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def state_at(e, y):
    if not e or e.get("init") is None:
        return None
    s = e["init"]
    for yy, st in e.get("tl", []):
        if yy <= y:
            s = st
    return s


def colour_fn(k, U, y=NOW, measure="first"):
    """Colour of a unit for switch k in year y, as on the page (at full strength)."""
    def f(iso):
        u = U.get(iso)
        if not u:
            return UNDATED
        e = u[k]
        if k == "road":
            s = state_at(e, y)
            return {"L": LEFTC, "R": ROADC, "M": MIXC}.get(s, UNDATED)
        s, st = state_at(e, y), e.get("status")
        if k == "cal":
            if st == "never": return NEVER
            if st == "undated": return UNDATED
            if s == "G": return ramp("cal", e["year"])
            if s == "P": return tint(ramp("cal", e["first"]), .55)
            if s == "S": return SWEC
            return NOTYET
        if k == "metric":
            if st in ("undated", "notmandatory"): return UNDATED
            if st == "transition": return tint(RAMP["metric"][2][5], .2)
            if s == "M": return ramp("metric", e["year"])
            if s == "P": return tint(ramp("metric", e["first"]), .55)
            return NOTYET
        if st == "novote": return NEVER
        if st == "undated": return UNDATED
        v = "N" if (measure == "full" and s == "P") else s
        if v in ("V", "E"): return ramp("vote", (e.get("equal") or e.get("first")) if measure == "full" else e.get("first"))
        if v == "P": return tint(ramp("vote", e["first"]), .5)
        return NOTYET
    return f


def sub_colours(k, SUB, y=NOW):
    out = {}
    for code, s in SUB.items():
        e = s.get(k)
        if not e or e.get("status") == "undated":
            continue
        e = dict(e, status="dated")
        if k == "road":
            out[code] = {"L": LEFTC, "R": ROADC, "M": MIXC}[state_at(e, y)]
        elif k == "cal":
            out[code] = ramp("cal", e["year"]) if state_at(e, y) == "G" else NOTYET
        elif k == "metric":
            out[code] = ramp("metric", e["year"]) if state_at(e, y) == "M" else NOTYET
        else:
            st = state_at(e, y); out[code] = ramp("vote", e["year"]) if st in ("V", "E") else NOTYET
    return out
