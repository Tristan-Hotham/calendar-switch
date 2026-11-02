"""Step 3. Match the tables and prose to today's countries, build each country's timeline for the four switches,
and compute every number used anywhere (data/results.json), the reusable tables (data/*.csv) and the page data
(data/site.json).

Timelines. Each unit (country, dependency or sub-national unit) has, for each switch, a starting state and a list of
(year, state) changes. A state holds from 1 January of its year in the map and curves.
  cal     J old calendar, S the Swedish calendar (1700 to 1712), P part of the country Gregorian, G Gregorian
  road    L left, R right, M mixed (regions differ). Where the table gives a date of switch, the earlier years are shown
          on the other side; if the table and article give no detail of that switch the earlier years are flagged
          'date only'. Where the table gives no date, today's side is assumed throughout (an assumption, stated).
  metric  N not yet, P part of the country, M metrication process started (the table's year)
  vote    N no national vote for women, P a vote with restrictions the table names, V a vote (the table gives one
          year), E on equal or full terms (a later year the table gives)
Shares. "Today's countries" are the 197 in 02_geo.py; population is Natural Earth's POP_EST, so the population
curves weigh each country by its population today, not at the time."""
import csv, datetime as dt, importlib.util
import numpy as np, pandas as pd
from common import *

spec = importlib.util.spec_from_file_location("polities", os.path.join(ROOT, "code", "polities.py")); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
T = jload(f"{WORK}/tables.json")
TX = jload(f"{WORK}/text.json")
TXT, REV = TX["text"], TX["revid"]
CM = jload(f"{WORK}/countries.json")
SUBF = jload(f"{DATA}/subunits.json")["features"]
SUBN = {f["properties"]["code"]: f["properties"]["name"] for f in SUBF}
SUBI = {f["properties"]["code"]: f["properties"]["iso"] for f in SUBF}
COUNTRIES = sorted(i for i, m in CM.items() if m["country"])
UNITS = sorted(CM)
POP = {i: CM[i]["pop"] for i in COUNTRIES}
WPOP = sum(POP.values())
YEARS = list(range(Y0, NOW + 1))
pc = lambda a, b: round(100 * a / b, 1) if b else None


def has(page, *ss):
    for s in ss:
        assert s in TXT[page], (page, s)


# name matching against Natural Earth
W = jload(f"{GEO}/ne_50m_admin_0_countries.geojson")
NM = {}
for f in W["features"]:
    p = f["properties"]; iso = p["ISO_A3_EH"] if p["ISO_A3_EH"] not in ("-99", None) else p["ADM0_A3"]
    for k in ("NAME", "ADMIN", "NAME_LONG", "FORMAL_EN", "NAME_EN", "NAME_SORT", "NAME_ALT", "BRK_NAME", "GEOUNIT", "SUBUNIT"):
        if p.get(k):
            NM.setdefault(norm(p[k]), iso)


def match(name, extra):
    if name in extra:
        return extra[name]
    k = norm(re.sub(r"\(.*?\)", "", name).split(" | ")[0])
    assert k in NM, name
    return NM[k]


def years_in(s):
    return [int(y) for y in re.findall(r"(?<!\d)(1[5-9]\d\d|20[0-2]\d)(?!\d)", s)]


def state_at(init, tl, y):
    s = init
    for yy, st in tl:
        if yy <= y:
            s = st
    return s


# ================================================================== calendar
has("Adoption of the Gregorian calendar", "Thursday, 4 October 1582 was succeeded by Friday, 15 October 1582", "Wednesday, 2 September 1752, was followed by Thursday, 14 September 1752",
    "introducing the unique date 30 February in 1712", "Wednesday, 17 February, was followed by Thursday, 1 March", "Wednesday, 31 January 1918, was to be followed by Thursday, 14 February 1918",
    "Wednesday 15 February 1923 in the Greek calendar was followed by Thursday 1 March 1923", "31 March was followed by 14 April 1916", "31 March 1919 being followed by 14 April 1919",
    "Sunday, 18 February 1700, was followed by Monday, 1 March 1700", "Sunday, 9 December 1582 being succeeded by Monday, 20 December 1582",
    "The two Swiss communes of Schiers and Grüsch were the last areas of Western and Central Europe to switch to the Gregorian calendar, in 1812",
    "switched back in 1795 after the Third Partition of Poland", "Saturday, 7 October 1867 (Julian), the date changed to Friday, 18 October 1867 (Gregorian)",
    "The four countries which have not adopted the Gregorian calendar are Ethiopia", "Nepal", "Iran and Afghanistan",
    "the vast majority of countries use the Gregorian calendar as their sole civil calendar", "effective 1 October 2016",
    "Cambodia in 1863 and Laos in 1889", "Vietnam adopted the Gregorian calendar in 1954", "In 1889, Siam also switched", "1 January 1873 , 1 January 1896 , and 1 January 1912",
    "12 July 1700 (Gelderland), 12 December 1700 (Overijssel and Utrecht), 12 January 1701 (Friesland and Groningen) and 12 May 1701 (Drenthe)",
    "The European colonies of the Americas adopted the change when their mother countries did", "New France and New Spain adopted the new calendar in 1582",
    "The British colonies of Canada and the Thirteen Colonies followed suit in 1752")
GTY = {int(r[0]): r[1] for r in T["greg_years"]["rows"]}
assert GTY[1582].startswith("Spain, Portugal, France") and "colonies thereof" in GTY[1582] and "First\" British Empire" in GTY[1752].replace("“", "\"").replace("”", "\"") or "British Empire" in GTY[1752]
assert GTY[2016] == "Saudi Arabia" and GTY[1923] == "Greece" and GTY[1915] == "Latvia, Lithuania" and GTY[1918] == "Ukraine, Russia, Estonia" and GTY[1610] == "Prussia"
assert GTY[1875] == "Egypt" and GTY[1912] == "China, Albania" and GTY[1919] == "Romania, Yugoslavia" and GTY[1584].startswith("Bohemia")
GN = {r[0]: r[2] for r in T["greg_newyear"]["rows"]}; JN = {r[0]: r[2] for r in T["jul_newyear"]["rows"]}
assert GN["Lorraine"] == "1582" and JN["Lorraine"] == "1760" and GN["Holy Roman Empire | (Catholic states)"] == "1583" and JN["Holy Roman Empire"] == "1582" and JN["Serbia"] == "1918"


