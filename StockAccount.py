#!/usr/bin/python

class StockAccount:
    def __init__(self, inimoney=10000.0):
        self.inimoney = inimoney
        self.moneyihave = inimoney
        self.stocks = 0 # 持有数量
        self.buyprice = 0.0
        self.highestpoint = 0.0
        self.incomes = 0.0
        self.taxes = 0.0
        self.profits = 0.0
        self.status = False  # 0:empty , 1:hold
        self.stoplossrate = 8.0  # 设置止损点, 单位：百分比
        self.stopearnrate = 26  # 设置止盈点, 单位：百分比
        self.turndownrate = 15.0  # 设置卖出点，当从买入持有阶段的历史高点下跌 N 个百分点后卖出

    def accountIni(self):
        self.moneyihave = self.inimoney
        self.stocks = 0 # 持有数量
        self.buyprice = 0.0
        self.highestpoint = 0.0
        self.incomes = 0.0
        self.taxes = 0.0
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

