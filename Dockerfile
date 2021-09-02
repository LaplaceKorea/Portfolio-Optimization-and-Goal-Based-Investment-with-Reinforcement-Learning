FROM burstableai/burst_base:ubu2004
RUN apt-get install -y wget jq
RUN wget https://github.com/LaplaceKorea/Portfolio-Optimization-and-Goal-Based-Investment-with-Reinforcement-Learning/releases/download/linux_python_env/portfolio2.tar.bz2 > /dev/zero 2>&1 \
    && export LASTPWD=$PWD && mkdir /env && cd /env && pwd && echo $PWD $LASTPWD && tar jxvf $LASTPWD/portfolio2.tar.bz2 > /dev/zero 2>&1
RUN mkdir data portfolios_and_tickers src tests  
COPY data data
COPY portfolios_and_tickers portfolios_and_tickers 
COPY src src
COPY tests test
COPY job*.sh .
COPY LICENSE .
COPY README.md .
COPY requirements.txt .
COPY setup.py .
RUN ls .
RUN /env/portfolio2/bin/python setup.py install
