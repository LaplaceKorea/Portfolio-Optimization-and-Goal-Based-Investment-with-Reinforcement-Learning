#!/bin/bash

## use env: burstable in conda ~
source $HOME/anaconda3/etc/profile.d/conda.sh
conda activate burstable
################################

burst --session-name burst-portfolio_optimization-$USER --gpu build
