"""Hand decisions: how the polities named in the Wikipedia tables and prose map to today's countries (Natural Earth
ISO 3 codes) and sub-national units (ISO 3166-2 codes in Natural Earth admin 1), and what each source says.

Source keys used in the 'src' fields:
  GT   Gregorian calendar, table "Adoption by country" (year, countries or areas)
  GN   Gregorian calendar, table of the start of the numbered year and the adoption of the Gregorian calendar
  JN   Julian calendar, table of the start of the year and the adoption of the new calendar
  AG   Adoption of the Gregorian calendar (prose, by country)
  ACT  Calendar (New Style) Act 1750 (prose)
  LR   Left- and right-hand traffic: table "Worldwide distribution by country" (LRT) and prose (LRP)
  DH   Dagen H
  MT   Metrication: table "Status by country/region" (MTT) and prose (MTP)
  WS   Women's suffrage: table (WST)
Where a historical polity is drawn with a modern border, the entry carries a 'standin' note saying so.

Calendar states: J old calendar (Julian or another), S the separate Swedish calendar (1700 to 1712), P part of
today's country on the Gregorian calendar, G Gregorian. A timeline is a list of (year, state) changes from 'init'.
Status: dated (the sources give the year), colonial (the table's "and colonies thereof" or "First British Empire",
applied by me to the territories those powers then ruled; listed below), standin, never (one of the four countries the
article says have not adopted it), undated (not named: the article says the Gregorian calendar is now the civil
calendar of the vast majority of countries, but gives no year)."""

