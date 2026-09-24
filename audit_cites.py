import re, html as ht

path = "CAS_Promotion_2026_GovtAidedColleges_Interactive_11_GO1438.html"
doc = open(path, encoding="utf-8").read()

bank = re.findall(r'\[(143[89]),(\d+),(\d+),"((?:[^"\\]|\\.)*)"', doc)
page_text = {}
for go,pg,ln,t in bank:
    page_text.setdefault((go,int(pg)), []).append(t)

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

# pull every ref-badge with its pg and label
badges = re.findall(r'<span class="pg">([^<]*)</span><i>([^<]*)</i>', doc)
print("badges:", len(badges))

def clause_keys(label):
    lab = ht.unescape(norm(label))
    keys = set()
    for m in re.findall(r"[A-F]\([a-z]\)-[IVX]+", lab): keys.add(m)
    for m in re.findall(r"\bE-\d+\b|\bC-I+\b|\bC-III\b|\bD-\d+\b", lab): keys.add(m)
    for m in re.findall(r"Sl\.?\s*\d+", lab): keys.add(m.replace(" ", ""))
    for m in re.findall(r"Appendix\s*(?:I|II|II-A|II-B|II-C)\s*,?\s*Table\s*\d+", lab): keys.add(norm(m).lower())
    for m in re.findall(r"Table\s*\d+", lab): keys.add(norm(m).lower())
    for m in re.findall(r"Part\s*[A-F]\b", lab): keys.add(norm(m).lower())
    return keys, lab

bad = 0
for pg, lab in badges:
    m = re.match(r"GO\s*(\d+)\s*·\s*P\.([\d–,\s]+)", norm(pg))
    if not m: continue
    go = m.group(1)
    pages = [int(x) for x in re.findall(r"\d+", m.group(2))]
    keys, labn = clause_keys(lab)
    if not keys: continue
    # gather text of cited pages
    txt = " ".join(" ".join(page_text.get((go, p), [])) for p in pages)
    tnorm = re.sub(r"\s+", "", txt.lower())
    hit = any(re.sub(r"\s+", "", k.lower()) in tnorm for k in keys)
    if not hit:
        bad += 1
        print(f"NO-MATCH {pg} | {labn[:70]} | keys={keys}")
print("badges with no clause-key match on cited pages:", bad)
