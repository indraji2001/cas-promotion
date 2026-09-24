import re, json

html = open("CAS_Promotion_2026_GovtAidedColleges_Interactive_11_GO1438.html", encoding="utf-8").read()
bank = re.findall(r'\[(143[89]),(\d+),(\d+),"((?:[^"\\]|\\.)*)"', html)
ocr = json.load(open("ocr_ground.json", encoding="utf-8"))

def toks(s):
    s = s.replace("<br>", " ").replace("`", "").replace("*", "")
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).split()

# bank words per page
bp = {}
for go,pg,ln,t in bank:
    bp.setdefault((go,int(pg)), set()).update(toks(t))

print("=== OCR words (len>=4, confident) missing from the bank page ===")
for key, pages in ocr.items():
    for i, lines in enumerate(pages, 1):
        bt = bp.get((key, i), set())
        miss = []
        for l in lines:
            if l["c"] < 0.85: continue
            for w in toks(l["t"]):
                if len(w) >= 4 and w not in bt and w not in miss:
                    miss.append(w)
        if miss:
            print(f"[{key} p{i}] missing: {miss[:14]}")
