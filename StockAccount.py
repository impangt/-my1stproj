#!/usr/bin/python
import sys
import configparser

class StockAccount:
    def __init__(self):
        self.stocks = 0 # 持有数量
        self.buyprice = 0.0 # 一次买入操作的买入价
        self.highestpoint = 0.0 # 一次买入操作中股价的最高点
        self.incomes = 0.0 # 一段时期内各个操作的总收入
        self.profits = 0.0 # 一次操作的盈利
        self.status = False  # 判断是否持有股票（买入期间） 0:empty , 1:hold
        fn = 'config\\config.ini'
        self.getinidata(fn)

    def accountReset(self):
        self.moneyihave = self.inimoney
        self.stocks = 0 # 持有数量
        self.buyprice = 0.0
        self.highestpoint = 0.0
        self.incomes = 0.0
        self.profits = 0.0
        self.status = False  # 0:empty , 1:hold

    # buy stocks
    def buyAction(self, money, buyprice):
        s = int(money / (buyprice * 100)) * 100  # 按照stocks的买入规则，每次买入100股的整数倍
        if s > 100:
            self.stocks = s
            self.buyprice = buyprice
            self.moneyihave = money - self.stocks * buyprice
            self.highestpoint = buyprice
            self.status = True
            #print('Buy buyprice is :', self.buyprice,' and stocks I have = ', self.stocks)
        return self.status

    # sell stocks, and count the profits
    def sellAction(self, sellprice):
        if self.stocks > 0:
            self.highestpoint = 0
            self.moneyihave = sellprice * self.stocks + self.moneyihave
            self.buyprice = 0
            self.status = False
            # print('sell price is :', sellprice,' and money I have = ', self.moneyihave)
        return self.status

    # get ini file data
    def getinidata(self,filename ):
        config = configparser.ConfigParser()
        try:
            config.read_file(open(filename))
        except Exception:
            info = sys.exc_info()
            print(info[0], ":", info[1])

        # parameters we get from ini file
        v = config.get("StockAccount", "inimoney")
        s1, s2 = v.split('#')
        self.inimoney = int(s1)
        self.moneyihave = self.inimoney

        v = config.get("StockAccount", "tax")
        s1, s2 = v.split('#')
        self.taxes = float(s1)

        v =  config.get("Sell", "stop_lossing_rate")
        s1, s2 = v.split('#')
        self.stoplossrate = float(s1)

        v =  config.get("Sell", "stop_earning_rate")
        s1, s2 = v.split('#')
        self.stopearnrate = float(s1)

        v =  config.get("Sell", "turn_down_rate")
        s1, s2 = v.split('#')
        self.turndownrate = float(s1)

        v =  config.get("Buy", "days_go_up")
        s1, s2 = v.split('#')
        self.daysgoup = int(s1)
