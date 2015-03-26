import sys
import csv
from collections import defaultdict

def protein(proteinReader):
    proteinDict = {}
    proteinIndex = 1
    for proteinRow in proteinReader:
        proteinDict[proteinRow[0].strip()] = proteinIndex
        proteinIndex+=1
    return proteinDict    

def mapping(mappingReader):
    mappingDict = defaultdict(list)
    for mappingRow in mappingReader:
        mappingDict[mappingRow[0].strip()].append((mappingRow[2].strip(),mappingRow[4].strip(),mappingRow[5].strip()))        
    return mappingDict    

def go(goReader):
    goIndex = 0
    goDict = {}
    for goRow in goReader:
        if goIndex != 0:
           goDict[goRow[0].strip()] = goIndex
        goIndex+=1
    return goDict

def Protein_GO(Protein_GOReader):
    Protein_GOList = {}
    i = 0
    for row in Protein_GOReader:
        if i!= 0:
           Protein_GOList[(row[0].strip(),row[1].strip())] = i
        i+=1
    return Protein_GOList                 

def Timepoint(TimepointReader):
    i = 1
    TimepointDict = {}
    for row in TimepointReader:
        TimepointDict[row[0]] = i
        i+=1
    return TimepointDict


def generateReader(file_handle): 
    r = csv.reader(file_handle, delimiter = "\t")
    return r


def gather(proteinDict,mappingDict, goDict, Protein_GODict, TimepointDict):
    jointEvidence = []
    for protein,proteinIndex in proteinDict.items():
        goIdECTimeList = mappingDict[protein]
        for goId,EC,Time in goIdECTimeList:
            goIndex         = goDict[goId]
            Protein_GOIndex = Protein_GODict[(str(proteinIndex), str(goIndex))]
            timeIndex       = TimepointDict[Time]
            jointEvidence.append((EC, Protein_GOIndex, proteinIndex, goIndex, timeIndex))
    return jointEvidence

proteinFileHandle = sys.argv[1]
oldmappingFileHandle = sys.argv[2]
newmappingFileHandle = sys.argv[3]
goFileHandle      = sys.argv[4]
Protein_GOHandle  = sys.argv[5]
TimepointHandle   = sys.argv[6]
Evidence          = sys.argv[7]


with open(proteinFileHandle , "r") as proteinFile ,open(oldmappingFileHandle , "r") as oldmappingFile ,open(newmappingFileHandle ,"r")as newmappingFile ,open(goFileHandle , "r") as goFile,open(Protein_GOHandle, "r") as Protein_GOFile ,open(TimepointHandle, "r") as TimepointFile, open(Evidence, "w") as outfile:

     proteinReader      = generateReader(proteinFile)
     oldmappingReader   = generateReader(oldmappingFile)
     newmappingReader   = generateReader(newmappingFile)
     goReader           = generateReader(goFile)
     Protein_GOReader   = generateReader(Protein_GOFile)
     TimepointReader    = generateReader(TimepointFile)

     proteinDict        = protein(proteinReader)
     oldmappingDict     = mapping(oldmappingReader)
     newmappingDict     = mapping(newmappingReader)
     goDict             = go(goReader)
     Protein_GOList     = Protein_GO(Protein_GOReader)     
     TimepointDict      = Timepoint(TimepointReader)

     oldjointEvidence      = gather(proteinDict,oldmappingDict, goDict, Protein_GOList, TimepointDict)
     newjointEvidence      = gather(proteinDict,newmappingDict, goDict, Protein_GOList, TimepointDict)

     jointEvidence         = set(oldjointEvidence + newjointEvidence)
     i = 0
     for EC, Protein_GOIndex, proteinIndex, goIndex, timeIndex in jointEvidence:
         if i == 0:
            print >> outfile, "EvidenceCode","\t","FK_Protein_GO","\t","FK_Protein", "\t", "FK_GO", "\t", "FK_Timepoint"
            i+=1
         print >> outfile, EC, "\t", Protein_GOIndex, "\t", proteinIndex, "\t", goIndex, "\t", timeIndex
     
        
