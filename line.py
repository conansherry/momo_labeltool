# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
import numpy as np

class Line(QtWidgets.QGraphicsPathItem):
    def __init__(self, p1, p2, sampleN, isHelp, *args, **kwargs):
        super(Line, self).__init__(*args, **kwargs)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(p1.pos())
        self.path.lineTo(p2.pos())
        self.setPath(self.path)

        self.p1 = p1
        self.p2 = p2
        self.sampleN = sampleN
        self.isHelp = isHelp

    def paint(self, painter, option, widget=None):
        self.path = QtGui.QPainterPath()
        self.path.moveTo(self.p1.pos())
        self.path.lineTo(self.p2.pos())
        self.setPath(self.path)
        self.setPath(self.path)
        if self.isHelp:
            pen = QtGui.QPen(QtGui.QColor(128, 128, 128))
        else:
            pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
        pen.setWidthF(3 / self.parentItem().scale_flag)
        pen.setDashPattern([1, 2])
        self.setPen(pen)
        super(Line, self).paint(painter, option, widget=widget)

        pen = QtGui.QPen(QtGui.QColor(0, 128, 128))
        pen.setWidthF(1.5)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(pen)
        for i in range(self.sampleN - 1):
            len = float(i + 1) / self.sampleN * self.path.length()
            painter.drawPoint(self.path.pointAtPercent(self.path.percentAtLength(len)))

    def getKeypoints(self, sampleN=None):
        if sampleN is None:
            sampleN = self.sampleN
        res = np.zeros((sampleN + 1, 2), dtype=np.float32)
        res[0] = [self.p1.pos().x(), self.p1.pos().y()]
        for i in range(sampleN - 1):
            len = float(i + 1) / sampleN * self.path.length()
            tmp_pt = self.path.pointAtPercent(self.path.percentAtLength(len))
            res[i + 1] = [tmp_pt.x(), tmp_pt.y()]
        res[-1] = [self.p2.pos().x(), self.p2.pos().y()]

        return res
