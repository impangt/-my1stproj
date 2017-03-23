"""
Draw figures according to the stock data
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import deduceEarning as de

originData = de.readDailyData('sh#603588.txt', '2016-01-01', '2017-01-01')

length = len(originData.index)
x = np.arange(0, length, 1)
y = originData.iloc[:, 1]
#y1=pd.Series(originData)

l2 = []
for i in np.arange(0, len(originData.index), 10):
    l2.append(originData.index[i])
# print(l2)
plt.xticks(np.arange(0, 244, 10), l2, rotation=90)  # show partial labels
plt.plot(x, y)
plt.ylabel('day price')
plt.plot(x, y)

yy = originData.iloc[:, 0]
plt.plot(x, yy)

plt.show()
