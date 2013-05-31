#!/usr/bin/python
import sys

if len(sys.argv) != 4 :
  print "Usage: "+sys.argv[0]+" InputConfigFilePath OutputConfigFilePath killdevilToolsPath"
  exit()
killdevilToolsPath = sys.argv[3]
configFileName = sys.argv[1]
outputFileName = sys.argv[2]
fi=open(configFileName, 'r')
fo=open(outputFileName, 'w')
for line in iter(fi.readline, b''):
  count = line.lower().find('set')
  if count >= 0:
    splitString=line.split('( ')
    if len(splitString) > 1:
      splitString2=splitString[1].split(" '@")
      if splitString > 1:
        fo.write( 'set( '+splitString2[0]+" "+killdevilToolsPath+splitString2[0]+')\n')
      else:
        fo.write(line)
    else:
      fo.write(line)
  else:
    fo.write(line)
fi.close()
fo.close()
