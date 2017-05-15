import matplotlib

matplotlib.use("Qt5Agg")

import sys
import myMainWindow
import pandas as pd
import numpy as np
from selectPoliciesDlg import PoliciesDialog
import deduceEarning as dE
import drawGraph

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pylab import *
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MultipleLocator
from matplotlib.widgets import MultiCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDateTimeEdit


class MyCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None):
        self.fig = plt.figure(facecolor='lightblue', dpi=100)  # 这里设置figsize没有用！
        # 设置两个绘图区域，图像高度比例为4:1
        gs = gridspec.GridSpec(3, 1, height_ratios=[4, 1, 1])
        self.axes  = plt.subplot(gs[0])
        self.axes1 = plt.subplot(gs[1])
        self.axes2 = plt.subplot(gs[2])
        # 设置区域的坐标属性
        self.axes.set_ylabel("day price")
        self.axes1.set_xticks([])  # 设置图v刻度为空
        self.axes2.set_xticks([])  # 设置图2刻度为空
        self.axes2.set_yticks([])
        # 调整画布的边界
        plt.subplots_adjust(left=0.08, bottom=0.02, right=0.98, top=0.98, wspace=None, hspace=0.2)
        #
        self.mycanvas = FigureCanvas(self.fig)
        FigureCanvas.__init__(self, self.fig)  # ???
        self.setParent(parent)  # ???
        # FigureCanvas.updateGeometry(self)# ???

        # parameters for computing
        self.showindicator = True
        self.dragrect = None

    def drawfigureK(self, dataframe):
        self.axes.clear()  # It's so hard i find this way to clear axes...
        length1 = len(dataframe.index)
        if length1 == 0: return False

        # list the display label of x-axis
        l1 = []
        step = int(length1 / 5)  # 如果选择的日期数量少于step，则会出错
        # print('step = ', step, 'length = ', length1)
        if step == 0:
            return False

        for i in np.arange(0, length1, step):
            l1.append(dataframe.index[i])

        self.axes.set_xlim(0, length1-1)
        self.axes.set_xticks(np.arange(0, length1, step))
        self.axes.set_xticklabels(l1)

        # draw candle figure
        for i in range(0, length1):
            openp = dataframe.iloc[i, 0]
            highp = dataframe.iloc[i, 1]
            lowp  = dataframe.iloc[i, 2]
            closep= dataframe.iloc[i, 3]
            w = 0.6
            col = ''
            #draw rect first
            rectx = [i-w/2, i+w/2, i+w/2, i-w/2, i-w/2]
            recty = [closep, closep, openp, openp, closep]
            if closep < openp:
                col = 'g'
                #draw up and down lines
                lx = [i, i]
                l1y = [highp, openp]
                l2y = [closep, lowp]
            else:
                col = 'r'
                #draw up and down lines
                lx = [i, i]
                l1y = [highp, closep]
                l2y = [openp, lowp]
            self.axes.plot(rectx, recty, col)
            self.axes.plot(lx, l1y, col)
            self.axes.plot(lx, l2y, col)

        self.axes.grid()
        self.draw()  # 在窗体内绘图，如果直接使用 plot.show()则会另外开启绘图窗口
        return True

    def drawfigure1(self, dataframe):
        self.axes.clear()  # It's so hard i find this way to clear axes...
        length1 = len(dataframe.index)
        if length1 == 0: return False

        viewx = np.arange(0, length1, 1)
        # print("length = ", length1, 'viewx=', viewx)

        # list the display label of x-axis
        l1 = []
        step = int(length1 / 5)  # 如果选择的日期数量少于step，则会出错
        # print('step = ', step, 'length = ', length1)
        if step == 0:
            return False

        for i in np.arange(0, length1, step):
            l1.append(dataframe.index[i])

        self.axes.set_xlim(0, length1-1)
        self.axes.set_xticks(np.arange(0, length1, step))
        self.axes.set_xticklabels(l1)

        y1 = dataframe.iloc[:, 0] # open price
        # y2 = dataframe.iloc[:, 3] # close price

        self.axes.plot(viewx, y1, 'c')
        # self.axes.plot(viewx, y2, 'b')

        self.axes.grid()
        self.draw()  # 在窗体内绘图，如果直接使用 plot.show()则会另外开启绘图窗口
        return True

    # the scope of zoom rate is [1, 10], 1 = no zoom , 2 = zoom to 90% , 3 = to 80%, ... 10 = 10%
    def drawfigure2(self, dataframe):
        self.axes2.clear()

        length1 = len(dataframe.index)
        if length1 == 0: return False

        viewx = np.arange(0, length1, 1)
        y = dataframe.iloc[:, 0]

        self.axes2.set_xlim(0, length1)
        self.axes2.plot(viewx, y, color='lightgrey')
        self.axes2.fill_between(viewx, y, color="lightgrey", alpha=0.8)
        self.draw()
        return True

    # ## this method is too slow
    # def drawfigureV2(self, dataframe):
    #     self.axes1.clear()
    #     data = dataframe['vol']
    #     data.plot(kind='bar', ax=self.axes1, color='g', alpha=0.7)
    #     return True

    def drawfigureV(self, dataframe):
        self.axes1.clear()

        length1 = len(dataframe.index)
        if length1 == 0: return False

        maxv = int(dataframe.iloc[:, 4].max()/10000)
        self.axes1.set_xlim(0, length1-1)
        self.axes1.set_ylim(0, maxv)
        lx = []
        ly = []
        w = 500 / length1
        for i in range(0, length1):
            openp = dataframe.iloc[i, 0]
            closep = dataframe.iloc[i, 3]

            lx = [i, i]
            ly = [0, int(dataframe.iloc[i, 4]/10000)]
            if closep < openp:
                col = 'g'
            else:
                col = 'r'
            self.axes1.plot(lx, ly, col, linewidth=w)
        self.draw()
        return True

    def drawindicator(self, dataframe):
        od = dataframe
        # list all the buy points and sell points
        length = len(od.index)
        l3x, l3y,l3z, l4x, l4y,l4z = [], [], [],[], [], []
        for n in range(0, length):
            if od.iloc[n, 6] != 0: # buy colunm
                l3x.append(n)
                l3y.append(od.iloc[n, 6])# buy price
                l3z.append(od.iloc[n, 1])# highest price
            if od.iloc[n, 7] != 0: # sell colunm
                l4x.append(n)
                l4y.append(od.iloc[n, 7])# sell price
                l4z.append(od.iloc[n, 2])# lowest price

            # draw buy points
        for i in range(0, len(l3x)):
            self.axes.plot(l3x[i], l3y[i], 'b*')
            self.axes.annotate('', xy=(l3x[i], l3z[i]), xytext=(l3x[i], l3z[i]+0.3), arrowprops=dict(facecolor='b', shrink=1), horizontalalignment='center')
        # draw sell points
        for i in range(0, len(l4x)):
            self.axes.plot(l4x[i], l4y[i], 'kx')
            self.axes.annotate('', xy=(l4x[i], l4z[i]), xytext=(l4x[i], l4z[i]-0.3), arrowprops=dict(facecolor='r', shrink=1), horizontalalignment='center')
        self.draw()

