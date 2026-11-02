"""Step 5. Header card, blog figures (release/blog/b_*.png, 1800 px wide) and paper figures (release/paper/f_*.png).
Numbers from data/results.json; colours and bins as on the page."""
import matplotlib.patheffects as pe
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from figstyle import *

R = jload(f"{DATA}/results.json")
SITE = jload(f"{DATA}/site.json")
U, SUB = SITE["units"], SITE["sub"]
BL = os.path.join(ROOT, "release", "blog"); PA = os.path.join(ROOT, "release", "paper")
os.makedirs(BL, exist_ok=True); os.makedirs(PA, exist_ok=True)
HALO = [pe.withStroke(linewidth=3.2, foreground=BG)]
COLONIAL = {i for i, u in U.items() if u["cal"].get("status") == "colonial"}
C, D, M, V = R["cal"], R["road"], R["metric"], R["vote"]
YRS = np.arange(R["meta"]["y0"], R["meta"]["now"] + 1)
NC = R["source"]["n_countries"]


def both(fig, name, blog=True):
    fig.savefig(os.path.join(PA, "f_" + name + ".png"), dpi=200, facecolor=fig.get_facecolor())
    if blog:
        fig.savefig(os.path.join(BL, "b_" + name + ".png"), dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def mapfig(k, title, handles, ncol=4, sub=True, hatch=None, colour=None, note=None):
    fig = plt.figure(figsize=(12, 6.6), facecolor=BG); ax = fig.add_axes([.01, .1, .98, .8])
    outline(ax, fc=SEA, ec="#C9CDD0"); world(ax, colour=colour or colour_fn(k, U), ec="#FFFFFF", sub=sub_colours(k, SUB) if sub else None, hatch=hatch)
    ax.set_ylim(WORLD_EXT[2], WORLD_EXT[3])
    fig.text(.02, .965, title, fontsize=12, color=FG, va="top")
    fig.legend(handles=handles, loc="lower center", ncol=ncol, frameon=False, fontsize=9.5, bbox_to_anchor=(.5, .005), handlelength=1.4, columnspacing=1.3)
    if note: fig.text(.98, .935, note, fontsize=8.5, color=MUT, ha="right", va="top")
    return fig, ax


sq = lambda c, l, **kw: Patch(facecolor=c, edgecolor="#9C978C" if c in (NOTYET, "#FFFFFF") else c, label=l, **kw)
# ---------- calendar map ----------
e, labs, cs = RAMP["cal"]
H = [sq(c, l) for c, l in zip(cs, labs)] + [sq(UNDATED, "Gregorian today, no date in the sources"), sq(NEVER, "Not adopted"),
                                           Patch(facecolor="none", edgecolor=FG, ls=(0, (2.5, 1.6)), label="Year taken from the colonial power")]
fig, ax = mapfig("cal", "The year each country's civil calendar became Gregorian, with regional detail where the sources give it", H, ncol=5, hatch=COLONIAL)
both(fig, "cal_map")

# ---------- adoption curves ----------
CV = [("cal", "Gregorian calendar", CALC), ("road", "Driving on the right", ROADC), ("metric", "Metrication started", METC), ("vote", "Women can vote nationally", VOTEC)]
fig = plt.figure(figsize=(12, 6.2), facecolor=BG); ax = fig.add_axes([.065, .1, .73, .8]); ax.set_facecolor(BG)
for k, nm, c in CV:
    v = 100 * np.array(R["curves"][k]["n"]) / NC
    ax.plot(YRS, v, color=c, lw=2.6, solid_joinstyle="round")
    ax.text(2030, {"cal": 31, "road": v[-1], "metric": 45, "vote": v[-1]}[k], f"{nm}\n{R['curves'][k]['n'][-1]} countries", color=c, fontsize=10, va="center", fontweight="medium")
for y, t, yy in ((1582, "1582: Catholic Europe\nand its colonies", 22), (1752, "1752: Britain\nand its colonies", 30), (1918, "1918: Russia", 70), (1967, "1967: Dagen H", 48)):
    ax.axvline(y, color=RULE, lw=1, zorder=0); ax.text(y + 3, yy, t, fontsize=9, color=MUT, va="bottom")
ax.set_xlim(1580, 2026); ax.set_ylim(0, 102); spines(ax); ax.grid(axis="y", color=RULE, lw=.8); ax.set_axisbelow(True)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%")); ax.set_ylabel(f"share of today's {NC} countries")
fig.text(.065, .955, "How fast the world switched: share of today's countries that had made each switch", fontsize=12, color=FG)
fig.text(.065, .015, f"Calendar and metric lines count only the countries the sources date ({C['n_with_year']} and {M['n_dated']}); most others use both today without a date in the tables.", fontsize=8.8, color=MUT)
both(fig, "curves")

# ---------- days dropped ----------
G = [("10 days", C["days_lists"]["10"]), ("11 days", C["days_lists"]["11"]), ("12 days", C["days_lists"]["12"]), ("13 days", C["days_lists"]["13"]),
     ("Other calendar", [x[0] for x in C["nonjulian"]])]
fig = plt.figure(figsize=(12, 8.4), facecolor=BG); ax = fig.add_axes([.14, .03, .83, .87]); ax.set_facecolor(BG)
GAP = 2.5
for j, (l, L) in enumerate(G):
    y = (len(G) - 1 - j) * GAP
    ax.barh([y + .55], [len(L)], height=.6, color=CALC if j < 4 else "#9C978C", alpha=.55 + .1 * j if j < 4 else .6)
    ax.text(len(L) + .4, y + .55, str(len(L)), va="center", fontsize=11, fontweight="medium")
    lines, cur = [], ""
    for w in L:
        if len(cur) + len(w) > 112: lines.append(cur.rstrip(", ")); cur = ""
        cur += w + ", "
    lines.append(cur.rstrip(", "))
    ax.text(0, y + .1, "\n".join(lines), fontsize=7.8, color=MUT, va="top", linespacing=1.35)
ax.set_yticks([(len(G) - 1 - j) * GAP + .55 for j in range(len(G))]); ax.set_yticklabels([g[0] for g in G], fontsize=11)
ax.set_xlim(0, max(len(L) for _, L in G) + 5); ax.set_ylim(-1.0, (len(G) - 1) * GAP + 1.0); spines(ax); ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0); ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
fig.text(.02, .96, "How many dates were left out when today's countries switched calendar", fontsize=12, color=FG)
fig.text(.02, .935, f"A country appears in more than one row when its regions switched in different centuries ({C['n_multi_days']} do). Other calendar: moved from a lunisolar, lunar or other calendar.", fontsize=9, color=MUT)
both(fig, "days")