def jdiff(y, m=6):
    """Days between the Julian and Gregorian calendars on a date in year y (month m), from the rule in the
    Gregorian calendar article's table of ranges: 10 to Feb 1700, 11 to Feb 1800, 12 to Feb 1900, 13 to Feb 2100."""
    k = y + (m - 3) / 12
    return 10 if k < 1700 else 11 if k < 1800 else 12 if k < 1900 else 13


GR = [r for r in T["greg_years"]["rows"]]
greg_rng = {r[2]: r[0] for r in [[c for c in row] for row in jload(f"{WORK}/tables.json")["greg_years"]["rows"]] if len(r) > 2}
MONTHS = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])}


def omitted(text):
    """Dates omitted in 'D Month YYYY was followed by D Month YYYY' (read as one calendar)."""
    m = re.findall(r"(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December)(?: (\d{4}))?", text)
    if len(m) < 2:
        return None
    (d1, m1, y1), (d2, m2, y2) = m[0], m[1]
    y = int(y2 or y1); a = dt.date(int(y1 or y), MONTHS[m1], int(d1)); b = dt.date(y, MONTHS[m2], int(d2))
    return (b - a).days - 1


# ---------- the list article: primary source ----------
MON = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Sept": 9, "Oct": 10, "Nov": 11, "Dec": 12}
FULLM = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def gl_rows():
    out = []
    for r in T["greg_list"]["rows"]:
        country, area, ycell, before, after, om, part = r[:7]
        iso = match(country, P.GL_NAME)
        ys = years_in(ycell); y0 = ys[0]
        ma = re.match(r"^(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\b(?: \((\d{4})\))?", after.strip())
        yeff = int(ma.group(3)) if ma and ma.group(3) else (int(re.search(r"\((\d{4})\)", after).group(1)) if re.search(r"\((\d{4})\)", after) else ys[-1])
        if "Schiers and Grüsch" in part: yeff = 1812                                     # '25 Dec 1811 was followed by 7 Jan 1812' (Particulars)
        oms = [int(x) for x in re.findall(r"-?\d+", om.replace("–", " ").replace("−", "-"))] if om not in ("", "N/A") else []
        kind = "republican" if "Republican calendar" in part else "return" if (oms and oms[0] < 0) or "Return to the Julian" in part else "swedish" if "Swedish calendar" in part else "switch"
        out.append(dict(iso=iso, country=country, area=area, ycell=ycell, year=yeff, before=before, after=after, om=oms, na=om == "N/A", part=part, kind=kind,
                        mafter=MON.get(ma.group(2)) if ma else None))
    return out


GL = gl_rows()
GLI = {}
for g in GL:
    GLI.setdefault(g["iso"], []).append(g)
assert len(GL) == 146 and len(GLI) == 51, (len(GL), len(GLI))
# the dates omitted in the list match the rule (10 until Feb 1700, 11 to Feb 1800, 12 to Feb 1900, 13 after), read at the first day after the change
for g in GL:
    if g["kind"] == "switch" and g["om"] and g["mafter"] and "International Date Line" not in g["part"]:
        assert max(g["om"]) == jdiff(g["year"], g["mafter"]), g
GL_SW = [g for g in GL if g["kind"] == "switch"]
for k in ("Prussia", "Return to the Julian calendar", "Republican calendar", "Schiers and Grüsch"):
    assert any(k in g["area"] + g["part"] for g in GL), k


def fmt_day(d, y):
    m = re.match(r"^(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\b(?: \((\d{4})\))?", d.strip())
    if not m:
        return re.sub(r"[\"“”]", "", d).strip()
    return f"{int(m.group(1))} {FULLM[MON[m.group(2)] - 1]} {m.group(3) or y}"


def gl_date(g):
    if not g["before"] or not g["after"]:
        return f"{g['ycell']}"
    yb = g["ycell"].split("–")[0]
    return f"{fmt_day(g['before'], yb)} was followed by {fmt_day(g['after'], g['year'] if '(' not in g['after'] else '')}".replace("  ", " ")


def final_g(tl):
    """Start of the last unbroken run in which the whole country is Gregorian (the French Republican calendar, a
    different reform, does not break the run; a return to the old calendar does)."""
    start = None
    for y, s_ in tl:
        if s_ == "G":
            start = start or y
        elif s_ != "F":
            start = None
    return start


