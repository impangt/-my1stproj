#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import sys

config = configparser.ConfigParser()
config.read_file(open('config\\config.ini'))

try:
    sec = config.sections()
    print('section:',sec)

    lop = []
    for i in range(len(sec)):
        lop.append(config.options(sec[i]))
        print('options ',i,' ',sec[i],'>>',lop[i])

    items = config.items(sec[0])#,lop[0][0])
    print(items)

    # inimoney = config.get("StockAccount","inimoney")
    # s1, s2 = inimoney.split('#')
    # print (s1, s2)
except Exception:
    info = sys.exc_info()
    print(info[0], ":", info[1])

# config.set("ZIP", "MD5", "1234")
# config.write(open('config\\update.ini', "r+"))
#
# fd = open(('config\\update.ini'), 'w')
# config.set("ZIP", "MD5", "2234")
# config.write(fd)  # 在内存中修改的内容写回文件中，相当于保存
# fd.close()


