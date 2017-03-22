import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# df=pd.DataFrame({"A":['2016-01-01','2016-01-04','2016-01-05','2016-01-06'],"B":['B5','B6','B7','B8'],"C":['C1','C2','C3','C4']})
# df.head()
# print(df.A)
#
# df=df.set_index('A')
# print(df)
# print('1-----------')
# print(df['2016-01-01':'2016-01-04'])
# print('2-----------')
# print(df.loc[:,['A','B','C']])
# print('3-----------')
# print(df.loc['2016-01-04':'2016-01-05',['B']])
# #print(df.at['2016-01-01',['A']])
#
# print(df.ix)
# print(df._is_mixed_type)
# print('4-----for语句迭代------')
# for value in enumerate(['A', 'B', 'C']):
#     print (value)
# print('5------强大的列表生成式-----')
# print([x * x for x in range(1, 11)])
# print([d for d in os.listdir('.')])#os.listdir可以列出文件和目录，一行语句搞定
#
# L = ['Hello', 'World', 'IBM', 'Apple']
# print([s.lower() for s in L])

#pd.Series([4,5,7]).plot() #用 plot 画图
#plt.show()  #必须有，否则显示不出来plot画的图

class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print('%s: %s' % (self.name, self.score)) # print  方式和 C 语言不同

peter=Student('Peter',100)
peter.print_score()

lisa = Student('Lisa', 88)
lisa.age = 8 # python 动态加载新属性，神奇！！
print('Lisa:%d' % lisa.age)