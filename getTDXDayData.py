#!/usr/bin/python
import struct as st
import os

"""
读取通达信的保存的二进制日数据文件，转换为二维数据结构，方便pandas处理
"""
def exactStock(fileName, code):
    ofile = open(fileName, 'rb')
    buf = ofile.read()
    ofile.close()
    num = len(buf)
    no = num / 32
    b = 0
    e = 32
    items = list()
    for i in range(int(no)):
        a = st.unpack('IIIIIfII', buf[b:e])
        year = int(a[0] / 10000)
        m = int((a[0] % 10000) / 100)
        month = str(m)
        if m < 10:
            month = "0" + month
        d = (a[0] % 10000) % 100
        day = str(d)
        if d < 10:
            day = "0" + str(d)
        dd = str(year) + "-" + month + "-" + day
        openPrice = a[1] / 100.0
        high = a[2] / 100.0
        low = a[3] / 100.0
        close = a[4] / 100.0
        amount = a[5] / 10.0
        vol = a[6]
        unused = a[7]
        if i == 0:
            preClose = close
        ratio = round((close - preClose) / preClose * 100, 2)
        preClose = close
        item = [code, dd, str(openPrice), str(high), str(low), str(close), str(ratio), str(amount), str(vol)]
        items.append(item)
        b = b + 32
        e = e + 32
    return items

"""
读取通达信的保存的二进制日数据文件，转换为csv格式，并生成新的文件
"""
def day2csv_data(dirname,fname,targetdir):
    ofile=open(dirname+os.sep+fname,'rb')
    buf=ofile.read()
    ofile.close()
    fname2=fname[:-4] #将原文件最后“.day”4个字符去除

    ifile=open(targetdir+os.sep+fname2+'.csv','w')
    num=len(buf)
    no=int(num/32)
    b=0
    e=32
    line=''
    linename=str('date')+','+str('open')+','+str('high')+','+str('low')+','+str('close')+','+str('amount')+','+str('vol')+','+str('str07')+','+'\n'
    ifile.write(linename)
    for i in range(1,no):
        a=st.unpack('IIIIIfII', buf[b:e])
        line=str(a[0])+','+str(a[1]/100.0)+','+str(a[2]/100.0)+','+str(a[3]/100.0)+','+str(a[4]/100.0)+','+str(a[5]/10.0)+','+str(a[6])+','+str(a[7])+','+'\n'
        ifile.write(line)
        b=b+32
        e=e+32
    ifile.close()

#exactStock('sh000001.day', "000001")
pathdir='E:\\github\\Pandas'
targetDir='E:\\github\\Pandas'
listfile=os.listdir(pathdir)

day2csv_data(pathdir,'sh600000.day',targetDir)
'''
#批量转换文件
for f in listfile:
      day2csv_data(pathdir,f,targetDir)
'''