# ----------------------------------------------------------------------------------------------- calendar
C1582 = "Thursday 4 October 1582 was followed by Friday 15 October 1582"
CAL = {
    "ESP": dict(tl=[(1582, "G")], date=C1582, src="GT 1582 Spain; AG Philip II's decree"),
    "PRT": dict(tl=[(1582, "G")], date=C1582, src="GT 1582 Portugal; AG"),
    "ITA": dict(tl=[(1582, "G")], date=C1582, src="GT 1582 Italy; GN Papal States, Venice and Tuscany 1582",
                note="The Papal States, Venice, Tuscany and Spain's Italian lands all switched in 1582."),
    "VAT": dict(tl=[(1582, "G")], date=C1582, src="AG: the Papal States", standin="The Papal States stand in for Vatican City."),
    "POL": dict(tl=[(1582, "G")], date=C1582, src="GT 1582 Polish-Lithuanian Commonwealth; AG",
                note="The Commonwealth switched back after the Third Partition of Poland in 1795 (AG); the sources give no later date for Poland.",
                standin="The Polish-Lithuanian Commonwealth is drawn with today's Poland."),
    "LTU": dict(tl=[(1582, "G"), (1795, "J"), (1915, "G")], date="1582 with the Commonwealth; again in 1915", src="GT 1582 Commonwealth, 1915 Lithuania; AG switch back in 1795",
                note="Part of the Polish-Lithuanian Commonwealth, which switched in 1582 and back after the Third Partition in 1795; Gregorian again from 1915 (GT).",
                standin="The Grand Duchy of Lithuania is drawn with today's Lithuania."),
    "UKR": dict(tl=[(1582, "P"), (1795, "J"), (1918, "G")], date="1582 in the Commonwealth's lands; 1918 with Russia", src="AG Ukraine; GT 1918 Ukraine",
                note="Most of Ukraine was then in the Polish-Lithuanian Commonwealth, which adopted the calendar in 1582 and switched back in 1795 (AG). GT gives 1918."),
    "LUX": dict(tl=[(1582, "G")], src="GT 1582 Luxembourg"),
    "FRA": dict(tl=[(1582, "G")], date="Sunday 9 December 1582 was followed by Monday 20 December 1582", src="GT 1582 France; AG",
                note="Alsace followed in 1648 and Strasbourg in 1682 (GT); for Lorraine GN gives 1582 and JN 1760."),
    "BEL": dict(tl=[(1582, "P"), (1583, "G")], date="25 December 1582 in the Duchy of Brabant, 1 January 1583 in the rest", src="AG; GN Southern Netherlands 1582",
                standin="The Duchy of Brabant is drawn with the provinces of Antwerp, Flemish Brabant, Walloon Brabant and Brussels."),
    "NLD": dict(tl=[(1582, "P"), (1701, "G")], date="Brabant and Zeeland on 25 December 1582, Holland on 12 January 1583, the last province (Drenthe) on 12 May 1701",
                src="AG; GT 1582 Catholic Low Countries, 1700 Protestant Low Countries; JN",
                note="Seven dates, province by province. Limburg and Flevoland are not named (Flevoland is reclaimed land)."),
    "CHE": dict(tl=[(1584, "P"), (1812, "G")], date="The seven Catholic cantons in January 1584; Geneva and several Protestant cantons in January 1701; the communes of Schiers and Grüsch in 1812",
                src="AG; GT 1584 some Catholic Swiss cantons, 1700 some Protestant Swiss cantons",
                note="Schiers and Grüsch were the last places in western and central Europe to switch (AG)."),
    "CZE": dict(tl=[(1584, "G")], src="GT 1584 Bohemia", standin="Bohemia is drawn with today's Czechia."),
    "DEU": dict(tl=[(1583, "P"), (1700, "G")], date="Catholic states 1583 (GN; JN gives 1582); Protestant states Sunday 18 February 1700, followed by Monday 1 March 1700 (AG)",
                src="GN; JN; AG; GT 1610 Prussia", note="The Duchy of Prussia, a Polish fief, switched in 1610 (GT) or 1612 (AG): 22 August was followed by 2 September 1612."),
    "AUT": dict(tl=[(1583, "G")], src="GN Holy Roman Empire (Catholic states) 1583; JN 1582",
                standin="Austria stands in for the Catholic states of the Holy Roman Empire, which the tables do not list one by one."),
    "DNK": dict(tl=[(1700, "G")], date="Sunday 18 February 1700 was followed by Monday 1 March 1700", src="GT 1700 Denmark-Norway; GN Denmark 1700; AG"),
    "NOR": dict(tl=[(1700, "G")], date="Sunday 18 February 1700 was followed by Monday 1 March 1700", src="GT 1700 Denmark-Norway; AG", standin="Part of Denmark-Norway."),
    "ISL": dict(tl=[(1700, "G")], date="Sunday 18 February 1700 was followed by Monday 1 March 1700", src="GT 1700 Denmark-Norway",
                standin="Iceland was ruled from Copenhagen as part of Denmark-Norway; it is not named separately."),
    "GBR": dict(tl=[(1752, "G")], date="Wednesday 2 September 1752 was followed by Thursday 14 September 1752", src="GT 1752 Great Britain; ACT; AG",
                note="The same Act moved New Year's Day from 25 March to 1 January (Scotland had done so in 1600)."),
    "IRL": dict(tl=[(1752, "G")], date="Wednesday 2 September 1752 was followed by Thursday 14 September 1752", src="GT 1752 Ireland; ACT",
                note="Applied at once in practice; the Irish Parliament confirmed it in 1782 (ACT)."),
    "IMN": dict(tl=[(1752, "G")], date="Observed from 1752; Tynwald's own act followed in 1753", src="ACT, Isle of Man"),
    "USA": dict(tl=[(1752, "G")], date="Wednesday 2 September 1752 was followed by Thursday 14 September 1752 in the British colonies", src="ACT, America; AG; GT 1752 First British Empire",
                note="New Spain and New France, which covered much of what is now the southern and central United States, had switched in 1582 (AG). Alaska switched in 1867.",
                standin="The Thirteen Colonies are drawn with today's United States."),
    "CAN": dict(tl=[(1582, "P"), (1752, "G")], date="New France in 1582; the British colonies in 1752", src="AG Americas; ACT",
                standin="New France is drawn with today's Quebec; the British colonies with the rest of Canada, much of which was not yet a colony."),
    "SWE": dict(tl=[(1700, "S"), (1712, "J"), (1753, "G")], date="Wednesday 17 February 1753 was followed by Thursday 1 March 1753",
                src="AG Sweden; GT 1753 Sweden, including Finland",
                note="From 1700 Sweden planned to drop eleven leap days over forty years, missed two, gave up and went back to the Julian calendar by adding 30 February 1712. It finally switched in 1753."),
    "FIN": dict(tl=[(1700, "S"), (1712, "J"), (1753, "G")], date="Wednesday 17 February 1753 was followed by Thursday 1 March 1753", src="AG Sweden; GT 1753 Sweden, including Finland",
                note="Part of Sweden then. Under Russian rule from 1809 official papers carried both styles of date until independence in 1917."),
    "RUS": dict(tl=[(1918, "G")], date="Wednesday 31 January 1918 was followed by Thursday 14 February 1918", src="GT 1918 Russia; AG",
                note="Since the switch the October Revolution of 25 October 1917 (Julian) falls on 7 November."),
    "EST": dict(tl=[(1918, "G")], src="GT 1918 Estonia"),
    "LVA": dict(tl=[(1915, "G")], src="GT 1915 Latvia"),
    "BGR": dict(tl=[(1916, "G")], date="31 March 1916 was followed by 14 April 1916", src="GT 1916 Bulgaria; AG"),
    "TUR": dict(tl=[(1917, "P"), (1926, "G")], date="Ottoman fiscal (Rumi) dates realigned on 1 March 1917; the Gregorian calendar in full from 1 January 1926",
                src="GT 1917 Ottoman Empire, 1926 Turkey; JN Ottoman Empire 1917; AG", standin="The Ottoman Empire is drawn with today's Turkey."),
    "ROU": dict(tl=[(1919, "G")], date="31 March 1919 was followed by 14 April 1919", src="GT 1919 Romania; AG"),
    "SRB": dict(tl=[(1919, "G")], src="GT 1919 Yugoslavia; JN 1918 Serbia", note="JN gives 1918 for Serbia.", standin="Yugoslavia (GT) is drawn with its successor states."),
    "MNE": dict(tl=[(1919, "G")], src="GT 1919 Yugoslavia", standin="Yugoslavia (GT) is drawn with its successor states."),
    "MKD": dict(tl=[(1919, "G")], src="GT 1919 Yugoslavia", standin="Yugoslavia (GT) is drawn with its successor states."),
    "BIH": dict(tl=[(1919, "G")], src="GT 1919 Yugoslavia", standin="Yugoslavia (GT) is drawn with its successor states."),
    "KOS": dict(tl=[(1919, "G")], src="GT 1919 Yugoslavia", standin="Yugoslavia (GT) is drawn with its successor states."),
    "GRC": dict(tl=[(1923, "G")], date="Wednesday 15 February 1923 was followed by Thursday 1 March 1923", src="GT 1923 Greece; AG",
                note="The last country of Orthodox Europe to switch, for civil purposes only; the Church kept its own calendar (AG)."),
    "ALB": dict(tl=[(1912, "G")], prev="not stated", src="GT 1912 Albania"),
    "EGY": dict(tl=[(1875, "G")], prev="not stated", src="GT 1875 Egypt"),
    "JPN": dict(tl=[(1873, "G")], prev="lunisolar", date="The second day of the twelfth month of Meiji 5 was followed by 1 January 1873", src="GT 1873 Japan; AG"),
    "KOR": dict(tl=[(1896, "G")], prev="lunisolar", date="1 January 1896", src="GT 1896 Korea; AG", standin="Korea is drawn with today's North and South Korea."),
    "PRK": dict(tl=[(1896, "G")], prev="lunisolar", date="1 January 1896", src="GT 1896 Korea; AG", standin="Korea is drawn with today's North and South Korea."),
    "CHN": dict(tl=[(1912, "G")], prev="lunisolar", date="1 January 1912, at the founding of the Republic; enforced by the Nationalist government from 1 January 1929", src="GT 1912 China; AG"),
    "VNM": dict(tl=[(1954, "G")], prev="lunisolar", src="AG Southeast Asia"),
    "KHM": dict(tl=[(1863, "G")], prev="lunisolar", src="AG Southeast Asia"),
    "LAO": dict(tl=[(1889, "G")], prev="lunisolar", src="AG Southeast Asia"),
    "THA": dict(tl=[(1889, "G")], prev="lunisolar", src="AG Southeast Asia", note="Siam switched in 1889, counting years in the Rattanakosin Era."),
    "MMR": dict(tl=[(1886, "G")], prev="lunisolar", src="AG Southeast Asia", note="Used alongside the Burmese calendar since the British conquest of 1886."),
    "SAU": dict(tl=[(2016, "G")], prev="lunar", date="For public sector pay from 1 October 2016", src="GT 2016 Saudi Arabia; AG Islamic calendar",
                note="The Islamic calendar is kept for religious purposes."),
    "ETH": dict(status="never", src="AG Present situation", note="Uses the Ethiopian calendar."),
    "NPL": dict(status="never", src="AG Present situation", note="Uses Vikram Samvat and Nepal Sambat."),
    "IRN": dict(status="never", src="AG Present situation", note="Uses the Solar Hijri calendar."),
    "AFG": dict(status="never", src="AG Present situation", note="Uses the Solar Hijri calendar."),
}
# colonies: GT's 1582 row ("Spain, Portugal, France ... and colonies thereof") and 1752 row ("Great Britain, Ireland, and
# the 'First' British Empire (1707 to 1783)"); AG: "The European colonies of the Americas adopted the change when their
# mother countries did". My mapping of which power then ruled each place:
COLONY_1582 = {"MEX": "Spain", "GTM": "Spain", "HND": "Spain", "SLV": "Spain", "NIC": "Spain", "CRI": "Spain", "PAN": "Spain",
               "CUB": "Spain", "DOM": "Spain", "HTI": "Spain, then France", "PRI": "Spain", "TTO": "Spain", "COL": "Spain", "VEN": "Spain",
               "ECU": "Spain", "PER": "Spain", "BOL": "Spain", "CHL": "Spain", "ARG": "Spain", "PRY": "Spain", "URY": "Spain",
               "BRA": "Portugal", "PHL": "Spain"}
