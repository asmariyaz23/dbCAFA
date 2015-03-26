import sys
import csv
from Bio import SwissProt as swiss
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from collections import defaultdict
from os.path import basename
import itertools 

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
    return EntryCAFAId 

def getVersion(filePath):
    l = basename((filePath)).split('/')
    for s in l:
        if "_" in s:
           version = s.split("_")
    return version[1]
    
if __name__ == '__main__':
   sp = sys.argv[1]
   versionEntry = sys.argv[2]
   EntryAcc = {}
   with open(sp, 'r') as file_handle:
        taxIds = generateTaxIds(file_handle)
        print ('1 of 5')
   with open(sp, 'r') as file_handle:  
        EntryCAFA = generate(file_handle,taxIds)
        print ('2 of 5')
   ##versionYear = getVersion(versionEntry)
   with open('EntryNameCAFAId','w') as file_handle:
        for k,v in EntryCAFA.items():
            print >> file_handle,k,"\t",v[0]
        print ('3 of 5')
   with open (versionEntry, 'r') as infile:
        r = csv.reader(infile, delimiter = "\t")
        for row in r:
            EntryAcc[row[0]] = row[1]
        print ('4 of 5')
   with open(versionEntry,'r') as infile, open('Protein','w') as outfile:
        r = csv.reader(infile, delimiter="\t")
        for k,v in EntryCAFA.items():
            target_id = EntryCAFA[k]
            print >> outfile, k , "\t", EntryAcc[k] , "\t", str(target_id[0]), "\t"      
        print ('5 of 5')

        

