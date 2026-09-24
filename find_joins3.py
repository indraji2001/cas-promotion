import re, json
from wordfreq import zipf_frequency

html = open("CAS_Promotion_2026_GovtAidedColleges_Interactive_11_GO1438.html", encoding="utf-8").read()
bank = re.findall(r'\[(143[89]),(\d+),(\d+),"((?:[^"\\]|\\.)*)"', html)

def english(w):
    return zipf_frequency(w.lower(), "en") >= 2.7

pat2 = re.compile(r"[A-Za-z]+")
seen = {}
for go,pg,ln,t in bank:
    for w in pat2.findall(t):
        lw = w.lower()
        if len(lw) < 5 or english(lw) or lw in seen: continue
        split = None
        # 2-way then 3-way splits, all parts must be real words
        for i in range(2, len(lw)-1):
            a, b = lw[:i], lw[i:]
            if english(a) and english(b): split = (a, b); break
        if not split:
            for i in range(2, len(lw)-3):
                for j in range(i+2, len(lw)-1):
                    a, b, c = lw[:i], lw[i:j], lw[j:]
                    if english(a) and english(b) and english(c):
                        split = (a, b, c); break
                if split: break
        if split:
            seen[lw] = (go, pg, ln, w, split)
OK = {"annexure","academician","weightage","proforma","redressal","chairing","satisfactory",
      "wheresoever","hereinafter","thereof","hereby","hereunder","thereunder","thereafter",
      "whereas","wherein","therein","hereto","thereto","thereby","hitherto","upgradation"}
for lw in list(seen):
    if lw in OK: del seen[lw]

for lw,(go,pg,ln,w,split) in sorted(seen.items(), key=lambda kv:(kv[1][0],int(kv[1][1]),int(kv[1][2]))):
    print(f"[{go},{pg},{ln}] {w} -> {' '.join(split)}")
