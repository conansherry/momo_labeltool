# -*- coding: utf-8 -*-

import sys
import mainwin
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = mainwin.Ui_main_window()
    ui.setupUi(MainWindow)

    ui.file_list.currentItemChanged.connect(ui.canvas.openItem)
    ui.index.stateChanged.connect(ui.canvas.showName)
    ui.fixitem.stateChanged.connect(ui.canvas.fixItem)
    ui.control.stateChanged.connect(ui.canvas.showControl)
    ui.keypoint.stateChanged.connect(ui.canvas.showKeypoint)
    ui.contour.stateChanged.connect(ui.canvas.showContour)
    ui.left_eyebrown.stateChanged.connect(ui.canvas.showLeftEyeBrown)
    ui.right_eyebrown.stateChanged.connect(ui.canvas.showRightEyeBrown)
    ui.left_eye.stateChanged.connect(ui.canvas.showLeftEye)
    ui.right_eye.stateChanged.connect(ui.canvas.showRightEye)
    ui.nose.stateChanged.connect(ui.canvas.showNose)
    ui.mouth_outter.stateChanged.connect(ui.canvas.showMouthOutter)
    ui.mouth_inner.stateChanged.connect(ui.canvas.showMouthInner)

    ui.canvas.fixitem_ = ui.fixitem
    ui.canvas.index_ = ui.index
    ui.canvas.control_ = ui.control
    ui.canvas.keypoint_ = ui.keypoint
    ui.canvas.contour_ = ui.contour
    ui.canvas.left_eyebrown_ = ui.left_eyebrown
    ui.canvas.right_eyebrown_ = ui.right_eyebrown
    ui.canvas.left_eye_ = ui.left_eye
    ui.canvas.right_eye_ = ui.right_eye
    ui.canvas.nose_ = ui.nose
    ui.canvas.mouth_outter_ = ui.mouth_outter
    ui.canvas.mouth_inner_ = ui.mouth_inner

    ui.actionload.triggered.connect(ui.file_list.loadDir)
    ui.actionConvert.triggered.connect(ui.file_list.convertAll)
    ui.actionConvert1k.triggered.connect(ui.file_list.convertAll_1k)

    MainWindow.show()
    sys.exit(app.exec_())
