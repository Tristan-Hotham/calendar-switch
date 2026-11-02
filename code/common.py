"""Shared paths, constants and helpers for the calendar-switch project ("When did your country lose 11 days?").

Raw inputs (read in place, never modified):
  raw/wiki_pages.json   Parsed English Wikipedia pages (HTML with revision ids), fetched in 2026. CC BY-SA 4.0.
      Used for the four switches:
        Adoption of the Gregorian calendar   prose by country (the per-country table has moved to a separate list
                                             article that is not in this file; see 01_parse.py)
        Gregorian calendar                   "Adoption by country" table (year, countries or areas) and the table of
                                             start of the numbered year and adoption year
        Julian calendar                      table of start of year and adoption of the new calendar
        Calendar (New Style) Act 1750, Old Style and New Style dates, Revised Julian calendar: context and checks
        Left- and right-hand traffic         "Worldwide distribution by country" table (side, date of switch, notes)
                                             and the prose on regional switches
        Dagen H                              Sweden's switch of 3 September 1967
        Metrication                          "Status by country/region" table (year official metrication process
                                             started, previous system, current status) and prose
        Metric system, Decimalisation        context
        Women's suffrage                     table of the year women first won the vote at national level, with notes
        Timeline of women's suffrage, Universal suffrage, Timeline of women's legal rights (other than voting):
                                             context and checks
        Daylight saving time by country, Coordinated Universal Time, Time zone: context only
      One requested page ("List of countries by date of adoption of decimal currency") does not exist and is recorded
      as missing.
  /home/claude/newdata/raw/geo/ne_50m_admin_0_countries.geojson   Natural Earth countries (public domain)
  /home/claude/newdata/raw/geo/ne_10m_admin_1_states_provinces.geojson   Natural Earth states and provinces
  /home/claude/newdata/raw/geo/ne_10m_populated_places_simple.geojson   Natural Earth places (for point positions)
"""
import json, gzip, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.environ.get("CS_RAW", os.path.join(ROOT, "raw"))
GEO = os.environ.get("CS_GEO", "/home/claude/newdata/raw/geo")
FONTS = os.environ.get("CS_FONTS", "/home/claude/ref/fonts")
DATA = os.path.join(ROOT, "data")
WORK = os.path.join(os.environ.get("CSTMP", "/dev/shm/calendarswitch"), "work")   # intermediates live in memory, not in the repo
for d in (DATA, WORK):
    os.makedirs(d, exist_ok=True)

SLUG = "calendar-switch"
PAGE = f"https://maps.tristanhotham.com/{SLUG}/"
REPO = f"https://github.com/Tristan-Hotham/{SLUG}"
DOI = "10.5281/zenodo.23873009"                # filled in by the publisher
BLOG = "https://blog.tristanhotham.com/2026/10/31/calendar-switch/"          # filled in by the publisher
AI = ("I wrote the text, with drafting and editing assistance from Claude (Anthropic), which also helped "
      "prepare the analysis code. I reviewed and checked all text and results.")
NOW = 2026                     # the year of the Wikipedia snapshot
Y0 = 1580                      # first year on the slider

# the four switches. key, tab label, short name, colour of "switched", colour of "not yet"
SWITCHES = [
    ("cal", "Calendar", "Gregorian calendar", "#B4432F"),
    ("road", "Driving side", "Driving on the right", "#2F5FA7"),
    ("metric", "Metric", "Metric system", "#2E8A6E"),
    ("vote", "Votes for women", "Women voting", "#7A4FA0"),
]
SW = {k: (lab, nm, c) for k, lab, nm, c in SWITCHES}
LHT_C, RHT_C = "#D08A2E", "#2F5FA7"     # driving: left, right

WIKI_URL = lambda t: "https://en.wikipedia.org/wiki/" + t.replace(" ", "_")


def jload(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def dash(v):
    """Remove em and en dashes and double hyphens from text (house style)."""
    if isinstance(v, str):
        v = re.sub(r"(\d)\s*[–—]\s*(\d)", r"\1 to \2", v)
        v = v.replace(" — ", ", ").replace("—", ", ").replace(" – ", ", ").replace("–", "-").replace("−", "-")
        while "--" in v:
            v = v.replace("--", "-")
        return v
    if isinstance(v, list):
        return [dash(x) for x in v]
    if isinstance(v, dict):
        return {k: dash(x) for k, x in v.items()}
    return v


def jsave(obj, path, indent=None):
    if os.path.abspath(path).startswith(DATA):
        obj = dash(obj)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent, separators=None if indent else (",", ":"))


def norm(s):
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    return re.sub(r"[\W_]+", " ", s).strip()


def get(R, path):
    v = R
    for k in path.split("."):
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


def fmt(v, f=None):
    if f is None or f == "raw": return str(v)
    if f == "int": return f"{round(float(v)):,}"
    if f == "pc": return f"{round(float(v))}%"
    if f == "pc1": return f"{float(v):.1f}%"
    if f == "f1": return f"{float(v):.1f}"
    if f == "f2": return f"{float(v):.2f}"
    if f == "bn": return f"{float(v) / 1e9:.1f} billion"
    if f == "mn": return f"{round(float(v) / 1e6):,} million"
    raise ValueError(f)


KEEP = ("DOI", "BLOG_URL", "DOI_URL")


def fill(text, R, keep=KEEP):
    """Replace {{path|format}} tokens with values from results.json; leave publisher placeholders and IMG tokens alone."""
    def rep(m):
        if m.group(1) in keep or m.group(1).startswith("IMG"):
            return m.group(0)
        return fmt(get(R, m.group(1)), m.group(3))
    return re.sub(r"\{\{([^}|]+)(\|(\w+))?\}\}", rep, text)


def visible_text_ok(s, where=""):
    for bad in ("—", "–", "--", "DSIT", "DCMS", "civil serv", "Civil Serv"):
        assert bad not in s, (where, bad, s[max(0, s.find(bad) - 80):s.find(bad) + 80])


def wiki(title):
    return jload(os.path.join(RAW, "wiki_pages.json"))[title]
