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
import pickle
from group_brezier import *

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

        self.img_path = None
        self.label = None

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
                    if child.isSelected() and isinstance(child, Keypoint):
                            if child.setPos(child.pos().x(), child.pos().y()):
                                current_doing.append(child)
                if len(current_doing) > 0:
                    self.change_history.append(current_doing)
                    # save npy
                    face_label_path = os.path.splitext(self.img_path)[0] + '.npy'
                    np.save(face_label_path, self.label)
        elif event.button() == QtCore.Qt.RightButton:
            print('release right button')

    def mouseMoveEvent(self, event):
        super(Canvas, self).mouseMoveEvent(event)
        # child_has_selected_and_move = False
        # if self.item is not None and self.mouse_left_press:
        #     for child in self.item.childItems():
        #         if child.isSelected():
        #             child_has_selected_and_move = True
        #             break
        # if child_has_selected_and_move:
        #     # update line
        #     for line in self.all_lines:
        #         self.tmp_scene.removeItem(line)
        #     self.updateLines()
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
                    if isinstance(child, Keypoint):
                        child.redoPos()
        elif event.key() == QtCore.Qt.Key_Shift:
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)
        elif event.key() == QtCore.Qt.Key_A:
            if self.item is not None:
                pos = QtCore.QPointF(0, 0)
                count = 0
                for child in self.item.childItems():
                    if child.isSelected() and isinstance(child, Keypoint):
                        pos += child.pos()
                        count += 1
                current_doing = []
                pos = pos / count
                for child in self.item.childItems():
                    if child.isSelected() and isinstance(child, Keypoint):
                        if child.setPos(pos):
                            current_doing.append(child)
                if len(current_doing) > 0:
                    self.change_history.append(current_doing)

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
        self.img_path = item.text()
        label_path = os.path.splitext(self.img_path)[0] + '_extract_137.pt'
        face_label_path = os.path.splitext(self.img_path)[0] + '.npy'

        # open image
        if self.item is not None:
            self.tmp_scene.removeItem(self.item)
        bg_pixel = QtGui.QPixmap(self.img_path)
        self.item = QtWidgets.QGraphicsPixmapItem(bg_pixel)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.tmp_scene.addItem(self.item)
        self.tmp_scene.setSceneRect(0, 0, bg_pixel.width(), bg_pixel.height())

        if os.path.exists(face_label_path):
            self.label = np.load(face_label_path)
        else:
            self.label = np.loadtxt(label_path, skiprows=1, delimiter=' ')
        self.face_label = FaceFinal(self.label, self.item)