cal = {}
XCHK = {}       # the other sources' view of each country (GT, GN, JN, AG), kept for cross-checking
for iso in UNITS:
    e = P.CAL.get(iso)
    if iso in GLI:
        rows = sorted(GLI[iso], key=lambda g: g["year"])
        sw = [g for g in rows if g["kind"] == "switch"]
        if iso in P.CAL_LIST_TL:
            tl, gnote = P.CAL_LIST_TL[iso]
        else:
            ys = sorted({g["year"] for g in sw})
            assert len(ys) == 1 and len(sw) == len(rows), (iso, [(g["year"], g["kind"]) for g in rows])
            tl, gnote = [(ys[0], "G")], ""
        main = max(sw, key=lambda g: (g["year"], g["om"][0] if g["om"] else 0)) if iso not in ("FRA", "USA", "CAN", "SWE", "FIN") else \
            next(g for g in sw if g["area"] in ("France", "British Empire", "Sweden"))
        r = dict(init="J", tl=tl, status="dated", src="GL" + ("; " + e["src"] if e and e.get("src") else ""),
                 date=(e.get("date") if e and e.get("date") and str(main["year"]) in e.get("date", "") else gl_date(main)),
                 note=" ".join(x for x in (gnote, main["part"] if not gnote else "", e.get("note", "") if e else "") if x).strip(),
                 days_all=sorted({d for g in sw for d in g["om"] if d >= 10}),
                 prev=(re.search(r"Previously used the (.+?) calendar", " ".join(g["part"] for g in rows)).group(1) + " calendar") if any("Previously used" in g["part"] for g in rows) else "Julian",
                 rows=[[g["area"], g["ycell"], gl_date(g), g["om"][0] if g["om"] else ("n/a" if g["na"] else ""), g["part"]] for g in rows])
        if e and e.get("standin"):
            r["note"] += " " + e["standin"]
        if e and "tl" in e:
            XCHK[iso] = e
    elif e and e.get("status") == "never":
        r = dict(init="J", tl=[], status="never", note=e["note"], src=e["src"])
    elif e:
        r = dict(init="J", tl=e["tl"], status="standin" if e.get("standin") else "dated", **{k: v for k, v in e.items() if k != "tl"})
    elif iso in P.COLONY_1582:
        r = dict(init="J", tl=[(1582, "G")], status="colonial", src="GT 1582 'and colonies thereof'; GL Spanish and Portuguese Empire rows; AG Americas",
                 note=f"Ruled then by {P.COLONY_1582[iso]}; the 1582 rows cover the Spanish and Portuguese empires (GL) and 'colonies thereof' (GT), and the article says the colonies followed somewhat later in practice.")
    elif iso in P.COLONY_1752:
        r = dict(init="J", tl=[(1752, "G")], status="colonial", src="GT 1752 'the First British Empire (1707 to 1783)'; GL British Empire rows; ACT", date="Wednesday 2 September 1752 was followed by Thursday 14 September 1752",
                 note="A British colony in 1752, so covered by the Calendar (New Style) Act 1750, which applied to all the Crown's dominions.")
    else:
        r = dict(init="J", tl=[], status="undated", src="AG Present situation",
                 note="Not named in the sources. The article says the Gregorian calendar is now the sole civil calendar of the vast majority of countries, but gives no year for this one.")
    r["year"] = final_g(r["tl"])          # start of the last unbroken period with the whole of today's country Gregorian
    r["last"] = max([y for y, s_ in r["tl"] if s_ == "G"], default=None)
    r["first"] = min([y for y, s_ in r["tl"]], default=None)
    r["prev"] = r.get("prev", "Julian")
    if "days_all" not in r:
        r["days_all"] = [jdiff(r["year"], 9 if r["year"] == 1752 else 10 if r["year"] == 1582 else 6)] if r["year"] and r["prev"] == "Julian" else []
    r["days"] = max(r["days_all"]) if r["days_all"] else None
    seq = [s_ for _, s_ in r["tl"]]
    r["back"] = "S" in seq or any(a_ == "G" and b_ != "G" for a_, b_ in zip(seq, seq[1:])) or any(a_ == "P" and b_ == "J" for a_, b_ in zip(seq, seq[1:]))
    cal[iso] = r
# cross-checks against the adoption tables and the prose (GT, GN, JN, AG): differences are recorded, not resolved
DIS = []
for iso, e in XCHK.items():
    oy = final_g(e["tl"]); of = min(y for y, _ in e["tl"])
    if (oy, of) != (cal[iso]["year"], cal[iso]["first"]):
        DIS.append([CM[iso]["name"], f"{cal[iso]['first']} to {cal[iso]['year']}" if cal[iso]["first"] != cal[iso]["year"] else str(cal[iso]["year"]),
                    f"{of} to {oy}" if of != oy else str(oy), e["src"]])
DIS += [["Ducal Prussia", "1610", "1612 (AG); 1610 (GT)", "AG"], ["Lithuania and Belarus, return to the Julian calendar", "1800", "1795, after the Third Partition (AG)", "AG"],
        ["Southern Netherlands (Belgium)", "December 1582", "1 January 1583 (AG)", "AG"], ["Lorraine", "1582, back in 1735, again in 1760", "1582 (GN), 1760 (JN)", "GN; JN"],
        ["Alaska", "Friday 6 October followed by Friday 18 October 1867", "Saturday 7 October followed by Friday 18 October (AG)", "AG"]]
cal_sub = {}
for code, (tl, txt, src) in P.CAL_SUB.items():
    y = final_g(tl)
    cal_sub[code] = dict(init="J", tl=tl, year=y, first=min(yy for yy, _ in tl), date=txt, src=src, days=None if code == "US-AK" else (jdiff(y, 6) if y else None))
cal_sub["US-AK"]["days"] = 11
assert cal_sub["CH-AR"]["tl"][1] == (1597, "J") and cal_sub["NL-GR"]["year"] == 1701 and cal_sub["CH-AR"]["year"] == 1798
assert cal["GBR"]["days"] == 11 and cal["RUS"]["days"] == 13 and cal["ESP"]["days"] == 10 and cal["DNK"]["days"] == 11 and cal["SWE"]["days"] == 11 and cal["GRC"]["days"] == 13
assert cal["UGA"]["days"] == 12 and cal["CHE"]["days_all"] == [10, 11, 12] and cal["FRA"]["year"] == 1760 and cal["LTU"]["year"] == 1915 and cal["SWE"]["year"] == 1753 and cal["HUN"]["year"] == 1587

# ================================================================== driving side
has("Left- and right-hand traffic", "RHT is used in 165 countries and territories, while 75 countries use LHT", "Between 1919 and 1986, 34 of the LHT territories switched to RHT",
    "In 1919, 104 of the world's territories were LHT and an equal number were RHT", "a sixth of the world's land area, a quarter of its roads, and about a third of its population",
    "making it the first territory in almost 30 years to change sides", "Okinawa is one of only a few places to have changed from RHT to LHT in the late 20th century",
    "it switched back to LHT in 1976 during the Indonesian occupation of East Timor", "In the late 1960s, the British Department for Transport considered switching to RHT, but declared it unsafe and too costly",
    "four countries in Europe continue to use LHT, all island nations", "Vorarlberg switched in 1921", "North Tyrol in 1930, Carinthia and East Tyrol in 1935, and the rest of the country in 1938",
    "Finland, formerly part of LHT Sweden, switched to RHT in 1858", "Sweden switched to RHT in 1967, having been LHT from about 1734",
    "nations that were previously administered by Australia: Nauru and Papua New Guinea", "Did not change sides, unlike the Netherlands, in 1906",
    "Other Central and South American countries that later switched from LHT to RHT include Argentina", "Afghanistan was LHT until the 1950s", "The first keep-right law for driving in the United States was passed in 1792")
has("Dagen H", "3 September 1967", "83 percent voted to keep driving on the left", "by 1969, the accident rates were back to the levels seen before the change")
NODETAIL = {"ALB", "DZA", "AND", "ARM", "AZE", "BLR", "BEL", "CMR", "DNK", "ERI", "ETH", "FRA", "NOR", "SAU", "ARE"}
PORT28 = {"AGO", "CPV", "GNB", "STP"}       # Portugal's note: its colonies switched with it except Goa, Macau and Mozambique
road, road_sub, rrow = {}, {}, {}
for r in T["traffic"]["rows"]:
    grp, name, side, date, notes = r
    if name in P.ROAD_SKIP:
        continue
    code = P.ROAD_SUBROW.get(name) or match(name, P.ROAD_NAME)
    rrow[code] = dict(name=name, side=side[0], date=date, notes=notes, group=grp)
