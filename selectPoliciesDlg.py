from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import selectPoliciesDialog
from PyQt5.QtWidgets import QApplication, QDialog, QCheckBox, QListWidgetItem, QTableWidget, QTableWidgetItem, QHeaderView

class PoliciesDialog(QDialog, selectPoliciesDialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(PoliciesDialog, self).__init__(parent)
        self.setupUi(self)

        self.tableWidget.setHorizontalHeaderLabels(['property', 'value', 'information'])
        # set the tableWidget header width and style
        headerview = self.tableWidget.horizontalHeader()
        headerview.setSectionResizeMode(2, QHeaderView.Stretch)
        for x in range(self.tableWidget.columnCount()):
            headItem = self.tableWidget.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象
            headItem.setForeground(QColor(0, 0, 255))
            #headItem.setBackground(QColor(Qt.cyan))      # 设置单元格背景颜色, 在windows环境中不起作用!!!

        for i in range(3):
            item1 = QTableWidgetItem("up rate1")
            item2 = QTableWidgetItem("up rate2")
            item3 = QTableWidgetItem("up rate3")
            self.tableWidget.setItem(i, 0, item1)
            self.tableWidget.setItem(i, 1, item2)
            self.tableWidget.setItem(i, 2, item3)


    def resetselections(self):
        l1=[]
        for i in range(self.listWidgetSell.count()):
            check_box = self.listWidgetSell.itemWidget(self.listWidgetSell.item(i))
            state = check_box.checkState()
            if state:
                l1.append(i)

        print(l1)

    def ini_buyandsell_lists(self, buylist, selllist):
        for i in range(len(buylist)):
            self.listWidgetBuy.setItemWidget(QListWidgetItem(self.listWidgetBuy), QCheckBox(buylist[i]))

        for j in range(len(selllist)):
            self.listWidgetSell.setItemWidget(QListWidgetItem(self.listWidgetSell), QCheckBox(selllist[j]))

    def get_buy_plist(self):
        l = []
        for i in range(self.listWidgetBuy.count()):
            cb1 = self.listWidgetBuy.itemWidget(self.listWidgetBuy.item(i))
            if cb1.checkState():
                l.append(i)
        return l

    def get_sell_plist(self):
        l = []
        for j in range(self.listWidgetSell.count()):
            cb2 = self.listWidgetSell.itemWidget(self.listWidgetSell.item(j))
            if cb2.checkState():
                l.append(j)
        return l

app = QApplication(sys.argv)
dialog = PoliciesDialog()
dialog.show()
app.exec_()