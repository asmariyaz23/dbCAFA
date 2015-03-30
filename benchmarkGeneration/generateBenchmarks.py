#!/usr/bin/env python
import sys
sys.path.insert(0, "/home/asmariyaz/dbCAFA/cafaModel")
import argparse
import os
from modelCAFA import Protein, ProteinGo, Go, Evidence

#This function queries the database 
def queries(year):
    nameGoEvidence = Protein.select(Protein.entryname ,Evidence.evidencecode ,Go.go_domain,
    Go.go_term).join(ProteinGo).join(Evidence).switch(ProteinGo).join(Go).where(Evidence.ondate.year ==
    year).order_by(Protein.entryname).naive()
    return nameGoEvidence

#Organize the data structure into a dictionary
def organize(nameGoEvidenceEarlier,nameGoEvidenceLater):
    earlierDict = {}
    laterDict = {}
    for earlier in nameGoEvidenceEarlier.iterator():
        earlierDict[earlier.entryname] = earlierDict.get(earlier.entryname,[]) + [((earlier.go_domain).strip(),(earlier.evidencecode).strip(),(earlier.go_term).strip())]
    for later in nameGoEvidenceLater.iterator():
        laterDict[later.entryname] = laterDict.get(later.entryname,[]) + [((later.go_domain).strip(),(later.evidencecode).strip(),(later.go_term).strip())]
    return earlierDict,laterDict

#Extract only those proteins which have non-exp 
#evidence codes alone
#this is only for no knowledge benchmarks
def collectNonExpProteinsEarlierOnly(earlierDict):
    nonexpEvidenceList = {'IEA':0,'ISS':0,'ISO':0,'ISA':0,'ISM':0,'IGC':0,'IBA':0,'IBD':0,'IKR':0,'IRD':0,'RCA':0}
    nonexpProteins = []
    for EntryName, EvidenceCodeList in earlierDict.items():
        allEviCodes = [c[1] for c in EvidenceCodeList]
        intersect = set(nonexpEvidenceList.keys()) & set(allEviCodes)
        if len(intersect) == len(set(allEviCodes)):
           nonexpProteins.append(EntryName)
    ##print "Accumalated non-exp proteins from earlier dataset."
    return nonexpProteins
                               
#Compare those earlier nonexp proteins with later
#proteins to check which ones turn exp in at least one of the ontologies
#this is only for no knowledge benchmarks
def compareNonExpWithLaterDict(laterDict,earlierDict):
    nonexpEvidenceList = {'IEA':0,'ISS':0,'ISO':0,'ISA':0,'ISM':0,'IGC':0,'IBA':0,'IBD':0,'IKR':0,'IRD':0,'RCA':0}
    expEvidenceList = {'EXP':0,'IDA':0,'IPI':0,'IMP':0,'IGI':0,'IEP':0}
    benchmarkProteins = {}
    for EntryName, later_ontoEviTermList in laterDict.items():
        if EntryName in nonexpProteins:
           for later_ontoEviTerm in later_ontoEviTermList:
               if later_ontoEviTerm[1] in expEvidenceList.keys():
                  earlier_ontoEviTermList = earlierDict[EntryName]
                  for earlier_ontoEviTerm in earlier_ontoEviTermList:
                      if earlier_ontoEviTerm[2] == later_ontoEviTerm[2]:
                         benchmarkProteins[EntryName] = benchmarkProteins.get(EntryName,[]) + [(later_ontoEviTerm[2],later_ontoEviTerm[1],later_ontoEviTerm[0])]
    return benchmarkProteins

## Only for partial knowledge
def compare(laterDict,earlierDict,ontology):
    ##proteinsforcheck = []
    proteinsType2 = {}
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
    return proteinsType2

def writingToFile(benchmarkProteins,dirname,filename):
    if not os.path.exists(dirname):
       os.makedirs(dirname)
    list_lines = []
    for proteinName, termEviOntoList in benchmarkProteins.items():
        for t,evi,o in termEviOntoList:
            list_lines.append(proteinName + "\t" + t + "\t"+ evi + "\t" + o + "\n")
    benchmarkFile = os.path.join(dirname,filename)
    f = open(benchmarkFile + ".csv","w")
    f.writelines(list_lines)

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("--chooseType","-t",help="Either noKnowledge or partialKnowledge")
   parser.add_argument("--chooseOntology","-o",help="Only if partialKnowledge choose: molecular_function OR biological_process OR cellular_component; skip this option if noKnowledge")
   parser.add_argument("--chooseoutput","-d",help="Output directory path")
   args = parser.parse_args()
   nameGoEvidenceEarlier = queries(2013)
   nameGoEvidenceLater = queries(2014)
   earlierDict,laterDict= organize(nameGoEvidenceEarlier,nameGoEvidenceLater)
   if args.chooseType == "noKnowledge":
      nonexpProteins = collectNonExpProteinsEarlierOnly(earlierDict)
      benchmarkProteins = compareNonExpWithLaterDict(laterDict,earlierDict)
      writingToFile(benchmarkProteins,args.chooseoutput,"noKnowledge")
   elif args.chooseType == "partialKnowledge":
      benchmarkProteins = compare(laterDict,earlierDict,args.chooseOntology)
      writingToFile(benchmarkProteins,args.chooseoutput,"partialKnowledge_"+args.chooseOntology)
   else:
      print "choose either noKnowledge or partialKnowledge"
