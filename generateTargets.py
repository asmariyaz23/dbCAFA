#!/usr/bin/env python
from dbCAFA import Protein, ProteinGo, Go, Evidence

nameGoEvidenceEarlier = Protein.select(Protein.entryname ,Evidence.evidencecode ,Go.go_domain,
Go.go_term).join(ProteinGo).join(Evidence).switch(ProteinGo).join(Go).where(Evidence.ondate.year ==
2013).order_by(Protein.entryname).naive()

nameGoEvidenceLater = Protein.select(Protein.entryname, Go.go_domain, Go.go_term
,Evidence.evidencecode).join(ProteinGo).join(Evidence).switch(ProteinGo).join(Go).where(Evidence.ondate.year ==
2014).order_by(Protein.entryname).naive()

print "done querying."

nonexpEvidenceList = {'IEA':0,'ISS':0,'ISO':0,'ISA':0,'ISM':0,'IGC':0,'IBA':0,'IBD':0,'IKR':0,'IRD':0,'RCA':0}
expEvidenceList = {'EXP':0,'IDA':0,'IPI':0,'IMP':0,'IGI':0,'IEP':0}
nonexpProteins = []
expProteins = []
earlierDict = {}
laterDict = {}


for earlier in nameGoEvidenceEarlier.iterator():
    earlierDict[earlier.entryname] = earlierDict.get(earlier.entryname,[]) + [((earlier.go_domain).strip(),(earlier.evidencecode).strip(),(earlier.go_term).strip())]
for later in nameGoEvidenceLater.iterator():
    laterDict[later.entryname] = laterDict.get(later.entryname,[]) + [((later.go_domain).strip(),(later.evidencecode).strip(),(later.go_term).strip())]



for EntryName, EvidenceCodeList in earlierDict.items():
    allEviCodes = [c[1] for c in EvidenceCodeList]
    intersect = set(nonexpEvidenceList.keys()) & set(allEviCodes)
    if len(intersect) == len(set(allEviCodes)):
       nonexpProteins.append(EntryName)
print "Accumalated non-exp proteins from earlier dataset."
                                   

for EntryName, later_ontoEviTermList in laterDict.items():
    if EntryName in nonexpProteins:
       for later_ontoEviTerm in later_ontoEviTermList:
           if later_ontoEviTerm[1] in expEvidenceList.keys():
              earlier_ontoEviTermList = earlierDict[EntryName]
              for earlier_ontoEviTerm in earlier_ontoEviTermList:
                  if earlier_ontoEviTerm[2] == later_ontoEviTerm[2]:
                     expProteins.append(EntryName)        

##print expProteins
print len(expProteins)








'''
nameEvidenceEarlier = Protein.select(Protein.entryname ,Evidence.evidencecode).join(ProteinGo).join(Evidence).where(Evidence.ondate.year == 2013).order_by(Protein.entryname).tuples()

nameEvidenceLater = Protein.select(Protein.entryname ,Evidence.evidencecode).join(ProteinGo).join(Evidence).where(Evidence.ondate.year == 2014).order_by(Protein.entryname).tuples()


for EntryName, EvidenceCode in nameEvidenceEarlier:
    EntryNameDictEarlier[EntryName] = EntryNameDictEarlier.get(EntryName,[]) + [EvidenceCode.strip()]

for EntryName, EvidenceCode in nameEvidenceLater:
    EntryNameDictLater[EntryName] = EntryNameDictLater.get(EntryName,[]) + [EvidenceCode.strip()]

print "Earlier:",EntryNameDictEarlier
print "Later:",EntryNameDictLater
'''
