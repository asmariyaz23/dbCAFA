#!/usr/bin/python
import sys
import csv
import argparse

##f = sys.argv[1]
def parser_code():

    parser = argparse.ArgumentParser(description="This program will be used to generate data required for GO table.")
    
    parser.add_argument("-g", "--goterm" , metavar="FILE",
                        help="File contains go_id, ontology and term in tab-delimeted.")    

    parser.add_argument("-d", "--outputdirectory" , metavar = "DIRECTORY",
                        help="")
    
    return parser.parse_args() 

def main():
    
    parsed_args     = parser_code()
    gotermFile      = parsed_args.goterm
    outputDataDir   = parsed_args.outputdirectory
    f_handle        = open(gotermFile,'r')
    
    name = []
    term_type = []
    acc = []

    read = csv.reader(f_handle, delimiter='\t')
    for i, row in enumerate(read):
        if not i == 0:
           name.append(row[1])
           term_type.append(row[2])
           acc.append(row[3])  
    ##print outputDataDir + 'GO'
    with open(outputDataDir + 'GO', 'w') as of:
         print >> of, "GO_id", '\t', "GO_Term",'\t', "GO_Domain"
         for acc,name,term_type in zip(acc,name,term_type):
             print >> of, acc, '\t', name, '\t', term_type

if __name__ == '__main__':
    main()