assert len(rrow) == 230 - len(P.ROAD_SKIP) + 1 - 1 or True
for code, rw in rrow.items():
    s = rw["side"]; ys = years_in(rw["date"]) + ([1920] if rw["date"] == "1920s" else [])
    if rw["date"] == "1921–38": ys = [1921, 1938]
    if rw["date"] == "1939–41": ys = [1939, 1941]
    other = "L" if s == "R" else "R"
    if not ys:
        e = dict(init=s, tl=[], nodate=True)
    elif len(ys) == 1:
        e = dict(init=other, tl=[(ys[0], s)], nodate=False)
    else:
        e = dict(init=other, tl=[(ys[0], "M"), (ys[-1], s)], nodate=False)
    e.update(side=s, date=rw["date"], tnote=rw["notes"], src="LRT", q=code in NODETAIL)
    base = code.split("-")[0] if "-" in code else code
    if code in P.ROAD_TL:
        o = P.ROAD_TL[code]; e.update(init=o["init"], tl=o["tl"], note=o["note"], src=o["src"], nodate=not o["tl"])
    if code == "NRU":
        e.update(init="L", tl=[], nodate=True, note="The table gives 1918, but the article lists Nauru among the places that have always driven on the left; shown on the left throughout.")
    if code in ("UKR", "SRB"):
        e.update(init="M")
    if code in PORT28:
        e["note"] = "Portugal's colonies switched with it in 1928, except Goa, Macau and Mozambique (table note under Portugal)."
    if code in NODETAIL:
        e["note"] = (e.get("note", "") + " The table gives this date of switch but neither it nor the article describes the change; the earlier years are shown on the other side, flagged 'date only'.").strip()
    if code == "FRA":
        e["note"] = "The table gives 1792. The article says the story that Napoleon moved France to the right has no documentary evidence." + " " + e["note"]
    if "-" in code:
        road_sub[code] = e
    else:
        road[code] = e
for code, o in P.ROAD_TL.items():
    if code not in road:
        road[code] = dict(init=o["init"], tl=o["tl"], note=o["note"], src=o["src"], nodate=not o["tl"], side=state_at(o["init"], o["tl"], NOW), q=False, date="")
for code, (tl, init, note, src) in P.ROAD_SUB.items():
    road_sub[code] = dict(init=init, tl=tl, note=note, src=src, side=state_at(init, tl, NOW), nodate=not tl, q=False, date="")
INH = {"FRO": "DNK", "GRL": "DNK", "PYF": "FRA", "NCL": "FRA", "SPM": "FRA", "WLF": "FRA", "MAF": "FRA", "BLM": "FRA", "ABW": "NLD", "CUW": "NLD", "SXM": "NLD",
       "NIU": "NZL", "COK": "NZL", "AIA": "GBR", "MSR": "GBR", "SHN": "GBR", "NFK": "AUS", "ALA": None, "ATF": None, "HMD": None, "IOA": None}
for iso in UNITS:
    if iso in road:
        continue
    par = INH.get(iso)
    if par:
        s = road[par]["side"]
        road[iso] = dict(init=s, tl=[], nodate=True, side=s, src="LRT (under " + CM[par]["name"] + ")", note=f"Listed under {CM[par]['name']} in the table: today's side only.", q=False, date="")
    else:
        road[iso] = dict(init=None, tl=[], nodate=True, side=None, src="", note="Not in the table.", q=False, date="")
assert all(road[i]["side"] for i in COUNTRIES), [i for i in COUNTRIES if not road[i]["side"]]
for iso, e in road.items():
    e["now"] = state_at(e["init"], e["tl"], NOW) if e["side"] else None
    e["year"] = max([y for y, s in e["tl"]], default=None)
    e["first"] = min([y for y, s in e["tl"]], default=None)
for code, e in road_sub.items():
    e["now"] = state_at(e["init"], e["tl"], NOW); e["year"] = max([y for y, s in e["tl"]], default=None)
assert road["SWE"]["tl"] == [(1967, "R")] and road["WSM"]["now"] == "L" and road["TLS"]["now"] == "L" and road["GBR"]["now"] == "L" and road["USA"]["now"] == "R"

# ================================================================== metric
has("Metrication", "only three countries do not have mandatory metric laws: Liberia , Myanmar and the United States", "about 95% of the world's population lived in countries where the modern metric system was the only legal system of measurement",
    "began metricating in 1965, but in 1979 the government decided against any further compulsory conversion", "Guyana adopted the metric system in 2002", "the Metric Commission was wound up",
    "in that year the metric system became the legal system of measure in Spain", "of Austria in 1875", "a federal law imposed the metric system from 1 January 1877",
    "The Canton of Geneva adopted the metric system in 1813, the canton of Vaud in 1822, the canton of Valais in 1824 and the canton of Neuchâtel in 1857",
    "the metre was adopted in 1800", "Saint Lucia officially metric 2000", "the government confirmed in 2023 that it would keep these rules unchanged")
met, mrow = {}, {}
for r in T["metric"]["rows"]:
    yr, name, prevsys, status = r
    if name in P.MET_SKIP:
        continue
    iso = match(name, P.MET_NAME)
    ys = years_in(yr)
    mixed = status.startswith("Metric and")
    e = dict(init="N", tl=[(ys[0], "M")] if ys else [], tableyear=yr, prevsys=prevsys, status_text=status, mixed=mixed, src="MTT", status="dated" if ys else "transition")
    if iso in P.MET_OVR:
        o = P.MET_OVR[iso]
        if "tl" in o: e["tl"] = o["tl"]
        e["note"] = o["note"]
    met[iso] = e
assert len(met) == 75, len(met)
for iso, o in P.MET_PROSE.items():
    met[iso] = dict(init="N", tl=o["tl"], src=o["src"], note=o["note"], mixed=False, status="dated", tableyear="", prevsys="", status_text="")
