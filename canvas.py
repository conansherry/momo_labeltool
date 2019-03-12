# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

from typing import Union
import numpy as np
import cv2
import re
import os
from kpt import Keypoint

class Canvas(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)
        self.painter = QtGui.QPainter()
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tmp_scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.tmp_scene)

        self.item = None

        self.change_history = []

        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

        self.mouse_left_press = False

        print('Canvas')

    def mousePressEvent(self, event):
        super(Canvas, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            print('press left button')
            self.mouse_left_press = True
        elif event.button() == QtCore.Qt.RightButton:
            print('press right button')

    def mouseReleaseEvent(self, event):
        super(Canvas, self).mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            print('release left button')
            self.mouse_left_press = False
            if self.item is not None:
                current_doing = []
                for child in self.item.childItems():
                    if child.isSelected():
                        if child.setPos(child.pos().x(), child.pos().y()):
                            current_doing.append(child)
                        child.debug()
                if len(current_doing) > 0:
                    self.change_history.append(current_doing)
        elif event.button() == QtCore.Qt.RightButton:
            print('release right button')

    def mouseMoveEvent(self, event):
        super(Canvas, self).mouseMoveEvent(event)
        child_has_selected_and_move = False
        if self.item is not None and self.mouse_left_press:
            for child in self.item.childItems():
                if child.isSelected():
                    child_has_selected_and_move = True
                    break
        if child_has_selected_and_move:
            # update line
            for line in self.all_lines:
                self.tmp_scene.removeItem(line)
            self.updateLines()
        # pos = event.pos()
        # print('item scene pos', self.item.scenePos().x(), self.item.scenePos().y())
        # print('x y', self.item.x(), self.item.y())

    def keyPressEvent(self, event):
        super(Canvas, self).keyPressEvent(event)
        key = event.key()
        print(key)
        if event.key() == (QtCore.Qt.Key_Control and QtCore.Qt.Key_Z):
            if len(self.change_history) > 0:
                last_changed_item = self.change_history.pop()
                for child in last_changed_item:
                    child.redoPos()
                # update line
                for line in self.all_lines:
                    self.tmp_scene.removeItem(line)
                self.updateLines()
        elif event.key() == QtCore.Qt.Key_Shift:
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Shift:
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)

    def wheelEvent(self, event):
        if self.item is not None:
            delta = event.angleDelta()
            pos = event.pos()
            pos_at_item = self.item.mapFromScene(self.mapToScene(pos))
            if event.modifiers() == QtCore.Qt.AltModifier:
                if delta.x() < 0:
                    M = cv2.getRotationMatrix2D((pos_at_item.x(), pos_at_item.y()), 0, 1/1.3)
                else:
                    M = cv2.getRotationMatrix2D((pos_at_item.x(), pos_at_item.y()), 0, 1.3)
                M = M.transpose()
                qM = QtGui.QTransform(M[0, 0], M[0, 1], 0, M[1, 0], M[1, 1], 0, M[2, 0], M[2, 1], 1)
                self.item.setTransform(qM, True)
            else:
                super(Canvas, self).wheelEvent(event)
        else:
            super(Canvas, self).wheelEvent(event)

    @pyqtSlot(QtWidgets.QListWidgetItem, name='openItem')
    def openItem(self, item):
        img_path = item.text()
        label_path = os.path.splitext(img_path)[0] + '_extract_137.pt'

        # open image
        if self.item is not None:
            self.tmp_scene.removeItem(self.item)
        bg_pixel = QtGui.QPixmap(img_path)
        self.item = QtWidgets.QGraphicsPixmapItem(bg_pixel)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.tmp_scene.addItem(self.item)
        self.tmp_scene.setSceneRect(0, 0, bg_pixel.width(), bg_pixel.height())

        # open label
        self.all_keypoints = []
        label = np.loadtxt(label_path, skiprows=1, delimiter=' ')
        anchor_index = [22, 48, 42, 60, 52, 29, 56, 36]
        for ix, pt in enumerate(label):
            center_x = pt[0]
            center_y = pt[1]
            radius = 1
            tmp = Keypoint('keypoint_{}'.format(ix), self.item)
            tmp.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
            tmp.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
            tmp.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
            # tmp.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
            tmp.setPos(center_x, center_y)
            tmp.setRect(0 - radius, 0 - radius, 2 * radius, 2 * radius)
            if ix in anchor_index:
                pen = QtGui.QPen(QtGui.QColor(0, 0, 255))
                pen.setWidthF(0.2)
                tmp.setPen(pen)
                tmp.setBrush(QtCore.Qt.darkBlue)
            else:
                pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
                pen.setWidthF(0.2)
                tmp.setPen(pen)
                tmp.setBrush(QtCore.Qt.cyan)
            self.all_keypoints.append(tmp)

        # update line
        self.updateLines()

    def updateLines(self):
        self.all_lines = []
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        pen.setWidthF(0.5)
        for i in range(0, 21):
            tmp = QtWidgets.QGraphicsLineItem(self.item)
            tmp.setLine(QtCore.QLineF(self.all_keypoints[i].pos(), self.all_keypoints[i + 1].pos()))
            tmp.setZValue(-1)
            tmp.setPen(pen)
            self.all_lines.append(tmp)
        tmp = QtWidgets.QGraphicsLineItem(self.item)
        tmp.setLine(QtCore.QLineF(self.all_keypoints[21].pos(), self.all_keypoints[0].pos()))
        tmp.setZValue(-1)
        tmp.setPen(pen)
        self.all_lines.append(tmp)
        for i in range(129, 136):
            tmp = QtWidgets.QGraphicsLineItem(self.item)
            tmp.setLine(QtCore.QLineF(self.all_keypoints[i].pos(), self.all_keypoints[i + 1].pos()))
            tmp.setZValue(-1)
            tmp.setPen(pen)
            self.all_lines.append(tmp)
        tmp = QtWidgets.QGraphicsLineItem(self.item)
        tmp.setLine(QtCore.QLineF(self.all_keypoints[136].pos(), self.all_keypoints[129].pos()))
        tmp.setZValue(-1)
        tmp.setPen(pen)
        self.all_lines.append(tmp)
        for i in range(121, 128):
            tmp = QtWidgets.QGraphicsLineItem(self.item)
            tmp.setLine(QtCore.QLineF(self.all_keypoints[i].pos(), self.all_keypoints[i + 1].pos()))
            tmp.setZValue(-1)
            tmp.setPen(pen)
            self.all_lines.append(tmp)
        tmp = QtWidgets.QGraphicsLineItem(self.item)
        tmp.setLine(QtCore.QLineF(self.all_keypoints[128].pos(), self.all_keypoints[121].pos()))
        tmp.setZValue(-1)
        tmp.setPen(pen)
        self.all_lines.append(tmp)
        for i in range(88, 103):
            tmp = QtWidgets.QGraphicsLineItem(self.item)
            tmp.setLine(QtCore.QLineF(self.all_keypoints[i].pos(), self.all_keypoints[i + 1].pos()))
            tmp.setZValue(-1)
            tmp.setPen(pen)
            self.all_lines.append(tmp)
        tmp = QtWidgets.QGraphicsLineItem(self.item)
        tmp.setLine(QtCore.QLineF(self.all_keypoints[103].pos(), self.all_keypoints[88].pos()))
        tmp.setZValue(-1)
        tmp.setPen(pen)
        self.all_lines.append(tmp)
        for i in range(105, 120):
            tmp = QtWidgets.QGraphicsLineItem(self.item)
            tmp.setLine(QtCore.QLineF(self.all_keypoints[i].pos(), self.all_keypoints[i + 1].pos()))
            tmp.setZValue(-1)
            tmp.setPen(pen)
            self.all_lines.append(tmp)
        tmp = QtWidgets.QGraphicsLineItem(self.item)
        tmp.setLine(QtCore.QLineF(self.all_keypoints[120].pos(), self.all_keypoints[105].pos()))
        tmp.setZValue(-1)
        tmp.setPen(pen)
        self.all_lines.append(tmp)
        for i in range(64, 78):
            tmp = QtWidgets.QGraphicsLineItem(self.item)
            tmp.setLine(QtCore.QLineF(self.all_keypoints[i].pos(), self.all_keypoints[i + 1].pos()))
            tmp.setZValue(-1)
            tmp.setPen(pen)
            self.all_lines.append(tmp)
        for i in range(83, 86):
            tmp = QtWidgets.QGraphicsLineItem(self.item)
            tmp.setLine(QtCore.QLineF(self.all_keypoints[i].pos(), self.all_keypoints[i + 1].pos()))
            tmp.setZValue(-1)
            tmp.setPen(pen)
            self.all_lines.append(tmp)
        tmp = QtWidgets.QGraphicsLineItem(self.item)
        tmp.setLine(QtCore.QLineF(self.all_keypoints[81].pos(), self.all_keypoints[82].pos()))
        tmp.setZValue(-1)
        tmp.setPen(pen)
        self.all_lines.append(tmp)
        tmp = QtWidgets.QGraphicsLineItem(self.item)
        tmp.setLine(QtCore.QLineF(self.all_keypoints[79].pos(), self.all_keypoints[80].pos()))
        tmp.setZValue(-1)
        tmp.setPen(pen)
        self.all_lines.append(tmp)
        for i in range(22, 47):
            tmp = QtWidgets.QGraphicsLineItem(self.item)
            tmp.setLine(QtCore.QLineF(self.all_keypoints[i].pos(), self.all_keypoints[i + 1].pos()))
            tmp.setZValue(-1)
            tmp.setPen(pen)
            self.all_lines.append(tmp)
        tmp = QtWidgets.QGraphicsLineItem(self.item)
        tmp.setLine(QtCore.QLineF(self.all_keypoints[47].pos(), self.all_keypoints[22].pos()))
        tmp.setZValue(-1)
        tmp.setPen(pen)
        self.all_lines.append(tmp)
        for i in range(48, 63):
            tmp = QtWidgets.QGraphicsLineItem(self.item)
            tmp.setLine(QtCore.QLineF(self.all_keypoints[i].pos(), self.all_keypoints[i + 1].pos()))
            tmp.setZValue(-1)
            tmp.setPen(pen)
            self.all_lines.append(tmp)
        tmp = QtWidgets.QGraphicsLineItem(self.item)
        tmp.setLine(QtCore.QLineF(self.all_keypoints[63].pos(), self.all_keypoints[48].pos()))
        tmp.setZValue(-1)
        tmp.setPen(pen)
        self.all_lines.append(tmp)