# ---------- driving side map ----------
def road_col(iso):
    u = U.get(iso)
    if not u or not u["road"].get("now"): return UNDATED
    e = u["road"]; sw = bool(e.get("tl"))
    if e["now"] == "R": return ROADC if sw else tint(ROADC, .55)
    if e["now"] == "L": return "#B5651D" if sw else tint(LEFTC, .35)
    return MIXC
H = [sq(ROADC, "Right, switched at a date in the table"), sq(tint(ROADC, .55), "Right, no switch dated"), sq("#B5651D", "Left, switched to the left"), sq(tint(LEFTC, .35), "Left, no switch dated")]
fig, ax = mapfig("road", f"Which side of the road today: {D['n_R']} countries drive on the right, {D['n_L']} on the left", H, ncol=4, colour=road_col, sub=False)
for nm, lon, lat, dx, dy, ha in (("Sweden 1967", 16, 62, 1.6e6, 1.25e6, "left"), ("Iceland 1968", -19, 65, -1.3e6, -1.1e6, "right"), ("Samoa 2009\n(to the left)", -172, -14, 0.35e6, -0.95e6, "left"),
                                 ("Timor-Leste 1976\n(back to the left)", 126, -9, -2.6e6, -1.9e6, "right"), ("Nigeria 1972", 8, 9, -2.6e6, -1.35e6, "center"), ("Ghana 1974", -1, 8, -1.9e6, -0.35e6, "right"),
                                 ("Myanmar 1970", 96, 21, 3.4e6, 1.25e6, "left"), ("Namibia 1920\n(to the left)", 17, -22, -2.6e6, -0.6e6, "right")):
    x, y = proj(lon, lat); x, y = float(x), float(y)
    ax.annotate(nm, (x, y), (x + dx, y + dy), fontsize=9, color=FG, ha=ha, va="center", path_effects=HALO, zorder=9,
                arrowprops=dict(arrowstyle="-", color=FG, lw=.6, shrinkA=2, shrinkB=2))