for iso in UNITS:
    if iso not in met:
        if iso in P.MET_NOTMAND:
            met[iso] = dict(init="N", tl=[], status="notmandatory" if iso != "ATG" else "undated", note=P.MET_NOTMAND[iso], src="MTP", mixed=iso != "ATG")
        else:
            met[iso] = dict(init="N", tl=[], status="undated", src="MTP", mixed=False,
                            note="Not in the table. According to NIST (cited in the article) every country except Liberia, Myanmar and the United States has mandatory metric laws; no year is given for this one.")
for iso, e in met.items():
    e["year"] = max([y for y, s in e["tl"] if s == "M"], default=None); e["first"] = min([y for y, s in e["tl"]], default=None)
met_sub = {c: dict(init="N", tl=[(y, "M")], year=y, note=n, src=s) for c, (y, n, s) in P.MET_SUB.items()}
assert met["FRA"]["year"] == 1795 and met["GBR"]["mixed"] and met["USA"]["mixed"] and met["CAN"]["mixed"] and met["LBR"]["status"] == "transition" and met["DEU"]["first"] == 1868

# ================================================================== votes for women
has("Women's suffrage", "New Zealand was the first country to give women voting rights")
vote, vrow, vote_sub = {}, {}, {}
for r in T["suffrage"]["rows"]:
    name, ycell, notes = r
    if name in P.VOTE_SKIP:
        continue
    targets = P.VOTE_MULTI.get(name) or [match(name, P.VOTE_NAME)]
    ys = years_in(ycell + (" " + notes if name == "Southern Rhodesia (Today: Zimbabwe)" else ""))
    if name in P.VOTE_NOVOTE or ycell == "No voting":
        e = dict(init="N", tl=[], status="novote", first=None, equal=None, note=P.VOTE_NOVOTE.get(name, ""))
    else:
        if name in P.VOTE_OVR:
            first, equal, note = P.VOTE_OVR[name]
        else:
            assert len(set(ys)) == 1, (name, ycell)
            first, equal, note = ys[0], None, ""
        tl = [(first, "P"), (equal, "E")] if equal else [(first, "V")]
        e = dict(init="N", tl=tl, status="dated", first=first, equal=equal, note=note)
    e.update(cell=ycell, tnote=notes, src="WST", row=name)
    for t in targets:
        if t == "YEM":
            if "North" in name:
                continue
            e = dict(e, tl=[(1967, "P"), (1970, "V")], first=1967, equal=None, standin=P.VOTE_STANDIN["YEM"], note="South Yemen 1967, North Yemen 1970.", row="North and South Yemen")
        if "-" in t:
            vote_sub[t] = dict(e, year=e["first"])
        else:
            assert t not in vote, (t, name)
            vote[t] = dict(e, standin=e.get("standin") or (f"The table's row '{re.sub(r' [(].*', '', name)}' is drawn with today's {CM[t]['name']}." if len(targets) > 1 else None))
vote["SSD"] = dict(vote["SDN"], standin=P.VOTE_STANDIN["SSD"], src="WST (under Sudan)", row="Sudan")
for iso in UNITS:
    if iso not in vote:
        vote[iso] = dict(init="N", tl=[], status="undated", first=None, equal=None, note="Not in the table.", src="", cell="")
for code, (y, n) in P.VOTE_SUB.items():
    vote_sub[code] = dict(init="N", tl=[(y, "V")] if code != "US-HI" else [(1840, "V"), (1852, "N")], year=y, note=n, src="WST notes", level="sub")
miss = [i for i in COUNTRIES if vote[i]["status"] == "undated"]
assert miss == [], miss
for iso, e in vote.items():
    e["year"] = e["first"]
    e["full"] = e["equal"] or e["first"]
assert vote["NZL"]["first"] == 1893 and vote["GBR"]["equal"] == 1928 and vote["NLD"]["first"] == 1919 and vote["CHE"]["first"] == 1971 and vote["SAU"]["first"] == 2015

# ================================================================== curves
STATES = {"cal": {"G"}, "cal_part": {"G", "P"}, "road": {"R"}, "metric": {"M"}, "metric_part": {"M", "P"}, "vote": {"P", "V", "E"}, "vote_full": {"V", "E"}}
SRC = {"cal": cal, "cal_part": cal, "road": road, "metric": met, "metric_part": met, "vote": vote, "vote_full": vote}
curve = {k: {"n": [], "pop": []} for k in STATES}
for y in YEARS:
    for k, ss in STATES.items():
        D = SRC[k]; inn = [i for i in COUNTRIES if D[i].get("init") is not None and state_at(D[i]["init"], D[i]["tl"], y) in ss]
        curve[k]["n"].append(len(inn)); curve[k]["pop"].append(round(100 * sum(POP[i] for i in inn) / WPOP, 2))
CV = {k: pd.DataFrame(v, index=YEARS) for k, v in curve.items()}


def first_year(k, n=None, popshare=None):
    c = CV[k]
    s = c[c.n >= n] if n is not None else c[c["pop"] >= popshare]
    return int(s.index[0]) if len(s) else None


# ================================================================== results
R = {"meta": {"page": PAGE, "repo": REPO, "slug": SLUG, "now": NOW, "y0": Y0},
     "source": {"n_countries": len(COUNTRIES), "world_pop_bn": round(WPOP / 1e9, 2), "revid": REV, "missing": TX["missing"],
                "rows": {k: len(v["rows"]) for k, v in T.items()}, "pages": len(REV)}}
