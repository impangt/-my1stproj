import sys
import myMainWindow
import deduceEarning as dE
import datetime
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

matplotlib.use("Qt5Agg")


class MyCanvas(FigureCanvas):
    """这是一个窗口部件，即QWidget（当然也是FigureCanvasAgg）"""

    def __init__(self, parent=None):  # , width=10, height=10, dpi=100):
        self.fig = plt.figure()  # Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.mycanvas = FigureCanvas(self.fig)
        # self.compute_initial_figure()
        #
        FigureCanvas.__init__(self, self.fig)  # ???
        self.setParent(parent)  # ???
        # FigureCanvas.updateGeometry(self)# ???

        # parameters for computing
        self.view_startx = 0  # the start x index of the current view window
        self.zoomidx = 1
        self.showindicator = True

    # draw sin figure
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)

    # the scope of zoom rate is [1, 10], 1 = no zoom , 2 = zoom to 90% , 3 = to 80%, ... 10 = 10%
    def drawfigure(self, dataframe):
        plt.clf()
        length1 = len(dataframe.index)

        viewx = np.arange(0, length1, 1)
        y = dataframe.iloc[:, 0]

        # list the display label of x-axis
        l1 = []
        step = int(length1 / 5)  # 如果选择的日期数量少于step，则会出错
        if step == 0:
            return False

        for i in np.arange(0, length1, step):
            l1.append(dataframe.index[i])

        plt.xlim(0, length1)
        plt.xticks(np.arange(0, length1, step), l1)  # , rotation=30)
        plt.ylabel('day price')
        plt.plot(viewx, y, color='c')  # , linestyle='dashed', marker='o')
        #
        plt.grid()
        self.draw()  # 在窗体内绘图，如果直接使用 plot.show()则会另外开启绘图窗口
        return True

    def drawindicator(self, dataframe):
        od = dataframe
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

        self.draw()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        # connect to the UI made by QtDesigner
        self.ui = myMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        # parameters for computing
        self.targetDir = ''
        self.view_start = 0  # the start index of the current view window
        self.slidewindowsize = 10
        self.zoomidx = 1
        self.showindicator = True

        self.mycanvas = MyCanvas(self)  # mainAppWindow.ui.mainWidget)#, width=5, height=4, dpi=100)
        self.ui.verticalLayout.addWidget(self.mycanvas)

        self.dataframe = pd.DataFrame()
        self.originaldatalength = 0

    def openButtonClicked(self):
        self.targetDir, filetype = QFileDialog.getOpenFileName(self,
                                                               "选取文件",
                                                               'E:\\github\\my1stproj',
                                                               "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        if self.targetDir != '':
            # read the file data into memory
            self.dataframe = dE.readDailyData(self.targetDir)
            self.dataframe['buy'] = 0.0
            self.dataframe['sell'] = 0.0

            # set the dateEdit controller
            self.setEditDate(self.dataframe.index[0], self.dataframe.index[-1])

            self.originaldatalength = len(self.dataframe.index)
            self.slidewindowsize = self.originaldatalength
            self.ui.hslider.setRange(0, 0)
            print("origin length is ", self.slidewindowsize)

            # draw the figure
            self.mycanvas.drawfigure(self.dataframe)

    def zoomInButtonClicked(self):
        if self.slidewindowsize > 10:
            view_lenth = int(self.slidewindowsize * 8 / 10)
            view_dateframe = self.dataframe.iloc[self.view_start:view_lenth - 1, ]
            self.mycanvas.drawfigure(view_dateframe)
            self.slidewindowsize = view_lenth
            self.ui.hslider.setRange(0, self.originaldatalength - view_lenth)
            # set the dateEdit controller
            self.setEditDate(view_dateframe.index[0], view_dateframe.index[-1])

    def zoomoutButtonClicked(self):
        self.view_start = 0
        if self.slidewindowsize <= len(self.dataframe.index):
            view_lenth = int(self.slidewindowsize * 12 / 10)
            view_dateframe = self.dataframe.iloc[self.view_start:view_lenth, ]
            self.mycanvas.drawfigure(view_dateframe)
            self.slidewindowsize = view_lenth
            self.ui.hslider.setRange(0, self.originaldatalength - view_lenth)
            # set the dateEdit controller
            self.setEditDate(view_dateframe.index[0], view_dateframe.index[-1])

    def applyButtonClicked(self):
        reply = QMessageBox.information(self,
                                        "Whoops",
                                        "To be completed in the future!",
                                        QMessageBox.Ok)  # .Yes | QMessageBox.No)

    def lookbackButtonClicked(self):
        print('select from ', self.dataframe.index[self.view_start], ' to ',
              self.dataframe.index[self.view_start + self.slidewindowsize - 1], self.slidewindowsize)
        view_dateframe = self.dataframe.iloc[self.view_start:self.view_start + self.slidewindowsize - 1, ]
        incomes = dE.runBackTrace(view_dateframe)
        self.mycanvas.drawindicator(view_dateframe)
        # print('look back', view_dateframe.head(10))
        print('---current income = ', incomes)

    def slideWindowZoom(self):
        pass

    def windowSliding(self):
        pos = self.ui.hslider.value()
        print('slider pos = ', pos)
        if pos + self.slidewindowsize <= self.originaldatalength + 1:
            view_dateframe = self.dataframe.iloc[pos:pos + self.slidewindowsize, ]
            self.mycanvas.drawfigure(view_dateframe)
            self.view_start = pos
            # set the dateEdit controller
            self.setEditDate(view_dateframe.index[0], view_dateframe.index[-1])

    # set the dateEdit controller
    def setEditDate(self, dfstr1, dfstr2):
        date1 = datetime.datetime.strptime(dfstr1, "%Y/%m/%d")
        date2 = datetime.datetime.strptime(dfstr2, "%Y/%m/%d")
        self.ui.dateEditFrom.setDate(QDate(date1.year, date1.month, date1.day))
        self.ui.dateEditTo.setDate(QDate(date2.year, date2.month, date2.day))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainAppWindow = ApplicationWindow()
    # ui = myMainWindow.Ui_MainWindow()
    # ui.setupUi(mainAppWindow)

    # layout = QVBoxLayout(ui.mainWidget)
    # canv = MyCanvas(ui.mainWidget)#, width=5, height=4, dpi=100)
    # layout.addWidget(canv)

    # canv = MyCanvas(mainAppWindow.ui.mainWidget)#, width=5, height=4, dpi=100)
    # mainAppWindow.ui.verticalLayout.addWidget(canv)

    mainAppWindow.show()
    sys.exit(app.exec_())