COLONY_1752 = {"JAM": "Britain", "BRB": "Britain", "BHS": "Britain", "ATG": "Britain", "KNA": "Britain", "BMU": "Britain", "MSR": "Britain"}
# The list article ("List of adoption dates of the Gregorian calendar by country", source key GL) is the primary calendar
# source. Each of its rows is a historic area within a present country, with the last day before and the first day after
# the change and the number of dates omitted (negative for a return to the Julian calendar). The effective year is the
# year of the first day after the change (so 21 Dec 1585 followed by 1 Jan 1586 counts as 1586). A country with one
# effective year and no return gets [(year, "G")]; every other country's timeline is set by hand here from its rows.
# State F: the French Republican calendar (1793 to 1805).
GL_NAME = {"Czech Republic": "CZE", "United States of America": "USA", "Faroe Islands": "FRO"}
CAL_LIST_TL = {   # iso -> (timeline, note on the list rows)
    "BLR": ([(1586, "G"), (1800, "J"), (1915, "P"), (1918, "G")], "In the Grand Duchy of Lithuania from 1586; back to the Julian calendar in 1800 as the Lithuania Governorate; Grodno Governorate 1915; the rest with Soviet Russia in 1918."),
    "BEL": ([(1582, "P"), (1583, "G")], "Flanders, Brabant and the Spanish-ruled Southern Netherlands in December 1582; the Prince-Bishopric of Liège in February 1583."),
    "CAN": ([(1582, "P"), (1752, "G")], "New France in December 1582; Nova Scotia returned to the Julian calendar under British rule in 1710; the British colonies switched in 1752."),
    "FRA": ([(1582, "P"), (1760, "G"), (1793, "F"), (1806, "G")], "France except Alsace and Lorraine in December 1582; Upper Alsace and the Catholic diocese of Strasbourg 1583; Protestant Strasbourg 1682; Mulhouse 1701; Lorraine 1582, back to the Julian calendar in 1735 and Gregorian again in 1760. The French Republican calendar replaced it from 1793 to the end of 1805."),
    "DEU": ([(1582, "P"), (1700, "G")], "Catholic states from 1582 to 1585, a few bishoprics and the Electoral Palatinate in the 1600s, the Protestant states on 1 March 1700."),
    "IRL": ([(1584, "P"), (1641, "J"), (1752, "G")], "The O'Neill and O'Donnell lordships in Ulster used it from 1584; a papal dispensation to return to the Julian calendar was applied for in 1630 and in operation by 1641; the Kingdom of Ireland switched with Britain in 1752."),
    "ITA": ([(1582, "P"), (1583, "G")], "Most of Italy in October 1582; Tyrol and Brixen in 1583."),
    "LVA": ([(1617, "P"), (1796, "J"), (1915, "G")], "Courland from 1617, back to the Julian calendar in 1796; Courland and Livland again in 1915."),
    "LTU": ([(1586, "P"), (1610, "G"), (1800, "P"), (1915, "G")], "The Grand Duchy of Lithuania from 1586 and the north of Ducal Prussia from 1610; the Lithuania Governorate went back to the Julian calendar in 1800; Kovno and Vilna Governorates 1915."),
    "NLD": ([(1582, "P"), (1701, "G")], "Brabant, Zeeland and the States General in December 1582, Holland and Groningen city in 1583 (Groningen went back to the Julian calendar in 1594), the other provinces in 1700 and 1701."),
    "POL": ([(1582, "P"), (1700, "G")], "Poland in October 1582, Silesia 1584, southern Ducal Prussia 1610, the parts in the Margraviate of Brandenburg in 1700."),
    "ROU": ([(1590, "P"), (1919, "G")], "The Principality of Transylvania in 1590; Romania in 1919."),
    "RUS": ([(1610, "P"), (1918, "G")], "The north of Ducal Prussia (today's Kaliningrad) in 1610; Russia in 1918."),
    "SWE": ([(1700, "S"), (1712, "J"), (1753, "G")], "The Swedish calendar from 1700, a 30 February in 1712 to return to the Julian calendar, and the Gregorian calendar in 1753, including Finland."),
    "FIN": ([(1700, "S"), (1712, "J"), (1753, "G")], "As part of Sweden (the list's Swedish rows include Finland)."),
    "CHE": ([(1583, "P"), (1812, "G")], "Canton by canton from 1583 (the Catholic diocese of Basel) to 1812 (the last Protestant communes of Graubünden). Appenzell Ausserrhoden switched in 1584, went back in 1597 and switched again in 1798."),
    "USA": ([(1582, "P"), (1752, "G")], "The French and Spanish colonies in December 1582; the British colonies in 1752. Alaska, then Russian, followed in 1867 and is drawn separately."),
}
CAL_SUB = {   # sub-national units: code -> (timeline, date or note, source)
    "NL-NB": ([(1582, "G")], "14 December 1582 followed by 25 December (Brabant)", "GL"), "NL-ZE": ([(1582, "G")], "14 December 1582 followed by 25 December", "GL"),
    "NL-NH": ([(1583, "G")], "1 January 1583 followed by 12 January (Holland)", "GL"), "NL-ZH": ([(1583, "G")], "1 January 1583 followed by 12 January (Holland)", "GL"),
    "NL-GE": ([(1700, "G")], "30 June 1700 followed by 12 July", "GL"), "NL-OV": ([(1700, "G")], "30 November 1700 followed by 12 December", "GL"),
    "NL-UT": ([(1700, "G")], "30 November 1700 followed by 12 December", "GL"), "NL-FR": ([(1701, "G")], "31 December 1700 followed by 12 January 1701 (Frisia)", "GL"),
    "NL-GR": ([(1583, "P"), (1594, "J"), (1701, "G")], "Groningen city switched in March 1583 and went back to the Julian calendar in November 1594; the whole province switched on 12 January 1701", "GL"),
    "NL-DR": ([(1701, "G")], "30 April 1701 followed by 12 May", "GL"),
    **{c: ([(1582, "G")], "December 1582 (Brabant, Flanders and the Spanish-ruled Southern Netherlands)", "GL") for c in ("BE-VAN", "BE-VBR", "BE-WBR", "BE-BRU", "BE-VWV", "BE-VOV", "BE-WHT", "BE-WNA", "BE-WLX", "BE-VLI")},
    "BE-WLG": ([(1583, "G")], "10 February 1583 followed by 21 February (Prince-Bishopric of Liège)", "GL"),
    **{c: ([(1584, "G")], "January or February 1584 (the Catholic cantons)", "GL") for c in ("CH-LU", "CH-UR", "CH-SZ", "CH-ZG", "CH-FR", "CH-SO", "CH-OW", "CH-NW")},
    "CH-TG": ([(1584, "G")], "1584", "GL"), "CH-AI": ([(1584, "G")], "1584", "GL"),
    "CH-AR": ([(1584, "G"), (1597, "J"), (1798, "G")], "Switched in 1584, went back to the Julian calendar in 1597, switched again on 25 December 1798", "GL"),
    "CH-JU": ([(1583, "G")], "October 1583 (the Catholic diocese of Basel)", "GL"),
    "CH-VS": ([(1623, "P"), (1655, "G")], "Lower Valais 1623; the rest on 11 March 1655", "GL"),
    "CH-GR": ([(1623, "P"), (1812, "G")], "Catholic parts 1623 to 1624; Protestant communes between 1783 and 1811, the last (Schiers and Grüsch) on 7 January 1812", "GL"),
    **{c: ([(1701, "G")], "31 December 1700 followed by 12 January 1701 (the Protestant cantons)", "GL") for c in ("CH-BS", "CH-BE", "CH-NE", "CH-SH", "CH-GE", "CH-ZH")},
    "CH-GL": ([(1701, "P"), (1798, "G")], "Catholic Glarus 12 January 1701; Protestant Glarus 4 July 1798", "GL"),
    "CH-SG": ([(1724, "P")], "The city of St. Gallen in 1724; the list gives no date for the rest of the canton", "GL"),
    "FR-67": ([(1583, "P"), (1682, "G")], "The Catholic diocese of Strasbourg in November 1583; Protestant Strasbourg and the Protestant parishes in February 1682", "GL"),
    "FR-68": ([(1583, "G")], "Austrian Upper Alsace in October 1583 (Mulhouse, then independent, in 1701)", "GL"),
    **{c: ([(1582, "G"), (1735, "J"), (1760, "G")], "Lorraine: December 1582, back to the Julian calendar in 1735, Gregorian again on 28 February 1760", "GL") for c in ("FR-54", "FR-55", "FR-57", "FR-88")},
    "US-AK": ([(1867, "G")], "Friday 6 October 1867 (Julian) was followed by Friday 18 October 1867 (Gregorian), on the sale of Alaska by Russia to the United States; with the date line moved, 11 dates were omitted", "GL; AG"),
    "CA-QC": ([(1582, "G")], "December 1582 (New France)", "GL; AG"),
    "CA-NS": ([(1752, "G")], "Nova Scotia returned to the Julian calendar under British rule in 1710 and switched with Britain in 1752", "GL"),
}
CAL_POINTS = [   # places named in the sources: (name, lon, lat, year, text, source)
    ("Strasbourg", 7.75, 48.58, 1682, "Protestant Strasbourg switched in February 1682; the Catholic diocese had switched in 1583.", "GL; GT"),
    ("Königsberg (Ducal Prussia)", 20.51, 54.71, 1610, "Ducal Prussia, a Polish fief, was the first Protestant state to switch: 22 August followed by 2 September 1610 in the list (AG says 1612).", "GL; AG"),
    ("Schiers and Grüsch", 9.66, 46.97, 1812, "In these two communes of Graubünden, 25 December 1811 was followed by 7 January 1812: 12 dates omitted, the last in western and central Europe.", "GL; AG"),
    ("Mulhouse", 7.34, 47.75, 1701, "Mulhouse, then an independent city allied to the Swiss, switched with the Protestant cantons in January 1701.", "GL"),
    ("Groningen", 6.57, 53.22, 1583, "Groningen city switched in 1583, went back to the Julian calendar in 1594, and switched again with its province in 1701.", "GL"),
]

