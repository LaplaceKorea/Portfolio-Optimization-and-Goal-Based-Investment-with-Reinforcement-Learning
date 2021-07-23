#!/bin/bash

#SBATCH --job-name="SAC_agent"
#SBATCH --output="%j.out" # job standard output file (%j replaced by job id)
#SBATCH --error="%j.err" # job standard error file (%j replaced by job id)

#SBATCH --time=48:00:00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=1   # 8 processor core(s) per node 
#SBATCH --mem=5G   # maximum memory per node
#SBATCH --gres=gpu:4
#SBATCH --partition=gpu    # gpu node(s)

#========================================================

# Simple command line: In case you trust the default values I gave to the various params/hyperparams, cf. main.py

#srun --unbuffered 
python src/main.py \
--mode train \
--initial_portfolio portfolios_and_tickers/initial_portfolio_subset.json \
--n_episodes 2 \
--agent_type distributional \
--assets_to_trade portfolios_and_tickers/tickers_S\&P500_subset.txt \
#--use_corr_eigenvalues \
#--checkpoint_directory saved_outputs/2021.07.22.21.15.17 \



# Detailed command line: In case you want to tune each param/hyperparam manually

#srun --unbuffered 
#python src/main.py \
#--assets_to_trade ./portfolios_and_tickers/tickers_S&P500_subset.txt \
#--initial_cash 10000000 \
#--buy_cost 0.0001 \
#--sell_cost 0.0001 \
#--bank_rate 0.5 \
#--sac_temperature 1.0 \
#--limit_n_stocks 100 \
#--lr_Q 0.0003 \
#--lr_pi 0.0003 \
#--lr_alpha 0.0003 \
#--gamma 0.99 \
#--tau 0.005 \
#--batch_size 256 \
#--layer_size 256 \
#--n_episodes 1000 \
#--seed 42 \
#--delay 2 \
#--mode train \
#--memory_size 1000000 \
#--initial_date 2015-01-01 \
#--final_date 2020-12-31 \
#--gpu_devices 0 1 2 3 \
#--grad_clip 2.0 \
#--buy_rule most_first \
#--agent_type distributional \
#--window 40 \
#--use_corr_matrix \
