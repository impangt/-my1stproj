# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(835, 521)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.selectButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectButton.setObjectName("selectButton")
        self.horizontalLayout.addWidget(self.selectButton)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(24, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.dateEditFrom = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEditFrom.setObjectName("dateEditFrom")
        self.horizontalLayout.addWidget(self.dateEditFrom)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.dateEditTo = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEditTo.setObjectName("dateEditTo")
        self.horizontalLayout.addWidget(self.dateEditTo)
        self.zoomInButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomInButton.setObjectName("zoomInButton")
        self.horizontalLayout.addWidget(self.zoomInButton)
        self.zoomoutButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomoutButton.setObjectName("zoomoutButton")
        self.horizontalLayout.addWidget(self.zoomoutButton)
        self.hslider = QtWidgets.QSlider(self.centralwidget)
        self.hslider.setOrientation(QtCore.Qt.Horizontal)
        self.hslider.setObjectName("hslider")
        self.horizontalLayout.addWidget(self.hslider)
        self.applyButton = QtWidgets.QPushButton(self.centralwidget)
        self.applyButton.setObjectName("applyButton")
        self.horizontalLayout.addWidget(self.applyButton)
        self.loadstButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadstButton.setObjectName("loadstButton")
        self.horizontalLayout.addWidget(self.loadstButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.mainWidget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainWidget.sizePolicy().hasHeightForWidth())
        self.mainWidget.setSizePolicy(sizePolicy)
        self.mainWidget.setObjectName("mainWidget")
        self.verticalLayout.addWidget(self.mainWidget)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 835, 23))
        self.menubar.setObjectName("menubar")
        self.menuMy_system = QtWidgets.QMenu(self.menubar)
        self.menuMy_system.setObjectName("menuMy_system")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.menuMy_system.addAction(self.actionOpen_File)
        self.menubar.addAction(self.menuMy_system.menuAction())

        self.retranslateUi(MainWindow)
        self.selectButton.clicked.connect(MainWindow.openButtonClicked)
        self.applyButton.clicked.connect(MainWindow.applyButtonClicked)
        self.loadstButton.clicked.connect(MainWindow.lookbackButtonClicked)
        self.dateEditFrom.dateChanged['QDate'].connect(MainWindow.slideWindowZoom)
        self.dateEditTo.dateChanged['QDate'].connect(MainWindow.slideWindowZoom)
        self.hslider.valueChanged['int'].connect(MainWindow.windowSliding)
        self.zoomInButton.clicked.connect(MainWindow.zoomInButtonClicked)
        self.zoomoutButton.clicked.connect(MainWindow.zoomoutButtonClicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.selectButton.setText(_translate("MainWindow", "Select File"))
        self.label.setText(_translate("MainWindow", "From"))
        self.label_2.setText(_translate("MainWindow", "To"))
        self.zoomInButton.setText(_translate("MainWindow", "+"))
        self.zoomoutButton.setText(_translate("MainWindow", "-"))
        self.applyButton.setText(_translate("MainWindow", "Set Strategy"))
        self.loadstButton.setText(_translate("MainWindow", "Look Back"))
        self.menuMy_system.setTitle(_translate("MainWindow", "Files"))
        self.actionOpen_File.setText(_translate("MainWindow", "Open File"))

