#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser

config = configparser.ConfigParser()
config.read_file(open('config\\update.ini'))
a = config.get("TEST","pang")
print (a)

# config.set("ZIP", "MD5", "1234")
# config.write(open('config\\update.ini', "r+"))

fd = open(('config\\update.ini'), 'w')
config.set("ZIP", "MD5", "2234")
config.write(fd)  # 在内存中修改的内容写回文件中，相当于保存
fd.close()


