#!/usr/bin/python

'''this is a tool for input data pre format'''

import os

filelist = []

# 遍历指定目录，显示目录下的所有文件名
def getEachFileName(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        #child.decode('gbk')  # .decode('gbk')是解决中文显示乱码问题
        filelist.append(child)


def formateFile(rfname, wfname):
    f1 = open(rfname, 'r')  # r 代表read
    f2 = open(wfname, 'w')
    linenum = 0
    for eachLine in f1:
        linenum+=1
    print("line num = ", linenum)

    i=0
    f1.seek(0)
    for eachLine in f1:
        # print("读取到得内容如下：", eachLine)
        if i == 0 or i == 1:
            i+=1
            continue
        if i == 2:
            i+=1
            tx = "date,open,high,low,close,vol,turn\n"
            f2.write(tx)
        if i == linenum: break
        f2.write(eachLine)
        i+=1

    f2.close()
    f1.close()
    print("read ",i,' lines')


if __name__ == '__main__':
    readfilePath = "D:\\stocks\\data\\"
    writefilePath = "D:\\github\\my1stproj\\data\\"
    getEachFileName(readfilePath)

    for fname in filelist:
        len1 = len(readfilePath)
        wname = writefilePath + fname[len1:]
        formateFile(fname, wname)
        print(wname)