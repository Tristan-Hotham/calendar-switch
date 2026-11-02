"""Step 8. Blog post and meta (release/blog), Zenodo files and metadata (release/zenodo).
10.5281/zenodo.23873009, https://doi.org/10.5281/zenodo.23873009 and https://blog.tristanhotham.com/2026/10/31/calendar-switch/ stay as placeholders for the publisher."""
import json as _json, shutil, zipfile, importlib.util
from common import *

R = jload(f"{DATA}/results.json")
REL = os.path.join(ROOT, "release"); NAME = "Hotham_Lost_Days"

U_ = jload(f"{DATA}/site.json")["units"]
# the page build checks the shared facts; these are numbers written in words or alt text in the blog and collage
spec = importlib.util.spec_from_file_location("b", os.path.join(ROOT, "code", "04_build_site.py")); spec.loader.exec_module(importlib.util.module_from_spec(spec))
C, D, M, V = R["cal"], R["road"], R["metric"], R["vote"]
assert (C["days"]["10"], C["days"]["11"], C["days"]["12"], C["days"]["13"], C["n_nonjulian"]) == (45, 19, 2, 19, 11)   # alt text of b_days
assert all(U_[i]["cal"]["year"] <= 1599 for i in ("ESP", "PRT", "ITA", "AUT", "HUN")) and all(1600 <= U_[i]["cal"]["year"] < 1752 for i in ("DEU", "POL", "NLD", "DNK", "NOR"))   # alt text of b_cal_map
assert V["n_two"] == 18 and V["two"][0] == ["Australia", 1902, 1962] and V["two"][-1] == ["Jordan", 1955, 1974]        # alt text of b_vote_two
assert [x[1] for x in D["to_L"]] == [1920, 1976, 2009] and D["switches"][0][1] == 1724                                 # alt text of b_road_switches
SITE = jload(f"{DATA}/site.json"); U = SITE["units"]
assert all(U[i]["cal"]["status"] == "never" for i in ("IRN", "AFG", "ETH", "NPL")) and U["SAU"]["cal"]["year"] == 2016
assert sum(U[i]["metric"].get("year", 9999) < 1900 for i in ("PRY", "CRI")) == 1                                       # "most of Latin America by the 1860s"

post = open(os.path.join(ROOT, "code", "blog_template.html"), encoding="utf-8").read()
post = fill(post, R)
used = re.findall(r"\{\{IMG\|([^|]+)\|", post)
assert 5 <= len(used) <= 8, len(used)
assert all(re.search(r"^\{\{IMG\|" + re.escape(u), post, re.M) for u in used) and "wp:image" not in post
for img in used:
    assert os.path.exists(f"{REL}/blog/{img}"), img
for fn in os.listdir(f"{REL}/blog"):
    if fn.startswith("b_") and fn not in used:
        os.remove(f"{REL}/blog/{fn}")
assert set(re.findall(r"\{\{[^|}]+\}\}", post)) <= {"https://doi.org/10.5281/zenodo.23873009"}
vis = re.sub(r"<!--.*?-->", "", post, flags=re.S)
visible_text_ok(vis, "blog")
open(f"{REL}/blog/post.html", "w", encoding="utf-8").write(post)
words = len(re.sub(r"<[^>]+>|\{\{IMG\|[^}]*\}\}", " ", vis).split())
meta = {"title": "When did your country lose 11 days? Four great switches, mapped",
        "slug": "calendar-switch",
        "excerpt": f"Britain lost eleven days in 1752, Russia thirteen in 1918, and Saudi Arabia switched its civil calendar only in 2016. I mapped when every country the sources date changed calendar, side of the road, units and votes for women.",
        "seo_description": "A map of when each country switched to the Gregorian calendar, changed driving side, went metric and gave women the vote, 1582 to 2026.",
        "tags": ["history", "maps", "data visualisation", "Gregorian calendar", "driving side", "metric system", "women's suffrage", "Wikipedia"],
        "header_alt": "Title card reading 'When did your country lose 11 days?' on pale paper, beside a world map coloured by the year each country adopted the Gregorian calendar, dark red for Spain, Portugal, Italy and Latin America in 1582, lighter for Britain and North America in 1752 and pale orange for Russia and China in the early 1900s, above four small rising lines for the calendar, driving on the right, metrication and votes for women."}
assert len(meta["seo_description"]) < 160, len(meta["seo_description"])
visible_text_ok(_json.dumps(meta, ensure_ascii=False), "meta")
jsave(meta, f"{REL}/blog/meta.json", indent=2)

