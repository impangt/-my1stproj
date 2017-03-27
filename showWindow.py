# encoding: utf-8
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

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
        # figure area
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111)
        #self.axes.hold(False) # We want the axes cleared every time plot() is called
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)
        ### self.toolbar.hide()

        # Just some button
        self.openButton = QtWidgets.QPushButton("Open")
        self.openButton.clicked.connect(self.msg)

        self.button1 = QtWidgets.QPushButton('Plot')
        self.button1.clicked.connect(self.plot)

        self.button2 = QtWidgets.QPushButton('Zoom')
        self.button2.clicked.connect(self.zoom)

        self.button3 = QtWidgets.QPushButton('Pan')
        self.button3.clicked.connect(self.pan)

        self.button4 = QtWidgets.QPushButton('Home')
        self.button4.clicked.connect(self.home)

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        btnlayout = QtWidgets.QHBoxLayout()
        btnlayout.addWidget(self.openButton)
        btnlayout.addWidget(self.button1)
        btnlayout.addWidget(self.button2)
        btnlayout.addWidget(self.button3)
        btnlayout.addWidget(self.button4)
        qw = QtWidgets.QWidget(self)
        qw.setLayout(btnlayout)
        layout.addWidget(qw)

        self.setLayout(layout)

        # other parameters
        self.targetDir = 'C:\\'
        self.dataframe = pd.DataFrame()

    def home(self):
        self.toolbar.home()

    def zoom(self):
        self.toolbar.zoom()

    def pan(self):
        self.toolbar.pan()

    def plot(self):
        self.dataframe = de.readDailyData(self.targetDir, '2016/01/01', '2017/01/01')
        self.dataframe['buy'] = 0.0
        self.dataframe['sell'] = 0.0
        de.runBackTrace(self.dataframe)

        length = len(self.dataframe.index)
        x = np.arange(0, length, 1)
        y = self.dataframe.iloc[:, 0]

        # list the display label of x-axis
        l2 = []
        for i in np.arange(0, len(self.dataframe.index), 1):
            l2.append(self.dataframe.index[i])

        # list all the buy points and sell points
        l3x, l3y = [], []
        l4x, l4y = [], []
        for n in range(0, length):
            if self.dataframe.iloc[n, 3] != 0:
                l3x.append(n)
                l3y.append(self.dataframe.iloc[n, 3])
            if self.dataframe.iloc[n, 4] != 0:
                l4x.append(n)
                l4y.append(self.dataframe.iloc[n, 4])

        # draw the main figure first
        plt.xticks(np.arange(0, length, 1), l2, rotation=60)  # show partial labels
        plt.plot(x, y, 'b')
        plt.ylabel('day price')
        plt.plot(x, y, color='k')  # , linestyle='dashed', marker='o')
        # draw buy points
        for i in range(0, len(l3x)):
            plt.plot(l3x[i], l3y[i], 'r*')
        # draw sell points
        for i in range(0, len(l4x)):
            plt.plot(l4x[i], l4y[i], 'yo')

        #plt.grid()
        plt.grid()
        self.canvas.draw()
        # ''' plot some random stuff '''
        # data = [random.random() for i in range(25)]
        # self.axes.plot(data, '*-')
        # self.canvas.draw()

    def msg(self):
        self.targetDir, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          'C:\\',
                                                          "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = ShowWindow()
    main.setWindowTitle('Simple QTpy and MatplotLib example with Zoom/Pan')
    main.show()

    sys.exit(app.exec_())