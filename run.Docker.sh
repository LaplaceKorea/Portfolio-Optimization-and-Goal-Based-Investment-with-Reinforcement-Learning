#!/bin/bash

SCRIPTPATH=`dirname "$(readlink -f "$0")"`
echo "scriptpath = $SCRIPTPATH"

user=`ls -l $1 | cut -d " " -f 3`
group=`ls -l $1 | cut -d " " -f 4`

echo $user $group
echo trying to execute $1 $2 $3 $4 $5 $6 $7 $8 $9 
echo $MYSUDO time docker run --rm -v $PWD:/prog -u `id -u $USER`:`id -g $USER` --gpus 1 --name portfolio_optimization portfolio_optimization /prog/$1 $2 $3 $4 $5 $6 $7 $8 $9 
$MYSUDO time docker run --rm -v $PWD:/prog -u `id -u $USER`:`id -g $USER` --gpus 1 --name portfolio_optimization portfolio_optimization /prog/$1 $2 $3 $4 $5 $6 $7 $8 $9 
#$MYSUDO chown $user:$group $2
#$MYSUDO chmod a+rw $2  

