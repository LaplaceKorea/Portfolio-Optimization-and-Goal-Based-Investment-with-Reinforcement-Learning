#!/bin/bash

SCRIPTPATH=`dirname "$(readlink -f "$0")"`
echo "scriptpath = $SCRIPTPATH"

export PATH=/env/portfolio2/bin:$SCRIPTPATH/env/portfolio2/bin:$PATH

which python
python setup.py install
