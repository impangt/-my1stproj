#!/usr/bin/python

# import struct as st
import numpy as np
import pandas as pd
import StockAccount as sa

mysa = sa.StockAccount()


# read days data from cvs file
def readDailyData(filename, starday, endday):
    df = pd.read_csv(filename)
    df = df.set_index('date')
    df = df.ix[starday:endday, ['open', 'close', 'vol']]
    return df


# Buy policy : buy when there are continually N(default N=3) days that the price go up ( open price < close price )
def buyPolicy_upfewdays(LOpen=[], LClose=[]):
    isbuypoint = True
    n = len(LOpen)
    for i in range(0, n):
        if LOpen[i] > LClose[i]:
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


def runBackTrace(dataframe):
    predays = 3
    i = predays
    while i < len(dataframe.index):
        todayopen = dataframe.iloc[i, 0]
        todayclose = dataframe.iloc[i, 1]

        if mysa.status:  # we can sell
            if mysa.highestpoint < max(todayopen, todayclose):
                mysa.highestpoint = max(todayopen, todayclose)
            issell = True
            t = i
            if sellPolicy_stoploss(mysa.buypoint, todayopen, mysa.stoplossrate):  # cut loss policy
                print('Failed:sell', dataframe.index[i], end='')
                i = i + predays - 1  # if sell out today for cut loss, we will not buy in n(predays) days
            elif sellPolicy_getprofits(mysa.buypoint, todayopen, mysa.stopearnrate):  # sell for getting profits
                print('>>>SUCCESS:sell', dataframe.index[i], end='')
                i = i + predays * 5  # if sell out today for cut earning, we will not buy in the next day
            elif sellPolicy_downfromhight(mysa.highestpoint, todayopen, mysa.turndownrate):
                print('FORCE:sell ', dataframe.index[i], end='')
            else:
                issell = False
            if issell:
                mysa.sellAction((todayopen+todayclose)/2)
                dataframe.iloc[t,4] = (todayopen+todayclose)/2
                mysa.status = False
                print('--', todayopen, mysa.moneyihave)
        else:  # we can buy
            L1 = dataframe.iloc[i - predays:i, 0]
            L2 = dataframe.iloc[i - predays:i, 1]
            if buyPolicy_upfewdays(L1, L2):  # buy policy
                mysa.buyAction(mysa.moneyihave, (todayopen+todayclose)/2)
                # dataframe.iloc[i,3] = (todayopen+todayclose)/2
                dayindex = dataframe.index[i]
                dataframe.at[dayindex, 'buy'] = (todayopen + todayclose) / 2
                mysa.status = True
                print('buy ', dayindex, todayopen, mysa.stocks * (todayopen+todayclose)/2 + mysa.moneyihave, dataframe.loc[dayindex, 'buy'])
        i = i + 1
    incomes = dataframe.iloc[i - 1, 0] * mysa.stocks + mysa.moneyihave
    mysa.accountIni() #计算完毕后将账户恢复为初始状态，以便再次计算
    return incomes

# originData = readDailyData('sh#603588.txt', '2016/01/01', '2017/03/09')
# originData['buy'] = 0.0
# originData['sell'] = 0.0
# #dataframe = originData.iloc[10:28,]
# incomes = runBackTrace(originData)
#
# # print(originData.iloc[:,0]) # first column
# # print(originData.index[0:3])
# print(originData.head(30))
# print('My profits = ', incomes)
