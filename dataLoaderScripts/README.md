Step 1: term_extract.py:

Run this script to extract required information from the GO file containing GO ids, GO term, ontology

This script requires the GO file as input and generates the data for GO table.

python term_extract.py term.txt

Step2: prepareCAFAIds.py:

Run this script to get a file with proteins with their CAFAId tragets.

Takes 2 files 1)Earlier swissprot file 2)Later swissprot file

Generates 3 files: 1)old mapping file 2)new mapping file 3)Protein

Step3: python prepareCAFAIds.py [earlier_swissprotfile] [later_swissprotfile]

prepareProtein_GO.py:

Run this script to get a file which connects the indices in Protein and GO files generated by the first 2 scripts.

Uses Protein, GO as reading files and generated data required for Protein_GO table.

python prepareProtein_GO.py [Protein file generated from 2 step] [earlier_swissprotfile] [later_swissprotfile] [GO file
gernerated from Step 1] [your choice of output file for Protein_GO table] 

Step 4: prepareEvidence.py:

Run this script to genearte a file containing Protein_GO indices mapped to evidence code and the year in which it was
associated with that protein.

Uses protien, old mapping, new mapping, Go, Protein_GO as reading files(from earlier step) and generates data required for insertion in Evidence table.

python prepareEvidence.py [Protein file generated from step 2] [earlier_swissprotfile] [later_swissprotfile] [GO file
gernerated from Step 1] [Protein_GO file from step 3] [A text file containing only the time points you are looking at (sample
in sample data directory)] [your choice of evidence outfile]
