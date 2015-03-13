#!/usr/bin/env python
from mockCAFA import Protein, ProteinGo, Go, Evidence
import sys
import pickle

ontology = sys.argv[1]

nameGoEvidenceEarlier = Protein.select(Protein.entryname ,Evidence.evidencecode ,Go.go_domain, Go.go_term).join(ProteinGo).join(Evidence).switch(ProteinGo).join(Go).where(Evidence.ondate.year == 2013).order_by(Protein.entryname).naive()

nameGoEvidenceLater = Protein.select(Protein.entryname, Go.go_domain, Go.go_term ,Evidence.evidencecode).join(ProteinGo).join(Evidence).switch(ProteinGo).join(Go).where(Evidence.ondate.year == 2014).order_by(Protein.entryname).naive()

print "done querying."

earlierDict = {}
laterDict = {}
proteinsforcheck = []
proteinsType2 = {}


for earlier in nameGoEvidenceEarlier.iterator():
    earlierDict[earlier.entryname] = earlierDict.get(earlier.entryname,[]) + [((earlier.go_domain).strip(),(earlier.evidencecode).strip(),(earlier.go_term).strip())] 
for later in nameGoEvidenceLater.iterator():
    laterDict[later.entryname] = laterDict.get(later.entryname,[]) + [((later.go_domain).strip(),(later.evidencecode).strip(),(later.go_term).strip())] 


nonexpEvidenceList = ['IEA','ISS','ISO','ISA','ISM','IGC','IBA','IBD','IKR','IRD','RCA','TAS','NAS','IC','ND']
expEvidenceList = ['EXP','IDA','IPI','IMP','IGI','IEP']

for entryName, later_ontoEviTermList in laterDict.items():
    for later_ontoEviTerm in later_ontoEviTermList:
        if (ontology == later_ontoEviTerm[0]) & (later_ontoEviTerm[1] in expEvidenceList):
           if earlierDict.has_key(entryName):
              earlier_ontoEviTermList = earlierDict[entryName]
              earlier_ontologies=[earlierOntology[0] for earlierOntology in earlier_ontoEviTermList if earlierOntology[0] == ontology]
              if not earlier_ontologies:
                 proteinsType2[entryName] = later_ontoEviTermList
               



                                      
print len(proteinsType2)




















##pickle.dump(earlierDict, open("earlier.p","wb"))
##pickle.dump(laterDict, open("later.p","wb"))

##earlierDict = pickle.load(open("earlier.p","rb"))
##laterDict = pickle.load(open("later.p","rb"))

##for entryname,earlier_ontologyCodeTermList in earlierDict.items():
##    for o,c,t in earlier_ontologyCodeTermList:
##        if c in nonexpEvidenceList:
##           if (o == ontology):
##              later_ontologyCodeTermList=laterDict[entryname]
##              for later_octerm in later_ontologyCodeTermList:
##                  if (later_octerm[0] == ontology) and (later_octerm[1] in expEvidenceList):
##                     proteinsType2[entryname] = later_octerm[0],later_octerm[1],later_octerm[2]
##print len(proteinsType2) 
