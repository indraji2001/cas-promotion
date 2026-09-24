import re

path = "CAS_Promotion_2026_GovtAidedColleges_Interactive_11_GO1438.html"
html = open(path, encoding="utf-8").read()

# (go,pg,ln, old, new, expected_count) — normalized spacing; wording untouched
fixes = [
 (1438,3,15, "yearsofservice and having", "years of service and having", 1),
 (1438,3,16, "six yearsofservice", "six years of service", 1),
 (1438,3,25, "MOOCscourse", "MOOCs course", 1),
 (1438,4,3, "haveacquired", "have acquired", 1),
 (1438,4,4, "Academic Level12:", "Academic Level 12:", 1),
 (1438,4,8, "Programmeof at least two weeks", "Programme of at least two weeks", 1),
 (1438,7,20, "andSelection Committee", "and Selection Committee", 1),
 (1438,9,12, "CASalong with", "CAS along with", 1),
 (1438,9,14, "to thecollege,", "to the college,", 1),
 (1438,9,14, "andcomplete the process", "and complete the process", 1),
 (1438,10,2, "from AssistantProfessor to", "from Assistant Professor to", 1),
 (1438,10,4, "gradingspecified", "grading specified", 1),
 (1438,10,5, "successful, thedate of promotion", "successful, the date of promotion", 1),
 (1438,10,7, "effectivedate of rejection", "effective date of rejection", 1),
 (1438,10,8, "under CASfrom 01.01.2025", "under CAS from 01.01.2025", 1),
 (1438,10,8, "dated 31.12.2012and subsequent", "dated 31.12.2012 and subsequent", 1),
 (1438,11,8, "assigned bythe college", "assigned by the college", 1),
 (1438,11,8, "extension andfield-based", "extension and field-based", 1),
 (1438,11,8, "projectsponsored by", "project sponsored by", 1),
 (1438,11,8, "undertaken anyof the activities", "undertaken any of the activities", 1),
 (1438,11,8, "across thebroad categories", "across the broad categories", 1),
 (1438,11,10, "durationwhich have been", "duration which have been", 1),
 (1438,12,10, "missingbooks", "missing books", 1),
 (1438,16,5, "Modeof Teaching", "Mode of Teaching", 1),
 (1438,19,8, "period ofassessment", "period of assessment", 1),
 (1438,19,15, "sealas per", "seal as per", 1),
 (1438,28,6, "Post of CollegeLibrarian(Academic Level 11/12) /CollegeLibrarian (Academic",
            "Post of College Librarian (Academic Level 11/12) / College Librarian (Academic", 1),
 (1439,1,22, "PageNo.2", "Page No. 2", 1),
 (1439,1,22, "Academic Level12) :", "Academic Level 12) :", 1),
 (1439,1,22, "MAYBE CONSIDERED", "MAY BE CONSIDERED", 1),
 (1439,2,1, "AppendixI,TableI", "Appendix I, Table I", 1),
 (1439,2,4, "PageNo.4", "Page No. 4", 1),
 (1439,2,4, "ITWILLBESAME", "IT WILL BE SAME", 1),
 (1439,3,3, "Appendix I,Table1,", "Appendix I, Table 1,", 1),
 (1439,3,3, "Atleast one single", "At least one single", 1),
 (1439,3,3, "BOOKCHAPTER", "BOOK CHAPTER", 1),
 (1439,3,3, "WITHISBNNUMBERCANBEIN CLUDEDASAN", "WITH ISBN NUMBER CAN BE INCLUDED AS AN", 1),
 (1439,3,3, "against Sl.No.2(g) in Appendix I, Table 1", "against Sl.No. 2(g) in Appendix I, Table 1", 1),
 (1439,3,4, "AppendixI,Table 2,", "Appendix I, Table 2,", 1),
]

fail = 0
for go,pg,ln,old,new,cnt in fixes:
    n = html.count(old)
    if n != cnt:
        print(f"FAIL [{go},{pg},{ln}] count={n} for: {old[:60]}")
        fail += 1
        continue
    html = html.replace(old, new)
print("applied:", len(fixes)-fail, "failed:", fail)

if not fail:
    open(path, "w", encoding="utf-8", newline="").write(html)
    print("SAVED")
