# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

class BrezierCurve(QtWidgets.QGraphicsPathItem):
    def __init__(self, p1, c1, c2, p2, sampleN, *args, **kwargs):
        super(BrezierCurve, self).__init__(*args, **kwargs)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(p1.pos())
        self.path.cubicTo(c1.pos(), c2.pos(), p2.pos())
        self.setPath(self.path)

        self.p1 = p1
        self.p2 = p2
        self.c1 = c1
        self.c2 = c2
        self.sampleN = sampleN

    def paint(self, painter, option, widget=None):
        self.path = QtGui.QPainterPath()
        self.path.moveTo(self.p1.pos())
        self.path.cubicTo(self.c1.pos(), self.c2.pos(), self.p2.pos())
        self.setPath(self.path)
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
        pen.setWidthF(0.5)
        pen.setDashPattern([1, 2])
        self.setPen(pen)
        super(BrezierCurve, self).paint(painter, option, widget=widget)

        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        pen = QtGui.QPen(QtGui.QColor(128, 128, 128))
        pen.setWidthF(0.2)
        painter.setPen(pen)
        painter.drawLine(self.p1.pos(), self.c1.pos())
        painter.drawLine(self.p2.pos(), self.c2.pos())
        pen = QtGui.QPen(QtGui.QColor(0, 128, 128))
        pen.setWidthF(1.5)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(pen)
        for i in range(self.sampleN - 1):
            len = float(i + 1) / self.sampleN * self.path.length()
            painter.drawPoint(self.path.pointAtPercent(self.path.percentAtLength(len)))

    def debug(self):
        print(self)
