# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwin.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1037, 784)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.canvas = Canvas(self.centralwidget)
        self.canvas.setInteractive(True)
        self.canvas.setObjectName("canvas")
        self.gridLayout_3.addWidget(self.canvas, 0, 0, 1, 1)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1037, 18))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.dockWidget_2 = QtWidgets.QDockWidget(main_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_2.sizePolicy().hasHeightForWidth())
        self.dockWidget_2.setSizePolicy(sizePolicy)
        self.dockWidget_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout.setObjectName("gridLayout")
        self.file_list = FileList(self.dockWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_list.sizePolicy().hasHeightForWidth())
        self.file_list.setSizePolicy(sizePolicy)
        self.file_list.setObjectName("file_list")
        self.gridLayout.addWidget(self.file_list, 0, 0, 1, 1)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        main_window.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_2)
        self.actionload = QtWidgets.QAction(main_window)
        self.actionload.setObjectName("actionload")
        self.menu.addAction(self.actionload)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "MomoLabel"))
        self.menu.setTitle(_translate("main_window", "文件"))
        self.actionload.setText(_translate("main_window", "载入文件夹"))

from canvas import Canvas
from filelist import FileList