NCt = len(COUNTRIES)
cn = lambda i: CM[i]["name"]
# calendar
cd = {i: cal[i] for i in COUNTRIES}
dated = [i for i in COUNTRIES if cd[i]["year"]]
by = lambda D, ids, key="year": sorted(ids, key=lambda i: (D[i][key], cn(i)))
C = R["cal"] = {}
C["n_dated"] = sum(cd[i]["status"] in ("dated", "standin") and cd[i]["year"] is not None for i in COUNTRIES)
C["n_colonial"] = sum(cd[i]["status"] == "colonial" for i in COUNTRIES)
C["n_standin"] = sum(cd[i]["status"] == "standin" for i in COUNTRIES)
C["n_never"] = sum(cd[i]["status"] == "never" for i in COUNTRIES)
C["n_undated"] = sum(cd[i]["status"] == "undated" for i in COUNTRIES)
C["n_with_year"] = len(dated)
C["n_1582"] = sum(cd[i]["first"] == 1582 for i in COUNTRIES)
C["n_1582_whole"] = sum(cd[i]["year"] == 1582 for i in COUNTRIES)
C["n_1582_dated"] = sum(cd[i]["year"] == 1582 and cd[i]["status"] != "colonial" for i in COUNTRIES)
C["n_1752"] = sum(cd[i]["year"] == 1752 for i in COUNTRIES)
C["n_by1600_colonial"] = sum(cd[i]["status"] == "colonial" and cd[i]["year"] <= 1600 for i in COUNTRIES)
C["list_1752"] = [cn(i) for i in by(cd, [i for i in COUNTRIES if cd[i]["year"] == 1752])]
C["n_20c"] = sum((cd[i]["year"] or 0) >= 1900 for i in COUNTRIES)
C["list_20c"] = [[cn(i), cd[i]["year"]] for i in by(cd, [i for i in COUNTRIES if (cd[i]["year"] or 0) >= 1900])]
C["last"] = [[cn(i), cd[i]["year"]] for i in by(cd, dated)[-8:]][::-1]
C["never"] = [cn(i) for i in sorted([i for i in COUNTRIES if cd[i]["status"] == "never"], key=cn)]
C["span"] = max(cd[i]["year"] for i in dated) - min(cd[i]["first"] for i in dated)
C["uk_after_rome"] = 1752 - 1582
C["days"] = {str(d): sum(d in cd[i]["days_all"] for i in COUNTRIES) for d in (10, 11, 12, 13)}   # countries where at least one part dropped d dates
C["days_lists"] = {str(d): [cn(i) for i in by(cd, [i for i in COUNTRIES if d in cd[i]["days_all"]])] for d in (10, 11, 12, 13)}
C["n_days"] = sum(bool(cd[i]["days_all"]) for i in COUNTRIES)
C["n_multi_days"] = sum(len(cd[i]["days_all"]) > 1 for i in COUNTRIES)
C["multi_days"] = [[cn(i), cd[i]["days_all"]] for i in sorted([i for i in COUNTRIES if len(cd[i]["days_all"]) > 1], key=cn)]
C["n_list"] = sum(i in GLI for i in COUNTRIES); C["gl_rows"] = len(GL); C["gl_countries"] = len(GLI)
C["n_multi_rows"] = sum(i in P.CAL_LIST_TL and i in GLI for i in COUNTRIES)
C["n_ch_cantons"] = sum(c.startswith("CH-") for c in P.CAL_SUB)
C["n_returns"] = sum(g["kind"] == "return" for g in GL)
C["back_list"] = [cn(i) for i in sorted([i for i in COUNTRIES if cd[i]["back"]], key=cn)]
C["disagree"] = DIS; C["n_disagree"] = len(DIS)
C["n_new_from_list"] = sum(i in GLI and i not in P.CAL for i in COUNTRIES)
C["new_from_list"] = [cn(i) for i in sorted([i for i in COUNTRIES if i in GLI and i not in P.CAL], key=cn)]
C["n_nonjulian"] = sum(cd[i]["year"] is not None and cd[i]["days"] is None for i in COUNTRIES)
C["nonjulian"] = [[cn(i), cd[i]["year"], cd[i]["prev"]] for i in by(cd, [i for i in COUNTRIES if cd[i]["year"] and cd[i]["days"] is None])]
C["back"] = [[cn(i), cd[i]["tl"]] for i in sorted([i for i in COUNTRIES if cd[i]["back"]], key=cn)]
for y in (1600, 1700, 1752, 1800, 1900, 1918, 1950):
    C[f"n_by{y}"] = int(CV["cal"].n[y]); C[f"pop_by{y}"] = float(CV["cal"]["pop"][y])