class ApplicationWindow(QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        # connect to the UI made by QtDesigner
        self.ui = myMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        # parameters for computing
        self.targetDir = ''
        self.showindicator = True

        self.mycanvas = MyCanvas(self)  # mainAppWindow.ui.mainWidget)#, width=5, height=4, dpi=100)
        self.mycanvas.mpl_connect('button_press_event', self.on_mousebutton_press)
        self.mycanvas.mpl_connect('button_release_event', self.on_mousebutton_release)
        self.mycanvas.mpl_connect('motion_notify_event', self.on_cursor_motion)

        self.ui.verticalLayout.addWidget(self.mycanvas)
        self.ui.loadstButton.setDisabled(True)

        self.dataframe = pd.DataFrame()
        self.pdfile = 'config\\policyselections'
        self.multicursor = MultiCursor(self.mycanvas, (self.mycanvas.axes, self.mycanvas.axes1), horizOn=True,
                                       color='r', lw=0.5)
        self.ui.buttonCursor.setText("-")

    def on_mousebutton_press(self, event):
        if event.inaxes != self.mycanvas.axes2: return
        self.mycanvas.dragrect.on_press(event)

    def on_mousebutton_release(self, event):
        # if event.inaxes != self.mycanvas.axes: return
        # if self.dataframe.empty: return
        #
        # # get cursor positions
        # print (event.button, event.x, event.y, event.xdata, event.ydata)
        pass

    def on_cursor_motion(self, event):
        if self.dataframe.empty: return

        if event.inaxes == self.mycanvas.axes2:
            if not self.mycanvas.dragrect.is_pressed(): return

            # set data frame according to the drag rectangle datas
            x1 = self.mycanvas.dragrect.get_rect_x1()
            x2 = self.mycanvas.dragrect.get_rect_x2() + 1

            # set spinBox and labels
            # because setSpinBox() include the drawfigureX methods ,we don't need to draw them again as below.
            self.setSpinBox(x1, x2)
            # view_dateframe = self.dataframe.iloc[x1:x2+1, ]
            # print("x1=",x1, "x2 = ", x2)
            # self.mycanvas.drawfigure1(view_dateframe)
            # self.mycanvas.drawfigureV(view_dateframe)

        elif event.inaxes == self.mycanvas.axes:
            xdata = int(event.xdata)
            # sometimes the event.xdata will over the bundage of the dataframe.
            if xdata >= self.ui.spinBoxTo.value() - self.ui.spinBoxFrom.value(): return

            cx = xdata + self.ui.spinBoxFrom.value()
            if event.xdata > xdata + 0.5:
                cx += 1
            txt = self.dataframe.index[cx]+" open:" + str(self.dataframe.iloc[cx, 0])\
                  + " high:" + str(self.dataframe.iloc[cx, 1]) \
                  + " low:" + str(self.dataframe.iloc[cx, 2]) \
                  + " close:" + str(self.dataframe.iloc[cx, 3])
            self.ui.labelX.setText(txt)
            # self.mycanvas.axes1.lines = [self.mycanvas.axes1.lines[0]]
            # self.mycanvas.axes1.axvline(x=event.xdata, color="k")

    def openButtonClicked(self):
        self.targetDir, filetype = QFileDialog.getOpenFileName(self,
                                                               "选取文件",
                                                               'D:\\github\\my1stproj\\data',
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
            x2 = self.mycanvas.dragrect.get_rect_x2() + 1
            view_dateframe = self.dataframe.iloc[x1:x2, ] # be careful the bundage
            # print('view_dataframe ---',x1, x2, self.dataframe.index[-1])

            # set the spinBox and labels
            self.ui.spinBoxFrom.setMaximum(len(self.dataframe.index) - 6)
            self.ui.spinBoxTo.setMaximum(len(self.dataframe.index) - 1)
            self.setSpinBox(x1, x2-1)

            # set buttons enable
            self.ui.loadstButton.setDisabled(False)
            self.ui.iniButton.setDisabled(False)

    def iniButtonClicked(self):
        self.setSpinBox(0, len(self.dataframe.index) - 1)
        self.mycanvas.dragrect.reset_rects(0,len(self.dataframe.index) - 1)

    def cursorButtonClicked(self):
        tx = self.ui.buttonCursor.text()
        if tx == "+":
            self.multicursor.visible = True
            self.ui.buttonCursor.setText("-")
        elif tx == '-':
            self.multicursor.visible = False
            self.ui.buttonCursor.setText("+")
        self.mycanvas.draw()

    def applyButtonClicked(self):
        pdlg = PoliciesDialog()
        bpl, spl = self.getbuysellpoliceslist()
        pdlg.ini_buyandsell_lists(dE.getbuypolicieslist(), bpl, dE.getsellpolicieslist(), spl)

        if pdlg.exec_():
            buypl = pdlg.get_buy_pstrlist()
            str1 = ','.join(buypl)
            sellpl = pdlg.get_sell_pstrlist()
            str2 = ','.join(sellpl)
            # print(buypl, sellpl)
            if buypl and sellpl:
                print("str", str1, str2)
                fd = open(self.pdfile, 'w')
                fd.write(str1)
                fd.write('\n')
                fd.write(str2)
                fd.close()
        pdlg.destroy()

    def lookbackButtonClicked(self):
        view_start = self.ui.spinBoxFrom.value()
        view_end = self.ui.spinBoxTo.value()
        print('select from ', self.dataframe.index[view_start], ' to ', self.dataframe.index[view_end])

        bpl, spl = self.getbuysellpoliceslist()
        view_dateframe = self.dataframe.iloc[view_start:view_end+1, ]
        incomes = dE.runBackTrace(view_dateframe, bpl, spl)
        self.mycanvas.drawfigureV(view_dateframe)
        if self.ui.buttonK.text() == "L":
            self.mycanvas.drawfigureK(view_dateframe)
        else:
            self.mycanvas.drawfigure1(view_dateframe)
        self.mycanvas.drawindicator(view_dateframe)
        pro = (incomes - dE.mysa.inimoney) * 100 / dE.mysa.inimoney
        # format the output value
        pro = '{:.2f}'.format(pro)
        incomes = '{:.2f}'.format(incomes)
        tx = 'We get '+ str(incomes) + ' (' + str(pro) + '%) finally '

        self.ui.labelResult.setText(tx)

    # read selected policies from file
    def getbuysellpoliceslist(self):
        fd = open(self.pdfile)
        lines = fd.readlines()
        # print(lines)
        bplist0 = lines[0].strip('\n').split(',')
        splist0 = lines[1].split(',')
        bplist1 = []
        for i in bplist0:
            bplist1.append(int(i))
        splist1 = []
        for i in splist0:
            splist1.append(int(i))
        return bplist1, splist1

    def setSpinBox(self, x1, x2):
        self.ui.spinBoxFrom.setValue(x1)
        self.ui.spinBoxTo.setValue(x2)
        self.ui.labelDateFrom.setText(self.dataframe.index[x1])
        self.ui.labelDateTo.setText(self.dataframe.index[x2])

    def fromOneDayChanged(self):
        if self.dataframe.empty: return
        print('from one day changed.')

        v1 = self.ui.spinBoxFrom.value()
        self.ui.labelDateFrom.setText(self.dataframe.index[v1])

        v2 = self.ui.spinBoxTo.value()
        view_dateframe = self.dataframe.iloc[v1:v2+1, ]
        self.mycanvas.drawfigure1(view_dateframe)
        self.mycanvas.drawfigureV(view_dateframe)
        self.ui.labelDays.setText(str(v2 - v1 + 1) + ' Days')
        if self.ui.buttonK.text() != "K":
            self.ui.buttonK.setText("K")
        # if mouse button is pressed in dragerect, then don't draw the dragrect again!!
        if not self.mycanvas.dragrect.is_pressed():
            self.mycanvas.dragrect.reset_rects(v1, v2)

    def toOneDayChanged(self):
        if self.dataframe.empty: return
        print('to one day changed.')

        v2 = self.ui.spinBoxTo.value()
        self.ui.labelDateTo.setText(self.dataframe.index[v2])
        v1 = self.ui.spinBoxFrom.value()
        view_dateframe = self.dataframe.iloc[v1:v2+1, ]
        self.mycanvas.drawfigure1(view_dateframe)
        self.mycanvas.drawfigureV(view_dateframe)
        self.ui.labelDays.setText(str(v2 - v1 + 1))
        if self.ui.buttonK.text() != "K":
            self.ui.buttonK.setText("K")
        # if mouse button is pressed in dragerect, then don't draw the dragrect again!!
        if not self.mycanvas.dragrect.is_pressed():
            self.mycanvas.dragrect.reset_rects(v1, v2)

    def kButtonClicked(self):
        if self.dataframe.empty: return

        v1 = self.ui.spinBoxFrom.value()
        self.ui.labelDateFrom.setText(self.dataframe.index[v1])

        v2 = self.ui.spinBoxTo.value()
        view_dateframe = self.dataframe.iloc[v1:v2+1, ]

        if self.ui.buttonK.text() == "K":
            self.mycanvas.drawfigureK(view_dateframe)
            self.ui.buttonK.setText("L")
        else:
            self.mycanvas.drawfigure1(view_dateframe)
            self.ui.buttonK.setText("K")
        return


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
