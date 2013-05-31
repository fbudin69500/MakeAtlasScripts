#!/usr/bin/python
import os
import sys

if len(sys.argv) != 4 :
  print "Usage: "+sys.argv[0]+" ConfigDirectory ProcessingDirectory int"
  exit()
configFilePath = sys.argv[1]
processingDirectory = sys.argv[2]
projectDir = os.path.realpath( configFilePath+"/../.." )
projectDir2 = os.path.realpath( processingDirectory+"/.." )
if projectDir != projectDir2:
  print "Error: ConfigDirectory and ProcessingDirectory do not match" 
  exit(-1)
if int(sys.argv[3]) == 0:
  print projectDir
elif int(sys.argv[3]) == 1:
  print os.path.abspath( configFilePath+"/../.." )
else:
  print os.path.abspath( processingDirectory+"/.." )
