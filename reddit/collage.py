"""r/dataisbeautiful collage for calendar-switch: 2400 x 3200 px, light background. Numbers from data/results.json.
Map labels sit on open sea (checked against Natural Earth land, buffered) or on the paper, with a halo; leader lines,
where needed, may not cross any other label."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "code"))
from figstyle import *
import matplotlib.patheffects as pe
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from shapely.geometry import shape as _shape, box as _box, Point as _Pt, LineString as _LS, Polygon as _Poly
from shapely.ops import unary_union, nearest_points
from shapely.prepared import prep as _prep

R = jload(f"{DATA}/results.json"); SITE = jload(f"{DATA}/site.json"); U, SUB = SITE["units"], SITE["sub"]
C, D, M, V, S = R["cal"], R["road"], R["metric"], R["vote"], R["source"]
BGc = "#F7F5F0"; SEAc = "#E6EDEF"
HALO = [pe.withStroke(linewidth=4, foreground=SEAc)]
HALOP = [pe.withStroke(linewidth=4, foreground=BGc)]
COLONIAL = {i for i, u in U.items() if u["cal"].get("status") == "colonial"}
fig = plt.figure(figsize=(12, 16.0), dpi=200, facecolor=BGc)
fig.text(.045, .985, "When did your country lose 11 days?", fontproperties=DISP, fontsize=42, color=FG, va="top")
fig.text(.045, .941, f"The year each country switched from the Julian to the Gregorian calendar, and the dates it dropped. Catholic Europe jumped\n"
         f"from 4 to 15 October 1582; Britain from 2 to 14 September 1752; Russia 13 days in 1918; Saudi Arabia's civil switch came in 2016.",
         fontproperties=SERP, fontsize=13.2, color=FG, va="top", linespacing=1.45)

# ---- main map
ax = fig.add_axes([0, .522, 1, .3735])
outline(ax, fc=SEAc, ec="#C9CDD0", lw=.8); world(ax, colour=colour_fn("cal", U), lw=.3, ec=BGc, sub=sub_colours("cal", SUB), hatch=COLONIAL)
ax.set_xlim(-17.1e6, 17.1e6); ax.set_ylim(-6.7e6, 10.1e6)
LAND_MARGIN = 60e3
_land = []
for f in jload(f"{GEO}/ne_50m_land.geojson")["features"]:
    g = _shape(f["geometry"]); gs = g.geoms if g.geom_type == "MultiPolygon" else [g]
    for q in gs:
        xy = np.array(q.exterior.coords); x, y = EE.transform(np.clip(xy[:, 0], -179.99, 179.99), np.clip(xy[:, 1], -89.9, 89.9))
        _land.append(_Poly(np.column_stack([x, y])).buffer(0))
LAND = unary_union(_land).buffer(LAND_MARGIN); LANDP = _prep(LAND)
fig.canvas.draw(); REN = fig.canvas.get_renderer()
PLACED, LINES = [], []


def tbox(t, a=ax):
    bb = t.get_window_extent(REN)
    (x0, y0), (x1, y1) = a.transData.inverted().transform([[bb.x0 - 5, bb.y0 - 4], [bb.x1 + 5, bb.y1 + 4]])
    return _box(x0, y0, x1, y1)


def bad(b):
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    if not _box(x0 + 1e5, y0 + 1e5, x1 - 1e5, y1 - 1e5).contains(b): return True
    return LANDP.intersects(b) or any(b.intersects(o) for _, _, o in PLACED) or any(b.intersects(l) for _, l in LINES)


def place(name, s, target, prefs, ha="center", col=FG, size=10, w="medium", lead_gap=3e5, maxr=35):
    """target (lon, lat); try each preferred (lon, lat) then rings around the first; keep the first clean spot."""
    t = ax.text(0, 0, s, ha=ha, va="center", fontsize=size, color=col, family=MONO, linespacing=1.2, zorder=10, path_effects=HALO, fontweight=w)
    lon0, lat0 = prefs[0]
    if lon0 == "xy":
        cands = prefs; lon0, lat0 = 0, 0
    else: cands = list(prefs) + [(lon0 + dx, lat0 + dy) for r in range(1, maxr + 1) for dx in range(-r, r + 1) for dy in range(-r, r + 1) if max(abs(dx), abs(dy)) == r]
    tx, ty = proj(*target); c = _Pt(float(tx), float(ty))
    for lon, lat in cands:
        if lon == "xy": x, y = lat
        elif abs(lat) > 90: continue
        else: x, y = proj(((lon + 180) % 360) - 180, lat)
        t.set_position((float(x), float(y))); b = tbox(t)
        if bad(b): continue
        ln = None
        if b.distance(c) > lead_gap:
            pb, _ = nearest_points(b, c); ln = _LS([(pb.x, pb.y), (c.x, c.y)])
            if any(ln.intersects(o) for _, _, o in PLACED): continue
        PLACED.append((name, t, b))
        if ln is not None:
            LINES.append((name, ln)); ax.plot(*ln.xy, color=FG, lw=.8, zorder=9); ax.plot([c.x], [c.y], "o", ms=3.2, color=FG, zorder=9)
        return
    raise RuntimeError("no clean spot for " + name)


place("uk", "1752: Britain\nand colonies,\n11 days", (-2, 53), [(-33, 54)], size=9)
place("iberia", "1582: Catholic\nEurope and its\ncolonies,\n10 days", (-4, 40), [(-30, 33)], size=9)
place("sweden", "Sweden: 30 Feb 1712,\nthen 1753, 11 days", (15, 62), [("xy", (x * 1e5, y * 1e5)) for y in (95, 94, 93, 92) for x in range(-10, 30, 2)], size=8.5)
place("russia", "Russia: 1918,\n13 days", (45, 58), [("xy", (x * 1e5, y * 1e5)) for y in (95, 94, 93, 92) for x in range(50, 110, 2)], size=9)
place("greece", "Greece: 1923", (22, 39), [(20, 34)], size=8.5)
place("japan", "Japan: 1873", (138, 36), [(155, 30)], size=9)
place("china", "China: 1912", (112, 30), [(128, 18)], size=9)
place("saudi", "Saudi Arabia:\n2016", (45, 24), [(64, 12)], size=9)
place("never", "Never adopted:\nEthiopia, Iran,\nAfghanistan, Nepal", (40, 9), [(62, -8)], size=9, col="#2B2F35")
place("alaska", "Alaska: 1867,\nbought from Russia", (-150, 63), [(-160, 47)], size=9)
for nm, t, b in PLACED:
    assert not LANDP.intersects(b), nm
    assert not any(b.intersects(o) for n2, _, o in PLACED if n2 != nm), nm
for nm, l in LINES:
    assert not any(l.intersects(o) for n2, _, o in PLACED if n2 != nm), nm
print("labels ok:", len(PLACED), "leaders:", [n for n, _ in LINES])

# ---- legend (full) under the map
e, labs, cs = RAMP["cal"]
LEG = [Patch(facecolor=c, label=l) for c, l in zip(cs, labs)] + [Patch(facecolor=UNDATED, label="In use today, no date in the sources"),
       Patch(facecolor=NEVER, label="Not adopted"), Patch(facecolor="none", edgecolor=FG, ls=(0, (2.5, 1.6)), label="Year taken from the colonial power")]
LP = SERP.copy(); LP.set_size(11)
fig.legend(handles=LEG, loc="upper left", bbox_to_anchor=(.035, .528), ncol=5, frameon=False, prop=LP, handletextpad=.5, columnspacing=1.3, labelspacing=.5)

# ---- three small maps
SM = [("road", "Driving side today", None), ("metric", "When metrication started", None), ("vote", "When women first voted nationally", None)]
def road_col(iso):
    u = U.get(iso)
    if not u or not u["road"].get("now"): return UNDATED
    return {"L": LEFTC, "R": ROADC}.get(u["road"]["now"], MIXC)
for j, (k, title, _) in enumerate(SM):
    a = fig.add_axes([.02 + j * .33, .362, .31, .11])
    outline(a, fc=SEAc, ec="#C9CDD0", lw=.5); world(a, colour=road_col if k == "road" else colour_fn(k, U), lw=.15, ec=BGc, sub=None if k == "road" else sub_colours(k, SUB))
    a.set_xlim(-17.1e6, 17.1e6); a.set_ylim(-6.7e6, 8.75e6)
    fig.text(.025 + j * .33, .477, title, fontsize=11.5, color=FG, fontweight="medium")
    if k == "road":
        hs = [Patch(facecolor=ROADC, label=f"Right: {D['n_R']} countries"), Patch(facecolor=LEFTC, label=f"Left: {D['n_L']}, {D['pop_L']:.0f}% of people")]
        txt = f"{D['n_switched']} dated switches, {D['n_to_L']} to the left.\nSweden: Dagen H, 3 September 1967.\nSamoa moved left in 2009."
    else:
        e, labs, cs = RAMP[k]
        hs = [Patch(facecolor=c, label=l) for c, l in zip(cs, labs)] + [Patch(facecolor=UNDATED if k == "metric" else NEVER, label="Not in the table" if k == "metric" else "No elections")]
        txt = (f"France first, 1795; {M['last'][0][0]} last, {M['last'][0][1]}.\nUK began 1965, US made it legal 1866:\nboth still use other units." if k == "metric"
               else f"New Zealand first, 1893; Saudi Arabia\nlast, 2015 (municipal). UK: 1918 with\nrestrictions, equal terms 1928.")
    leg = fig.legend(handles=hs, loc="upper left", bbox_to_anchor=(.02 + j * .33, .358), ncol=2, frameon=False, fontsize=8.2, handlelength=1.1, handletextpad=.4, columnspacing=.8, labelspacing=.35)
    fig.text(.025 + j * .33, .296, txt, fontsize=8.8, color=FG, va="top", linespacing=1.45, family=MONO)

# ---- curves
a = fig.add_axes([.075, .085, .68, .14]); a.set_facecolor(BGc)
YRS = np.arange(R["meta"]["y0"], R["meta"]["now"] + 1); NC = S["n_countries"]
CV = [("cal", "Gregorian calendar", CALC, 31), ("road", "Driving on the right", ROADC, None), ("metric", "Metrication started", METC, 45), ("vote", "Women vote nationally", VOTEC, None)]
for k, nm, c, ly in CV:
    v = 100 * np.array(R["curves"][k]["n"]) / NC; a.plot(YRS, v, color=c, lw=2.2)
    a.text(2034, ly if ly is not None else v[-1], f"{nm}: {R['curves'][k]['n'][-1]}", color=c, fontsize=9.5, va="center", fontweight="medium", path_effects=HALOP)
a.set_xlim(1580, 2026); a.set_ylim(0, 102); spines(a); a.tick_params(labelsize=9); a.grid(axis="y", color=RULE, lw=.8); a.set_axisbelow(True)
a.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
a.set_title(f"Share of today's {NC} countries that had made each switch", family=MONO, fontsize=12, color=FG, loc="left", pad=8)

fig.text(.045, .006, f"Source: English Wikipedia (CC BY-SA 4.0), 2026 revisions: 'Gregorian calendar' and 'Julian calendar' adoption tables, 'Adoption of the Gregorian calendar',\n"
         f"'Left- and right-hand traffic', 'Metrication', 'Women's suffrage', 'List of adoption dates of the Gregorian calendar by country'. Outlines: Natural Earth.\n"
         f"Calendar colour: the year the whole of today's country had switched (France 1760, when Lorraine followed). Dates exist for {C['n_with_year']} countries (calendar), {M['n_dated']} (metric);\n"
         "most others use both today with no year in the tables. Analysis and chart: Tristan Hotham, Python and matplotlib  ·  maps.tristanhotham.com/calendar-switch",
         family=MONO, fontsize=8, color=MUT, linespacing=1.5, va="bottom")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lost_days_collage.png")
fig.savefig(out, facecolor=BGc, dpi=200)
print("ok", out)
