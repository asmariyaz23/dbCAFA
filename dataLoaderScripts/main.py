#!/usr/bin/python
import argparse
import os

def parser_code():
    
    parser = argparse.ArgumentParser(description='The purpose of this step is generate all swissprot data required to load into database for querying')

    parser.add_argument("-o", "--older", metavar="FILE",
                         help = "Older swissprot input file.")
     
    parser.add_argument("-n", "--newer", metavar="FILE",
                         help = "Newer swissprot input file.")
    
    parser.add_argument("-g", "--goterm", metavar="FILE",
                         help = "Go term file, tab separated.")
    
    ##parser.add_argument("-p", "--timepoint", metavar="FILE",
    ##                     help = "file with timepoints of the 2 swisssprot releases being used.")

    parser.add_argument("-d", "--dataoutput", 
                         help = "Provide path for redirecting your output.")

    return parser.parse_args()

def dirMaking(dataOutputDir):
    if not os.path.exists(dataOutputDir):
       os.makedirs(dataOutputDir)
       os.makedirs(dataOutputDir +'/tempdir')
    if dataOutputDir[:-1]!= "/":
       dataOutputDir = dataOutputDir + "/"
    return dataOutputDir

def makeSubFolder(dataOutputDir):
    if not os.path.exists(dataOutputDir + 'tempdir'):
       os.makedirs(dataOutputDir + 'tempdir')
       tempDir = dataOutputDir + 'tempir/'
    return tempDir



def main():
  
    parsed_args = parser_code()

    dataOutputDir     = parsed_args.dataoutput
    swissOlderFile    = parsed_args.older
    swissNewerFile    = parsed_args.newer
    gotermFile        = parsed_args.goterm
    ##timepointFile     = parsed_args.timepoint
    
    ##print dataOutputDir,swissOlderFile ,swissNewerFile,gotermFile  ,timepointFile 

    outputdir = dirMaking(dataOutputDir)
    
    tempdir = outputdir + 'tempdir/'

    ##tempdir = makeSubFolder(outputdir)  
    
    ##print outputdir,tempdir
    
    cmd1 = "./prepareProtein.py -o %s -n %s -d %s -t %s" % (swissOlderFile,swissNewerFile,outputdir,tempdir)
    os.system(cmd1)
    print cmd1 
     
    cmd2 = "./term_extract.py -g %s -d %s" % (gotermFile,outputdir)
    os.system(cmd2)
    print cmd2
    
    cmd3 = "./prepareProtein_GO.py -d %s -t %s" % (outputdir,tempdir)
    os.system(cmd3)
    print cmd3

    cmd4 = "./prepareEvidence.py -d %s -t %s" % (outputdir,tempdir)
    os.system(cmd4)
    print cmd4

if __name__ == '__main__':
    main()
