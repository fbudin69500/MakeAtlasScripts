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
set cmd = "${ANTSAtlasCMD} -d 3 -o ${suffix} -c 2 -j 8 -n 0 -s CC -t GR -m 100x100x50 $cases"
echo ${cmd}
${cmd}
cd $currentdir
