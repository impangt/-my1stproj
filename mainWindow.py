import matplotlib
matplotlib.use("Qt5Agg")

import sys
import myMainWindow
import datetime
import pandas as pd
import numpy as np
from numpy import arange, sin, pi
from selectPoliciesDlg import PoliciesDialog
import deduceEarning as dE
import drawGraph

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

class MyCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None):
        self.fig = plt.figure(facecolor='lightblue', dpi=100) # 这里设置figsize没有用！
        # 设置两个绘图区域，图像高度比例为4:1
        gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
        self.axes = plt.subplot(gs[0])
        self.axes2 = plt.subplot(gs[1])
        # 设置区域的坐标属性
        self.axes.set_ylabel("day price")
        self.axes2.set_xticks([])#设置图2刻度为空
        self.axes2.set_yticks([])
        # 调整画布的边界
        plt.subplots_adjust(left=0.08, bottom=0.02, right=0.98, top=0.98, wspace=None, hspace=0.2)
        #
        self.mycanvas = FigureCanvas(self.fig)
        FigureCanvas.__init__(self, self.fig)  # ???
        self.setParent(parent)  # ???
        # FigureCanvas.updateGeometry(self)# ???

        # parameters for computing
        self.view_startx = 0  # the start x index of the current view window
        self.zoomidx = 1
        self.showindicator = True

        self.dragrect = None
    # draw sin figure
    def compute_initial_figure(self):
        pass

    # the scope of zoom rate is [1, 10], 1 = no zoom , 2 = zoom to 90% , 3 = to 80%, ... 10 = 10%
    def drawfigure1(self, dataframe):
        self.axes.clear() # It's so hard i find this way to clear axes...

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

        self.axes.set_xlim(0, length1-1)
        self.axes.set_xticks(np.arange(0, length1, step))
        self.axes.set_xticklabels(l1)
        self.axes.plot(viewx, y, color='c')

        self.axes.grid()
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
            self.axes.plot(l3x[i], l3y[i], 'r*')
        # draw sell points
        for i in range(0, len(l4x)):
            self.axes.plot(l4x[i], l4y[i], 'kx')

        self.draw()

    # the scope of zoom rate is [1, 10], 1 = no zoom , 2 = zoom to 90% , 3 = to 80%, ... 10 = 10%
    def drawfigure2(self, dataframe):
        length1 = len(dataframe.index)

        viewx = np.arange(0, length1, 1)
        y = dataframe.iloc[:, 0]

        self.axes2.set_xlim(0, length1-1)
        self.axes2.plot(viewx, y, color='lightgrey')
        self.draw()
        return True

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
        self.mycanvas.mpl_connect('button_press_event', self.on_mousebutton_press)
        self.mycanvas.mpl_connect('button_release_event', self.on_mousebutton_release)

        self.ui.verticalLayout.addWidget(self.mycanvas)
        self.ui.loadstButton.setDisabled(True)

        self.dataframe = pd.DataFrame()
        self.originaldatalength = 0
        self.pdfile = 'config\\policyselections'

    def on_mousebutton_press(self,event):
        if event.inaxes != self.mycanvas.axes2: return

        # boxpoint = event.artist.get_bbox().get_points()
        self.mycanvas.dragrect.on_press(event)

    def on_mousebutton_release(self,event):
        if event.inaxes != self.mycanvas.axes2: return

        # set data frame according to the drag rectangle datas
        x1 = self.mycanvas.dragrect.get_rect_x1()
        x2 = self.mycanvas.dragrect.get_rect_x2()

        print(x1,x2,x2-x1)

        view_dateframe = self.dataframe.iloc[x1:x2, ]
        self.mycanvas.drawfigure1(view_dateframe)
        # set the dateEdit controller
        self.setEditDate(self.dataframe.index[x1], self.dataframe.index[x2])

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

            # draw figure2 first, then we get the right axes2 x limit
            self.mycanvas.drawfigure2(self.dataframe)

            # create drag rectangle in axes2
            self.mycanvas.dragrect = drawGraph.DraggableRectangle(self.mycanvas.axes2)

            # set data frame according to the drag rectangle datas
            x1 = self.mycanvas.dragrect.get_rect_x1()
            x2 = self.mycanvas.dragrect.get_rect_x2()
            print(x1,x2)
            view_dateframe = self.dataframe.iloc[x1:x2, ]

            # set the dateEdit controller
            print(self.dataframe.index[x1], self.dataframe.index[x2])
            self.setEditDate(self.dataframe.index[x1], self.dataframe.index[x2])

            # draw the figure1
            self.mycanvas.drawfigure1(view_dateframe)

            # set buttons enable
            self.ui.loadstButton.setDisabled(False)
            self.ui.iniButton.setDisabled(False)
            self.ui.zoomInButton.setDisabled(False)
            self.ui.zoomoutButton.setDisabled(False)

    def iniButtonClicked(self):
        self.mycanvas.drawfigure1(self.dataframe)
        self.mycanvas.dragrect.reset_full()

    def zoomInButtonClicked(self):
        if self.slidewindowsize > 10:
            view_lenth = int(self.slidewindowsize * 8 / 10)
            view_dateframe = self.dataframe.iloc[self.view_start:view_lenth - 1, ]
            self.mycanvas.drawfigure1(view_dateframe)
            self.slidewindowsize = view_lenth
            self.ui.hslider.setRange(0, self.originaldatalength - view_lenth)
            # set the dateEdit controller
            self.setEditDate(view_dateframe.index[0], view_dateframe.index[-1])

    def zoomoutButtonClicked(self):
        self.view_start = 0
        if self.slidewindowsize <= len(self.dataframe.index):
            view_lenth = int(self.slidewindowsize * 12 / 10)
            view_dateframe = self.dataframe.iloc[self.view_start:view_lenth, ]
            self.mycanvas.drawfigure1(view_dateframe)
            self.slidewindowsize = view_lenth
            self.ui.hslider.setRange(0, self.originaldatalength - view_lenth)
            # set the dateEdit controller
            self.setEditDate(view_dateframe.index[0], view_dateframe.index[-1])

    def applyButtonClicked(self):
        pdlg = PoliciesDialog()
        bpl, spl = self.getbuysellpoliceslist()
        pdlg.ini_buyandsell_lists(dE.getbuypolicieslist(),bpl, dE.getsellpolicieslist(),spl)

        if pdlg.exec_():
            buypl = pdlg.get_buy_pstrlist()
            str1 = ','.join(buypl)
            sellpl = pdlg.get_sell_pstrlist()
            str2 = ','.join(sellpl)
            print(buypl,sellpl)
            if buypl and sellpl:
                print("str",str1,str2)
                fd = open(self.pdfile, 'w')
                fd.write(str1)
                fd.write('\n')
                fd.write(str2)
                fd.close()
        pdlg.destroy()

    def lookbackButtonClicked(self):
        print('select from ', self.dataframe.index[self.view_start], ' to ',
              self.dataframe.index[self.view_start + self.slidewindowsize - 1], self.slidewindowsize)
        bpl, spl = self.getbuysellpoliceslist()
        view_dateframe = self.dataframe.iloc[self.view_start:self.view_start + self.slidewindowsize - 1, ]
        incomes = dE.runBackTrace(view_dateframe,bpl, spl)
        self.mycanvas.drawindicator(view_dateframe)
        # print('look back', view_dateframe.head(10))
        print('---current income = ', incomes)

    # read selected policies from file
    def getbuysellpoliceslist(self):
        fd = open(self.pdfile)
        lines = fd.readlines()
        print(lines)
        bplist0 = lines[0].strip('\n').split(',')
        splist0 = lines[1].split(',')
        bplist1 = []
        for i in bplist0:
            bplist1.append(int(i))
        splist1 = []
        for i in splist0:
            splist1.append(int(i))
        return bplist1, splist1

    def slideWindowZoom(self):
        pass

    def windowSliding(self):
        pos = self.ui.hslider.value()
        print('slider pos = ', pos)
        if pos + self.slidewindowsize <= self.originaldatalength + 1:
            view_dateframe = self.dataframe.iloc[pos:pos + self.slidewindowsize, ]
            self.mycanvas.drawfigure1(view_dateframe)
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
