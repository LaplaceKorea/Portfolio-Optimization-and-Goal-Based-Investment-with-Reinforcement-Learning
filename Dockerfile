FROM burstableai/burst_base:ubu2004
RUN apt-get install -y wget
RUN wget https://github.com/LaplaceKorea/Portfolio-Optimization-and-Goal-Based-Investment-with-Reinforcement-Learning/releases/download/linux_python_env/portfolio2.tar.bz2 > /dev/zero 2>&1 \
    && export LASTPWD=$PWD && mkdir /env && cd /env && pwd && echo $PWD $LASTPWD && tar jxvf $LASTPWD/portfolio2.tar.bz2 > /dev/zero 2>&1

COPY data .
COPY portfolios_and_tickers .
COPY src .
COPY tests .
COPY job*.sh .
COPY LICENSE .
COPY README.md .
COPY requirements.txt .
COPY setup.py .
