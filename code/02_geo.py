"""Step 2. Geography: a light world outline file for the page and figures (Natural Earth 1:50m countries, simplified),
country names, label positions and populations, today's countries (the set used for shares), and the sub-national
units named in the sources (Natural Earth 1:10m states and provinces).

Today's countries: every Natural Earth 1:50m unit that is its own sovereign (193 UN members and Vatican City, Taiwan),
plus Kosovo and Palestine: 197 in all. Northern Cyprus and Somaliland are drawn as parts of Cyprus and Somalia.
Dependencies (Greenland, Puerto Rico, Hong Kong...) are drawn and coloured where a table gives them a row, but are not
counted. Population: Natural Earth POP_EST (mostly 2019), used only to weight the adoption curves."""
from shapely.geometry import shape, mapping
from common import *

iso_of = lambda p: p["ISO_A3_EH"] if p.get("ISO_A3_EH") not in ("-99", None) else p["ADM0_A3"]
FIX = {"CNM": "CYP", "ESB": "CYP", "WSB": "CYP", "PSX": "PSE", "SAH": "ESH", "KAS": "IND", "SOL": "SOM", "CYN": "CYP"}
NAME = {"CHN": "China", "USA": "United States", "TZA": "Tanzania", "BHS": "Bahamas", "SWZ": "Eswatini", "CZE": "Czechia", "SRB": "Serbia",
        "COD": "DR Congo", "COG": "Congo", "MKD": "North Macedonia", "TLS": "Timor-Leste", "FSM": "Micronesia", "HKG": "Hong Kong",
        "MAC": "Macau", "CPV": "Cape Verde", "STP": "São Tomé and Príncipe", "GMB": "Gambia", "VAT": "Vatican City", "CIV": "Ivory Coast",
        "KOS": "Kosovo", "PSE": "Palestine", "TWN": "Taiwan", "KOR": "South Korea", "PRK": "North Korea", "LAO": "Laos", "RUS": "Russia",
        "SYR": "Syria", "IRN": "Iran", "VNM": "Vietnam", "BRN": "Brunei", "BOL": "Bolivia", "VEN": "Venezuela", "MDA": "Moldova"}


def rnd(c, k=2):
    if isinstance(c, (list, tuple)) and c and isinstance(c[0], (int, float)):
        return [round(c[0], k), round(c[1], k)]
    return [rnd(x, k) for x in c]


W50 = jload(f"{GEO}/ne_50m_admin_0_countries.geojson")
feats, meta = [], {}
for f in W50["features"]:
    p = f["properties"]; iso = FIX.get(iso_of(p), iso_of(p))
    if iso == "ATA":
        continue
    gs = shape(f["geometry"]).simplify(0.03, preserve_topology=True)
    if gs.is_empty:
        continue
    gm = mapping(gs)
    feats.append({"type": "Feature", "properties": {"iso": iso}, "geometry": {"type": gm["type"], "coordinates": rnd(gm["coordinates"])}})
    main = iso_of(p) == iso and p.get("HOMEPART") == 1 and p["ADMIN"] not in ("Northern Cyprus", "Somaliland")
    pop = float(p.get("POP_EST") or 0)
    if iso not in meta or main:
        sov = (p["ADMIN"] == p["SOVEREIGNT"] and p["TYPE"] != "Indeterminate" and p["ADMIN"] not in ("Northern Cyprus", "Somaliland")) or p["ADMIN"] in ("Kosovo", "Palestine")
        nm = NAME.get(iso) or p.get("NAME_EN") or p["NAME"]
        old = meta.get(iso, {})
        meta[iso] = {"name": nm, "lx": round(p["LABEL_X"], 2), "ly": round(p["LABEL_Y"], 2), "pop": pop + old.get("pop", 0),
                     "country": bool(sov), "sov": p["SOV_A3"], "continent": p["CONTINENT"], "admin": p["ADMIN"]}
    else:
        meta[iso]["pop"] += pop
meta["CYP"]["name"] = "Cyprus"
NC = sorted(i for i, m in meta.items() if m["country"])
assert len(NC) == 197, len(NC)
jsave({"type": "FeatureCollection", "features": feats}, f"{DATA}/world.json")
jsave(meta, f"{WORK}/countries.json")

# sub-national units named in the sources
import importlib.util
spec = importlib.util.spec_from_file_location("polities", os.path.join(ROOT, "code", "polities.py")); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
want = set(P.CAL_SUB) | set(P.ROAD_SUB) | set(P.VOTE_SUB) | set(P.MET_SUB) | {"NL-LI", "NL-FL"} | {c for c in P.ROAD_SUBROW.values() if "-" in c}
A1 = jload(f"{GEO}/ne_10m_admin_1_states_provinces.geojson")
subs, seen = [], {}
for f in A1["features"]:
    p = f["properties"]; code = p["iso_3166_2"]
    if code not in want:
        continue
    if code == "AU-NSW" and p["name"] != "New South Wales":      # Lord Howe Island shares the code
        continue
    gs = shape(f["geometry"]).simplify(0.02, preserve_topology=True)
    gm = mapping(gs)
    subs.append({"type": "Feature", "properties": {"code": code, "name": p["name"], "iso": p["adm0_a3"]}, "geometry": {"type": gm["type"], "coordinates": rnd(gm["coordinates"], 2)}})
    seen[code] = p["name"]
assert want <= set(seen), sorted(want - set(seen))
jsave({"type": "FeatureCollection", "features": subs}, f"{DATA}/subunits.json")
print("countries", len(NC), "units drawn", len(meta), "features", len(feats), "subunits", len(subs),
      "world", os.path.getsize(f"{DATA}/world.json") // 1024, "KB", "subunits", os.path.getsize(f"{DATA}/subunits.json") // 1024, "KB")