# ----------------------------------------------------------------------------------------------- driving side
ROAD_NAME = {"Congo": "COG", "DR Congo": "COD", "Mainland": "CHN", "Contiguous U.S.": "USA", "United Kingdom proper": "GBR",
             "U.S. Virgin Islands": "VIR", "Ivory Coast": "CIV", "Georgia": "GEO", "Timor-Leste": "TLS", "Hong Kong": "HKG", "Macau": "MAC",
             "Federated States of Micronesia": "FSM", "Palestine": "PSE", "Kosovo": "KOS", "Eswatini": "SWZ", "Bahamas": "BHS", "Gambia": "GMB",
             "Cape Verde": "CPV", "São Tomé and Príncipe": "STP", "Tanzania": "TZA", "Czech Republic": "CZE", "Serbia": "SRB", "North Macedonia": "MKD",
             "Vatican City": "VAT", "Western Sahara": "ESH", "Falkland Islands": "FLK", "South Georgia and the South Sandwich Islands": "SGS",
             "Pitcairn Islands": "PCN", "British Indian Ocean Territory": "IOT"}
ROAD_SUBROW = {"Alberta": "CA-AB", "British Columbia": "CA-BC", "Manitoba": "CA-MB", "New Brunswick": "CA-NB", "Newfoundland and Labrador": "CA-NL",
               "Northwest Territories": "CA-NT", "Nova Scotia": "CA-NS", "Nunavut": "CA-NU", "Ontario": "CA-ON", "Prince Edward Island": "CA-PE",
               "Quebec": "CA-QC", "Saskatchewan": "CA-SK", "Yukon": "CA-YT", "Alaska": "US-AK", "Hawaii": "US-HI"}
