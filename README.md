To use this CAFA benchmarking software perform the following 4 steps:

1) Generate Data (use the dataLoadingScripts directory):

usage: main.py [-h] [-o FILE] [-n FILE] [-g FILE] [-d DATAOUTPUT]

The purpose of this step is generate all swissprot data required to load into
database for querying

optional arguments:

  -h, --help            show this help message and exit

  -o FILE, --older FILE

                        Older swissprot input file.

  -n FILE, --newer FILE

                        Newer swissprot input file.

  -g FILE, --goterm FILE
                        
                        Go term file, tab separated.
  -d DATAOUTPUT, --dataoutput DATAOUTPUT

                        Provide path for redirecting your output.


2) Create database and load schema 

   1.Create the database in mysql command line:

     create [dbname];

     exit

   2.mysql -u [username] -p try < cafa.sql

     (Note: cafa.sql located in schema directory)


3) Loading data generated in Step (1) into the database created in Step (2):

   Edit file: /dbCAFA/dataLoaderScripts/cafaDBLoading.txt to reflect dbNAME and file paths of all the data files generated in Step 1.

   Run the following command in shell:
   
   mysql -u [username] -p < /dbCAFA/dataLoaderScripts/cafaDBLoading.txt

   Note: Sometimes the path of the file is not found by mysql due to some problems, here is what I did to solve the issue:

         sudo apt-get install apparmor-utils

         sudo aa-complain /usr/sbin/mysqld

         sudo /etc/init.d/apparmor reload


4) Benchmark generation (use folder benchmarkGeneration):

   To generate benchmarks firstly modify 2nd line in cafaModel/modelCAFA.py to reflect your username, password and database name.

   Next run the script in benchmarkGeneration folder

   usage: generateBenchmarks.py [-h] [--chooseType CHOOSETYPE]

                                [--chooseOntology CHOOSEONTOLOGY]

   optional arguments:

   -h, --help            show this help message and exit

   --chooseType CHOOSETYPE, -t CHOOSETYPE

                        Either noKnowledge or partialKnowledge

   --chooseOntology CHOOSEONTOLOGY, -o CHOOSEONTOLOGY

                        Only if partialKnowledge choose:

                        molecular_function OR

                        biological_process OR
 
                        cellular_component; 
                        
                        skip this option if noKnowledge
