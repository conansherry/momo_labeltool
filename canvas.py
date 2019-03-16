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
                self.save()
                self.item.update()
        elif event.button() == QtCore.Qt.RightButton:
            print('release right button')

    def mouseMoveEvent(self, event):
        super(Canvas, self).mouseMoveEvent(event)
        if self.item is not None:
            self.item.update()

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
                self.save()
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
                    self.save()
        # elif event.key() == QtCore.Qt.Key_S:
        #     if self.item is not None:
        #         for child in self.item.childItems():
        #             if isinstance(child, Keypoint):
        #                 child.showName(not child.show_name)
        #             # child.update()
        #         self.item.update()

    def keyReleaseEvent(self, event):
        super(Canvas, self).keyReleaseEvent(event)

    def wheelEvent(self, event):
        if self.item is not None:
            delta = event.angleDelta()
            pos = event.pos()
            pos_at_item = self.item.mapFromScene(self.mapToScene(pos))
            if event.modifiers() == QtCore.Qt.AltModifier:
                if delta.x() < 0:
                    M = cv2.getRotationMatrix2D((pos_at_item.x(), pos_at_item.y()), 0, 1/1.3)
                    self.item.scale_flag *= 1 / 1.3
                else:
                    M = cv2.getRotationMatrix2D((pos_at_item.x(), pos_at_item.y()), 0, 1.3)
                    self.item.scale_flag *= 1.3
                M = M.transpose()
                qM = QtGui.QTransform(M[0, 0], M[0, 1], 0, M[1, 0], M[1, 1], 0, M[2, 0], M[2, 1], 1)
                self.item.setTransform(qM, True)
            else:
                super(Canvas, self).wheelEvent(event)
        else:
            super(Canvas, self).wheelEvent(event)

    @pyqtSlot(QtWidgets.QListWidgetItem, QtWidgets.QListWidgetItem, name='openItem')
    def openItem(self, item, item_previous):
        self.img_path = item.text()
        label_path = os.path.splitext(self.img_path)[0] + '_extract_137.pt'
        face_label_path = os.path.splitext(self.img_path)[0] + '.npy'

        # open image
        if self.item is not None:
            self.tmp_scene.removeItem(self.item)
        bg_pixel = QtGui.QPixmap(self.img_path)
        self.item = QtWidgets.QGraphicsPixmapItem(bg_pixel)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        self.item.scale_flag = 1.0
        self.tmp_scene.addItem(self.item)
        self.tmp_scene.setSceneRect(0, 0, bg_pixel.width(), bg_pixel.height())

        if os.path.exists(face_label_path):
            self.label = np.load(face_label_path)
        else:
            self.label = np.loadtxt(label_path, skiprows=1, delimiter=' ')
        self.face_label = FaceFinal(self.label, self.item)

    @pyqtSlot(int, name='showName')
    def showName(self, state):
        if self.item is not None:
            for child in self.item.childItems():
                if isinstance(child, Keypoint):
                    child.showName(bool(state))
                # child.update()
            self.item.update()

    @pyqtSlot(int, name='fixItem')
    def fixItem(self, state):
        if self.item is not None:
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, not bool(state))
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, not bool(state))
            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, not bool(state))

    @pyqtSlot(int, name='showControl')
    def showControl(self, state):
        if self.item is not None:
            self.face_label.showControl(bool(state))

    @pyqtSlot(int, name='showKeypoint')
    def showKeypoint(self, state):
        if self.item is not None:
            self.face_label.showKeypoint(bool(state))

    @pyqtSlot(int, name='showContour')
    def showContour(self, state):
        if self.item is not None:
            self.face_label.showContour(bool(state))

    @pyqtSlot(int, name='showLeftEyeBrown')
    def showLeftEyeBrown(self, state):
        if self.item is not None:
            self.face_label.showLeftEyeBrown(bool(state))

    @pyqtSlot(int, name='showRightEyeBrown')
    def showRightEyeBrown(self, state):
        if self.item is not None:
            self.face_label.showRightEyeBrown(bool(state))

    @pyqtSlot(int, name='showLeftEye')
    def showLeftEye(self, state):
        if self.item is not None:
            self.face_label.showLeftEye(bool(state))

    @pyqtSlot(int, name='showRightEye')
    def showRightEye(self, state):
        if self.item is not None:
            self.face_label.showRightEye(bool(state))

    @pyqtSlot(int, name='showNose')
    def showNose(self, state):
        if self.item is not None:
            self.face_label.showNose(bool(state))

    @pyqtSlot(int, name='showMouthOutter')
    def showMouthOutter(self, state):
        if self.item is not None:
            self.face_label.showMouthOutter(bool(state))

    @pyqtSlot(int, name='showMouthInner')
    def showMouthInner(self, state):
        if self.item is not None:
            self.face_label.showMouthInner(bool(state))

    def save(self):
        print('save npy')
        face_label_path = os.path.splitext(self.img_path)[0] + '.npy'
        np.save(face_label_path, self.label)