ROAD_SKIP = {"Gibraltar"}          # not drawn separately in Natural Earth 1:50m (RHT, switched 16 June 1929; kept in the notes)
# Overrides of the timeline built from the table (today's side, date of switch). Values: init side and changes.
ROAD_TL = {
    "TLS": dict(init="L", tl=[(1928, "R"), (1976, "L")], src="LRT; LRP", note="Switched to the right with Portugal in 1928 and back to the left in 1976, under Indonesian occupation."),
    "URY": dict(init="R", tl=[(1918, "L"), (1945, "R")], src="LRT", note="Became left-hand in 1918 and changed back to the right on 2 September 1945. The table does not say which side it used before 1918; I show today's side."),
    "AUT": dict(init="L", tl=[(1921, "M"), (1938, "R")], src="LRT 1921 to 38; LRP", note="Province by province: Vorarlberg 1921, North Tyrol 1930, Carinthia and East Tyrol 1935, the rest in 1938."),
    "SVK": dict(init="L", tl=[(1939, "M"), (1941, "R")], src="LRT 1939 to 41", note="Switched during the German occupation of Czechoslovakia."),
    "BRA": dict(init="M", tl=[(1928, "R")], src="LRT; LRP", note="Mixed rules in the 19th and early 20th centuries; the remaining left-hand regions switched in 1928."),
    "CHN": dict(init="M", tl=[(1946, "R")], src="LRT; LRP", note="Parts of China, such as the Shanghai International Settlement and Canton, drove on the left in the 1930s; right-hand traffic became mandatory in 1946."),
    "ESP": dict(init="M", tl=[(1924, "R")], src="LRT; LRP", note="Up to the 1920s Barcelona drove on the right and Madrid on the left; Spain switched in 1918 except Madrid, which followed in 1924."),
    "CAN": dict(init="M", tl=[(1947, "R")], src="LRT; LRP", note="Quebec and Ontario always drove on the right; British Columbia 1920 to 1922, New Brunswick 1922, Nova Scotia 1923, Prince Edward Island 1924 and Newfoundland 1947."),
    "SUR": dict(init="L", tl=[], src="LRT", note="The table gives '1920s' as the date but says Suriname did not switch sides, unlike the Netherlands; shown on the left throughout."),
    "ROU": dict(init="M", tl=[(1919, "R")], src="LRT; LRP", note="Transylvania, the Banat and Bukovina drove on the left until 1919; Wallachia and Moldavia were already on the right."),
    "POL": dict(init="R", tl=[], src="LRT; LRP", note="The former Austrian Partition in the south east drove on the left until the 1920s; the table gives no single year."),
    "ITA": dict(init="M", tl=[(1924, "R")], src="LRT 1924; LRP", note="Each province chose its own side from 1901; Mussolini decreed in 1923 that left-hand areas would move to the right."),
    "JPN": dict(init="L", tl=[], src="LRT; LRP", note="Left-hand traffic was acknowledged in 1872 and made law in 1924. Okinawa drove on the right from 1945 until 30 July 1978."),
    "SWE": dict(init="L", tl=[(1967, "R")], src="LRT; DH", note="Dagen H, Sunday 3 September 1967: at 04:50 all traffic stopped, changed sides and set off again at 05:00. A 1955 referendum had voted 83% to keep left."),
    "ISL": dict(init="L", tl=[(1968, "R")], src="LRT; LRP", note="H-dagurinn, 26 May 1968, the year after Sweden."),
    "WSM": dict(init="R", tl=[(2009, "L")], src="LRT; LRP", note="Right-hand for more than a century, then left from 7 September 2009, to allow cheaper cars from Australia, New Zealand and Japan; the first territory in almost 30 years to change sides."),
    "HRV": dict(init="L", tl=[(1926, "R")], src="LRT 1926; LRP", note="The table gives 1926; the prose says Croatia-Slavonia switched on joining the Kingdom of Yugoslavia in 1918, while Istria and Dalmatia were already right-hand."),
    "YEM": dict(init="M", tl=[(1977, "R")], src="LRT", note="South Yemen, formerly the British colony of Aden, changed to the right in 1977; North Yemen was already right-hand."),
    "SOM": dict(init="R", tl=[], src="LRT", note="Former British Somaliland drove on the left until it united with Italian Somaliland, which drove on the right; the table gives no year, so today's side is shown throughout."),
}
ROAD_SUB = {   # code -> (timeline, init, note, source)
    "CA-BC": ([(1920, "M"), (1922, "R")], "L", "The interior changed on 15 July 1920, Vancouver and the coast on 1 January 1922.", "LRT"),
    "CA-NB": ([(1922, "R")], "L", "1 December 1922.", "LRT"), "CA-NS": ([(1923, "R")], "L", "15 April 1923.", "LRT"),
    "CA-PE": ([(1924, "R")], "L", "1 May 1924.", "LRT"), "CA-NL": ([(1947, "R")], "L", "2 January 1947, as the Dominion of Newfoundland.", "LRT"),
    "CA-QC": ([], "R", "Always right-hand, as a former part of New France.", "LRP"), "CA-ON": ([], "R", "Always right-hand, as a former part of New France.", "LRP"),
    "AT-8": ([(1921, "R")], "L", "Vorarlberg switched in 1921.", "LRP"), "AT-7": ([(1930, "R")], "L", "North Tyrol 1930; East Tyrol, also in today's Tirol, in 1935.", "LRP"),
    "AT-2": ([(1935, "R")], "L", "Carinthia 1935.", "LRP"),
    "AT-1": ([(1938, "R")], "L", "The rest of Austria switched in 1938.", "LRP"), "AT-3": ([(1938, "R")], "L", "The rest of Austria switched in 1938.", "LRP"),
    "AT-4": ([(1938, "R")], "L", "The rest of Austria switched in 1938.", "LRP"), "AT-5": ([(1938, "R")], "L", "The rest of Austria switched in 1938.", "LRP"),
    "AT-6": ([(1938, "R")], "L", "The rest of Austria switched in 1938.", "LRP"), "AT-9": ([(1938, "R")], "L", "The rest of Austria switched in 1938.", "LRP"),
    "JP-47": ([(1945, "R"), (1978, "L")], "L", "Okinawa drove on the right under American rule from 24 June 1945 and switched back to the left at 6 am on 30 July 1978 ('730').", "LRT; LRP"),
}
ROAD_POINTS = [
    ("Madrid", -3.70, 40.42, 1924, "Madrid kept left until a national law moved it to the right in 1924; Barcelona was already right-hand.", "LRT; LRP"),
    ("Rotterdam", 4.48, 51.92, 1917, "Rotterdam had no fixed rule until May 1917, when the police enforced right-hand traffic.", "LRP"),
    ("Gibraltar", -5.35, 36.14, 1929, "Gibraltar switched to the right on 16 June 1929 because of its land border with Spain; it is not drawn separately.", "LRT"),
]