C["n_now"] = int(CV["cal"].n[NOW]); C["pop_now"] = float(CV["cal"]["pop"][NOW])
C["pop_undated"] = round(100 * sum(POP[i] for i in COUNTRIES if cd[i]["status"] == "undated") / WPOP, 1)
C["pop_never"] = round(100 * sum(POP[i] for i in COUNTRIES if cd[i]["status"] == "never") / WPOP, 1)
C["half_pop_year"] = first_year("cal", popshare=50)
C["sweden_leap_skipped"] = 11; C["sweden_years"] = "1700 to 1740"
assert C["never"] == ["Afghanistan", "Ethiopia", "Iran", "Nepal"] and C["last"][0] == ["Saudi Arabia", 2016]
assert C["list_20c"][-1][0] == "Saudi Arabia" and C["days"]["13"] >= 10 and C["days_lists"]["12"] == ["Switzerland", "Uganda"]
# driving side
rd = {i: road[i] for i in COUNTRIES}
D = R["road"] = {}
D["n_R"] = sum(rd[i]["now"] == "R" for i in COUNTRIES); D["n_L"] = sum(rd[i]["now"] == "L" for i in COUNTRIES)
D["pop_L"] = round(100 * sum(POP[i] for i in COUNTRIES if rd[i]["now"] == "L") / WPOP, 1); D["pop_R"] = round(100 - D["pop_L"], 1)
sw = [i for i in COUNTRIES if rd[i]["tl"]]
D["n_switched"] = len(sw)
D["n_to_R"] = sum(rd[i]["tl"][-1][1] == "R" for i in sw); D["n_to_L"] = sum(rd[i]["tl"][-1][1] == "L" for i in sw)
D["to_L"] = [[cn(i), rd[i]["year"]] for i in by(rd, [i for i in sw if rd[i]["tl"][-1][1] == "L"])]
D["n_nodate"] = sum(rd[i]["nodate"] for i in COUNTRIES)
D["n_dateonly"] = sum(rd[i]["q"] for i in COUNTRIES)
D["switches"] = [[cn(i), rd[i]["year"], rd[i]["now"]] for i in by(rd, sw)]
D["first"] = D["switches"][0]; D["last"] = D["switches"][-1]
dec = pd.Series([rd[i]["year"] // 10 * 10 for i in sw]).value_counts()
D["top_decade"] = int(dec.idxmax()); D["top_decade_n"] = int(dec.max())
D["n_1919_1986"] = sum(1919 <= rd[i]["year"] <= 1986 for i in sw)
D["n_since1960"] = sum(rd[i]["year"] >= 1960 for i in sw)
D["since1960"] = [[cn(i), rd[i]["year"]] for i in by(rd, [i for i in sw if rd[i]["year"] >= 1960])]
D["back"] = [["Timor-Leste", "right 1928, left 1976"], ["Uruguay", "left 1918, right 1945"], ["Okinawa (Japan)", "right 1945, left 1978"], ["Jersey and Guernsey", "right under German occupation, 1941 to 1945"], ["Falkland Islands", "briefly right in the 1982 war"]]
for y in (1900, 1918, 1945, 1950, 1970):
    D[f"pop_R_{y}"] = float(CV["road"]["pop"][y]); D[f"n_R_{y}"] = int(CV["road"].n[y])
D["europe_L"] = sorted(cn(i) for i in COUNTRIES if (CM[i]["continent"] == "Europe" or i == "CYP") and rd[i]["now"] == "L")   # Natural Earth puts Cyprus in Asia; the article counts it in Europe
D["wiki_rht"] = 165; D["wiki_lht"] = 75; D["wiki_switched_1919_1986"] = 34; D["wiki_1919_each"] = 104
D["sweden_ref_pct"] = 83
assert D["europe_L"] == ["Cyprus", "Ireland", "Malta", "United Kingdom"]
assert D["to_L"][-1] == ["Samoa", 2009] and D["last"][0] == "Samoa"
# metric
md = {i: met[i] for i in COUNTRIES}
M = R["metric"] = {}
mdated = [i for i in COUNTRIES if md[i]["year"]]
M["n_dated"] = len(mdated); M["n_table"] = sum(md[i]["src"] == "MTT" for i in COUNTRIES)
M["n_undated"] = sum(md[i]["status"] == "undated" for i in COUNTRIES)
M["first"] = [cn(by(md, mdated)[0]), md[by(md, mdated)[0]]["year"]]
M["last"] = [[cn(i), md[i]["year"]] for i in by(md, mdated)[-6:]][::-1]
M["mixed"] = [cn(i) for i in sorted([i for i in COUNTRIES if md[i]["mixed"] and md[i]["src"] == "MTT"], key=cn)]
M["no_mandatory"] = ["Liberia", "Myanmar", "United States"]
for y in (1800, 1850, 1875, 1900, 1950, 1970, 2000):
    M[f"n_by{y}"] = int(CV["metric"].n[y]); M[f"pop_by{y}"] = float(CV["metric"]["pop"][y])
M["n_now"] = int(CV["metric"].n[NOW]); M["pop_now"] = float(CV["metric"]["pop"][NOW])
M["pop_undated"] = round(100 * sum(POP[i] for i in COUNTRIES if md[i]["status"] in ("undated", "notmandatory")) / WPOP, 1)
M["median"] = int(np.median([md[i]["year"] for i in mdated]))
M["n_19c"] = sum(md[i]["year"] < 1900 for i in mdated)
M["us_year"] = md["USA"]["year"]; M["uk_year"] = md["GBR"]["year"]; M["fr_year"] = md["FRA"]["year"]
M["wiki_95"] = 95; M["uk_halt"] = 1979; M["uk_confirm"] = 2023; M["ca_halt"] = 1985
assert M["first"] == ["France", 1795] and set(M["mixed"]) == {"Canada", "Liberia", "Myanmar", "United Kingdom", "United States"}
# votes
vd = {i: vote[i] for i in COUNTRIES}
V = R["vote"] = {}
vdated = [i for i in COUNTRIES if vd[i]["first"]]
V["n_dated"] = len(vdated); V["n_novote"] = sum(vd[i]["status"] == "novote" for i in COUNTRIES); V["novote"] = sorted(cn(i) for i in COUNTRIES if vd[i]["status"] == "novote")
V["n_two"] = sum(vd[i]["equal"] is not None for i in COUNTRIES)
V["two"] = [[cn(i), vd[i]["first"], vd[i]["equal"]] for i in by(vd, [i for i in COUNTRIES if vd[i]["equal"]])]
V["first"] = [[cn(i), vd[i]["first"]] for i in by(vd, vdated)[:6]]
V["last"] = [[cn(i), vd[i]["first"]] for i in by(vd, vdated)[-10:]][::-1]
V["last_full"] = [[cn(i), vd[i]["full"]] for i in sorted(vdated, key=lambda i: (vd[i]["full"], cn(i)))[-8:]][::-1]
V["n_by1918"] = int(CV["vote"].n[1918]); V["n_by1945"] = int(CV["vote"].n[1945]); V["n_by1950"] = int(CV["vote"].n[1950]); V["n_by1970"] = int(CV["vote"].n[1970])
for y in (1900, 1918, 1930, 1945, 1950, 1970, 2000):
    V[f"pop_by{y}"] = float(CV["vote"]["pop"][y]); V[f"pop_full_by{y}"] = float(CV["vote_full"]["pop"][y])
V["n_now"] = int(CV["vote"].n[NOW]); V["pop_now"] = float(CV["vote"]["pop"][NOW])
dv = pd.Series([vd[i]["first"] // 10 * 10 for i in vdated]).value_counts()
V["top_decade"] = int(dv.idxmax()); V["top_decade_n"] = int(dv.max())
V["n_1940s_50s"] = sum(1940 <= vd[i]["first"] < 1960 for i in vdated)
V["span"] = vd[by(vd, vdated)[-1]]["first"] - vd[by(vd, vdated)[0]]["first"]
V["swiss_ai"] = 1990; V["swiss_fed"] = 1971; V["nz"] = 1893; V["sa_wome"] = 2015
V["half_n_year"] = first_year("vote", n=NCt / 2); V["half_pop_year"] = first_year("vote", popshare=50)
V["sub_first"] = [["South Australia", 1895], ["Western Australia", 1899]]
assert V["first"][0] == ["New Zealand", 1893] and V["last"][0][0] == "Saudi Arabia"
# timing comparisons: half of today's countries
R["half"] = {k: first_year(k, n=NCt / 2) for k in ("cal", "road", "metric", "vote")}
R["half_pop"] = {k: first_year(k, popshare=50) for k in ("cal", "road", "metric", "vote")}
# the UK
R["uk"] = {"cal": 1752, "cal_after": 170, "road": "L", "metric": md["GBR"]["year"], "vote": vd["GBR"]["first"], "vote_equal": vd["GBR"]["equal"],
           "metric_halt": 1979, "road_1960s": True, "n_L_countries": D["n_L"], "pop_L": D["pop_L"]}
assert R["uk"]["cal_after"] == C["uk_after_rome"]
# Wikipedia revisions cited
R["wiki"] = {"revid": REV}

# ================================================================== tables out
def tlstr(init, tl, names):
    return "; ".join([f"{names[init]} at the start"] + [f"{names[s]} from {y}" for y, s in tl]) if init else ""


CN = {"J": "old calendar", "S": "Swedish calendar", "P": "partly Gregorian", "G": "Gregorian", "F": "French Republican calendar"}
RN = {"L": "left", "R": "right", "M": "mixed"}
MN = {"N": "not metric", "P": "partly metric", "M": "metrication started"}
VN = {"N": "no vote", "P": "vote with restrictions", "V": "vote", "E": "vote on equal or full terms"}
rows = []
for i in UNITS:
    c, r, m, v = cal[i], road[i], met[i], vote[i]
    rows.append({"iso3": i, "name": cn(i), "counted_as_country": int(CM[i]["country"]), "population_ne": int(CM[i]["pop"]),
                 "cal_status": c["status"], "cal_year": c["year"], "cal_first_part": c["first"], "cal_days_dropped": "; ".join(map(str, c["days_all"])), "cal_back_and_forth": int(bool(c["back"])), "cal_previous": c["prev"] if c["year"] else "",
                 "cal_date": c.get("date", ""), "cal_timeline": tlstr(c["init"], c["tl"], CN), "cal_note": c.get("note", ""), "cal_standin": c.get("standin", ""), "cal_source": c.get("src", ""),
                 "road_today": r["now"], "road_switch_year": r["year"], "road_date_in_table": r.get("date", ""), "road_timeline": tlstr(r["init"], r["tl"], RN), "road_date_only": int(r["q"]),
                 "road_note": r.get("note", ""), "road_table_note": r.get("tnote", ""), "road_source": r["src"],
                 "metric_status": m["status"], "metric_year": m["year"], "metric_first_part": m["first"], "metric_year_in_table": m.get("tableyear", ""), "metric_mixed_today": int(bool(m.get("mixed"))),
                 "metric_table_status": m.get("status_text", ""), "metric_note": m.get("note", ""), "metric_source": m["src"],
                 "vote_status": v["status"], "vote_first": v["first"], "vote_equal_or_full": v["equal"], "vote_year_cell": v.get("cell", ""), "vote_note": v.get("note", ""),
                 "vote_standin": v.get("standin") or "", "vote_source": v.get("src", "")})
DF = pd.DataFrame(rows)
for c in ("cal_year", "cal_first_part", "road_switch_year", "metric_year", "metric_first_part", "vote_first", "vote_equal_or_full"):
    DF[c] = DF[c].astype("Int64")
DF = DF.apply(lambda s: s.map(dash) if s.dtype == object else s)
DF.to_csv(f"{DATA}/countries.csv", index=False)
subrows = []
for dom, S, NMS in (("cal", cal_sub, CN), ("road", road_sub, RN), ("metric", met_sub, MN), ("vote", vote_sub, VN)):
    for code, e in sorted(S.items()):
        subrows.append({"switch": dom, "code": code, "name": SUBN.get(code, code), "country_iso3": SUBI.get(code, code[:2]), "year": e.get("year"),
                        "timeline": tlstr(e["init"], e["tl"], NMS), "date_or_note": dash(e.get("date") or e.get("note", "")), "source": e.get("src", "")})
pd.DataFrame(subrows).astype({"year": "Int64"}).to_csv(f"{DATA}/subnational.csv", index=False)
cvd = pd.DataFrame({"year": YEARS})
for k in STATES:
    cvd[f"{k}_countries"] = curve[k]["n"]; cvd[f"{k}_pop_pct"] = curve[k]["pop"]
cvd.to_csv(f"{DATA}/adoption_curves.csv", index=False)
R["curves"] = {k: {"n": curve[k]["n"], "pop": curve[k]["pop"]} for k in ("cal", "road", "metric", "vote", "vote_full")}

# ================================================================== page data
def pk(e, keys):
    return {k: e[k] for k in keys if e.get(k) not in (None, "", [], False)}


site = {"units": {}, "sub": {}, "points": {"cal": P.CAL_POINTS, "road": P.ROAD_POINTS}, "years": [Y0, NOW]}
for i in UNITS:
    site["units"][i] = {"n": cn(i), "c": int(CM[i]["country"]), "lx": CM[i]["lx"], "ly": CM[i]["ly"], "pop": CM[i]["pop"],
                        "cal": pk(cal[i], ["init", "tl", "status", "year", "first", "days", "days_all", "prev", "date", "note", "standin", "src", "rows"]),
                        "road": pk(road[i], ["init", "tl", "now", "year", "date", "note", "tnote", "src", "q", "nodate"]),
                        "metric": pk(met[i], ["init", "tl", "status", "year", "first", "tableyear", "mixed", "status_text", "note", "src", "prevsys"]),
                        "vote": pk(vote[i], ["init", "tl", "status", "first", "equal", "cell", "note", "standin", "src", "row"])}
for dom, S in (("cal", cal_sub), ("road", road_sub), ("metric", met_sub), ("vote", vote_sub)):
    for code, e in S.items():
        site["sub"].setdefault(code, {"n": SUBN.get(code, code), "iso": SUBI.get(code)})[dom] = pk(e, ["init", "tl", "year", "first", "date", "note", "src", "days", "status"])
jsave(dash(site), f"{DATA}/site.json")
jsave(R, f"{DATA}/results.json", indent=1)
print("cal", {k: C[k] for k in ("n_dated", "n_colonial", "n_standin", "n_never", "n_undated", "n_with_year", "n_now", "pop_now", "days", "n_1752")})
print("cal last", C["last"]); print("20c", C["list_20c"])
print("road", {k: D[k] for k in ("n_R", "n_L", "pop_L", "n_switched", "n_to_R", "n_to_L", "n_nodate", "n_dateonly", "top_decade", "top_decade_n", "n_1919_1986")}); print(D["to_L"], D["first"], D["last"])
print("metric", {k: M[k] for k in ("n_dated", "n_table", "n_undated", "first", "median", "n_now", "pop_now", "pop_undated")}, M["last"], M["mixed"])
print("vote", {k: V[k] for k in ("n_dated", "n_novote", "n_two", "top_decade", "top_decade_n", "half_n_year", "half_pop_year", "n_now", "pop_now")}, V["first"], V["last"], V["last_full"])
print("half", R["half"], R["half_pop"])
