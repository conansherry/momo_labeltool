# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

class Keypoint(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, name, pt, *args, **kwargs):
        super(Keypoint, self).__init__(*args, **kwargs)
        self.name = name
        self.pt = pt
        self.history_pos = []
        self.last_pos = None

    def setPos(self, *__args):
        super(Keypoint, self).setPos(*__args)
        if isinstance(__args[0], QtCore.QPointF):
            x_ = __args[0].x()
            y_ = __args[0].y()
        else:
            x_ = __args[0]
            y_ = __args[1]
        is_change = False
        if self.last_pos is None or self.last_pos != [x_, y_]:
            if self.last_pos is not None and self.last_pos != [x_, y_]:
                self.pt[0] = x_
                self.pt[1] = y_
            self.updatePos(x_, y_)
            is_change = True
        self.last_pos = [x_, y_]
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
