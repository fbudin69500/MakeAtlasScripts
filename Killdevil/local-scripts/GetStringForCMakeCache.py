#!/usr/bin/python
import sys

if len(sys.argv) != 3 :
  print "Usage: "+sys.argv[0]+" ConfigPath StringToFind"
  exit()
configFilePath = sys.argv[1]
stringToFind = sys.argv[2]
fi=open(configFilePath+'/CMakeCache.txt', 'r')
for line in iter(fi.readline, b''):
  count = line.find(stringToFind)
  if count >= 0:
    splitString=line.split('=')
    print splitString[1].rstrip()
fi.close()
