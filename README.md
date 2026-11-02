# When did your country lose 11 days? Four great switches, mapped

A world map, in time, of four switches most countries have made: from the Julian to the Gregorian calendar (and how many days each dropped), changes of driving side, the start of metrication, and the year women first won the national vote, with the date on equal terms where the source separates it. Built from the tables and prose of 19 English Wikipedia articles, matched to today's 197 countries and to provinces, cantons and states where the sources give them.

Interactive page: https://maps.tristanhotham.com/calendar-switch/
Paper: https://doi.org/10.5281/zenodo.23873009
Blog post: https://blog.tristanhotham.com/2026/10/31/calendar-switch/

## Headline results

- Calendar: the primary source is Wikipedia's list of 146 historic areas with their switch dates, checked against two adoption tables and the main article's prose (19 differences recorded). Together they date the switch for 82 of today's countries (27 through the colonial power that then ruled them), from Catholic Europe and its colonies in 1582 to Saudi Arabia's civil switch in 2016, 434 years later. Parts of 45 countries dropped 10 dates, of 19 dropped 11 (Britain and its colonies, Wednesday 2 September 1752 followed by Thursday 14 September; Denmark and Norway on 1 March 1700), of two dropped 12 (Switzerland's last communes in 1812 and Uganda in 1894) and of 19 dropped 13 (the Orthodox east and the Caucasus, 1915 to 1923). 11 came from other calendars; Afghanistan, Ethiopia, Iran and Nepal have not adopted it. The list records 8 returns to the Julian calendar (Sweden's 30 February 1712, Lorraine 1735, the Lithuanian lands 1800 and others), and France used its Republican calendar from 1793 to 1805.
- Driving side: 62 countries have a dated switch, 59 to the right and 3 to the left (Namibia 1920, Timor-Leste 1976, Samoa 2009). The busiest decade was the 1920s (16 switches). Today 54 countries, with 35.6% of the world's people, drive on the left; in Europe only Cyprus, Ireland, Malta and the United Kingdom.
- Metric: 73 countries dated, from France (1795) to Samoa (2015); median start 1920. Listed as still using other units officially: Canada, Liberia, Myanmar, United Kingdom and United States.
- Votes for women: New Zealand first (1893); 23 countries by 1918, half of today's countries by 1951; the last was Saudi Arabia (2015, municipal elections). 18 countries have separate years for a restricted first vote and equal terms (the United Kingdom 1918 and 1928). Eritrea and Vatican City hold no elections.

## Files

| File | What it is |
|---|---|
| `index.html` | The interactive page (built by `code/04_build_site.py`; all data embedded). |
| `header.png` | Social card, 1200 x 630. |
| `data/countries.csv` | One row per country or territory drawn: for each switch the status, year(s), timeline, date text, days dropped, notes, stand in notes and source. |
| `data/subnational.csv` | Provinces, cantons, states and other sub-national units the sources date, by switch. |
| `data/adoption_curves.csv` | For each year 1580 to 2026, the number of today's countries and share of today's population that had made each switch. |
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

- English Wikipedia contributors, the 19 articles listed in the paper, revisions of 2026. CC BY-SA 4.0. The tables derived from them (`data/source_tables/`, `data/countries.csv`, `data/subnational.csv`) are released under CC BY-SA 4.0.
- Natural Earth countries and states and provinces (https://www.naturalearthdata.com/). Public domain.
- Optional relief shading on the page: Esri.

## Citation

Hotham, T. (2026) When did your country lose 11 days? Four great switches, from the Gregorian calendar to votes for women. Zenodo. https://doi.org/10.5281/zenodo.23873009

Dr Tristan Hotham, Independent researcher. ORCID 0000-0003-4931-9349.

I wrote the text, with drafting and editing assistance from Claude (Anthropic), which also helped prepare the analysis code. I reviewed and checked all text and results.
