# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from brezier import BrezierCurve
from line import Line
from kpt import Keypoint
import numpy as np

def single_pt(landmark137, index, parent, isEye=False):
    pen = QtGui.QPen(QtCore.Qt.cyan)
    pen.setWidthF(0)

    pt = Keypoint(index, landmark137[index], -2, -2, 4, 4, parent)
    pt.setPos(landmark137[index, 0], landmark137[index, 1])
    pt.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
    pt.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
    pt.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
    pt.setPen(pen)
    pt.setBrush(QtCore.Qt.darkMagenta)
    pt.setOpacity(0.5)

    pt.setIsEye(isEye)

    return pt

def brezier_p(landmark137, index, parent):
    pen = QtGui.QPen(QtCore.Qt.cyan)
    pen.setWidthF(0.2)

    pt = Keypoint(index, landmark137[index], -2, -2, 4, 4, parent)
    pt.setPos(landmark137[index, 0], landmark137[index, 1])
    pt.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
    pt.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
    pt.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
    pt.setPen(pen)
    pt.setBrush(QtCore.Qt.yellow)

    return pt

def brezier_c(landmark137, index, parent):
    pen = QtGui.QPen(QtCore.Qt.cyan)
    pen.setWidthF(0.2)

    pt = Keypoint(None, landmark137[index], -2, -2, 4, 4, parent)
    pt.setPos(landmark137[index, 0], landmark137[index, 1])
    pt.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
    pt.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
    pt.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
    pt.setPen(pen)
    pt.setBrush(QtCore.Qt.red)

    return pt

