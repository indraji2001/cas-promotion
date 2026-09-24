import re

path = "CAS_Promotion_2026_GovtAidedColleges_Interactive_11_GO1438.html"
doc = open(path, encoding="utf-8").read()

# (label, oldPg, newPg) — truth verified against the MBANK transcription
M = [
 # A(a)-I notes -> PDF p4
 ("Note (i) to Clause A(a)-I", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Note (ii) to Clause A(a)-I", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Notes (i)–(ii) to Clause A(a)-I", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Notes (ii) to A(a)-I and to A(b)-I", "GO 1438 · P.2, P.4", "GO 1438 · P.4, P.6"),
 # A(a)-II -> PDF p4
 ("Clause A(a)-II, Eligibility i–ii", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II, Eligibility (i)", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II, Eligibility (ii)(1) — \"in lieu\" clause", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II (ii)", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II (ii)(1) — OR-substitution structure", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II(ii)(1) — substitution", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II (ii)(2)", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II (ii)(2) — \"relevant subject\" for MOOCs", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II (ii)(3)–(4)", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II (ii)(4)", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II — \"in the last five years of Academic Level-11\"", "GO 1438 · P.2", "GO 1438 · P.4"),
 ("Clause A(a)-II complete", "GO 1438 · P.2–3", "GO 1438 · P.4"),
 ("Clause A(a)-II criteria; Table 1 bands &amp; Note", "GO 1438 · P.2, P.9", "GO 1438 · P.4, P.11"),
 # A(a)-III -> PDF p4-5
 ("Clause A(a)-III, Eligibility i–iii &amp; Criteria", "GO 1438 · P.3", "GO 1438 · P.4–5"),
 ("Clause A(a)-III, Eligibility (iii)", "GO 1438 · P.3", "GO 1438 · P.5"),
 ("Clause A(a)-III, Eligibility (ii)(1)–(4)", "GO 1438 · P.3", "GO 1438 · P.5"),
 ("Clause A(a)-III, Criteria (i)", "GO 1438 · P.3", "GO 1438 · P.5"),
 ("Clause A(a)-III, Criteria (ii)", "GO 1438 · P.3", "GO 1438 · P.5"),
 ("Clause A(a)-III vs A(a)-I(ii)", "GO 1438 · P.3", "GO 1438 · P.3–5"),
 ("Clause A(a)-III(iii); Clause F(a),(c)", "GO 1438 · P.3, P.8", "GO 1438 · P.5, P.10"),
 ("Clauses A(a)-III(ii), A(b)-III(ii), E-3", "GO 1438 · P.3, P.5, P.8", "GO 1438 · P.5, P.7, P.10"),
 ("Clause A(a)-III(iii) absent from A(b)-III", "GO 1438 · P.3 vs P.5", "GO 1438 · P.5 vs P.7"),
 # A(b)-I -> PDF p5-6
 ("Clause A(b), Note (i)", "GO 1438 · P.3", "GO 1438 · P.6"),
 ("Clause A(b), Note (ii)", "GO 1438 · P.3", "GO 1438 · P.6"),
 ("Clause A(b)-I, Eligibility i–iii &amp; Notes", "GO 1438 · P.3–4", "GO 1438 · P.5–6"),
 ("Clause A(b)-I vs A(a)-I", "GO 1438 · P.3–4", "GO 1438 · P.3, P.5–6"),
 ("Clause A(b)-I, Eligibility (i)", "GO 1438 · P.4", "GO 1438 · P.5–6"),
 ("Clause A(b)-I, Eligibility (iii)", "GO 1438 · P.4", "GO 1438 · P.5–6"),
 ("Clause A(b)-I, Promotion Criteria i–ii", "GO 1438 · P.4", "GO 1438 · P.5–6"),
 ("Notes (i)–(ii) to Clause A(b)-I", "GO 1438 · P.4", "GO 1438 · P.6"),
 ("Note (ii) to Clause A(b)-I", "GO 1438 · P.4", "GO 1438 · P.6"),
 # A(b)-II -> PDF p6-7
 ("Clause A(b)-II, Eligibility i–ii", "GO 1438 · P.4", "GO 1438 · P.6–7"),
 ("Clause A(b)-II (ii)(2)", "GO 1438 · P.4", "GO 1438 · P.6–7"),
 ("Clause A(b)-II (ii)(3)", "GO 1438 · P.4", "GO 1438 · P.6–7"),
 ("Clause A(b)-II (ii)(4)", "GO 1438 · P.4", "GO 1438 · P.6–7"),
 ("Clause A(b)-II complete", "GO 1438 · P.4–5", "GO 1438 · P.6–7"),
 # promotion criteria across stages
 ("Clause A, Promotion Criteria (i) at each stage", "GO 1438 · P.3–5", "GO 1438 · P.3–5"),
 ("Clause A(a)/(b), Promotion Criteria (i) at each stage", "GO 1438 · P.3–5", "GO 1438 · P.3–7"),
 # A(b)-III -> PDF p7
 ("Clause A(b)-III, Eligibility &amp; Criteria", "GO 1438 · P.5", "GO 1438 · P.7"),
 ("Clause A(b)-III, Eligibility (ii)", "GO 1438 · P.5", "GO 1438 · P.7"),
 ("Clause A(b)-III — identical option text", "GO 1438 · P.5", "GO 1438 · P.7"),
 ("Clause A(b)-III(ii) &amp; Clause C-II", "GO 1438 · P.5", "GO 1438 · P.7–8"),
 ("Clause A(b)-III; Table 2 notes", "GO 1438 · P.5, P.11", "GO 1438 · P.7, P.13"),
 # B -> PDF p7
 ("Clause B", "GO 1438 · P.5", "GO 1438 · P.7"),
 ("Clause B — \"on and from 01.01.2025\"", "GO 1438 · P.5", "GO 1438 · P.7"),
 ("Clause B; E-5, E-6", "GO 1438 · P.5, P.8", "GO 1438 · P.7, P.10"),
 # C-I -> PDF p7-8
 ("Clause C-I", "GO 1438 · P.5", "GO 1438 · P.7–8"),
 ("Clause C-I — \"from one level to the other higher level\"", "GO 1438 · P.5", "GO 1438 · P.7–8"),
 ("Clause C-I — nomination structure", "GO 1438 · P.6", "GO 1438 · P.7–8"),
 ("Clause C-I; C-III(4)", "GO 1438 · P.5–6", "GO 1438 · P.7–8"),
 # C-II -> PDF p8
 ("Clause C-II(i)", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-II(i) — quorum sentence", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-II(i) — quorum for Selection only", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-II(i) — minority-institution sentence", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-II(i) — \"two subject experts\"", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-II(ii)", "GO 1438 · P.6", "GO 1438 · P.8"),
 # C-III -> PDF p8
 ("Clause C-III", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-III 2–3", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-III(1)–(2)", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-III(2)", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-III(3)", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-III(3) — \"signed by all members\"", "GO 1438 · P.6", "GO 1438 · P.8"),
 ("Clause C-III(4)", "GO 1438 · P.6", "GO 1438 · P.8"),
 # D -> PDF p8-9
 ("Clause D — \"college teachers\"", "GO 1438 · P.7", "GO 1438 · P.8–9"),
 ("Clause D (i)–(v)", "GO 1438 · P.7", "GO 1438 · P.9"),
 ("Clause D-i, including direct-teaching table", "GO 1438 · P.7", "GO 1438 · P.9"),
 ("Clause D-i — \"Thirty working weeks (One Hundred and Eighty teaching days)\"", "GO 1438 · P.7", "GO 1438 · P.9"),
 ("Clause D-i — mentoring sentence", "GO 1438 · P.7", "GO 1438 · P.9"),
 ("Clause D-i — direct teaching-learning workload table", "GO 1438 · P.7", "GO 1438 · P.9"),
 ("Clause D-ii — internal assessment sentence", "GO 1438 · P.7", "GO 1438 · P.9"),
 ("Clause D-v Step 1", "GO 1438 · P.7", "GO 1438 · P.9"),
 ("Clause D-v, Steps 1–2", "GO 1438 · P.7", "GO 1438 · P.9"),
 ("Clause D-v Step 1 — \"documentary evidence… verified\"", "GO 1438 · P.7", "GO 1438 · P.9"),
 # E -> PDF p9-10
 ("Clause E-1 — six-month rule", "GO 1438 · P.7", "GO 1438 · P.9–10"),
 ("Clauses E-1, E-5, E-6", "GO 1438 · P.7", "GO 1438 · P.9–10"),
 ("Clauses E-1, E-5, E-6, E-7", "GO 1438 · P.7–8", "GO 1438 · P.9–10"),
 ("Clauses E-1, E-5, E-6", "GO 1438 · P.7–8", "GO 1438 · P.9–10"),
 ("Clauses E-1, E-5", "GO 1438 · P.7–8", "GO 1438 · P.9–10"),
 ("Clauses E-5, E-6", "GO 1438 · P.7", "GO 1438 · P.10"),
 ("Clauses E-5, E-6", "GO 1438 · P.7–8", "GO 1438 · P.10"),
 ("Clauses E-5, E-6", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clauses E-6, E-7", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause E-2, E-3", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause E-4", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause E-6", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause E-7", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause E-8", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause E-9", "GO 1438 · P.8", "GO 1438 · P.10"),
 # F -> PDF p10
 ("Clause F — opening paragraph", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause F — \"should count for promotion under the CAS\"", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause F — \"national or international\"", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause F — post classes &amp; institution list", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause F (a)–(e)", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause F (a)–(e) applied to unlisted categories", "GO 1438 · P.8", "GO 1438 · P.10"),
 ("Clause F(a),(c) — equivalence conditions", "GO 1438 · P.8", "GO 1438 · P.10"),
 # Table 1 -> PDF p11
 ("Appendix I, Table 1, Sl. 1–2 &amp; Overall Grading", "GO 1438 · P.9", "GO 1438 · P.11"),
 ("Table 1, Sl. 1 — parenthetical", "GO 1438 · P.9", "GO 1438 · P.11"),
 ("Table 1, Sl. 1 grading bands", "GO 1438 · P.9", "GO 1438 · P.11"),
 ("Table 1, Sl. 2 (a)–(g)", "GO 1438 · P.9", "GO 1438 · P.11"),
 ("Table 1, Sl. 2 grading + Note", "GO 1438 · P.9", "GO 1438 · P.11"),
 ("Table 1, Sl. 2(g)", "GO 1438 · P.9", "GO 1438 · P.11"),
 ("Table 1 — Overall Grading block", "GO 1438 · P.9", "GO 1438 · P.11"),
 ("Table 1 — Note (leave exclusion)", "GO 1438 · P.9", "GO 1438 · P.11"),
 ("Table 1 note — \"within or across the broad categories\"", "GO 1438 · P.9", "GO 1438 · P.11"),
 ("Table 1 Note — exclusion + extrapolation text", "GO 1438 · P.9", "GO 1438 · P.11"),
 ("Table 1 Note — exclusion &amp; extrapolation", "GO 1438 · P.9", "GO 1438 · P.11"),
 # Table 2 -> PDF p12-13
 ("Table 2, Sl. 1", "GO 1438 · P.10", "GO 1438 · P.12–13"),
 ("Table 2, Sl. 1 — bullet list", "GO 1438 · P.10", "GO 1438 · P.12–13"),
 ("Table 2, Sl. 1 — librarian frame", "GO 1438 · P.10", "GO 1438 · P.12–13"),
 ("Table 2, Sl. 2", "GO 1438 · P.10", "GO 1438 · P.12–13"),
 ("Table 2, Sl. 2 grading bands", "GO 1438 · P.10", "GO 1438 · P.12–13"),
 ("Table 2, Sl. 3 (a) OR (b)", "GO 1438 · P.10", "GO 1438 · P.12–13"),
 ("Table 2, Sl. 4", "GO 1438 · P.10", "GO 1438 · P.12–13"),
 ("Table 2, Sl. 5 (i)–(vi)", "GO 1438 · P.10–11", "GO 1438 · P.12–13"),
 ("Table 2, Sl. 3(b) &amp; Sl. 5(i)", "GO 1438 · P.10–11", "GO 1438 · P.12–13"),
 ("Table 2, Sl. 3(b), Sl. 5(i), overall formula", "GO 1438 · P.10–11", "GO 1438 · P.12–13"),
 ("Appendix I, Table 2", "GO 1438 · P.10–11", "GO 1438 · P.12–13"),
 ("Table 2 notes 1–3", "GO 1438 · P.11", "GO 1438 · P.13"),
 ("Table 2 note 2", "GO 1438 · P.11", "GO 1438 · P.13"),
 ("Table 2 — Overall Grading block", "GO 1438 · P.11", "GO 1438 · P.13"),
 ("Table 2 — Notes (1)(2)(3)", "GO 1438 · P.11", "GO 1438 · P.13"),
 ("Overall Grading — Item 1 gate", "GO 1438 · P.11", "GO 1438 · P.13"),
 ("Note (1) — ICT monitoring", "GO 1438 · P.11", "GO 1438 · P.13"),
 # Appendix II-A -> PDF p14-21
 ("Appendix II-A heading &amp; signature blocks", "GO 1438 · P.12", "GO 1438 · P.14"),
 ("Appendix II-A — \"end of each academic year\"", "GO 1438 · P.12", "GO 1438 · P.14"),
 ("Appendix II-A / II-B headings", "GO 1438 · P.12, P.19", "GO 1438 · P.14, P.21"),
 ("Appendix II-A, Part A items 11 &amp; 16", "GO 1438 · P.12–13", "GO 1438 · P.14–15"),
 ("Appendix II-A/B, Part A items 1–16", "GO 1438 · P.12–13, P.19–20", "GO 1438 · P.14–15, P.21–23"),
 ("Appendix II-A &amp; II-B, complete", "GO 1438 · P.12–26", "GO 1438 · P.14–28"),
 ("Proforma signature blocks", "GO 1438 · P.13, P.26", "GO 1438 · P.15, P.23"),
 ("Proforma verification blocks", "GO 1438 · P.13, P.16, P.23–24", "GO 1438 · P.15, P.18, P.23, P.26"),
 ("Appendix II-A, Part B(1)", "GO 1438 · P.14", "GO 1438 · P.16"),
 ("Appendix II-A, Part B(2)", "GO 1438 · P.14–16", "GO 1438 · P.16–18"),
 ("Appendix II-A, Part B(1)–(3)", "GO 1438 · P.14–18", "GO 1438 · P.16–19"),
 ("Appendix II-A, Part B(2)(a)–(g) &amp; (3)", "GO 1438 · P.14–18", "GO 1438 · P.16–19"),
 ("Proforma II-A, Part B, 2(g) — ISSN/ISBN column", "GO 1438 · P.16", "GO 1438 · P.17"),
 ("Proforma 2(g) — ISSN/ISBN column", "GO 1438 · P.16", "GO 1438 · P.17"),
 ("Proforma 2(g) columns", "GO 1438 · P.16", "GO 1438 · P.17"),
 ("Part B(3) grading summary", "GO 1438 · P.17", "GO 1438 · P.19"),
 ("Proforma grading summary note", "GO 1438 · P.17", "GO 1438 · P.19"),
 ("II-A Part B(3); II-B grading summary", "GO 1438 · P.17, P.24", "GO 1438 · P.19, P.26"),
 ("Appendix II-A, Part C", "GO 1438 · P.18", "GO 1438 · P.20"),
 ("Appendix II-A/B, Part C", "GO 1438 · P.18, P.25", "GO 1438 · P.20, P.27"),
 ("Proforma Part C", "GO 1438 · P.18, P.25", "GO 1438 · P.20, P.27"),
 ("Proforma Part C — reversion clause", "GO 1438 · P.18, P.25", "GO 1438 · P.20, P.27"),
 ("Appendix II-A/II-B, Part D", "GO 1438 · P.19, P.26", "GO 1438 · P.21, P.28"),
 ("Appendix II-A/II-B, Parts C–D", "GO 1438 · P.19, P.26", "GO 1438 · P.20–21, P.27–28"),
 ("Appendix II-B, Part B(1)", "GO 1438 · P.21", "GO 1438 · P.23"),
 ("Appendix II-B, Part B(1)–(5)", "GO 1438 · P.21–24", "GO 1438 · P.23–26"),
 ("Appendix II-B, Part B(1)–(5) &amp; grading summary", "GO 1438 · P.21–24", "GO 1438 · P.23–26"),
 ("Appendix II-B, Part C", "GO 1438 · P.25", "GO 1438 · P.27"),
 ("All other clauses unaffected", "GO 1438 · P.3–26", "GO 1438 · P.3–28"),
]

applied, failed = 0, 0
for label, oldpg, newpg in M:
    old = f'<span class="pg">{oldpg}</span><i>{label}</i>'
    n = doc.count(old)
    if n == 0:
        print("NOT FOUND:", oldpg, "|", label[:60]); failed += 1; continue
    doc = doc.replace(old, f'<span class="pg">{newpg}</span><i>{label}</i>')
    applied += n

print("applied:", applied, "not-found:", failed)
if not failed:
    open(path, "w", encoding="utf-8", newline="").write(doc)
    print("SAVED")
