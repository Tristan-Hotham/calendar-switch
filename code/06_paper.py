"""Step 6. Build the paper: fill code/paper_template.tex from data/results.json, add tables, compile with xelatex.
Output: release/paper/<NAME>.pdf and .tex (figures f_*.png sit beside them). The DOI stays as the 10.5281/zenodo.23873009 placeholder."""
import subprocess
from common import *

R = jload(f"{DATA}/results.json")
SITE = jload(f"{DATA}/site.json"); U = SITE["units"]
OUT = os.path.join(ROOT, "release", "paper"); NAME = "Hotham_Lost_Days"
tex = lambda s: str(s).replace("\\", "").replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#").replace("$", "\\$")

# statements made in words in the paper only
V = R["vote"]
assert max(b - a for _, a, b in V["two"]) == 65 and [b - a for n, a, b in V["two"] if n == "South Africa"] == [64] and [b - a for n, a, b in V["two"] if n == "Portugal"] == [65] and min(b - a for _, a, b in V["two"]) == 1
assert [x[0] for x in V["last"][:6]] == ["Saudi Arabia", "United Arab Emirates", "Kuwait", "Oman", "Bahrain", "Qatar"] and V["last"][3][1] == V["last"][4][1] == 2002
assert R["road"]["n_R"] / R["source"]["n_countries"] > .7 and R["road"]["n_R"] / R["source"]["n_countries"] < .75   # "nearly three quarters"
assert len(R["metric"]["mixed"]) == 5 and R["cal"]["days_lists"]["12"] == ["Switzerland", "Uganda"] and R["cal"]["n_ch_cantons"] == 22 and R["cal"]["n_returns"] == 8
assert all(U[i]["cal"]["first"] == 1583 or U[i]["cal"]["year"] == 1583 for i in ("AUT", "SVN")) and U["HUN"]["cal"]["year"] == 1587 and U["UGA"]["cal"]["year"] == 1894
assert {U[i]["cal"]["year"] for i in ("ARM", "GEO", "AZE")} == {1918} and U["FRA"]["cal"]["year"] == 1760
assert all(U[i]["cal"]["status"] == "undated" for i in ("IND", "IDN", "PAK", "NGA"))


def tfmt(v, f):
    if f == "int": return f"{int(round(float(v))):,}"
    if f == "pc": return f"{round(float(v))}\\%"
    if f == "pc1": return f"{float(v):.1f}\\%"
    if f == "f1": return f"{float(v):.1f}"
    return tex(str(v))


DATES = [("Spain, Portugal", "ESP"), ("Denmark and Norway", "DNK"), ("Great Britain", "GBR"), ("Sweden", "SWE"), ("Uganda", "UGA"),
         ("Bulgaria", "BGR"), ("Russia", "RUS"), ("Romania", "ROU"), ("Greece", "GRC"), ("Albania", "ALB")]
rows = "".join(f"{tex(n)} & {tex(U[i]['cal']['date'])} & {U[i]['cal']['days']}\\\\\n" for n, i in DATES)
TD = ("\\begin{table}[tbp]\\centering\\small\\caption{Before and after dates in the sources (the list article, or the prose where it gives the weekday), and the dates omitted.}\\label{tab:days}"
      "\\begin{tabular}{p{3.6cm}p{9.2cm}r}\\toprule Where & Switch & Days\\\\\\midrule\n" + rows + "\\bottomrule\\end{tabular}\\end{table}")
SW = R["road"]["switches"]
half = (len(SW) + 1) // 2
cell = lambda x: f"{tex(x[0])} & {x[1]} & {'left' if x[2] == 'L' else 'right'}" if x else " & & "
rows = "".join(cell(SW[j]) + " & " + cell(SW[j + half] if j + half < len(SW) else None) + "\\\\\n" for j in range(half))
TR = ("\\begin{table}[tbp]\\centering\\footnotesize\\setlength{\\tabcolsep}{4pt}\\caption{Every dated change of driving side in the table, matched to today's countries.}\\label{tab:road}"
      "\\begin{tabular}{lrl@{\\hspace{1.4em}}lrl}\\toprule Country & Year & To & Country & Year & To\\\\\\midrule\n" + rows + "\\bottomrule\\end{tabular}\\end{table}")
