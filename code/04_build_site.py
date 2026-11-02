"""Step 4. Build index.html from code/page_template.html. Every number in the text is a {{path|format}} token filled
from data/results.json; the page data (results, site.json, world.json, subunits.json) is embedded. Facts stated in
words on the page, blog, paper and collage are checked here against the data. The full-screen map snippet
(code/fullscreen_snippet.html) is pasted before </body>. 10.5281/zenodo.23873009 and https://blog.tristanhotham.com/2026/10/31/calendar-switch/ stay as placeholders for the publisher."""
import json
from common import *

R = jload(f"{DATA}/results.json")
SITE = jload(f"{DATA}/site.json")
U = SITE["units"]
C, D, M, V = R["cal"], R["road"], R["metric"], R["vote"]
cy = lambda i: U[i]["cal"].get("year"); ry = lambda i: U[i]["road"].get("year"); rn = lambda i: U[i]["road"].get("now")
my = lambda i: U[i]["metric"].get("year"); vf = lambda i: U[i]["vote"].get("first"); ve = lambda i: U[i]["vote"].get("equal")

# facts stated in words (page, blog, paper, collage)
assert R["uk"]["cal_after"] == 170 and cy("GBR") == 1752 and cy("RUS") == 1918 and cy("GRC") == 1923 and cy("SAU") == 2016 and C["span"] == 434
assert C["n_by1600_colonial"] * 2 > C["n_by1600"]                                    # "most of them Spain's and Portugal's colonies"
assert V["n_by1918"] > 20 and R["curves"]["vote"]["n"][1900 - R["meta"]["y0"]] == 1   # "almost nowhere in 1900" (New Zealand only)
assert C["days"]["12"] == 2 and C["days_lists"]["12"] == ["Switzerland", "Uganda"] and U["UGA"]["cal"]["year"] == 1894   # "only two ... twelve"
assert U["DNK"]["cal"]["days_all"] == U["NOR"]["cal"]["days_all"] == [11] and U["DEU"]["cal"]["days_all"] == [10, 11] and U["GBR"]["cal"]["days"] == 11 and U["SWE"]["cal"]["days"] == 11
assert C["n_returns"] == 8 and {"Belarus", "Lithuania", "Latvia", "France", "Ireland", "Sweden"} <= set(C["back_list"])     # the returns named in the text
assert [y for y, s in U["FRA"]["cal"]["tl"]] == [1582, 1760, 1793, 1806] and SITE["sub"]["CH-AR"]["cal"]["tl"][1] == [1597, "J"] and SITE["sub"]["NL-GR"]["cal"]["tl"][1] == [1594, "J"]
assert U["LTU"]["cal"]["first"] == 1586 and U["LVA"]["cal"]["tl"][1] == [1796, "J"] and U["IRL"]["cal"]["tl"][1] == [1641, "J"]
assert {cy(i) for i in ("LVA", "LTU", "BGR", "EST", "RUS", "UKR", "ROU", "SRB", "GRC", "ARM", "GEO", "AZE")} <= set(range(1915, 1924)) and all(U[i]["cal"]["days"] == 13 for i in ("RUS", "GRC", "BGR", "ROU"))
assert (cy("JPN"), cy("KOR"), cy("CHN"), cy("VNM")) == (1873, 1896, 1912, 1954)
assert [cy(i) for i in ("ESP", "PRT")] == [1582] * 2 and [U[i]["cal"]["first"] for i in ("ITA", "POL", "FRA")] == [1582] * 3 and U["BEL"]["cal"]["tl"][-1][0] == 1583
assert U["SWE"]["cal"]["tl"] == [[1700, "S"], [1712, "J"], [1753, "G"]] and U["LTU"]["cal"]["tl"] == [[1586, "P"], [1610, "G"], [1800, "P"], [1915, "G"]]
assert D["n_to_R"] + D["n_to_L"] == D["n_switched"] and D["n_to_L"] == 3 and D["top_decade"] == 1920
assert (ry("GMB"), ry("SLE"), ry("NGA"), ry("GHA"), ry("SDN"), ry("MMR"), ry("ISL"), ry("SWE")) == (1965, 1971, 1972, 1974, 1973, 1970, 1968, 1967)
assert all(rn(i) == "L" for i in ("JPN", "IND", "IDN", "THA", "KEN", "TZA", "ZAF", "MOZ", "ZMB", "ZWE", "GBR")) and rn("SWE") == "R"
assert [x[0] for x in D["to_L"]] == ["Namibia", "Timor-Leste", "Samoa"] and D["sweden_ref_pct"] == 83
assert (my("PRT"), my("NLD"), my("BEL"), my("DEU"), my("ESP"), my("CHL"), my("MEX"), my("BRA"), my("ARG")) == (1814, 1820, 1820, 1872, 1852, 1848, 1852, 1862, 1863)
assert my("USA") == 1866 and my("GBR") == 1965 and M["last"][0] == ["Samoa", 2015]
assert (vf("NZL"), vf("AUS"), vf("FIN"), vf("NOR")) == (1893, 1902, 1906, 1913) and (vf("GBR"), ve("GBR")) == (1918, 1928) and (vf("PRT"), ve("PRT")) == (1911, 1976)
assert (vf("ZAF"), ve("ZAF")) == (1930, 1994) and vf("CHE") == 1971 and SITE["sub"]["CH-AI"]["vote"]["year"] == 1990
assert [vf(i) for i in ("LIE", "WSM", "QAT", "BHR", "OMN", "KWT", "ARE", "SAU")] == [1984, 1990, 1997, 2002, 2002, 2005, 2006, 2015]
assert V["novote"] == ["Eritrea", "Vatican City"] and V["first"][0] == ["New Zealand", 1893]
assert C["never"] == ["Afghanistan", "Ethiopia", "Iran", "Nepal"]


def build():
    tpl = open(os.path.join(ROOT, "code", "page_template.html"), encoding="utf-8").read()
    html = fill(tpl, R)
    left = re.findall(r"\{\{[^}]*\}\}", html)
    assert set(left) <= {"10.5281/zenodo.23873009", "https://blog.tristanhotham.com/2026/10/31/calendar-switch/"}, left[:5]
    J = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    html = html.replace("/*RESULTS*/", J(R)).replace("/*SITE*/", J(SITE))
    html = html.replace("/*WORLD*/", open(f"{DATA}/world.json", encoding="utf-8").read())
    html = html.replace("/*SUBUNITS*/", open(f"{DATA}/subunits.json", encoding="utf-8").read())
    html = html.replace("/*FULLSCREEN*/", open(os.path.join(ROOT, "code", "fullscreen_snippet.html"), encoding="utf-8").read())
    vis = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", "", html, flags=re.S)
    vis = re.sub(r"<[^>]+>", " ", vis)
    visible_text_ok(vis, "index.html")
    for scr in re.findall(r"<script>(.*?)</script>", html, flags=re.S):
        for bad in ("—", "–"):
            assert bad not in scr, bad
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    print("index.html", len(html.encode()) // 1024, "KB")


if __name__ == "__main__":
    build()