# ----------------------------------------------------------------------------------------------- metric
MET_NAME = {"Ottoman Empire/Turkey": "TUR", "United States of America": "USA", "North Korea": "PRK", "South Korea": "KOR",
            "Hong Kong": "HKG", "Macau": "MAC", "Taiwan": "TWN", "Greece | 1959": "GRC", "Poland (former Congress Poland and Russian partition)": "POL",
            "Austria (including Austrian Poland)": "AUT"}
MET_SKIP = {"North German Confederation (including German Poland)": "DEU part", "South German states": "DEU part"}
MET_OVR = {   # iso -> dict(tl, note)
    "DEU": dict(tl=[(1868, "P"), (1872, "M")], note="The North German Confederation started in 1868 and the South German states in 1869; the German Empire made it official in 1872."),
    "POL": dict(tl=[(1868, "P"), (1920, "M")], note="German Poland started with the North German Confederation in 1868 and Austrian Poland in 1871; the former Russian partition followed in 1920."),
    "PHL": dict(note="First adopted under Spanish rule in 1860; US customary units came with American rule; the metric system was made official in 1906."),
    "GRC": dict(note="The table also gives 1959 beside Greece, without saying what it marks."),
    "MMR": dict(note="The table gives 2011 and 2013; full metrication was announced in 2014. One of three countries without mandatory metric laws, according to NIST (MTP)."),
    "ESP": dict(note="The table gives 1852; the prose says the metric system became the legal system in Spain in 1849."),
    "AUT": dict(note="The table gives 1871; the prose says the metric system became official in Austria in 1875."),
    "CHE": dict(note="The table gives 1876; a federal law imposed the metric system from 1 January 1877. Some cantons were earlier: Geneva 1813, Vaud 1822, Valais 1824, Neuchâtel 1857 (MTP)."),
    "LCA": dict(note="The table gives 2005; the prose says Saint Lucia was officially metric in 2000."),
    "IND": dict(note="The Standards of Weights and Measures Act 1956 came into force on 1 October 1958; metric weights became mandatory in October 1960 and metric measures in April 1962."),
    "GBR": dict(note="Began in 1965 with a ten year target; in 1979 the government decided against further compulsory conversion. Imperial units remain for road signs, draught beer and cider, milk in returnable containers and precious metals."),
    "USA": dict(note="The 1866 Act made metric units lawful without displacing customary units. One of three countries without mandatory metric laws, according to NIST (MTP)."),
    "CAN": dict(note="Metrication was halted in 1985."),
    "LBR": dict(note="The table gives no year ('Indeterminate'); Liberia pledged to adopt the metric system in 2018. One of three countries without mandatory metric laws, according to NIST (MTP)."),
}
MET_PROSE = {   # countries absent from the table with a year in the prose
    "GUY": dict(tl=[(2002, "M")], src="MTP", note="Adopted in 2002; mandatory in local trade from 2017, after the system was fully adopted in schools."),
}
MET_NOTMAND = {"FSM": "Vera (2011), cited in MTP: metric use not mandatory in practice.", "MHL": "Vera (2011), cited in MTP: metric use not mandatory in practice.",
               "PLW": "Vera (2011), cited in MTP: metric use not mandatory in practice.", "ATG": "Officially metric, converting slowly (MTP); no year given."}
