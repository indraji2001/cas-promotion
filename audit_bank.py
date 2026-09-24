import re, json, difflib, sys

html = open("CAS_Promotion_2026_GovtAidedColleges_Interactive_11_GO1438.html", encoding="utf-8").read()
bank = re.findall(r'\[(143[89]),(\d+),(\d+),"((?:[^"\\]|\\.)*)"', html)
print("bank lines:", len(bank))

ocr = json.load(open("ocr_ground.json", encoding="utf-8"))

def norm(s):
    s = s.replace("<br>", " ").replace("`", "").replace("*", "")
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    return s.split()

def page_tokens(key, pg):
    toks = []
    for l in ocr[key][pg-1]:
        toks.extend(norm(l["t"]))
    return toks

report = []
for go,pg,ln,t in bank:
    key = go
    ptoks = page_tokens(key, int(pg))
    if not ptoks: continue
    toks = norm(t)
    # every bank word should appear somewhere on the OCR page (order-independent,
    # since OCR may break/merge lines differently)
    pset = set(ptoks)
    missing = [w for w in toks if w not in pset and len(w) >= 4]
    if missing:
        report.append((go,pg,ln,t[:150],missing))

print("lines with words absent from their cited OCR page:", len(report))
for go,pg,ln,t,missing in report:
    print(f"[{go},{pg},{ln}] missing={missing}")
    print("   ", t)
