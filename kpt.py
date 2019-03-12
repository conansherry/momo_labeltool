# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

class Keypoint(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, name, *args, **kwargs):
        super(Keypoint, self).__init__(*args, **kwargs)
        self.name = name
        self.history_pos = []
        self.last_pos = None

    def setPos(self, *__args):
        super(Keypoint, self).setPos(*__args)
        is_change = False
        if self.last_pos is None or self.last_pos != [__args[0], __args[1]]:
            self.updatePos(__args[0], __args[1])
            is_change = True
        self.last_pos = [__args[0], __args[1]]
        return is_change

    def redoPos(self):
        if len(self.history_pos) > 1:
            self.history_pos.pop()
            lastPos = self.history_pos.pop()
            self.setPos(lastPos[0], lastPos[1])
            print(self.name, self.history_pos)

    def updatePos(self, x, y):
        self.history_pos.append([x, y])

    def debug(self):
        print(self.name, self.history_pos)

    # def itemChange(self, *args, **kwargs):
    #     print(self.name, 'item change')
    #     return super(Keypoint, self).itemChange(*args, **kwargs)
