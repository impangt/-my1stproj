from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import configparser
import selectPoliciesDialog
from PyQt5.QtWidgets import QApplication, QDialog, QCheckBox, QListWidgetItem, QTableWidget, QTableWidgetItem, \
    QHeaderView

class PoliciesDialog(QDialog, selectPoliciesDialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(PoliciesDialog, self).__init__(parent)
        self.setupUi(self)

        self.tableWidget.setHorizontalHeaderLabels(['property', 'value', 'information'])
        # set the tableWidget header width and style
        # headerview = self.tableWidget.horizontalHeader()
        # headerview.setSectionResizeMode(2, QHeaderView.Stretch)
        # for x in range(self.tableWidget.columnCount()):
        #     headItem = self.tableWidget.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象
        #     headItem.setForeground(QColor(0, 0, 255))
        #     headItem.setBackground(QColor(Qt.cyan))      # 设置单元格背景颜色, 在windows环境中不起作用!!!
        self.filename = 'config\\config.ini' # 如果使用双引号会出错，为什么？？？？
        self.filltabledata()

    def resetselections1(self):
        l1 = []
        for i in range(self.listWidgetBuy.count()):
            check_box = self.listWidgetBuy.itemWidget(self.listWidgetBuy.item(i))
            state = check_box.checkState()
            if state:
                l1.append(i)
        print(l1)

    def resetselections2(self):
        l1 = []
        for i in range(self.listWidgetSell.count()):
            check_box = self.listWidgetSell.itemWidget(self.listWidgetSell.item(i))
            state = check_box.checkState()
            if state:
                l1.append(i)
        print(l1)

    def selectall1(self):
        state = self.checkBoxBuySelectAll.isChecked()
        for i in range(self.listWidgetBuy.count()):
            check_box = self.listWidgetBuy.itemWidget(self.listWidgetBuy.item(i))
            if state:
                check_box.setChecked(True)
            else:
                check_box.setChecked(False)

    def selectall2(self):
        state = self.checkBoxSellSelectAll.isChecked()
        for i in range(self.listWidgetSell.count()):
            check_box = self.listWidgetSell.itemWidget(self.listWidgetSell.item(i))
            if state:
                check_box.setChecked(True)
            else:
                check_box.setChecked(False)

    def ini_buyandsell_lists(self, buylist, bselections, selllist,sselections):
        if len(buylist) != len(bselections) or len(selllist) != len(sselections):
            return False

        for i in range(len(buylist)):
            self.listWidgetBuy.setItemWidget(QListWidgetItem(self.listWidgetBuy), QCheckBox(buylist[i]))
        for i in range(self.listWidgetBuy.count()):
            check_box = self.listWidgetBuy.itemWidget(self.listWidgetBuy.item(i))
            if bselections[i]:
                check_box.setChecked(True)

        for j in range(len(selllist)):
            self.listWidgetSell.setItemWidget(QListWidgetItem(self.listWidgetSell), QCheckBox(selllist[j]))
        for i in range(self.listWidgetSell.count()):
            check_box = self.listWidgetSell.itemWidget(self.listWidgetSell.item(i))
            if sselections[i]:
                check_box.setChecked(True)

        return True

    def get_buy_pstrlist(self):
        l = []
        for i in range(self.listWidgetBuy.count()):
            cb1 = self.listWidgetBuy.itemWidget(self.listWidgetBuy.item(i))
            if cb1.checkState():
                l.append('1')
            else:
                l.append('0')
        return l

    def get_sell_pstrlist(self):
        l = []
        for j in range(self.listWidgetSell.count()):
            cb2 = self.listWidgetSell.itemWidget(self.listWidgetSell.item(j))
            if cb2.checkState():
                l.append('1')
            else:
                l.append('0')
        return l

    def filltabledata(self):
        # get ini file data
        config = configparser.ConfigParser()
        config.read_file(open(self.filename))
        sec = config.sections()
        lop = []
        for i in range(len(sec)):
            lop.append(config.options(sec[i]))
        # fill data to the table widget
        i = 0
        for n in range(len(sec)):
            self.tableWidget.setRowCount(i + 1)
            self.tableWidget.setSpan(i, 0, 1, 3)
            secitem = QTableWidgetItem(sec[n])
            secitem.setForeground(QColor(Qt.red))
            self.tableWidget.setItem(i, 0, secitem)
            secitem.setFlags(secitem.flags() & (~Qt.ItemIsEditable))
            for j in range(len(lop[n])):
                i = i + 1
                self.tableWidget.setRowCount(i + 1)
                item0 = QTableWidgetItem(lop[n][j])
                item0.setFlags(item0.flags() & (~Qt.ItemIsEditable))  # Item name can't edit
                s = config.get(sec[n], lop[n][j])
                s1, s2 = s.split("#")
                item1 = QTableWidgetItem(s1)
                item2 = QTableWidgetItem(s2)
                self.tableWidget.setItem(i, 0, item0)
                self.tableWidget.setItem(i, 1, item1)
                self.tableWidget.setItem(i, 2, item2)
                # print(n, j, lop[n][j], i)
            i = i + 1
            self.tableWidget.resizeColumnsToContents()
            # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def resetedit(self):
        self.tableWidget.clear()
        self.filltabledata()

    def savechanges(self):
        config = configparser.ConfigParser()
        config.read_file(open(self.filename))
        sec = config.sections()
        lop = []
        for i in range(len(sec)):
            lop.append(config.options(sec[i]))

        fd = open(self.filename, 'w')
        i = 0
        for n in range(len(sec)):
            for j in range(len(lop[n])):
                i = i + 1
                s0 = self.tableWidget.item(i, 0).text()
                s1 = self.tableWidget.item(i, 1).text()
                s2 = self.tableWidget.item(i, 2).text()
                config.set(sec[n], s0, s1.strip()+' # '+s2.strip())
                #print(s0,s1,s2)
            i = i + 1
        config.write(fd)
        fd.close()

# app = QApplication(sys.argv)
# dialog = PoliciesDialog()
# dialog.show()
# app.exec_()
