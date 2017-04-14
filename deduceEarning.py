#!/usr/bin/python
import numpy as np
import pandas as pd
import StockAccount as sa

mysa = sa.StockAccount()

def getbuypolicieslist():
    buyplist = ['N days go up',
                'N days go down']
    return buyplist

def getsellpolicieslist():
    sellplist = ['stop loss at',
                 'get profits after earning ',
                 'sdown from hight']
    return sellplist

# read days data from cvs file
def readDailyData(filename):  # , starday, endday):
    df = pd.read_csv(filename)
    df = df.set_index('date')
    # df = df.ix[starday:endday, ['open', 'close', 'vol']]
    df = df.ix[:, ['open', 'close', 'vol']]
    return df

# Buy policy : buy when there are continually N(default N=3) days that the price go up ( open price < close price )
def buyPolicy_upfewdays(LOpen=[], LClose=[]):
    isbuypoint = True
    n = len(LOpen)
    for i in range(0, n):
        if LOpen[i] >= LClose[i]:
            isbuypoint = False
            break
    return isbuypoint

def buyPolicy_dowfewdays(LOpen=[], LClose=[]):
    isbuypoint = True
    n = len(LOpen)
    for i in range(0, n):
        if LOpen[i] <= LClose[i]:
            isbuypoint = False
            break
    return isbuypoint

# Sell policy 1: sell when we loss capital over N%, default N = 10
def sellPolicy_stoploss(buypoint, currentprice, lossrate=10):
    if lossrate < 0 or lossrate > 100:
        print('WARNING: input loss rate should be in the range of 0 to 100')
        return False

    if buypoint > currentprice:
        c1 = (buypoint - currentprice) / buypoint * 100.0
        if c1 >= lossrate:
            return True

    return False


# Sell policy 2: sell when we get enough profits
def sellPolicy_getprofits(buypoint, currentprice, uprate):
    if (buypoint < currentprice) and (buypoint > 0.0):
        c2 = (currentprice - buypoint) / buypoint * 100.0
        if c2 >= uprate:
            return True
    return False


# s Sell policy3: sell when the price turns down N rate from the highest point
def sellPolicy_downfromhight(highpoint, currentprice, downrate):
    if highpoint < currentprice or downrate <= 0:
        return False

    elif highpoint > 0:
        c3 = (highpoint - currentprice) / highpoint * 100.0
        if c3 >= downrate:
            return True
    return False

def runBackTrace(dataframe, buyplist, sellplist):
    predays = mysa.daysgoup
    i = predays
    while i < len(dataframe.index):
        todayopen = dataframe.iloc[i, 0]
        todayclose = dataframe.iloc[i, 1]

        if mysa.status:  # we can sell
            if mysa.highestpoint < max(todayopen, todayclose):
                mysa.highestpoint = max(todayopen, todayclose)
            issell = True
            t = i
            if len(sellplist) < 3: # if we add policy , then the number should +1
                return 0

            # sell policies frame work
            if sellPolicy_stoploss(mysa.buyprice, todayopen, mysa.stoplossrate) and sellplist[0]:  # cut loss policy
                print('sell:stoploss ', dataframe.index[i], end='')
                i = i + predays - 1  # if sell out today for cut loss, we will not buy in n(predays) days
            elif sellPolicy_getprofits(mysa.buyprice, todayopen, mysa.stopearnrate) and sellplist[1]:  # sell for getting profits
                print('>>>sell:getprofits ', dataframe.index[i], end='')
                i = i + predays * 2  # if sell out today for cut earning, we will not buy in the next few days
            elif sellPolicy_downfromhight(mysa.highestpoint, todayopen, mysa.turndownrate) and sellplist[2]:
                print('sell:downfromhight ', dataframe.index[i], end='')
            else:
                issell = False
            if issell:
                mysa.sellAction((todayopen + todayclose) / 2)
                dataframe.iloc[t, 4] = (todayopen + todayclose) / 2
                mysa.status = False
                print('--', todayopen, mysa.moneyihave)
        else:  # we can buy
            L1 = dataframe.iloc[i - predays:i, 0]
            L2 = dataframe.iloc[i - predays:i, 1]
            isbuy = True
            if len(buyplist) < 2: # if we add policy , then the number should +1
                return  0
            # buy policies frame work
            if buyPolicy_upfewdays(L1, L2) and buyplist[0]:  # buy policy
                print('buy:upfewdays', dataframe.index[i], end='')
            elif buyPolicy_dowfewdays(L1, L2) and buyplist[1]: # add other buy policy action as this.
                print('buy:downfewdays', dataframe.index[i], end='')
            else:
                isbuy = False

            if isbuy:
                mysa.buyAction(mysa.moneyihave, (todayopen + todayclose) / 2)
                # dataframe.iloc[i,3] = (todayopen+todayclose)/2
                dayindex = dataframe.index[i]
                dataframe.at[dayindex, 'buy'] = (todayopen + todayclose) / 2
                mysa.status = True
                print('buy ', dayindex, todayopen, mysa.stocks * (todayopen + todayclose) / 2 + mysa.moneyihave,
                      dataframe.loc[dayindex, 'buy'])
        i = i + 1
    incomes = dataframe.iloc[i - 1, 0] * mysa.stocks + mysa.moneyihave
    mysa.accountReset()  # 计算完毕后将账户信息恢复为初始状态，以便再次计算
    return incomes

# originData = readDailyData('sh#603588.txt')
# originData['buy'] = 0.0
# originData['sell'] = 0.0
# #print(originData.head(5))
# #dataframe = originData.iloc[10:28,]
# buypl = [1,0]
# sellpl = [1,1,1]
# incomes = runBackTrace(originData,buypl,sellpl)
# #print(originData.head(30))
# print('My profits = ', incomes)
