#!/bin/bash
# to run : ./run.local.sh ./job.sh

SCRIPTPATH=`dirname "$(readlink -f "$0")"`
echo "scriptpath = $SCRIPTPATH"

export PATH=/env/portfolio2/bin:$SCRIPTPATH/env/portfolio2/bin:$PATH

which python
$1 $2 $3 $4 $5 $6 $7 $8 $9 
