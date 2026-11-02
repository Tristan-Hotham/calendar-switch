"""Step 1. Read the Wikipedia pages in raw/wiki_pages.json and pull out the tables and prose that the study uses.

Tables are read cell by cell with rowspan and colspan expanded, footnote markers (sup.reference) removed and the
"citation needed" tags recorded as a flag. Each table is checked against its header so that a change in the page
layout stops the build. The tables are written verbatim to data/source_tables/*.csv (CC BY-SA 4.0, see LICENSE) and
to WORK/tables.json; the plain text of every page goes to WORK/text.json, for the checks in later steps.

Tables used:
  greg_years     Gregorian calendar, "Adoption by country": Year | Countries / Areas
  greg_newyear   Gregorian calendar: Country | Start numbered year on 1 January | Adoption of Gregorian calendar
  jul_newyear    Julian calendar: Country | Year starting 1 January | Adoption of new calendar
  traffic        Left- and right-hand traffic, "Worldwide distribution by country":
                 group | Country | Road traffic | Date of switch | Notes, exceptions
  metric         Metrication, "Status by country/region": Year official metrication process started | Country/Region |
                 Previous system of measure | Current official status of metrication
  suffrage       Women's suffrage: Country | Year women first granted suffrage at national level | Notes
  greg_list      List of adoption dates of the Gregorian calendar by country (raw/wiki_gregorian_list.json, the article
                 "Adoption of the Gregorian calendar" points to): Present country | Historic area | Year | Date of the last
                 day before the change | Date of the first day after the change | Number of dates omitted | Particulars |
                 Source. This is the primary calendar source; the other tables and the prose are cross-checks.
The same raw file also holds "List of calendars", which is not used."""
import csv
from bs4 import BeautifulSoup
from common import *

PAGES = jload(os.path.join(RAW, "wiki_pages.json"))
LIST = jload(os.path.join(RAW, "wiki_gregorian_list.json"))   # fetched separately: the per-country list the Adoption article points to
LT = "List of adoption dates of the Gregorian calendar by country"
PAGES[LT] = LIST["parse:" + LT]


def soup(title):
    return BeautifulSoup(PAGES[title]["html"], "lxml")


def cell_text(c):
    c = BeautifulSoup(str(c), "lxml")
    cn = bool(c.select("sup.Template-Fact, sup.noprint")) or "citation needed" in c.get_text(" ").lower()
    for s in c.select("sup, style, .sortkey, span[style*='display:none'], .mw-ref"):
        s.decompose()
    for br in c.find_all("br"):
        br.replace_with(" | ")
    t = re.sub(r"\s+", " ", c.get_text(" ")).replace(" ,", ",").replace("( ", "(").replace(" )", ")").strip()
    t = re.sub(r"\s*\|\s*$", "", re.sub(r"^\s*\|\s*", "", t))
    return t, cn


def grid(t):
    rows, span = [], {}
    for tr in t.find_all("tr"):
        if tr.find_parent("table") is not t:
            continue
        row, ci = [], 0
        cells = iter([c for c in tr.find_all(["td", "th"]) if c.find_parent("tr") is tr])
        while True:
            if (len(rows), ci) in span:
                row.append(span.pop((len(rows), ci))); ci += 1; continue
            c = next(cells, None)
            if c is None:
                break
            tx = cell_text(c)
            rs = int(re.sub(r"\D", "", c.get("rowspan", "1")) or 1); cs = int(re.sub(r"\D", "", c.get("colspan", "1")) or 1)
            for _ in range(cs):
                row.append(tx)
                for r in range(1, rs):
                    span[(len(rows) + r, ci)] = tx
                ci += 1
        while (len(rows), ci) in span:
            row.append(span.pop((len(rows), ci))); ci += 1
        rows.append(row)
    return rows


def wikitables(title):
    return [t for t in soup(title).find_all("table") if "wikitable" in (t.get("class") or [])]


def find(title, header_start):
    for t in wikitables(title):
        g = grid(t)
        if g and [c[0].replace(" | ", " ") for c in g[0]][:len(header_start)] == header_start:
            return g
    raise AssertionError((title, header_start))


SPEC = {
    "greg_years": ("Gregorian calendar", ["Year", "Countries / Areas"]),
    "greg_newyear": ("Gregorian calendar", ["Country", "Start numbered year on 1 January", "Adoption of Gregorian calendar"]),
    "jul_newyear": ("Julian calendar", ["Country", "Year starting 1 January", "Adoption of new calendar"]),
    "traffic": ("Left- and right-hand traffic", ["Country", "Country", "Road traffic", "Date of switch", "Notes, exceptions"]),
    "metric": ("Metrication", ["Year official metrication process started", "Country/Region", "Previous system of measure", "Current official status of metrication"]),
    "suffrage": ("Women's suffrage", ["Country", "Year women first granted suffrage at national level", "Notes"]),
    "greg_list": (LT, ["Present country", "Historic area", "Year", "Date of the last day before the change", "Date of the first day after the change", "Number of dates omitted", "Particulars", "Source"]),
}
T = {}
os.makedirs(os.path.join(DATA, "source_tables"), exist_ok=True)
for k, (title, head) in SPEC.items():
    g = find(title, head)
    rows = [[c[0] for c in r] for r in g[1:]]
    cn = [any(c[1] for c in r) for r in g[1:]]
    T[k] = {"page": title, "revid": PAGES[title]["revid"], "header": head, "rows": rows, "citation_needed": cn}
    with open(os.path.join(DATA, "source_tables", f"{k}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(head + ["citation_needed"])
        for r, c in zip(rows, cn):
            w.writerow([dash(x) for x in r] + [int(c)])

# sizes the later steps rely on (a change in the pages should stop the build here)
N = {k: len(v["rows"]) for k, v in T.items()}
assert N == {"greg_years": 20, "greg_newyear": 16, "jul_newyear": 16, "traffic": 231, "metric": 77, "suffrage": 199, "greg_list": 146}, N


def text_of(title):
    s = soup(title)
    for x in s.select("style, sup.reference, .mw-editsection, .navbox, table.ambox"):
        x.decompose()
    return re.sub(r"\s+", " ", s.get_text(" ")).replace("\xa0", " ").strip()


TXT = {t: text_of(t) for t in PAGES if "html" in PAGES[t]}
missing = [t for t in PAGES if "html" not in PAGES[t]]
assert missing == ["List of countries by date of adoption of decimal currency"], missing
assert "List of adoption dates of the Gregorian calendar per country" in PAGES["Adoption of the Gregorian calendar"]["html"].replace("_", " ")
REV = {t: PAGES[t]["revid"] for t in PAGES if "revid" in PAGES[t]}
jsave(T, f"{WORK}/tables.json")
jsave({"text": TXT, "revid": REV, "missing": missing}, f"{WORK}/text.json")
print("tables", N, "pages", len(TXT), "missing", missing)
