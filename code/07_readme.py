"""Step 7. README.md, LICENSE and reddit/post.md, with numbers from data/results.json. 10.5281/zenodo.23873009 and https://blog.tristanhotham.com/2026/10/31/calendar-switch/ stay as
placeholders for the publisher."""
from common import *

R = jload(f"{DATA}/results.json")
s, C, D, M, V = R["source"], R["cal"], R["road"], R["metric"], R["vote"]
N = lambda v: f"{round(v):,}"
readme = f"""# When did your country lose 11 days? Four great switches, mapped

A world map, in time, of four switches most countries have made: from the Julian to the Gregorian calendar (and how many days each dropped), changes of driving side, the start of metrication, and the year women first won the national vote, with the date on equal terms where the source separates it. Built from the tables and prose of {s['pages']} English Wikipedia articles, matched to today's {s['n_countries']} countries and to provinces, cantons and states where the sources give them.

Interactive page: {PAGE}
Paper: https://doi.org/{DOI}
Blog post: {BLOG}

## Headline results

- Calendar: the primary source is Wikipedia's list of {C['gl_rows']} historic areas with their switch dates, checked against two adoption tables and the main article's prose ({C['n_disagree']} differences recorded). Together they date the switch for {C['n_with_year']} of today's countries ({C['n_colonial']} through the colonial power that then ruled them), from Catholic Europe and its colonies in 1582 to Saudi Arabia's civil switch in 2016, {C['span']} years later. Parts of {C['days']['10']} countries dropped 10 dates, of {C['days']['11']} dropped 11 (Britain and its colonies, Wednesday 2 September 1752 followed by Thursday 14 September; Denmark and Norway on 1 March 1700), of two dropped 12 (Switzerland's last communes in 1812 and Uganda in 1894) and of {C['days']['13']} dropped 13 (the Orthodox east and the Caucasus, 1915 to 1923). {C['n_nonjulian']} came from other calendars; {', '.join(C['never'][:-1])} and {C['never'][-1]} have not adopted it. The list records {C['n_returns']} returns to the Julian calendar (Sweden's 30 February 1712, Lorraine 1735, the Lithuanian lands 1800 and others), and France used its Republican calendar from 1793 to 1805.
- Driving side: {D['n_switched']} countries have a dated switch, {D['n_to_R']} to the right and {D['n_to_L']} to the left (Namibia 1920, Timor-Leste 1976, Samoa 2009). The busiest decade was the {D['top_decade']}s ({D['top_decade_n']} switches). Today {D['n_L']} countries, with {D['pop_L']:.1f}% of the world's people, drive on the left; in Europe only {', '.join(D['europe_L'][:-1])} and the {D['europe_L'][-1]}.
- Metric: {M['n_dated']} countries dated, from France (1795) to {M['last'][0][0]} ({M['last'][0][1]}); median start {M['median']}. Listed as still using other units officially: {', '.join(M['mixed'][:-1])} and {M['mixed'][-1]}.
- Votes for women: New Zealand first (1893); {V['n_by1918']} countries by 1918, half of today's countries by {V['half_n_year']}; the last was Saudi Arabia (2015, municipal elections). {V['n_two']} countries have separate years for a restricted first vote and equal terms (the United Kingdom 1918 and 1928). Eritrea and Vatican City hold no elections.

## Files

| File | What it is |
|---|---|
| `index.html` | The interactive page (built by `code/04_build_site.py`; all data embedded). |
| `header.png` | Social card, 1200 x 630. |
| `data/countries.csv` | One row per country or territory drawn: for each switch the status, year(s), timeline, date text, days dropped, notes, stand in notes and source. |
| `data/subnational.csv` | Provinces, cantons, states and other sub-national units the sources date, by switch. |
| `data/adoption_curves.csv` | For each year 1580 to {NOW}, the number of today's countries and share of today's population that had made each switch. |
| `data/source_tables/*.csv` | The seven Wikipedia tables exactly as parsed, including the calendar list (`greg_list.csv`) (CC BY-SA 4.0). |
| `data/results.json` | Every number used in the page, paper, blog, collage and post. |
| `data/site.json`, `data/world.json`, `data/subunits.json` | Page data. |
| `code/` | Scripts, run in order (below), the hand mapping (`polities.py`) and the page, paper and blog templates. |
| `release/` | Paper PDF and LaTeX source with figures (`paper/`), blog post, figures and meta (`blog/`), Zenodo files (`zenodo/`). |
| `reddit/` | Collage (`collage.py`, PNG) and post text. |
| `qa/` | Screenshots of the page at desktop and phone widths. |

## Method in brief

- Sources: "List of adoption dates of the Gregorian calendar by country" (primary calendar source), "Gregorian calendar" (adoption table; start of year table), "Julian calendar" (start of year table), "Adoption of the Gregorian calendar" (prose), "Calendar (New Style) Act 1750", "Left- and right-hand traffic" (country table and prose), "Dagen H", "Metrication" (status table and prose), "Women's suffrage" (table). Revision numbers are in `data/results.json` and the paper.
- Matching: by name to Natural Earth countries; historical states drawn with modern stand ins (flagged). Colonies in the Americas and the Philippines are dated by their colonial power for the calendar (my mapping, from the table's "and colonies thereof").
- Days dropped: the list's number of dates omitted, which matches the rule (10 before March 1700, 11 to February 1800, 12 to February 1900, 13 after, read at the first new style day) for every row except Alaska, where the date line moved. A country year is the start of the last unbroken period with the whole of today's country Gregorian.
- Driving: the table's date of switch, with earlier years on the other side; no date means today's side throughout (an assumption); dates with no described change flagged.
- Metric: the year the official process started. Votes: first national vote at all, and equal or full terms where the table gives a separate year.
- Caveats: Wikipedia tables, partly unsourced; many countries undated for the calendar and metric; population weights are today's.

## How to rerun

Needs Python 3 with numpy, pandas, shapely, pyproj, matplotlib, beautifulsoup4, lxml and fontTools, xelatex and pdftotext; node with Playwright for `code/qa.js`. Raw input: `raw/wiki_pages.json` and `raw/wiki_gregorian_list.json` (the calendar list article); Natural Earth in `/home/claude/newdata/raw/geo/` (set `CS_GEO`). Intermediate files go to `/dev/shm/calendarswitch/work` (set `CSTMP`).

```
python3 code/01_parse.py        # read the Wikipedia tables and text
python3 code/02_geo.py          # outlines, today's countries, sub-national units
python3 code/03_results.py      # match, timelines, results.json, data tables, page data
python3 code/04_build_site.py   # index.html
python3 code/05_figures.py      # header, blog and paper figures
python3 code/06_paper.py        # paper PDF
python3 reddit/collage.py       # collage
python3 code/07_readme.py       # README, LICENSE, Reddit post
python3 code/08_release.py      # blog post, Zenodo files
```

## Sources and licences

- English Wikipedia contributors, the {s['pages']} articles listed in the paper, revisions of 2026. CC BY-SA 4.0. The tables derived from them (`data/source_tables/`, `data/countries.csv`, `data/subnational.csv`) are released under CC BY-SA 4.0.
- Natural Earth countries and states and provinces (https://www.naturalearthdata.com/). Public domain.
- Optional relief shading on the page: Esri.

## Citation

Hotham, T. (2026) When did your country lose 11 days? Four great switches, from the Gregorian calendar to votes for women. Zenodo. https://doi.org/{DOI}

Dr Tristan Hotham, Independent researcher. ORCID 0000-0003-4931-9349.

{AI}
"""
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(readme)

