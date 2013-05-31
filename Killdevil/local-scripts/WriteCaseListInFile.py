#!/usr/bin/python
import sys

if len(sys.argv) != 3 :
  print "Usage: "+sys.argv[0]+" inputbmsfile caseListFile"
  exit()
inputFile = sys.argv[1]
outputFile = sys.argv[2]
fi=open(inputFile,'r')
fo=open(outputFile,'w')
for line in iter(fi.readline, b''):
  count = line.find("CASES")
  if count >= 0:
    splitString=line.split('CASES')
    splitString2=splitString[1].split(' ')
    for case in splitString2:
      if case.rstrip().lstrip() != ')' and case.rstrip().lstrip():
        fo.write(case.rstrip().lstrip()+'\n')
fi.close()
fo.close()
