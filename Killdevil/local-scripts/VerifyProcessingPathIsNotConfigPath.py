#!/usr/bin/python
import sys

if len(sys.argv) != 3 :
  print "Usage: "+sys.argv[0]+" ProcessingPath ConfigPath"
  exit( -1 )
ProcessingPath = sys.argv[1]
ConfigPath = sys.argv[2]
foundInc1 = ConfigPath.find(ProcessingPath)
foundInc2 = ProcessingPath.find(ConfigPath)
if foundInc1 >= 0 or foundInc2 >= 0:
  print "Error: inclusion of ConfigPath in ProcessingPath or vice versa. This will lead to problems. Abort."
  exit( -1 )
else:
  exit( 0 )
