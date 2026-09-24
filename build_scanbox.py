import json, re, difflib

path = "CAS_Promotion_2026_GovtAidedColleges_Interactive_11_GO1438.html"
ocr = json.load(open("ocr_boxes.json", encoding="utf-8"))
html_src = open(path, encoding="utf-8").read()

def norm(s):
    s = s.replace("<br>", " ").replace("`", "").replace("*", "")
    return re.sub(r"[^a-z0-9]+", "", s.lower())

def containment(frag, line):
    """share of the OCR fragment's characters found in the bank line"""
    if not frag or len(frag) < 4: return 0.0
    m = difflib.SequenceMatcher(None, frag, line)
    total = sum(bl.size for bl in m.get_matching_blocks())
    return total / len(frag)

bank = re.findall(r'\[(143[89]),(\d+),(\d+),"((?:[^"\\]|\\.)*)"', html_src)

pages = {}
for go, pg, ln, t in bank:
    pages.setdefault((str(go), int(pg)), []).append((int(ln), t))

SCANBOX = {}
matched = total = 0
for (key, pg), blines in sorted(pages.items()):
    pdata = ocr[key][pg - 1]
    olines = [ol for ol in pdata["lines"] if len(norm(ol["t"])) >= 4]
    h, w = pdata["h"], pdata["w"]
    blines = sorted(blines)
    bnorm = [norm(t) for ln, t in blines]
    m, n = len(olines), len(blines)

    # DP alignment: fragments (rows) against printed lines (columns).
    # monotonic — reading order; a fragment may join the line the previous
    # fragment joined (OCR splits one printed line into pieces), or advance
    score = [[containment(norm(ol["t"]), bnorm[j]) for j in range(n)] for ol in olines]

    NEG = -1e9
    f = [[0.0] * (n + 1) for _ in range(m + 1)]
    bt = [[None] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(n + 1):
            bestv, bta = f[i - 1][j], ("skipF", i - 1, j)          # fragment unmatched
            if f[i][j - 1] > bestv: bestv, bta = f[i][j - 1], ("skipL", i, j - 1)
            if j >= 1:
                v = f[i - 1][j - 1] + (score[i - 1][j - 1] if score[i - 1][j - 1] >= 0.5 else NEG)
                if v > bestv: bestv, bta = v, ("match", i - 1, j - 1)
                v2 = f[i - 1][j] + (score[i - 1][j - 1] if score[i - 1][j - 1] >= 0.5 else NEG)
                if v2 > bestv: bestv, bta = v2, ("same", i - 1, j)
            f[i][j], bt[i][j] = bestv, bta

    # backtrack matches
    assign = {}
    i, j = m, n
    while i > 0 and j >= 0:
        tag, pi, pj = bt[i][j]
        if tag == "match":
            assign.setdefault(blines[j - 1][0], []).append(olines[pi])
            i, j = pi, pj
        elif tag == "same":
            assign.setdefault(blines[j - 1][0], []).append(olines[pi])
            i = pi
        elif tag == "skipF":
            i = pi
        else:
            j = pj

    for ln, frags in assign.items():
        total += 1
        y0 = min(f["y0"] for f in frags)
        y1 = max(f["y1"] for f in frags)
        x0 = min(f["x0"] for f in frags)
        x1 = max(f["x1"] for f in frags)
        SCANBOX.setdefault(key, {}).setdefault(str(pg), []).append(
            [ln, round(max(0, x0 - 8) / w * 100, 2), round(max(0, y0 - 3) / h * 100, 2),
             round(min(w, x1 + 8) / w * 100, 2), round(min(h, y1 + 3) / h * 100, 2)])
        matched += 1

print("bank lines with scan bands:", matched, "/", len(bank))
html_src = re.sub(r"\nwindow\.SCANBOX = .*?;\n", "\n", html_src, flags=re.S)
js = "\nwindow.SCANBOX = " + json.dumps(SCANBOX, separators=(",", ":")) + ";\n"
i = html_src.index("window.PAGESCAN = ")
j = html_src.index(";\n", i) + 2
html_src = html_src[:j] + js + html_src[j:]
open(path, "w", encoding="utf-8", newline="").write(html_src)
print("SCANBOX SAVED")
