# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

def get_foot(pt, line_begin, line_end):
    dx = line_begin.x() - line_end.x()
    dy = line_begin.y() - line_end.y()
    if dx == 0 or dy == 0:
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
        super(Keypoint, self).paint(painter, option, widget=widget)

        if self.name is not None and self.show_name:
            pen = QtGui.QPen(QtGui.QColor(253, 67, 23))
            pen.setWidthF(0.2)
            painter.setPen(pen)
            painter.setFont(QtGui.QFont('times', 2))
            painter.drawText(0, 0, str(self.name))

        if self.begin is not None and self.end is not None:
            tmp_foot = get_foot(self.pos(), self.begin.pos(), self.end.pos())
            self.setPosNoHistory(tmp_foot)

    def showName(self, flag):
        self.show_name = flag

    def setAlongPath(self, begin, end):
        self.begin = begin
        self.end = end

    # def mouseMoveEvent(self, event):
    #     super(Keypoint, self).mouseMoveEvent(event)
    #     if self.begin is not None and self.end is not None:
    #         print(self.parentItem().mapFromScene(self.mapToScene(event.pos())), self.pos())
    #         mouse_pos = self.parentItem().mapFromScene(self.mapToScene(event.pos()))
    #         tmp_foot = get_foot(mouse_pos, self.begin.pos(), self.end.pos())
    #         self.setPosNoHistory(tmp_foot)

    # def itemChange(self, *args, **kwargs):
    #     print(self.name, 'item change')
    #     return super(Keypoint, self).itemChange(*args, **kwargs)