I = {u["n"]: i for i, u in U.items()}
rows = "".join(f"{tex(n)} & {a} & {b} & {tex(U[I[n]]['vote']['note'])}\\\\\n" for n, a, b in V["two"])
TV = ("\\begin{table}[tbp]\\centering\\footnotesize\\caption{Countries where the suffrage table gives a restricted first vote and a later year of full or equal terms, with my reading of the table.}\\label{tab:votes}"
      "\\begin{tabular}{lrrp{9.6cm}}\\toprule Country & First & Equal & Reading of the table\\\\\\midrule\n" + rows + "\\bottomrule\\end{tabular}\\end{table}")
rows = "".join(f"{tex(a)} & {tex(b)} & {tex(c)} ({tex(src)})\\\\\n" for a, b, c, src in R["cal"]["disagree"])
TDIS = ("\\begin{table}[tbp]\\centering\\footnotesize\\caption{Where the list article and the other calendar sources (adoption tables in Gregorian calendar and Julian calendar, and the prose of Adoption of the Gregorian calendar) differ. Most differences are finer regional detail in the list. Years are first part and whole country. GT: adoption table in Gregorian calendar; GN and JN: start of year tables in Gregorian calendar and Julian calendar; AG: Adoption of the Gregorian calendar; ACT: Calendar (New Style) Act 1750.}\\label{tab:dis}"
        "\\begin{tabular}{p{4.2cm}p{4.4cm}p{5.6cm}}\\toprule Country or area & List & Other sources\\\\\\midrule\n" + rows + "\\bottomrule\\end{tabular}\\end{table}")
rows = "".join(f"{tex(t)} & {r}\\\\\n" for t, r in sorted(R["source"]["revid"].items()))
TS = ("\\begin{table}[tbp]\\centering\\small\\caption{English Wikipedia articles used, with the revision read (CC BY-SA 4.0).}\\label{tab:revs}"
      "\\begin{tabular}{lr}\\toprule Article & Revision\\\\\\midrule\n" + rows + "\\bottomrule\\end{tabular}\\end{table}")
t = open(os.path.join(ROOT, "code", "paper_template.tex"), encoding="utf-8").read()
for k in ("page", "repo"):
    t = t.replace("\\url{{{meta.%s}}}" % k, "\\url{%s}" % R["meta"][k])
t = re.sub(r"\{\{(?!TABLE_)([^}|]+)(\|(\w+))?\}\}", lambda m: tfmt(get(R, m.group(1)), m.group(3) or "raw"), t)
for k, v in (("DAYS", TD), ("DIS", TDIS), ("ROAD", TR), ("VOTES", TV), ("REVS", TS)):
    t = t.replace("{{TABLE_%s}}" % k, v)
t = t.replace("@@DOILINK@@", "https://doi.org/\\{\\{DOI\\}\\}")
assert "{{" not in t and "--" not in t and "—" not in t and "–" not in t, re.findall(r"\{\{[^}]*\}\}", t)[:4]
for bad in ("DSIT", "DCMS", "civil serv"):
    assert bad not in t
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, NAME + ".tex"), "w", encoding="utf-8").write(t)
for _ in range(2):
    r = subprocess.run(["xelatex", "-interaction=nonstopmode", NAME + ".tex"], cwd=OUT, capture_output=True, text=True)
log = open(os.path.join(OUT, NAME + ".log"), encoding="utf-8", errors="ignore").read()
print([l for l in log.splitlines() if "Missing character" in l or "undefined" in l.lower() or "Overfull" in l][:12])
for ext in (".aux", ".log", ".out"):
    q = os.path.join(OUT, NAME + ext)
    if os.path.exists(q): os.remove(q)
txt = subprocess.run(["pdftotext", os.path.join(OUT, NAME + ".pdf"), "-"], capture_output=True, text=True).stdout
pages = subprocess.run(["pdfinfo", os.path.join(OUT, NAME + ".pdf")], capture_output=True, text=True).stdout
print("paper", r.returncode, len(txt.split()), "words;", [l for l in pages.splitlines() if l.startswith("Pages")], "dashes:", txt.count("—") + txt.count("–") + txt.count("--"))