# Zenodo
Z = f"{REL}/zenodo"; os.makedirs(Z, exist_ok=True)
for fn in os.listdir(Z):
    os.remove(os.path.join(Z, fn))
shutil.copy(f"{REL}/paper/{NAME}.pdf", f"{Z}/{NAME}.pdf")
zp = f"{Z}/calendar-switch_data_and_code.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for d in ("code", "data", "data/source_tables"):
        for fn in sorted(os.listdir(os.path.join(ROOT, d))):
            p = os.path.join(ROOT, d, fn)
            if fn.endswith(".pyc") or fn == "__pycache__" or os.path.isdir(p):
                continue
            z.write(p, f"calendar-switch/{d}/{fn}")
    for fn in ("README.md", "LICENSE"):
        z.write(os.path.join(ROOT, fn), f"calendar-switch/{fn}")
    z.write(os.path.join(ROOT, "reddit", "collage.py"), "calendar-switch/reddit/collage.py")
    z.write(os.path.join(RAW, "wiki_pages.json"), "calendar-switch/raw/wiki_pages.json")
    z.write(os.path.join(RAW, "wiki_gregorian_list.json"), "calendar-switch/raw/wiki_gregorian_list.json")
tex = open(f"{REL}/paper/{NAME}.tex", encoding="utf-8").read()
ab = re.search(r"\\begin\{center\}\\textbf\{Abstract\}\\end\{center\}\n(.*?)\n\n\\textbf\{Keywords", tex, re.S).group(1)
ab = ab.replace("\\%", "%").replace("\\&", "&")
zmeta = {"title": "When Did Your Country Lose 11 Days? Four Great Switches, from the Gregorian Calendar to Votes for Women",
         "upload_type": "publication", "publication_type": "workingpaper",
         "description": f"<p>{ab}</p><p>Interactive version: <a href=\"{PAGE}\">{PAGE}</a>. Data and code: <a href=\"{REPO}\">{REPO}</a>. Blog post: {BLOG}.</p><p>Sources: English Wikipedia (CC BY-SA 4.0); the tables derived from it are released under CC BY-SA 4.0. Natural Earth (public domain).</p>",
         "creators": [{"name": "Hotham, Tristan", "affiliation": "Independent researcher", "orcid": "0000-0003-4931-9349"}],
         "keywords": ["Gregorian calendar", "calendar reform", "driving side", "left-hand traffic", "metrication", "women's suffrage", "diffusion", "standardisation", "historical geography", "Wikipedia", "open data", "maps"],
         "license": "cc-by-4.0", "language": "eng",
         "notes": "Code MIT; text and figures CC BY 4.0; data/source_tables, data/countries.csv and data/subnational.csv CC BY-SA 4.0 (derived from English Wikipedia).",
         "related_identifiers": [{"identifier": REPO, "relation": "isSupplementedBy", "resource_type": "software"},
                                 {"identifier": PAGE, "relation": "isSupplementedBy", "resource_type": "other"},
                                 {"identifier": "https://en.wikipedia.org/wiki/List_of_adoption_dates_of_the_Gregorian_calendar_by_country", "relation": "isDerivedFrom", "resource_type": "other"},
                                 {"identifier": "https://en.wikipedia.org/wiki/Adoption_of_the_Gregorian_calendar", "relation": "isDerivedFrom", "resource_type": "other"},
                                 {"identifier": "https://en.wikipedia.org/wiki/Left-_and_right-hand_traffic", "relation": "isDerivedFrom", "resource_type": "other"},
                                 {"identifier": "https://en.wikipedia.org/wiki/Metrication", "relation": "isDerivedFrom", "resource_type": "other"},
                                 {"identifier": "https://en.wikipedia.org/wiki/Women%27s_suffrage", "relation": "isDerivedFrom", "resource_type": "other"},
                                 {"identifier": "https://www.naturalearthdata.com/", "relation": "isDerivedFrom", "resource_type": "dataset"}],
         "files": sorted(os.listdir(Z))}
sj = _json.dumps(zmeta, ensure_ascii=False)
assert "\u2014" not in sj and "\u2013" not in sj and "--" not in sj
jsave(zmeta, f"{Z}/metadata.json", indent=2)
print("blog words", words, "figures", len(used), "; zenodo", sorted(os.listdir(Z)), os.path.getsize(zp) // 1024, "KB zip")
