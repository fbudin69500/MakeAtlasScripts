#!/usr/bin/python
import os
import sys

if len(sys.argv) != 3 :
  print "Usage: "+sys.argv[0]+" MakeAtlasDirectory ProjectDirectory"
  exit()
MakeAtlasPath = sys.argv[1]
ProjectDirectory = sys.argv[2]
projectDir = os.path.realpath( ProjectDirectory )
MakeAtlasDir = os.path.realpath( MakeAtlasPath )
print "ProjectDir: "+projectDir
print "MakeAtlasDir: "+MakeAtlasDir
if MakeAtlasDir.find(projectDir) < 0:
  print "Error: MakeAtlas directory is not included in ProjectDirectory" 
  exit(-1)

