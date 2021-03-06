#!/usr/bin/python
import sys
import csv
from collections import defaultdict
import argparse

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
        mappingDict[mappingRow[0].strip()].append(mappingRow[2].strip())        
    return mappingDict    

def go(goReader):
    goIndex = 0
    goDict = {}
    for goRow in goReader:
        if goIndex != 0:
           goDict[goRow[0].strip()] = goIndex
        goIndex+=1
    return goDict

def gather(proteinDict,mappingDict, goDict):
    jointGOProtein = []
    for protein,proteinIndex in proteinDict.items():
        goIdList = mappingDict[protein]
        for goId in goIdList:
            goIndex = goDict[goId]
            jointGOProtein.append((proteinIndex, goIndex))
    return jointGOProtein

                 
def generateReader(file_handle): 
    r = csv.reader(file_handle, delimiter = "\t")
    return r

def getVersion(filePath):
    l = basename((filePath)).split('/')
    for s in l:
        if "_" in s:
           version = s.split("_")
    return version[1]



##proteinFileHandle = sys.argv[1]
##oldmappingFileHandle = sys.argv[2]
##newmappingFileHandle = sys.argv[3]
##goFileHandle      = sys.argv[4]
##Protein_GO        = sys.argv[5]

def parser_code():
    
    parser = argparse.ArgumentParser(description='This script generates Protein_GO data.')

    parser.add_argument("-d", "--dataoutputdir", metavar="DIRECTORY",
                        help="Folder contains the output.")
                 
    parser.add_argument("-t", "--tempdir",  metavar="DIRETORY",
                        help="Folder contains the temporary files.")
    

    return parser.parse_args()

def main():

    parsed_args = parser_code()

    dataoutputdir = parsed_args.dataoutputdir    
    tempdir       = parsed_args.tempdir   

    proteinFileHandle = dataoutputdir + "Protein" 
    goFileHandle      = dataoutputdir + "GO"
    Protein_GO        = dataoutputdir + "Protein_GO"
    
    oldmappingFileHandle = tempdir + "EntryAccGOontoEviYearEarlier"
    newmappingFileHandle = tempdir + "EntryAccGOontoEviYearLater" 
    
    ##print proteinFileHandle 
    ##print goFileHandle    
    ##print Protein_GO
    ##print oldmappingFileHandle
    ##print newmappingFileHandle  

    with open(proteinFileHandle , "r") as proteinFile ,open(oldmappingFileHandle , "r") as oldmappingFile,open(newmappingFileHandle , "r") as newmappingFile ,open(goFileHandle , "r") as goFile, open(Protein_GO, "w") as outfile:

         proteinReader    = generateReader(proteinFile)
         oldmappingReader = generateReader(oldmappingFile)
         newmappingReader = generateReader(newmappingFile)
         goReader         = generateReader(goFile)

         proteinDict       = protein(proteinReader)
         newmappingDict    = mapping(newmappingReader)
         oldmappingDict    = mapping(oldmappingReader)
         goDict            = go(goReader)
         oldjointGOProtein = gather(proteinDict,oldmappingDict, goDict)
         newjointGOProtein = gather(proteinDict,newmappingDict, goDict)    
 
         i = 0
         joint = set(oldjointGOProtein + newjointGOProtein)
         for proteinIndex, goIndex in joint:
             if i == 0:
                print >> outfile, "FK_Protein", "\t", "FK_GO"
                i+=1
             print >> outfile,proteinIndex,"\t",goIndex
     
       
if __name__ == '__main__':
    main() 