MET_SUB = {"CH-GE": (1813, "Geneva adopted the metric system in 1813.", "MTP"), "CH-VD": (1822, "Vaud, 1822.", "MTP"),
           "CH-VS": (1824, "Valais, 1824.", "MTP"), "CH-NE": (1857, "Neuchâtel, 1857.", "MTP"), "CH-JU": (1800, "The territory of today's Jura, then French, adopted the metre in 1800.", "MTP")}

# ----------------------------------------------------------------------------------------------- votes for women
VOTE_NAME = {"Belarusian People's Republic": "BLR", "British Honduras (Today: Belize)": "BLZ", "Dahomey (Today: Benin)": "BEN",
             "Kingdom of Bulgaria": "BGR", "Upper Volta (Today: Burkina Faso)": "BFA", "Burma": "MMR", "British Cameroons (Today: Cameroon)": "CMR",
             "Zaire (Today: Democratic Republic of the Congo)": "COD", "Congo, Republic of the": "COG", "Grand Duchy of Finland": "FIN",
             "Democratic Republic of Georgia": "GEO", "Hungarian Republic": "HUN", "Kazakh SSR": "KAZ", "Korea, North": "PRK", "Korea, South": "KOR",
             "Kyrgyz SSR": "KGZ", "Kingdom of Laos": "LAO", "Kingdom of Libya": "LBY", "Federation of Malaya (Today: Malaysia)": "MYS",
             "Mongolian People's Republic": "MNG", "People's Republic of Mozambique": "MOZ", "Russian Republic": "RUS", "Tajik SSR": "TJK",
             "Turkmen SSR": "TKM", "Uzbek SSR": "UZB", "Southern Rhodesia (Today: Zimbabwe)": "ZWE", "Gambia, The": "GMB",
             "Micronesia, Federated States of": "FSM", "Kingdom of Cambodia": "KHM", "East Timor": "TLS", "Cape Verde": "CPV", "Ivory Coast": "CIV",
             "Eswatini (Formerly: Swaziland)": "SWZ", "Palestine": "PSE", "Georgia": "GEO", "Hong Kong": "HKG", "Puerto Rico": "PRI",
             "Dominion of Newfoundland (Joined Canada in 1949)": "CA-NL", "Kingdom of Hawaii": "US-HI"}
