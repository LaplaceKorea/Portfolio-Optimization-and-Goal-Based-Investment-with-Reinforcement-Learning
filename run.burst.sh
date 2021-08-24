#!/bin/bash

## use env: burstable in conda ~
source $HOME/anaconda3/etc/profile.d/conda.sh
conda activate burstable
################################

time burst run --session-name burst-portfolio_optimization-$USER $1 $2 $3 $4 $5 $6 $7 $8 $9 