class GroupObject(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        super(GroupObject, self).__init__(*args, **kwargs)

    def show(self, flag):
        for k, v in vars(self).items():
            if isinstance(v, QtWidgets.QGraphicsItem):
                v.setVisible(flag)

    def showControl(self, flag):
        for k, v in vars(self).items():
            if isinstance(v, Keypoint):
                if v.name is None:
                    v.setVisible(flag)

    def showKeypoint(self, flag):
        for k, v in vars(self).items():
            if isinstance(v, Keypoint):
                if v.name is not None:
                    v.setVisible(flag)

class MouthOutterGroupBrezier(GroupObject):
    def __init__(self, landmark137, parent, *args, **kwargs):
        super(MouthOutterGroupBrezier, self).__init__(*args, **kwargs)

        self.p22 = brezier_p(landmark137, 22, parent)
        self.p29 = brezier_p(landmark137, 29, parent)
        self.c23 = brezier_c(landmark137, 23, parent)
        self.c28 = brezier_c(landmark137, 28, parent)
        self.p43 = brezier_p(landmark137, 43, parent)
        self.c47 = brezier_c(landmark137, 47, parent)
        self.c44 = brezier_c(landmark137, 44, parent)
        self.p41 = brezier_p(landmark137, 41, parent)
        self.p36 = brezier_p(landmark137, 36, parent)
        self.c40 = brezier_c(landmark137, 40, parent)
        self.c37 = brezier_c(landmark137, 37, parent)
        self.c35 = brezier_c(landmark137, 35, parent)
        self.c30 = brezier_c(landmark137, 30, parent)
        self.brezier_1 = BrezierCurve(self.p22, self.c23, self.c28, self.p29, 7, parent)
        self.brezier_2 = BrezierCurve(self.p43, self.c44, self.c47, self.p22, 5, parent)
        self.brezier_3 = BrezierCurve(self.p36, self.c37, self.c40, self.p41, 5, parent)
        self.brezier_4 = BrezierCurve(self.p29, self.c30, self.c35, self.p36, 7, parent)

        self.p42 = single_pt(landmark137, 42, parent)
        self.line_1 = Line(self.p42, self.p43, 1, False, parent)
        self.line_2 = Line(self.p41, self.p42, 1, False, parent)

    def getLabel(self):
        res = np.concatenate((
            self.brezier_1.getKeypoints()[:-1],
            self.brezier_4.getKeypoints()[:-1],
            self.brezier_3.getKeypoints(),
            [[self.p42.pos().x(), self.p42.pos().y()]],
            self.brezier_2.getKeypoints()[:-1],
        ), axis=0)
        return res

    def getLabel_1k(self):
        res = np.concatenate((
            self.brezier_1.getKeypoints(42)[:-1],
            self.brezier_4.getKeypoints(42)[:-1],
            self.brezier_3.getKeypoints(30)[:-1],
            self.line_2.getKeypoints(6)[:-1],
            self.line_1.getKeypoints(6)[:-1],
            self.brezier_2.getKeypoints(30)[:-1],
        ), axis=0)
        return res

class MouthInnerGroupBrezier(GroupObject):
    def __init__(self, landmark137, parent, *args, **kwargs):
        super(MouthInnerGroupBrezier, self).__init__(*args, **kwargs)

        self.p48 = brezier_p(landmark137, 48, parent)
        self.p60 = brezier_p(landmark137, 60, parent)
        self.c63 = brezier_c(landmark137, 63, parent)
        self.c61 = brezier_c(landmark137, 61, parent)
        self.p56 = brezier_p(landmark137, 56, parent)
        self.c59 = brezier_c(landmark137, 59, parent)
        self.c57 = brezier_c(landmark137, 57, parent)
        self.p52 = brezier_p(landmark137, 52, parent)
        self.c55 = brezier_c(landmark137, 55, parent)
        self.c53 = brezier_c(landmark137, 53, parent)
        self.c51 = brezier_c(landmark137, 51, parent)
        self.c49 = brezier_c(landmark137, 49, parent)
        self.brezier_5 = BrezierCurve(self.p60, self.c61, self.c63, self.p48, 4, parent)
        self.brezier_6 = BrezierCurve(self.p56, self.c57, self.c59, self.p60, 4, parent)
        self.brezier_7 = BrezierCurve(self.p52, self.c53, self.c55, self.p56, 4, parent)
        self.brezier_8 = BrezierCurve(self.p48, self.c49, self.c51, self.p52, 4, parent)

    def getLabel(self):
        res = np.concatenate((
            self.brezier_8.getKeypoints()[:-1],
            self.brezier_7.getKeypoints()[:-1],
            self.brezier_6.getKeypoints()[:-1],
            self.brezier_5.getKeypoints()[:-1],
        ), axis=0)
        return res

    def getLabel_1k(self):
        res = np.concatenate((
            self.brezier_8.getKeypoints(20)[:-1],
            self.brezier_7.getKeypoints(20)[:-1],
            self.brezier_6.getKeypoints(20)[:-1],
            self.brezier_5.getKeypoints(20)[:-1],
        ), axis=0)
        return res

class NoseGroupBrezier(GroupObject):
    def __init__(self, landmark137, parent, p88, p105, *args, **kwargs):
        super(NoseGroupBrezier, self).__init__(*args, **kwargs)

        self.p64 = brezier_p(landmark137, 64, parent)
        self.p68 = brezier_p(landmark137, 68, parent)
        self.c65 = brezier_c(landmark137, 65, parent)
        self.c67 = brezier_c(landmark137, 67, parent)
        self.p78 = brezier_p(landmark137, 78, parent)
        self.p74 = brezier_p(landmark137, 74, parent)
        self.c77 = brezier_c(landmark137, 77, parent)
        self.c75 = brezier_c(landmark137, 75, parent)
        self.p86 = brezier_p(landmark137, 86, parent)
        self.p83 = brezier_p(landmark137, 83, parent)
        self.p64.setAlongPath(p88, p105)
        self.p78.setAlongPath(p88, p105)

        self.brezier_1 = BrezierCurve(self.p64, self.c65, self.c67, self.p68, 4, parent)
        self.brezier_2 = BrezierCurve(self.p74, self.c75, self.c77, self.p78, 4, parent)

        for pt_index in [82, 81, 80, 79, 69, 70, 71, 72, 73]:
            setattr(self, 'p{}'.format(pt_index), single_pt(landmark137, pt_index, parent))

        self.line_1 = Line(self.p83, self.p86, 3, False, parent)

        self.line_2 = Line(self.p82, self.p81, 0, False, parent)
        self.line_3 = Line(self.p81, self.p80, 0, False, parent)
        self.line_4 = Line(self.p80, self.p79, 0, False, parent)

        self.line_5 = Line(self.p69, self.p70, 0, False, parent)
        self.line_6 = Line(self.p70, self.p71, 0, False, parent)
        self.line_7 = Line(self.p71, self.p72, 0, False, parent)
        self.line_8 = Line(self.p72, self.p73, 0, False, parent)

        self.help1 = Line(p88, p105, 0, True, parent)

    def getLabel(self):
        res = np.concatenate((
            self.brezier_1.getKeypoints(),
            [
                [self.p69.pos().x(), self.p69.pos().y()],
                [self.p70.pos().x(), self.p70.pos().y()],
                [self.p71.pos().x(), self.p71.pos().y()],
                [self.p72.pos().x(), self.p72.pos().y()],
                [self.p73.pos().x(), self.p73.pos().y()],
            ],
            self.brezier_2.getKeypoints(),
            [
                [self.p79.pos().x(), self.p79.pos().y()],
                [self.p80.pos().x(), self.p80.pos().y()],
                [self.p81.pos().x(), self.p81.pos().y()],
                [self.p82.pos().x(), self.p82.pos().y()],
            ],
            self.line_1.getKeypoints(),
        ), axis=0)
        return res

    def getLabel_1k(self):
        res = np.concatenate((
            self.brezier_1.getKeypoints(32),
            [
                [self.p69.pos().x(), self.p69.pos().y()],
                [self.p70.pos().x(), self.p70.pos().y()],
                [self.p71.pos().x(), self.p71.pos().y()],
                [self.p72.pos().x(), self.p72.pos().y()],
                [self.p73.pos().x(), self.p73.pos().y()],
            ],
            self.brezier_2.getKeypoints(32),
            [
                [self.p79.pos().x(), self.p79.pos().y()],
                [self.p80.pos().x(), self.p80.pos().y()],
                [self.p81.pos().x(), self.p81.pos().y()],
                [self.p82.pos().x(), self.p82.pos().y()],
            ],
            self.line_1.getKeypoints(32),
        ), axis=0)
        return res


class LeftEyeGroupBrezier(GroupObject):
    def __init__(self, landmark137, parent, *args, **kwargs):
        super(LeftEyeGroupBrezier, self).__init__(*args, **kwargs)

        self.p96 = brezier_p(landmark137, 96, parent)
        self.p88 = brezier_p(landmark137, 88, parent)
        self.c95 = brezier_c(landmark137, 95, parent)
        self.c89 = brezier_c(landmark137, 89, parent)
        self.c97 = brezier_c(landmark137, 97, parent)
        self.c103 = brezier_c(landmark137, 103, parent)
        self.brezier_1 = BrezierCurve(self.p88, self.c89, self.c95, self.p96, 8, parent)
        self.brezier_2 = BrezierCurve(self.p96, self.c97, self.c103, self.p88, 8, parent)

        self.p87 = single_pt(landmark137, 87, parent, isEye=True)

    def getLabel(self):
        res = np.concatenate((
            [
                [self.p87.pos().x(), self.p87.pos().y()],
            ],
            self.brezier_1.getKeypoints()[:-1],
            self.brezier_2.getKeypoints()[:-1],
        ), axis=0)
        return res

    def getLabel_1k(self):
        res = np.concatenate((
            [
                [self.p87.pos().x(), self.p87.pos().y()],
            ],
            self.brezier_1.getKeypoints(32)[:-1],
            self.brezier_2.getKeypoints(32)[:-1],
        ), axis=0)
        return res

    def getScale(self):
        return self.p87.scale()

    def setScale(self, value):
        self.p87.setScale(value)

class RightEyeGroupBrezier(GroupObject):
    def __init__(self, landmark137, parent, *args, **kwargs):
        super(RightEyeGroupBrezier, self).__init__(*args, **kwargs)

        self.p105 = brezier_p(landmark137, 105, parent)
        self.p113 = brezier_p(landmark137, 113, parent)
        self.c106 = brezier_c(landmark137, 106, parent)
        self.c112 = brezier_c(landmark137, 112, parent)
        self.c120 = brezier_c(landmark137, 120, parent)
        self.c114 = brezier_c(landmark137, 114, parent)
        self.brezier_1 = BrezierCurve(self.p105, self.c106, self.c112, self.p113, 8, parent)
        self.brezier_2 = BrezierCurve(self.p113, self.c114, self.c120, self.p105, 8, parent)

        self.p104 = single_pt(landmark137, 104, parent, isEye=True)

    def getLabel(self):
        res = np.concatenate((
            [
                [self.p104.pos().x(), self.p104.pos().y()],
            ],
            self.brezier_1.getKeypoints()[:-1],
            self.brezier_2.getKeypoints()[:-1],
        ), axis=0)
        return res

    def getLabel_1k(self):
        res = np.concatenate((
            [
                [self.p104.pos().x(), self.p104.pos().y()],
            ],
            self.brezier_1.getKeypoints(32)[:-1],
            self.brezier_2.getKeypoints(32)[:-1],
        ), axis=0)
        return res

    def getScale(self):
        return self.p104.scale()

    def setScale(self, value):
        self.p104.setScale(value)

class LeftEyeBrownGroupBrezier(GroupObject):
    def __init__(self, landmark137, parent, *args, **kwargs):
        super(LeftEyeBrownGroupBrezier, self).__init__(*args, **kwargs)

        self.p129 = brezier_p(landmark137, 129, parent)
        self.p133 = brezier_p(landmark137, 133, parent)
        self.p131 = brezier_p(landmark137, 131, parent)
        self.p135 = brezier_p(landmark137, 135, parent)
        self.c130 = brezier_c(landmark137, 130, parent)
        self.c132 = brezier_c(landmark137, 132, parent)
        self.c136 = brezier_c(landmark137, 136, parent)
        self.c134 = brezier_c(landmark137, 134, parent)
        self.brezier_1 = BrezierCurve(self.p129, self.c130, self.c130, self.p131, 2, parent)
        self.brezier_2 = BrezierCurve(self.p131, self.c132, self.c132, self.p133, 2, parent)
        self.brezier_3 = BrezierCurve(self.p135, self.c136, self.c136, self.p129, 2, parent)
        self.brezier_4 = BrezierCurve(self.p133, self.c134, self.c134, self.p135, 2, parent)

    def getLabel(self):
        res = np.concatenate((
            self.brezier_1.getKeypoints()[:-1],
            self.brezier_2.getKeypoints()[:-1],
            self.brezier_4.getKeypoints()[:-1],
            self.brezier_3.getKeypoints()[:-1],
        ), axis=0)
        return res

    def getLabel_1k(self):
        res = np.concatenate((
            self.brezier_1.getKeypoints(18)[:-1],
            self.brezier_2.getKeypoints(18)[:-1],
            self.brezier_4.getKeypoints(18)[:-1],
            self.brezier_3.getKeypoints(18)[:-1],
        ), axis=0)
        return res

class RightEyeBrownGroupBrezier(GroupObject):
    def __init__(self, landmark137, parent, *args, **kwargs):
        super(RightEyeBrownGroupBrezier, self).__init__(*args, **kwargs)

        self.p121 = brezier_p(landmark137, 121, parent)
        self.p125 = brezier_p(landmark137, 125, parent)
        self.p123 = brezier_p(landmark137, 123, parent)
        self.p127 = brezier_p(landmark137, 127, parent)
        self.c122 = brezier_c(landmark137, 122, parent)
        self.c124 = brezier_c(landmark137, 124, parent)
        self.c128 = brezier_c(landmark137, 128, parent)
        self.c126 = brezier_c(landmark137, 126, parent)
        self.brezier_1 = BrezierCurve(self.p121, self.c122, self.c122, self.p123, 2, parent)
        self.brezier_2 = BrezierCurve(self.p123, self.c124, self.c124, self.p125, 2, parent)
        self.brezier_3 = BrezierCurve(self.p127, self.c128, self.c128, self.p121, 2, parent)
        self.brezier_4 = BrezierCurve(self.p125, self.c126, self.c126, self.p127, 2, parent)

    def getLabel(self):
        res = np.concatenate((
            self.brezier_1.getKeypoints()[:-1],
            self.brezier_2.getKeypoints()[:-1],
            self.brezier_4.getKeypoints()[:-1],
            self.brezier_3.getKeypoints()[:-1],
        ), axis=0)
        return res

    def getLabel_1k(self):
        res = np.concatenate((
            self.brezier_1.getKeypoints(18)[:-1],
            self.brezier_2.getKeypoints(18)[:-1],
            self.brezier_4.getKeypoints(18)[:-1],
            self.brezier_3.getKeypoints(18)[:-1],
        ), axis=0)
        return res

class FaceGroupBrezier(GroupObject):
    def __init__(self, landmark137, parent, *args, **kwargs):
        super(FaceGroupBrezier, self).__init__(*args, **kwargs)

        self.p0 = brezier_p(landmark137, 0, parent)
        self.p18 = brezier_p(landmark137, 18, parent)
        self.c19 = brezier_c(landmark137, 19, parent)
        self.c21 = brezier_c(landmark137, 21, parent)
        self.p4 = brezier_p(landmark137, 4, parent)
        self.c3 = brezier_c(landmark137, 3, parent)
        self.c1 = brezier_c(landmark137, 1, parent)
        self.p14 = brezier_p(landmark137, 14, parent)
        self.p8 = brezier_p(landmark137, 8, parent)
        self.c15 = brezier_c(landmark137, 15, parent)
        self.c7 = brezier_c(landmark137, 7, parent)
        self.c17 = brezier_c(landmark137, 17, parent)
        self.c5 = brezier_c(landmark137, 5, parent)
        self.p11 = brezier_p(landmark137, 11, parent)
        self.c13 = brezier_c(landmark137, 13, parent)
        self.c12 = brezier_c(landmark137, 12, parent)
        self.c10 = brezier_c(landmark137, 10, parent)
        self.c9 = brezier_c(landmark137, 9, parent)
        self.brezier_1 = BrezierCurve(self.p18, self.c19, self.c21, self.p0, 4, parent)
        self.brezier_2 = BrezierCurve(self.p0, self.c1, self.c3, self.p4, 4, parent)
        self.brezier_3 = BrezierCurve(self.p14, self.c15, self.c17, self.p18, 4, parent)
        self.brezier_4 = BrezierCurve(self.p4, self.c5, self.c7, self.p8, 4, parent)
        self.brezier_5 = BrezierCurve(self.p11, self.c12, self.c13, self.p14, 3, parent)
        self.brezier_6 = BrezierCurve(self.p8, self.c9, self.c10, self.p11, 3, parent)

        self.help1 = Line(self.p14, self.p8, 0, True, parent)
        self.help2 = Line(self.p18, self.p4, 0, True, parent)

    def getLabel(self):
        res = np.concatenate((
            self.brezier_2.getKeypoints()[:-1],
            self.brezier_4.getKeypoints()[:-1],
            self.brezier_6.getKeypoints()[:-1],
            self.brezier_5.getKeypoints()[:-1],
            self.brezier_3.getKeypoints()[:-1],
            self.brezier_1.getKeypoints()[:-1],
        ), axis=0)
        return res

    def getLabel_1k(self):
        res = np.concatenate((
            self.brezier_2.getKeypoints(48)[:-1],
            self.brezier_4.getKeypoints(52)[:-1],
            self.brezier_6.getKeypoints(56)[:-1],
            self.brezier_5.getKeypoints(56)[:-1],
            self.brezier_3.getKeypoints(52)[:-1],
            self.brezier_1.getKeypoints(48)[:-1],
        ), axis=0)
        return res

class FaceFinal(object):
    def __init__(self, landmark137, eye_scale, parent):
        self.aaa_1 = MouthOutterGroupBrezier(landmark137, parent)
        self.aaa_2 = MouthInnerGroupBrezier(landmark137, parent)
        self.ccc = LeftEyeGroupBrezier(landmark137, parent)
        self.ddd = RightEyeGroupBrezier(landmark137, parent)
        self.bbb = NoseGroupBrezier(landmark137, parent, self.ccc.p88, self.ddd.p105)
        self.eee = LeftEyeBrownGroupBrezier(landmark137, parent)
        self.fff = RightEyeBrownGroupBrezier(landmark137, parent)
        self.ggg = FaceGroupBrezier(landmark137, parent)

        self.ccc.setScale(eye_scale[0])
        self.ddd.setScale(eye_scale[1])

    def showControl(self, flag):
        self.aaa_1.showControl(flag)
        self.aaa_2.showControl(flag)
        self.bbb.showControl(flag)
        self.ccc.showControl(flag)
        self.ddd.showControl(flag)
        self.eee.showControl(flag)
        self.fff.showControl(flag)
        self.ggg.showControl(flag)

    def showKeypoint(self, flag):
        self.aaa_1.showKeypoint(flag)
        self.aaa_2.showKeypoint(flag)
        self.bbb.showKeypoint(flag)
        self.ccc.showKeypoint(flag)
        self.ddd.showKeypoint(flag)
        self.eee.showKeypoint(flag)
        self.fff.showKeypoint(flag)
        self.ggg.showKeypoint(flag)

    def showContour(self, flag):
        self.ggg.show(flag)

    def showLeftEyeBrown(self, flag):
        self.eee.show(flag)

    def showRightEyeBrown(self, flag):
        self.fff.show(flag)

    def showLeftEye(self, flag):
        self.ccc.show(flag)

    def showRightEye(self, flag):
        self.ddd.show(flag)

    def showNose(self, flag):
        self.bbb.show(flag)

    def showMouthOutter(self, flag):
        self.aaa_1.show(flag)

    def showMouthInner(self, flag):
        self.aaa_2.show(flag)

    def getLabel_137(self):
        res = np.concatenate((
            self.ggg.getLabel(),
            self.aaa_1.getLabel(),
            self.aaa_2.getLabel(),
            self.bbb.getLabel(),
            self.ccc.getLabel(),
            self.ddd.getLabel(),
            self.fff.getLabel(),
            self.eee.getLabel(),
        ), axis=0)
        return res

    def getLabel_1k(self):
        res = np.concatenate((
            self.ggg.getLabel_1k(),
            self.aaa_1.getLabel_1k(),
            self.aaa_2.getLabel_1k(),
            self.bbb.getLabel_1k(),
            self.ccc.getLabel_1k(),
            self.ddd.getLabel_1k(),
            self.fff.getLabel_1k(),
            self.eee.getLabel_1k(),
        ), axis=0)
        return res

    def getEyeScale(self):
        return [self.ccc.getScale(), self.ddd.getScale()]

