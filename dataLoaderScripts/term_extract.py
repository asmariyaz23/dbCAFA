import sys
import csv

f = sys.argv[1]
f_handle = open(f,'r')
name = []
term_type = []
acc = []

read = csv.reader(f_handle, delimiter='\t')
for i, row in enumerate(read):
    if not i == 0:
       name.append(row[1])
       term_type.append(row[2])
       acc.append(row[3])  
##extracted = zip(name,term_type,acc)

with open('extracted_term.txt', 'w') as of:
    print >> of, "GO_id", '\t', "GO_Term",'\t', "GO_Domain"
    for acc,name,term_type in zip(acc,name,term_type):
        print >> of, acc, '\t', name, '\t', term_type


       
