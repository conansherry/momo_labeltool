# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

import numpy as np

def get_foot(pt, line_begin, line_end):
    dx = line_begin.x() - line_end.x()
    dy = line_begin.y() - line_end.y()
    if dx == 0 and dy == 0:
        return QtCore.QPointF(0, 0)
    u = (pt.x() - line_begin.x()) * (line_begin.x() - line_end.x()) + (pt.y() - line_begin.y()) * (line_begin.y() - line_end.y())
    u = u / (dx * dx + dy * dy)
    return QtCore.QPointF(line_begin.x() + u * dx, line_begin.y() + u * dy)

class Keypoint(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, name, pt, *args, **kwargs):
        super(Keypoint, self).__init__(*args, **kwargs)
        self.name = name
        self.pt = pt
        self.history_pos = []
        self.last_pos = None

        self.show_name = False
        self.begin = None
        self.end = None

        self.is_eye = False

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

    def setPosNoHistory(self, *__args):
        super(Keypoint, self).setPos(*__args)
        if isinstance(__args[0], QtCore.QPointF):
            x_ = __args[0].x()
            y_ = __args[0].y()
        else:
            x_ = __args[0]
            y_ = __args[1]
        self.pt[0] = x_
        self.pt[1] = y_
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

    def paint(self, painter, option, widget=None):
        if not self.is_eye:
            keypoint_scale = 4 / self.parentItem().scale_flag
            if keypoint_scale < 0.5:
                keypoint_scale = 0.5
            elif keypoint_scale > 2:
                keypoint_scale = 2
            self.setScale(keypoint_scale)
        super(Keypoint, self).paint(painter, option, widget=widget)

        if self.name is not None and self.show_name:
            pen = QtGui.QPen(QtGui.QColor(253, 67, 23))
            pen.setWidthF(0.2)
            painter.setPen(pen)
            painter.setFont(QtGui.QFont('times', 5))
            painter.drawText(0, 0, str(self.name))

        if self.begin is not None and self.end is not None:
            tmp_foot = get_foot(self.pos(), self.begin.pos(), self.end.pos())
            self.setPosNoHistory(tmp_foot)

    def wheelEvent(self, event):
        delta = event.delta()
        cur_scale = self.scale()
        if delta < 0:
            self.setScale(cur_scale - 0.2)
        elif delta > 0:
            self.setScale(cur_scale + 0.2)

        # super(Keypoint, self).wheelEvent(event)
        # myshape = self.shape()
        # for i in range(20):
        #     len = float(i) / 20
        #     print(self.mapToParent(myshape.pointAtPercent(len)))

    def showName(self, flag):
        self.show_name = flag

    def setAlongPath(self, begin, end):
        self.begin = begin
        self.end = end

    def setIsEye(self, flag):
        self.is_eye = flag

    def getKeypoints(self, sampleN=36, rotate_degree=0.):
        if self.is_eye:
            self.setRotation(rotate_degree)
        path = QtGui.QPainterPath(self.shape())
        path.closeSubpath()
        res = np.zeros((sampleN, 2), dtype=np.float32)
        for i in range(0, sampleN):
            len = float(i) / sampleN * path.length() / 3
            tmp_pt = self.mapToParent(path.pointAtPercent(path.percentAtLength(len)))
            res[i] = [tmp_pt.x(), tmp_pt.y()]
        return res

        # myshape = self.shape()
        # res = np.zeros((sampleN + 1, 2), dtype=np.float32)
        # tmp_pt = self.mapToParent(myshape.pointAtPercent(0))
        # res[0] = [tmp_pt.x(), tmp_pt.y()]
        # for i in range(1, sampleN):
        #     len = float(i) / sampleN * 0.5
        #     tmp_pt = self.mapToParent(myshape.pointAtPercent(len))
        #     res[i] = [tmp_pt.x(), tmp_pt.y()]
        # return res
