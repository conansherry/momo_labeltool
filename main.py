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

    ui.file_list.itemClicked.connect(ui.canvas.openItem)

    MainWindow.show()
    sys.exit(app.exec_())
