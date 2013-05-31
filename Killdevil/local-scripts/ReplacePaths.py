#!/usr/bin/python
import sys

if len(sys.argv) != 5 :
  print "Usage: "+sys.argv[0]+" inputFile outputFile oldString newString"
  exit()
inputFile = sys.argv[1]
outputFile = sys.argv[2]
oldString = sys.argv[3]
newString = sys.argv[4]
fi=open(inputFile, 'r')
fo=open(outputFile, 'w')
for line in iter(fi.readline, b''):
  newline = line.replace( oldString , newString )
  fo.write( newline )
fi.close()
fo.close()
