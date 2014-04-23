#!/bin/tcsh
set ANTSAtlasCMD=$1
set tempDirectory=$2
set suffix=$3
shift
shift
shift
set cases="$*"
set currentdir=`pwd`
cd $tempDirectory
if( ! $?ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS ) then
  setenv ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS 1
endif
set cmd = "${ANTSAtlasCMD} -d 3 -o ${suffix} -c 2 -j 8 -n 0 -s CC -t GR -m 100x100x50 $cases"
echo ${cmd}
${cmd}
cd $currentdir