lic = open("/home/claude/studies/rocket-launches/LICENSE", encoding="utf-8").read().split("\n\n\nThis licence covers")[0]
lic += """


This licence covers the code in code/, reddit/collage.py and the page scripts.

The text of the page, paper and blog post, the figures and the derived data
files in data/ that do not come from Wikipedia (results.json,
adoption_curves.csv, site.json page data apart from quoted notes, world.json,
subunits.json) are released under the Creative Commons Attribution 4.0
International licence (CC BY 4.0).

The tables derived from English Wikipedia (data/source_tables/*.csv,
data/countries.csv, data/subnational.csv, and the notes quoted from Wikipedia
in site.json) are released under the Creative Commons Attribution-ShareAlike
4.0 International licence (CC BY-SA 4.0), as the Wikipedia text they come from
is. Credit: "Wikipedia contributors, English Wikipedia, CC BY-SA 4.0", with the
article names and revision numbers given in README.md and the paper.

Natural Earth is public domain.
"""
open(os.path.join(ROOT, "LICENSE"), "w", encoding="utf-8").write(lic)

post = f"""## Title

[OC] When did your country lose 11 days? The year every country switched to the Gregorian calendar, from Rome in 1582 to Saudi Arabia in 2016, plus three other great switches: driving side, metric and votes for women

## Body

In 1752 Britain and its colonies went to bed on Wednesday 2 September and woke on Thursday 14 September. Catholic Europe had made the same jump in 1582; Russia waited until 1918 (which is why the October Revolution is in November), Greece until 1923. I mapped the year each country switched, and how many dates it dropped: 10 in Catholic Europe, 11 in Britain and its colonies, 13 in the Orthodox east; only Switzerland's last communes and Uganda dropped 12. Sweden tried to do it gradually, botched it, and had to add a 30 February in 1712; France ditched it for its Republican calendar from 1793 to 1805. The same map has three more switches: the side of the road ({D['n_switched']} dated switches, all but {D['n_to_L']} to the right; Sweden's Dagen H in 1967, Samoa to the left in 2009), metrication (France 1795 to {M['last'][0][0]} {M['last'][0][1]}) and votes for women (New Zealand 1893 to Saudi Arabia 2015). Caveats: the calendar data date {C['n_with_year']} of {s['n_countries']} countries; many others use the Gregorian calendar today but the sources give no year. Interactive map with a play button: {PAGE}

## Source comment

Source: English Wikipedia (CC BY-SA 4.0), revisions of 2026: "List of adoption dates of the Gregorian calendar by country", checked against the adoption tables in "Gregorian calendar" and "Julian calendar" and the prose of "Adoption of the Gregorian calendar"; the country table in "Left- and right-hand traffic"; the status table in "Metrication"; the table in "Women's suffrage". Matched to today's countries with Natural Earth outlines. Colonies in the Americas dated by their colonial power for the calendar (the table's "and colonies thereof").

Tools: Python (pandas, BeautifulSoup, shapely, pyproj, matplotlib); MapLibre for the interactive map.

Interactive version: {PAGE}
Paper: https://doi.org/{DOI}
Blog post: {BLOG}
"""
for t in (readme, post, lic):
    for bad in ("—", "–", "--", "DSIT", "DCMS"):
        assert bad not in t.replace("```", "").replace("|---|---|", ""), bad
open(os.path.join(ROOT, "reddit", "post.md"), "w", encoding="utf-8").write(post)
print("readme, licence, post ok")
