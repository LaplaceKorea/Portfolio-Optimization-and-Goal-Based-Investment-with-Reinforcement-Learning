# use env: amazon-braket
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Tuple, Callable, Union
# from UserTokenSerde import *
import numpy as np
from dataclasses_serialization.json import JSONSerializer
import orjson
import json
import os
import tempfile

"""
exampleConfig = {
    "__class__": "RLPortfolio",
    "query": {
        "EnvId": "default",
        "From":"2021-01-01",
        "To": "2021-01-21",
        "InitialPortfolio": {
            "BankAccount": 100000, 
            "MMM":1,
            "AA":1,
            "AXP":1,
            "BA":1,
            "BAC":1,
            "C":1,
            "CAT":1,
            "CVX":1,
            "DD":1,
            "DIS":1,
            "GE":1,
            "GM":1,
            "HD":1,
            "HPQ":1,
            "IBM":1,
            "JNJ":1,
            "JPM":1,
            "KO":1,
            "MCD":1,
            "MRK":1,
            "PFE":1,
            "PG":1,
            "T":1,
            "UTX":1,
            "VZ":1,
            "WMT":1,
            "XOM":1
        }
    }
}
"""

stocks_symbol: List[str] = []
with open('tickers.txt') as f:
    stocks_symbols = f.read().splitlines()

@dataclass
class Trade:
    Step: int
    Buy: bool
    Ticker: str
    Qty: float
    Price: float

@dataclass
class SimulationStep:
    Step: int
    Pnl: float
    Portfolio: Dict[str,float]
    Trades: List[Trade]

def readTrades(path:str) -> List[List[SimulationStep]]:
    last_step = 0
    rv : List[List[SimulationStep]] = []
    currentEpisode : List[SimulationStep] = []
    currentSS = SimulationStep(0, 0.0, {}, [])

    with open(path, "r") as f:
        for l in f:
            #print(l)
            try:
                elts = l.split(" ")
                step = int(elts[0])
                buy = elts[1] == "buy"
                idx = int(elts[2])
                qty = -float(elts[5]) if not buy else float(elts[5])
                price = float(elts[7])
                trade = Trade(step, buy, stocks_symbols[idx], qty, price)
                #print(trade)
                if step < last_step:
                    currentEpisode.append(currentSS)
                    rv.append(currentEpisode)                
                    currentEpisode = []

                    for i in range(step - last_step - 1):
                        currentEpisode.append(SimulationStep(last_step + 1+i, 0.0, {}, []))

                    last_step = step
                    currentSS = SimulationStep(step, 0.0, {}, [trade])
                else:
                    if last_step == step:
                        currentSS.Trades.append(trade)
                    else:
                        currentEpisode.append(currentSS)
                        for i in range(step - last_step - 1):
                            currentEpisode.append(SimulationStep(last_step + 1+i, 0.0, {}, []))
                        currentSS = SimulationStep(step, 0.0, {}, [trade])
                        last_step = step
            except Exception as e:
                print("skip", e)
    rv.append(currentEpisode)
    return rv

def readValues(path:str, simu: List[List[SimulationStep]]) -> List[List[SimulationStep]]:
    last_step = 0
    episode = 0 
    rv : List[List[SimulationStep]] = [simu[0]]
    with open(path, "r") as f:
        for l in f:
            #print(l)
            try:
                elts = l.split(" ")
                step = int(elts[0])
                pnl = float(elts[2])
                if step < last_step:                
                    episode = episode + 1
                    rv.append(simu[episode])
                    last_step = step
                else:
                    last_step = step
                while len(rv[-1]) <= step:
                    rv[-1].append(SimulationStep(len(rv[-1]), 0.0, {}, []))
                rv[-1][step].Pnl = pnl
            except Exception as e:
                print("skip", e)
    return rv

#trades = readTrades("x.json.trades")
#print(trades)
#values = readValues("x.json.values", trades)
#print(values)
#print(trades[0][0], trades[0][1], trades[0][203])
#print(values[0][0], values[0][1], values[0][203])

@dataclass
class RLQuery:
    EndId: str # "default"
    From: datetime
    To: datetime
    InitialPortfolio: Dict[str,float] # special key: BankAccount

