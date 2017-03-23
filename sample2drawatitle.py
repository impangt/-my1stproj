import matplotlib.lines as mlines  
import matplotlib.pyplot as plt  
import numpy as np  
import pandas as pd

# plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
# plt.figure()
# x=pd.Series(np.exp(np.arange(20)))
# p1=x.plot(label=u'原始数据图')
# plt.ylabel('正常坐标')
# x2=pd.Series(np.log10(x)) #np.log()是以e为底的
# p2=x2.plot(secondary_y=True,style='--',color='r',)
# plt.yticks(plt.yticks()[0],['$10^%d$'%w for w in range(len(plt.yticks()[0]))])
# #x.plot(logy=True,label=u'对数数据图',legend=True,secondary_y=True,style='--',color='r') #这里不能用这个，因为它会同时改变图中的x坐标轴和y坐标轴
# plt.ylabel('指数坐标')
# blue_line = mlines.Line2D([],[],linestyle='-',color='blue',markersize=2, label=u'原始数据图')
# red_line= mlines.Line2D([],[],linestyle='--',color='red',markersize=2, label=u'对数数据图')
# plt.legend(handles=[blue_line,red_line],loc='upper left')
# plt.grid(True)
# plt.show()

#plt.figure(1) # 创建图表1
#plt.figure(2) # 创建图表2
# ax1 = plt.subplot(211) # 在图表2中创建子图1
# ax2 = plt.subplot(212) # 在图表2中创建子图2
x = np.linspace(0, 3, 100)
for i in range(3):
   # plt.figure(1)  #❶ # 选择图表1
    plt.plot(x, np.exp(i*x/3))
    # plt.sca(ax1)   #❷ # 选择图表2的子图1
    # plt.plot(x, np.sin(i*x))
    # plt.sca(ax2)  # 选择图表2的子图2
    # plt.plot(x, np.cos(i*x))
plt.show()