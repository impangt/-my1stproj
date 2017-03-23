"""
Draw figures according to the stock data
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import deduceEarning as de

od = de.readDailyData('sh#603588.txt', '2016/01/01', '2016/06/01')
od['buy'] = 22.0
od['sell'] = 22.0
de.runBackTrace(od)

length = len(od.index)
x = np.arange(0, length, 1)
y = od.iloc[:, 0]
#y1=pd.Series(originData)

l2 = []
for i in np.arange(0, len(od.index), 10):
    l2.append(od.index[i])
# print(l2)
plt.xticks(np.arange(0, 244, 10), l2, rotation=60)  # show partial labels
plt.plot(x, y, 'b')
plt.ylabel('day price')
plt.plot(x, y)

yy = od.iloc[:, 3]
plt.plot(x, yy, 'r*')

yyy=od.iloc[:,4]
plt.plot(x,yyy,'y*')
plt.grid()
plt.show()