def makeQuery(q: RLQuery):
    return orjson.dumps(q, option=orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY).decode("utf-8")

def makeIP(q: RLQuery):
    rv = {}
    for k in q.InitialPortfolio:
        if k=="BankAccount":
            rv["Bank_account"] = q.InitialPortfolio[k]
        else:
            rv[k] = q.InitialPortfolio[k]
    return rv

#print(makeQuery(exampleQuery))
#print(makeIP(exampleQuery))

def completePfInfo(ip: Dict[str,float], simu: List[List[SimulationStep]]):
    def cloneIp(ip: Dict[str, float]) -> Dict[str,float]:
        rv = {}
        for k in ip:
            rv[k] = ip[k]
        return rv
    for sc in range(len(simu)):
        pf = cloneIp(ip)
        del pf["BankAccount"]
        for st in range(len(simu[sc])):
            for t in simu[sc][st].Trades:
                if t.Buy:
                    pf[t.Ticker] = pf[t.Ticker] + t.Qty
                else:
                    pf[t.Ticker] = pf[t.Ticker] - t.Qty
            simu[sc][st].Portfolio = cloneIp(pf)

#completePfInfo(exampleQuery.InitialPortfolio, values)
# print(values)
#print(values[0][0], values[0][1], values[0][203])

def runRLsimu(prefix: str, rlquery: RLQuery) -> List[List[SimulationStep]]:
    ip = makeIP(rlquery)
    query = makeQuery(rlquery)
    ipPath = prefix + "IP.json"
    xPath = prefix + "X.json"
    queryPath = prefix + "Q.json"

    with open(ipPath, "w") as f:
        f.write(orjson.dumps(ip, option=orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY).decode("utf-8"))
    # ~ with open(xPath, "w") as f:
    with open(queryPath, "w") as f:
        f.write(query)

    command = "./runit.sh " + ipPath + " " + xPath + " " + queryPath
    print(command)
    os.system(command)
    trades = readTrades(xPath + ".trades")
    values = readValues(xPath + ".values", trades)
    completePfInfo(exampleQuery.InitialPortfolio, values)
    return values

def cleanupSimu(prefix: str):
    ipPath = prefix + "IP.json"
    xPath = prefix + "X.json"
    queryPath = prefix + "Q.json"
    tradesPath = xPath + ".trades"
    valuesPath = xPath + ".values"
    os.unlink(ipPath)
    os.unlink(xPath + ".log")
    os.unlink(queryPath)
    os.unlink(tradesPath)
    os.unlink(valuesPath)

# ./runit.sh ip.json x.json query2.json
#res = runRLsimu("xxx", exampleQuery)
#print(res[0][0], res[0][1], res[0][203])
#cleanupSimu("xxx")

@dataclass
class RLResult:
    Steps: List[List[SimulationStep]]

def runRLsimuFull(rlquery: RLQuery) -> RLResult:
    try:
        tempfile.tempdir = "."
        n = tempfile.NamedTemporaryFile(prefix="rls_")
        p = os.path.basename(n.name)
        res: List[List[SimulationStep]] = []
        try:
            res = runRLsimu(p, rlquery)
        except:
            pass
        try:
            cleanupSimu(p)
        except:
            return RLResult([])
        return RLResult(res)
    except:
        return RLResult([])

exampleQuery = RLQuery("default", datetime(2021,1,1), datetime(2021,1,21), {
            "BankAccount": 100000, 
            "MMM":1,
            "AA":1,
            "AXP":1,
            "BA":1,
            "BAC":1,
            "C":1,
            "CAT":1,
            "CVX":1,
            "DD":1,
            "DIS":1,
            "GE":1,
            "GM":1,
            "HD":1,
            "HPQ":1,
            "IBM":1,
            "JNJ":1,
            "JPM":1,
            "KO":1,
            "MCD":1,
            "MRK":1,
            "PFE":1,
            "PG":1,
            "T":1,
            "UTX":1,
            "VZ":1,
            "WMT":1,
            "XOM":1
})

res = runRLsimuFull(exampleQuery)
print(res.Steps[0][0], res.Steps[0][1], res.Steps[0][203])
print("number of scenarios", len(res.Steps))
