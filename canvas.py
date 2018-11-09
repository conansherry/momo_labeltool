# -*- coding: utf-8 -*-

from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets

import numpy as np

class Canvas(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)

        self.scale = 1.0

        self.painter = QtGui.QPainter()
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.tmp_pixel = QtGui.QPixmap(r'E:\labelme_imgs\YMGIeytZxkPEaCNv.jpg')



        tmp_scene = QtWidgets.QGraphicsScene(self)

        self.item = QtWidgets.QGraphicsPixmapItem(self.tmp_pixel)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)

        tmp_scene.addItem(self.item)

        self.setScene(tmp_scene)


    # def paintEvent(self, event):
    #     p = self.painter
    #     p.begin(self)
    #
    #     p.setRenderHint(QtGui.QPainter.Antialiasing)
    #     p.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
    #     p.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
    #     p.scale(self.scale, self.scale)
    #
    #     # pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
    #     # pen.setWidth(10)
    #     #
    #     # p.setPen(pen)
    #
    #     p.drawPixmap(0, 0, self.tmp_pixel)
    #
    #     p.end()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        print(pos)

    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        if key == QtCore.Qt.Key_P:
            print('p')
            self.scale += 0.1
        elif key == QtCore.Qt.Key_O:
            print('o')
            self.scale -= 0.1

        self.scale = np.clip(self.scale, 0.01, 100)

        self.item.setScale(self.scale)

        # self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta()
        self.scale += (float(delta.y()) / 1000)

        self.scale = np.clip(self.scale, 0.01, 100)
        self.item.setScale(self.scale)

        # self.update()
        print(delta)

    # def transformPos(self, point):
    #     """Convert from widget-logical coordinates to painter-logical ones."""
    #     return point / self.scale - self.offsetToCenter()
    #
    # def offsetToCenter(self):
    #     s = self.scale
    #     area = super(Canvas, self).size()
    #     w, h = self.pixmap.width() * s, self.pixmap.height() * s
    #     aw, ah = area.width(), area.height()
    #     x = (aw - w) / (2 * s) if aw > w else 0
    #     y = (ah - h) / (2 * s) if ah > h else 0
    #     return QtCore.QPoint(x, y)