VOTE_MULTI = {   # rows standing for several of today's countries
    "British Leeward Islands (Today: Antigua and Barbuda, British Virgin Islands, Montserrat, Saint Kitts and Nevis, Anguilla)": ["ATG", "VGB", "MSR", "KNA", "AIA"],
    "British Windward Islands (Today: Grenada, St Lucia, St Vincent and the Grenadines, Dominica)": ["GRD", "LCA", "VCT", "DMA"],
    "Czechoslovakia (Today: Czech Republic, Slovakia)": ["CZE", "SVK"],
    "Netherlands Antilles (Today: Aruba, Curaçao, Sint Maarten, Caribbean Netherlands)": ["ABW", "CUW", "SXM"],
    "North Yemen (Today: Yemen)": ["YEM"], "South Yemen (Today: Yemen)": ["YEM"],
    "Yugoslavia (Today: Serbia, Montenegro, Croatia, Slovenia, Bosnia and Herzegovina, Kosovo, North Macedonia)": ["SRB", "MNE", "HRV", "SVN", "BIH", "KOS", "MKD"],
    "Kingdom of Denmark (Including the Faroe Islands and, at that time, Iceland)": ["DNK", "FRO", "ISL"],
    "Ethiopia (Then including Eritrea)": ["ETH"],
}
VOTE_SKIP = {"Grand Duchy of Tuscany": "A pre-unification Italian state (1848); kept as a note under Italy."}
# Rows whose year cell holds more than one year, read with the notes: first = the first year women could vote in national
# elections at all; equal = the year the table or its notes give for full or equal terms (None: no separate year given).
VOTE_OVR = {
    "Armenia": (1917, None, "1917 by applying the Russian law; March 1919 by Armenia's own law."),
    "Australia": (1902, 1962, "1902 at federal level except for 'natives of Australia, Asia, Africa and the Pacific Islands'; 1962 full."),
    "Belgium": (1948, None, "The 1919 constitution gave women the communal vote only; the national vote came in 1948."),
    "Bolivia": (1938, 1952, "1938 for literate women with an income; equal with men from 1952."),
    "Kingdom of Bulgaria": (1944, None, "1937 for married and widowed women in local elections only; full voting rights in 1944."),
    "Canada": (1917, None, "1917 for war widows and the female relatives of servicemen; 1918 for women over 21 who were not alien-born and met property qualifications; Aboriginal people, men and women, only in 1960."),
    "Kingdom of Denmark (Including the Faroe Islands and, at that time, Iceland)": (1915, None, "1908 in local elections, 1915 in national parliamentary elections."),
    "Ecuador": (1929, 1967, "1929, but voting was optional for women and compulsory for men until 1967."),
    "El Salvador": (1939, 1950, "1939 with literacy and higher age requirements; all restrictions lifted in 1950."),
    "Greece": (1952, None, "1930 in local elections for literate women only; unconditional in 1952."),
    "Guatemala": (1945, 1965, "1945 for literate women; restrictions lifted in 1965."),
    "Hungarian Republic": (1919, 1945, "1919 from age 30 with higher criteria than men (men from 24); universal from age 20 for both in 1945."),
    "India (Then under British colonial rule)": (1921, None, "1921 in Bombay and Madras; 1929 in all provinces, including the princely states."),
    "Indonesia": (1937, 1945, "1937 for Europeans only; 1945 for all citizens, at independence."),
    "Ireland": (1918, 1922, "1918 at 30 with property qualifications, as in the rest of the United Kingdom; equal in the Irish Free State from 1922."),
    "Italy": (1945, None, "1925 in local elections, which were then abolished; full suffrage in 1945."),
    "Jordan": (1955, 1974, "1955 for educated women; all women in 1974."),
    "Kingdom of Libya": (1963, None, "1951 in local elections; 1963 nationally."),
    "Moldova": (1939, 1940, "1929 local elections as part of Romania; general elections from the 1939 electoral law; equal in 1940 in the Moldavian SSR."),
    "Netherlands": (1919, None, "The table gives 1917, the year women could be elected; its notes say women have voted since 1919."),
    "Panama": (1941, 1946, "1941 conditioned by education; equal from 1946."),
    "Portugal": (1911, 1976, "1911 with restrictions, then made illegal again until 1931, when it returned with restrictions; restrictions other than age lifted in 1976."),
    "Puerto Rico": (1929, 1935, "1929 for literate women; all women in 1935."),
    "Romania": (1939, 1946, "1929 in local elections with qualifications; general elections under the 1939 electoral law, with restrictions that weighed more on women; full equality in 1946."),
    "South Africa": (1930, 1994, "1930 for European and Asian women; women of other races in 1994, at the same time as men of all races."),
    "Spain": (1924, 1931, "Women briefly held the vote from 1924 to 1926 but no elections were held; the 1931 constitution gave the vote, first used in 1933; nobody voted again until after Franco."),
    "Switzerland": (1971, None, "1971 at federal level; cantons between 1959 and 1990."),
    "Trinidad and Tobago": (1925, 1945, "1925 for women over 30 (men over 21), as in the United Kingdom; full suffrage in 1945."),
    "Turkey": (1934, None, "1930 in local elections, 1934 in national elections."),
    "Ukraine": (1917, None, "1917 in the Ukrainian People's Republic, 1918 in the West Ukrainian People's Republic, 1919 in the Ukrainian SSR."),
    "United Kingdom": (1918, 1928, "1918 at 30 with property qualifications or as graduates, while men voted at 21; equal from 1928."),
    "United States": (1920, None, "The Nineteenth Amendment, 1920; legal protections for Black voters, women and men, only in 1965."),
    "Uruguay": (1917, None, "In the 1917 constitution; first exercised in 1927, put into national law in 1932, first national election 1938."),
    "Venezuela": (1946, None, "1946 (partial), the table says."),
    "Southern Rhodesia (Today: Zimbabwe)": (1919, 1978, "1919 for white women only; full in 1978."),
    "Chile": (1949, None, "Local elections from 1934; national in 1949."),
    "Oman": (2002, None, "Municipal suffrage in Muscat in 1994 and in all Oman in 1996; national suffrage in 2002, for a consultative assembly."),
    "Saudi Arabia": (2015, None, "December 2015, in municipal elections: there are no national elections in Saudi Arabia."),
    "Palestine": (1972, None, "Local elections in the West Bank in 1972, for women and men; a Palestinian parliament first elected in 1996."),
    "Philippines": (1937, None, "A 1937 plebiscite; local elections later that year."),
    "Kingdom of Hawaii": (1840, None, "Universal suffrage from 1840, specifically denied to women in the 1852 constitution."),
    "Brunei": (1959, None, "National elections are suspended; men and women vote only in local elections."),
}
VOTE_NOVOTE = {"Eritrea": "No elections since independence in 1993.", "Vatican City": "The Pope is elected by the all-male College of Cardinals."}
VOTE_SUB = {   # state, provincial or cantonal votes named in the table's notes (not national): code -> (year, note)
    "CA-MB": (1916, "Provincial vote, 1916."), "CA-SK": (1916, "Provincial vote, 1916."), "CA-AB": (1916, "Provincial vote, 1916."),
    "CA-BC": (1917, "Provincial vote, 1917."), "CA-ON": (1917, "Provincial vote, 1917."), "CA-NS": (1918, "Provincial vote, 1918."),
    "CA-NB": (1919, "Provincial vote, 1919 (women could not run for office until 1934)."), "CA-PE": (1922, "Provincial vote, 1922."),
    "CA-QC": (1940, "Provincial vote, 1940, the last province."), "CA-NL": (1925, "The Dominion of Newfoundland, 1925 (joined Canada in 1949)."),
    "AU-SA": (1895, "Colony of South Australia, 1895."), "AU-WA": (1899, "Colony of Western Australia, 1899 (with racial restrictions)."),
    "AU-NSW": (1902, "New South Wales, 1902."), "AU-TAS": (1903, "Tasmania, 1903."), "AU-QLD": (1905, "Queensland, 1905 (with racial restrictions)."),
    "AU-VIC": (1908, "Victoria, 1908."),
    "CH-VD": (1959, "Cantonal vote, 1959."), "CH-NE": (1959, "Cantonal vote, 1959."),
    "CH-AR": (1989, "Cantonal vote, 1989."), "CH-AI": (1990, "Cantonal vote, 1990, the last canton."),
    "US-HI": (1840, "The Kingdom of Hawaii: universal suffrage in 1840, denied to women in 1852."),
}
VOTE_STANDIN = {"YEM": "South Yemen 1967, North Yemen 1970: shown as 1967 for part and 1970 for the whole of today's Yemen.",
                "ETH": "Ethiopia then included Eritrea.", "SSD": "Not in the table; part of Sudan (1964) until 2011."}
