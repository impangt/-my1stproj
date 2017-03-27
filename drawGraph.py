"""
Draw figures according to the stock data
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import deduceEarning as de

od = de.readDailyData('sh#603588.txt', '2016/01/01', '2017/01/01')
od['buy'] = 0.0
od['sell'] = 0.0
de.runBackTrace(od)

length = len(od.index)
x = np.arange(0, length, 1)
y = od.iloc[:, 0]
# y1=pd.Series(originData)

#list the display label of x-axis
l2 = []
for i in np.arange(0, len(od.index), 1):
    l2.append(od.index[i])

# list all the buy points and sell points
l3x, l3y = [], []
l4x, l4y = [], []
for n in range(0, length):
    if od.iloc[n, 3] != 0:
        l3x.append(n)
        l3y.append(od.iloc[n, 3])
    if od.iloc[n, 4] != 0:
        l4x.append(n)
        l4y.append(od.iloc[n, 4])

#draw the main figure first
plt.xticks(np.arange(0, length, 1), l2, rotation=60)  # show partial labels
plt.plot(x, y, 'b')
plt.ylabel('day price')
plt.plot(x, y, color='k') #, linestyle='dashed', marker='o')
#draw buy points
for i in range(0, len(l3x)):
    plt.plot(l3x[i], l3y[i], 'r*')
#draw sell points
for i in range(0, len(l4x)):
    plt.plot(l4x[i], l4y[i], 'yo')

plt.grid()
plt.show()
