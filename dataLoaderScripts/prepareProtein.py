#!/usr/bin/python
import sys
import csv
from Bio import SwissProt as swiss
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from collections import defaultdict
from os.path import basename
import itertools 
import argparse

def has_go(sp_rec):
    retval = False
    for xref in sp_rec.cross_references:
        if xref[0] == 'GO':
            retval = True
            break
    return retval

def generateTaxIds(f_handle):
    EntryNameTaxIdDict = {}
    for sp_rec in swiss.parse(f_handle):
        EntryNameTaxIdDict[sp_rec.entry_name] = sp_rec.taxonomy_id 
    return EntryNameTaxIdDict

def generate(sp_handle, EntryNameTaxIdDict):
    EntryCAFAId = defaultdict(list)
    visited_taxa = {}
    entryAcc = {}
    for sp_rec in swiss.parse(sp_handle):
        if has_go(sp_rec):
           taxList = EntryNameTaxIdDict[sp_rec.entry_name]
           for tax in taxList:
               if not tax in visited_taxa.keys():
                  target_id = int(tax + str("%07d" % 1))
                  visited_taxa[tax] = "%07d" % 1
               else:
                  extraNum = visited_taxa[tax]        
                  visited_taxa[tax] = "%07d" % (int(extraNum) + 1)
                  target_id = int(tax + visited_taxa[tax])
               EntryCAFAId[sp_rec.entry_name].append('T'+str(target_id))
           entryAcc[sp_rec.entry_name]= ','.join(sp_rec.accessions)
    return EntryCAFAId, entryAcc

go_ontology_lut = {'P': 'BPO', 'C':'CCO', 'F':'MFO'}
def parse_go(sp_rec, year):
    go_list = []
    for xref in sp_rec.cross_references:
        if xref[0] == 'GO':
            go_rec = {}
            go_rec['go_id'] = xref[1]
            go_rec['ontology'] = go_ontology_lut[xref[2].split(':')[0]]
            go_rec['accessions'] = ', '.join(sp_rec.accessions)
            go_rec['year'] = year
            try:
                go_rec['evidence'] = xref[3].split(':')[0]
            except IndexError:
                print sp_rec.entry_name
                print go_rec
                print xref
                raise
            go_list.append(go_rec)
    return go_list



def generateMapping(sp1,sp2):
    mappingEarlier = {}
    mappingLater = {}
    year1 = "2013-05-29"
    year2 = "2014-05-29"
    for sp_rec in swiss.parse(sp1):
        go_list = parse_go(sp_rec,year1) 
        mappingEarlier[sp_rec.entry_name]= go_list
    for sp_rec in swiss.parse(sp2):    
        if mappingEarlier.has_key(sp_rec.entry_name):
           go_list = parse_go(sp_rec,year2) 
           mappingLater[sp_rec.entry_name]= go_list           
    return mappingEarlier, mappingLater

def writeMapping(mapWriterHandle,mapDict):
    for entryName, go_dicts in mapDict.items():
        for go_dict in go_dicts:
            print >> mapWriterHandle, entryName, "\t" ,go_dict['accessions'] , "\t", go_dict['go_id'] , "\t", go_dict['ontology'], "\t", go_dict['evidence'], "\t", go_dict['year'] 



def getVersion(filePath):
    l = basename((filePath)).split('/')
    for s in l:
        if "_" in s:
           version = s.split("_")
    return version[1]

def parser_code():

    parser = argparse.ArgumentParser(description='The purpose of this step is generate all swissprot data required to load into database for querying')

    parser.add_argument("-o", "--older", metavar="FILE",
                         help = "Older swissprot input file.")
    parser.add_argument("-d", "--outputdata",
                         help = "Provide path for redirecting your output.")
    parser.add_argument("-n", "--newer", metavar="FILE",
                         help = "Newer swissprot input file.")
    parser.add_argument("-t", "--tempdir", 
                         help = "Provide path for temporary directory.")
    return parser.parse_args()



def main():

    parsed_args     = parser_code()

    olderSwissFile  = parsed_args.older
    newSwissFile    = parsed_args.newer
    outputDir       = parsed_args.outputdata
    tempdir         = parsed_args.tempdir

    with open(olderSwissFile, 'r') as file_handle:
         taxIds = generateTaxIds(file_handle)
         print "Preparing protein data - Step 1: fetching taxonomy Ids."
    

    with open(olderSwissFile, 'r') as file_handle:  
         EntryCAFA, entryAccDict = generate(file_handle,taxIds)
         print "Preparing protein data - Step 2: generating CAFA Ids based on taxonomy ids."
    

    with open(tempdir + 'EntryNameCAFAId','w') as file_handle:
         for k,v in EntryCAFA.items():
             print >> file_handle,k,"\t",v[0]
         print "Preparing protein data - Step 3: writing a temp file, maps protein with its CAFA Ids."


    with open (olderSwissFile, 'r') as sp1_fileHandle , open(newSwissFile, 'r') as sp2_fileHandle:
         mappingEarlier, mappingLater = generateMapping(sp1_fileHandle, sp2_fileHandle)

         
    with open (tempdir + 'EntryAccGOontoEviYearEarlier','w') as earlierWriter, open(tempdir + 'EntryAccGOontoEviYearLater','w') as laterWriter:
         writeMapping(earlierWriter,mappingEarlier)
         writeMapping(laterWriter,mappingLater)
         print "Preparing protein data - Step 4: writing the old and new mapping files to temp directory."


    with open(outputDir + 'Protein','w') as outfile:
         for k,v in EntryCAFA.items():
             target_id = EntryCAFA[k]
             print >> outfile, k , "\t", entryAccDict[k] , "\t", str(target_id[0]), "\t"      
         print "Preparing protein data - Step 5: writing Protein data to %s" %  (outputDir + 'Protein')
     
if __name__ == '__main__':
    main()    


'''    
if __name__ == '__main__':
   sp1 = sys.argv[1]
   sp2 = sys.argv[2]
   with open(sp1,'r') as file_handle:
        for sp in swiss.parse(file_handle):
            print sp
   with open(sp1, 'r') as file_handle:
        taxIds = generateTaxIds(file_handle)
        print ('1 of 6')
   with open(sp1, 'r') as file_handle:  
        EntryCAFA, entryAccDict = generate(file_handle,taxIds)
        print ('2 of 6')
   ##versionYear = getVersion(versionEntry)
   with open('EntryNameCAFAId','w') as file_handle:
        for k,v in EntryCAFA.items():
            print >> file_handle,k,"\t",v[0]
        print ('3 of 6')
   with open (sp1, 'r') as sp1_fileHandle , open(sp2, 'r') as sp2_fileHandle:
        mappingEarlier, mappingLater = generateMapping(sp1_fileHandle, sp2_fileHandle)
        print ('4 of 6')
   with open ('EntryAccGOontoEviYearEarlier','w') as earlierWriter, open('EntryAccGOontoEviYearLater','w') as laterWriter:
        writeMapping(earlierWriter,mappingEarlier)
        writeMapping(laterWriter,mappingLater)
        print ('5 of 6')
   with open('Protein','w') as outfile:
        for k,v in EntryCAFA.items():
            target_id = EntryCAFA[k]
            print >> outfile, k , "\t", entryAccDict[k] , "\t", str(target_id[0]), "\t"      
        print ('6 of 6')
'''
        

