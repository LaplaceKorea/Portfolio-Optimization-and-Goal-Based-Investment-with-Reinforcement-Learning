#!/bin/bash

mkdir env
pushd env
wget https://github.com/LaplaceKorea/Portfolio-Optimization-and-Goal-Based-Investment-with-Reinforcement-Learning/releases/download/linux_python_env/portfolio2.tar.bz2
tar jxvf portfolio2.tar.bz2
popd

./build.sh
