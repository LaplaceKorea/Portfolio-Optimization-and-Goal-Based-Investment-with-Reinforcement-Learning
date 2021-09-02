#!/bin/bash

#source $HOME/anaconda3/etc/profile.d/conda.sh
#conda activate portfolio

SCRIPTPATH=`dirname "$(readlink -f "$0")"`
echo "scriptpath = $SCRIPTPATH"

# trick!
cd $SCRIPTPATH 
pwd
ls

export PATH=/env/portfolio2/bin:$SCRIPTPATH/env/portfolio2/bin:$PATH
which python

portfolio=$1 
dest=$2
extra=$3

##### RUNNER.sh ./runit.sh ip.json x.json query.json
echo portfolio $1 dest $2 extra $3

from=`jq -r .From $extra`
to=`jq -r .To $extra`

which python

## python setup.py install
TRACING=YES python src/main.py \
--mode test \
--n_episodes 100 \
--gpu_devices 0 \
--assets_to_trade portfolios_and_tickers/tickers_S\&P500_dummy.txt \
--initial_portfolio $portfolio \
--plot \
--use_corr_matrix \
--checkpoint_directory model  > $dest.log 
# 2>&1

# python src/main.py \
# --initial_portfolio $portfolio \
# --buy_cost 0.0001 \
# --sell_cost 0.0001 \
# --bank_rate 0.5 \
# --sac_temperature 1.0 \
# --limit_n_stocks 100 \
# --lr_Q 0.0003 \
# --lr_pi 0.0003 \
# --lr_alpha 0.0003 \
# --gamma 0.99 \
# --tau 0.005 \
# --batch_size 256 \
# --layer_size 256 \
# --n_episodes 10 \
# --seed 42 \
# --delay 2 \
# --mode test \
# --memory_size 100 \
# --initial_date $from \
# --final_date $to \
# --gpu_devices 0 \
# --grad_clip 2.0 \
# --buy_rule most_first \
# --agent_type automatic_temperature \
# --window 20 \
# --use_corr_matrix > $dest.log 2>&1

cat $dest.log
grep portfolio_value $dest.log | uniq > $dest.values
egrep "buy|sell" $dest.log > $dest.trades


exit 0

#############################################################################
# SCRIPTPATH=`dirname "$(readlink -f "$0")"`
# echo "scriptpath = $SCRIPTPATH"

# # trick!
# cd $SCRIPTPATH 
# pwd
# ls

# export PATH=/env/portfolio2/bin:$SCRIPTPATH/env/portfolio2/bin:$PATH
# which python

# #srun --unbuffered 
# python src/main.py \
# --mode train \
# --n_episodes 100 \
# --gpu_devices 0 \
# --assets_to_trade portfolios_and_tickers/tickers_S\&P500_dummy.txt \
# --initial_portfolio portfolios_and_tickers/initial_portfolio_subset.json \
# --plot \
# --use_corr_matrix \
# #--checkpoint_directory saved_outputs/2021.07.26.21.49.56 \