both(fig, "road_map")

# ---------- switches dot strip ----------
S = D["switches"]
fig = plt.figure(figsize=(12, 4.8), facecolor=BG); ax = fig.add_axes([.03, .17, .94, .68]); ax.set_facecolor(BG)
stack = {}
for n, y, s in S:
    k = y // 2; stack[k] = stack.get(k, 0) + 1; yy = stack[k]
    q = U[next(i for i, u in U.items() if u["n"] == n)]["road"].get("q")
    c = LEFTC if s == "L" else ROADC
    ax.scatter([k * 2 + 1], [yy], s=58, c="none" if q else c, edgecolors=c, linewidths=1.5, zorder=3)
for n, y, ha in (("Andorra 1724", 1724, "center"), ("France 1792", 1792, "center"), ("Finland 1858", 1858, "center"), ("Netherlands 1906", 1906, "right"),
                 ("Portugal and its\ncolonies, 1928", 1928, "right"), ("China, the Koreas,\nthe Philippines, 1946", 1946, "left"), ("Sweden 1967", 1967, "center"), ("Samoa 2009", 2009, "center")):
    ax.text(y // 2 * 2 + 1 + {"right": 1.5, "left": -1.5, "center": 0}[ha], stack[y // 2] + .8, n, fontsize=9, ha=ha, va="bottom", color=FG, path_effects=HALO)
MX = max(stack.values())
ax.set_xlim(1715, 2015); ax.set_ylim(0, MX + 3); ax.set_yticks([]); spines(ax); ax.spines["left"].set_visible(False)
ax.set_xticks(range(1720, 2020, 20))
fig.text(.03, .93, f"Every dated change of driving side in the table: {D['n_to_R']} to the right, {D['n_to_L']} to the left", fontsize=12, color=FG)
fig.legend(handles=[Line2D([], [], ls="", marker="o", ms=8, mfc=ROADC, mec=ROADC, label="to the right"), Line2D([], [], ls="", marker="o", ms=8, mfc=LEFTC, mec=LEFTC, label="to the left"),
                    Line2D([], [], ls="", marker="o", ms=8, mfc="none", mec=ROADC, label="date given, change not described")], loc="lower center", ncol=3, frameon=False, fontsize=9.5, bbox_to_anchor=(.5, .0))
both(fig, "road_switches")

# ---------- metric map ----------
e, labs, cs = RAMP["metric"]
MIXED = {i for i, u in U.items() if u["metric"].get("mixed") and u["metric"].get("src") == "MTT"}
H = [sq(c, l) for c, l in zip(cs, labs)] + [sq(UNDATED, "Not in the table"), Patch(facecolor="none", edgecolor=FG, ls=(0, (2.5, 1.6)), label="Non-metric units still official")]
fig, ax = mapfig("metric", "The year each country's official metrication process started, according to the table", H, ncol=4, hatch=MIXED)
both(fig, "metric_map")

# ---------- votes map ----------
e, labs, cs = RAMP["vote"]
H = [sq(c, l) for c, l in zip(cs, labs)] + [sq(NEVER, "No elections")]
fig, ax = mapfig("vote", "The year women could first vote in national elections (state and provincial votes shown where the table gives them)", H, ncol=4)
both(fig, "vote_map")

# ---------- first and equal votes ----------
T2 = V["two"]
fig = plt.figure(figsize=(12, 6.2), facecolor=BG); ax = fig.add_axes([.2, .08, .77, .82]); ax.set_facecolor(BG)
for j, (n, a, b) in enumerate(T2):
    y = len(T2) - 1 - j
    ax.plot([a, b], [y, y], color=VOTEC, lw=2.2, alpha=.45, zorder=2)
    ax.scatter([a], [y], s=46, c="white", edgecolors=VOTEC, linewidths=1.8, zorder=3); ax.scatter([b], [y], s=52, c=VOTEC, zorder=3)
    ax.text(b + 1.2, y, f"{b - a} yrs", fontsize=8.5, color=MUT, va="center")
ax.set_yticks(range(len(T2))); ax.set_yticklabels([t[0] for t in T2][::-1], fontsize=10); ax.tick_params(axis="y", length=0)
ax.set_xlim(1895, 2003); spines(ax); ax.spines["left"].set_visible(False); ax.grid(axis="x", color=RULE, lw=.8); ax.set_axisbelow(True)
fig.text(.02, .955, f"The {V['n_two']} countries where the table gives a restricted first vote for women and a later year of full or equal terms", fontsize=12, color=FG)
fig.legend(handles=[Line2D([], [], ls="", marker="o", ms=8, mfc="white", mec=VOTEC, label="first vote, with restrictions"), Line2D([], [], ls="", marker="o", ms=8, mfc=VOTEC, mec=VOTEC, label="full or equal terms")],
           loc="upper right", ncol=2, frameon=False, fontsize=9.5, bbox_to_anchor=(.98, .99))
both(fig, "vote_two")

# ---------- header card 1200 x 630 ----------
fig = plt.figure(figsize=(12, 6.3), dpi=100, facecolor=BG)
ax = fig.add_axes([.43, .2, .57, .72]); outline(ax, fc=SEA, ec="#C9CDD0", lw=.6); world(ax, colour=colour_fn("cal", U), lw=.2, ec=BG, sub=sub_colours("cal", SUB)); ax.set_ylim(WORLD_EXT[2], WORLD_EXT[3])
a2 = fig.add_axes([.47, .06, .5, .14]); a2.set_facecolor(BG)
for k, nm, c in CV:
    a2.plot(YRS, 100 * np.array(R["curves"][k]["n"]) / NC, color=c, lw=1.8)
a2.set_xlim(1580, 2026); a2.set_ylim(0, 100); a2.set_yticks([]); spines(a2); a2.spines["left"].set_visible(False); a2.tick_params(labelsize=8)
fig.text(.04, .9, "When did", fontproperties=DISP, fontsize=44, color=FG, va="top")
fig.text(.04, .76, "your country", fontproperties=DISP, fontsize=44, color=FG, va="top")
fig.text(.04, .62, "lose 11 days?", fontproperties=DISP, fontsize=44, color=CALC, va="top")
fig.text(.04, .44, "The calendar, the side of the road,\nthe metric system and votes for women:\nfour great switches, country by country,\n1582 to 2026.", fontproperties=SERP, fontsize=14.5, color=FG, va="top", linespacing=1.35)
fig.text(.04, .04, "maps.tristanhotham.com/calendar-switch", fontsize=11, color=MUT)
fig.savefig(os.path.join(ROOT, "header.png"), dpi=100, facecolor=BG)
plt.close(fig)
print("figures done", sorted(os.listdir(BL)), sorted(x for x in os.listdir(PA) if x.endswith(".png")))
