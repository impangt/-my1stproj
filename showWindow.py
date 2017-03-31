# encoding: utf-8
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import deduceEarning as de
import pandas as pd
import numpy as np
import random

class ShowWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ShowWindow, self).__init__()
        self.setWindowFlags(Qt.Widget)# set the style of the dialog ( with max and min button )

        # figure area
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111)
        ###self.axes.hold(False) # We want the axes cleared every time plot() is called
        self.canvas = FigureCanvas(self.figure)
        self.setSizeGripEnabled(True) # 对话框右下角的拖拽区域
        plt.clf()

        # self.toolbar = NavigationToolbar(self.canvas, self)
        # self.toolbar.hide()

        # Just some button
        self.openButton = QtWidgets.QPushButton("Open")
        self.openButton.clicked.connect(self.msg)

        self.button1 = QtWidgets.QPushButton('Plot')
        self.button1.clicked.connect(self.plot)
        self.button1.setDisabled(True)

        self.button2 = QtWidgets.QPushButton('Zoom +')
        self.button2.clicked.connect(self.zoomin)
        self.button2.setDisabled(True)

        self.button3 = QtWidgets.QPushButton('Zoom -')
        self.button3.clicked.connect(self.zoomout)
        self.button3.setDisabled(True)

        self.button4 = QtWidgets.QPushButton('Home')
        self.button4.clicked.connect(self.home)
        self.button4.setDisabled(True)

        self.buttonIndicator = QtWidgets.QPushButton('Indicator')
        self.buttonIndicator.clicked.connect(self.indicator)
        self.buttonIndicator.setDisabled(True)

        self.buttonPre = QtWidgets.QPushButton('<<')
        self.buttonPre.clicked.connect(self.gotopre)
        self.buttonPre.setDisabled(True)

        self.buttonNext = QtWidgets.QPushButton('>>')
        self.buttonNext.clicked.connect(self.gotonext)
        self.buttonNext.setDisabled(True)

        self.buttonBegin = QtWidgets.QPushButton('|<')
        self.buttonBegin.clicked.connect(self.gotobegin)
        self.buttonBegin.setDisabled(True)

        self.buttonEnd = QtWidgets.QPushButton('>|')
        self.buttonEnd.clicked.connect(self.gotoend)
        self.buttonEnd.setDisabled(True)

        slider_label = QLabel('【Bar width (%)】:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(20)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.onslider)  # int

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        btnlayout = QtWidgets.QHBoxLayout()
        btnlayout.addWidget(self.openButton)
        btnlayout.addWidget(self.button1)
        btnlayout.addWidget(self.button2)
        btnlayout.addWidget(self.button3)
        btnlayout.addWidget(self.button4)
     #   btnlayout.addWidget(self.buttonPre)
     #   btnlayout.addWidget(self.buttonNext)
     #   btnlayout.addWidget(self.buttonBegin)
     #   btnlayout.addWidget(self.buttonEnd)
        btnlayout.addWidget(self.buttonIndicator)
        btnlayout.addWidget(self.slider)

        qw = QtWidgets.QWidget(self)
        qw.setLayout(btnlayout)
        layout.addWidget(qw)

        self.setLayout(layout)

        # other parameters
        self.targetDir = ''
        self.dataframe = pd.DataFrame()
        self.view_startx = 0 # the start x index of the current view window
        self.zoomidx = 1
        self.showindicator = True



    def home(self):
        plt.clf()
        self.zoomidx = 1
        self.view_startx = 0
        self.drawFigue(self.zoomidx,self.view_startx)
        self.button2.setDisabled(False)
        self.button3.setDisabled(True)

    def zoomin(self):
        b=False
        z = self.zoomidx + 1
        if self.zoomidx < 10 and self.zoomidx>0:
            b = self.drawFigue(z,self.view_startx)
            if b:
                self.zoomidx = self.zoomidx + 1
                self.button3.setDisabled(False)
        if self.zoomidx == 10 or b == False:
            self.button2.setDisabled(True)

        print('zoomin = ',self.zoomidx, b)

    def zoomout(self):
        b=False
        z = self.zoomidx - 1
        if self.zoomidx <= 10 and self.zoomidx>1:
            b = self.drawFigue(z, self.getStartFromBack())
            if b:
                self.zoomidx = self.zoomidx-1
                self.button2.setDisabled(False)
        if self.zoomidx == 1 or b == False:
            self.button3.setDisabled(True)
        print('zoomout = ',self.zoomidx, b, 'view_startx', self.view_startx)

    def plot(self):
        de.runBackTrace(self.dataframe)
        self.drawFigue(1)
        self.button1.setDisabled(True)
        self.button2.setDisabled(False)
        self.button4.setDisabled(False)
        self.buttonIndicator.setDisabled(False)
        self.buttonEnd.setDisabled(False)

    def msg(self):
        self.targetDir, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          'E:\\github\\my1stproj',
                                                          "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        if self.targetDir != '' :
            self.dataframe = de.readDailyData(self.targetDir, '2016/01/01', '2017/04/11')
            self.dataframe['buy'] = 0.0
            self.dataframe['sell'] = 0.0
            self.button1.setDisabled(False)

    # the scope of zoom rate is [1, 10], 1 = no zoom , 2 = zoom to 90% , 3 = to 80%, ... 10 = 10%
    def drawFigue(self, zoomrate, start=0):
        plt.clf()

        zm = 11-zoomrate
        length1 = len(self.dataframe.index)
        length2 = int(length1*zm/10)
        # to tell the length of data list
        if length1 - start < length2:
            length2 = length1 - start

        print('lengh1 = ',length1,' length2 = ',length2, 'start = ',start)
        viewx = np.arange(0, length2, 1)
        y = self.dataframe.iloc[start:start+length2, 0]

        # list the display label of x-axis
        l2 = []
        step = int(length2/5) # 如果选择的日期数量少于step，则会出错
        if step == 0:
            return False

        for i in np.arange(0, length2, step):
            l2.append(self.dataframe.index[i+start])

        plt.xlim(0,length2)
        plt.xticks(np.arange(0, length2, step), l2)#, rotation=30)
        plt.ylabel('day price')
        plt.plot(viewx, y, color='c')  # , linestyle='dashed', marker='o')

        plt.grid()
        self.canvas.draw() # 在窗体内绘图，如果直接使用 plot.show()则会另外开启绘图窗口
        return True

    def indicator(self):
        if self.showindicator :
            od = self.dataframe
            # list all the buy points and sell points
            length = len(od.index)
            l3x, l3y = [], []
            l4x, l4y = [], []
            for n in range(0, length):
                if od.iloc[n, 3] != 0:
                    l3x.append(n)
                    l3y.append(od.iloc[n, 3])
                if od.iloc[n, 4] != 0:
                    l4x.append(n)
                    l4y.append(od.iloc[n, 4])

            # draw buy points
            for i in range(0, len(l3x)):
                plt.plot(l3x[i], l3y[i], 'r*')
            # draw sell points
            for i in range(0, len(l4x)):
                plt.plot(l4x[i], l4y[i], 'kx')

        else :
            # plt.clf()
            self.drawFigue(self.zoomidx,self.view_startx)

        self.showindicator = not (self.showindicator)
        self.canvas.draw() # 在窗体内绘图，如果直接使用 plot.show()则会另外开启绘图窗口

    def gotopre(self):
        pass

    def gotonext(self):
        pass

    def gotobegin(self):
        pass

    def gotoend(self):
        # plt.clf()
        self.drawFigue(self.zoomidx,self.getStartFromBack())
        print('go to end:', self.zoomidx,self.getStartFromBack() )

    def getStartFromBack(self):
        length1 = len(self.dataframe.index)
        if length1 < 5:
            return 0

        length2 = int(length1*(11-self.zoomidx)/10)
        self.view_startx = length1 - length2
        return self.view_startx

    def onslider(self):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = ShowWindow()
    main.setWindowTitle('Simple QTpy and MatplotLib example with Zoom/Pan')
    main.show()

    sys.exit(app.exec_())