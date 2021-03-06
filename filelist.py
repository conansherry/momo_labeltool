# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from typing import Union
import numpy as np
import cv2
import re
import os
import pickle
import shutil
from tqdm import tqdm
import json
from group_brezier import *

class FileList(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(FileList, self).__init__(*args, **kwargs)

    def loadDir(self):
        print('loadDir')
        self.clear()
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open a folder', './')
        pattern = re.compile(r'((.*[jJ][pP][gG]$)|(.*[pP][nN][gG]$))')
        for dirpath, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                match = pattern.match(filename)
                if match:
                    img_file = os.path.join(dirpath, filename)
                    if os.path.exists(img_file):
                        self.addItem(img_file)

    def convertAll(self):
        show_pts = False
        dst_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Save folder', './')
        if show_pts:
            dst_show_dir = os.path.join(dst_dir, 'show')
            if not os.path.exists(dst_show_dir):
                os.makedirs(dst_show_dir)

        all_count = self.count()
        for i in tqdm(range(all_count)):
            item = self.item(i)

            try:
                img_path = item.text()
                label_path = os.path.splitext(img_path)[0] + '.pt137'
                face_label_path = os.path.splitext(img_path)[0] + '.npy'
                pickle_path = os.path.splitext(img_path)[0] + '.pickle'

                bg_pixel = QtGui.QPixmap(img_path)
                item = QtWidgets.QGraphicsPixmapItem(bg_pixel)
                item.scale_flag = 1.0

                if os.path.exists(face_label_path) and not os.path.exists(pickle_path):
                    label = np.load(face_label_path)
                    pickle_data = ['v0', label, [1, 1]]
                    with open(pickle_path, 'wb') as outfile:
                        pickle.dump(pickle_data, outfile)
                elif os.path.exists(pickle_path):
                    with open(pickle_path, 'rb') as outfile:
                        pickle_data = pickle.load(outfile)
                        label = pickle_data[1]
                else:
                    label = np.loadtxt(label_path, skiprows=1, delimiter=' ')
                    pickle_data = ['v0', label, [1, 1]]

                face_label = FaceFinal(label, pickle_data[2], item)

                base_name = os.path.basename(img_path)
                save_jpg = os.path.join(dst_dir, base_name)
                save_pts = os.path.join(dst_dir, base_name.replace('.jpg', '.pt137'))

                tmp_label = face_label.getLabel_137()

                shutil.copy2(img_path, save_jpg)
                np.savetxt(save_pts, tmp_label, fmt='%f', delimiter=' ')

                if show_pts:
                    save_jpg_show = os.path.join(dst_show_dir, base_name)
                    tmp_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
                    tmp_label = face_label.getLabel_137().astype(np.int32)
                    for ix, pt in enumerate(tmp_label):
                        cv2.putText(tmp_img, str(ix), (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
                        cv2.circle(tmp_img, (pt[0], pt[1]), 1, (0, 255, 0), 1)

                    cv2.imwrite(save_jpg_show, tmp_img)
            except:
                print('load {} error'.format(img_path))
                assert False

            # cv2.imshow('tmp_img', tmp_img)
            # cv2.waitKey()

    def convertAll_1k(self):
        show_pts = False
        dst_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Save folder', './')
        if show_pts:
            dst_show_dir = os.path.join(dst_dir, 'show')
            if not os.path.exists(dst_show_dir):
                os.makedirs(dst_show_dir)

        all_count = self.count()
        for i in tqdm(range(all_count)):
            item = self.item(i)

            try:
                img_path = item.text()
                label_path = os.path.splitext(img_path)[0] + '.pt137'
                face_label_path = os.path.splitext(img_path)[0] + '.npy'
                pickle_path = os.path.splitext(img_path)[0] + '.pickle'

                bg_pixel = QtGui.QPixmap(img_path)
                item = QtWidgets.QGraphicsPixmapItem(bg_pixel)
                item.scale_flag = 1.0

                if os.path.exists(face_label_path) and not os.path.exists(pickle_path):
                    label = np.load(face_label_path)
                    pickle_data = ['v0', label, [1, 1]]
                    with open(pickle_path, 'wb') as outfile:
                        pickle.dump(pickle_data, outfile)
                elif os.path.exists(pickle_path):
                    with open(pickle_path, 'rb') as outfile:
                        pickle_data = pickle.load(outfile)
                        label = pickle_data[1]
                else:
                    label = np.loadtxt(label_path, skiprows=1, delimiter=' ')
                    pickle_data = ['v0', label, [1, 1]]

                face_label = FaceFinal(label, pickle_data[2], item)

                base_name = os.path.basename(img_path)
                save_jpg = os.path.join(dst_dir, base_name)
                save_pts = os.path.join(dst_dir, base_name.replace('.jpg', '.pt1000'))

                tmp_label = face_label.getLabel_1k()

                shutil.copy2(img_path, save_jpg)
                np.savetxt(save_pts, tmp_label, fmt='%f', delimiter=' ')

                if show_pts:
                    save_jpg_show = os.path.join(dst_show_dir, base_name)
                    tmp_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
                    tmp_label = face_label.getLabel_1k().astype(np.int32)
                    for ix, pt in enumerate(tmp_label):
                        # cv2.putText(tmp_img, str(ix), (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
                        cv2.circle(tmp_img, (pt[0], pt[1]), 1, (0, 255, 0), 1)

                    cv2.imwrite(save_jpg_show, tmp_img)
            except:
                print('load {} error'.format(img_path))
                assert False

    def convertAll_brezier(self):
        show_pts = True
        dst_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Save folder', './')
        if show_pts:
            dst_show_dir = os.path.join(dst_dir, 'show')
            if not os.path.exists(dst_show_dir):
                os.makedirs(dst_show_dir)

        all_count = self.count()
        for i in tqdm(range(all_count)):
            item = self.item(i)

            try:
                img_path = item.text()
                label_path = os.path.splitext(img_path)[0] + '.pt137'
                face_label_path = os.path.splitext(img_path)[0] + '.npy'
                pickle_path = os.path.splitext(img_path)[0] + '.pickle'

                bg_pixel = QtGui.QPixmap(img_path)
                item = QtWidgets.QGraphicsPixmapItem(bg_pixel)
                item.scale_flag = 1.0

                if os.path.exists(face_label_path) and not os.path.exists(pickle_path):
                    label = np.load(face_label_path)
                    pickle_data = ['v0', label, [1, 1]]
                    with open(pickle_path, 'wb') as outfile:
                        pickle.dump(pickle_data, outfile)
                elif os.path.exists(pickle_path):
                    with open(pickle_path, 'rb') as outfile:
                        pickle_data = pickle.load(outfile)
                        label = pickle_data[1]
                else:
                    label = np.loadtxt(label_path, skiprows=1, delimiter=' ')
                    pickle_data = ['v0', label, [1, 1]]

                face_label = FaceFinal(label, pickle_data[2], item)

                base_name = os.path.basename(img_path)
                save_jpg = os.path.join(dst_dir, base_name)
                save_pts = os.path.join(dst_dir, base_name.replace('.jpg', '.json'))

                key_pts, ctrl_pts = face_label.getBrezierLabel()

                shutil.copy2(img_path, save_jpg)
                save_data = dict()
                save_data['key_pts'] = key_pts.tolist()
                save_data['ctrl_pts'] = ctrl_pts.tolist()
                json.dump(save_data, open(save_pts, 'w'))

                if show_pts:
                    save_jpg_show = os.path.join(dst_show_dir, base_name)
                    tmp_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)

                    tmp_label = (key_pts * 1).astype(np.int32)
                    for ix, pt in enumerate(tmp_label):
                        cv2.putText(tmp_img, str(ix), (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
                        cv2.circle(tmp_img, (pt[0], pt[1]), 1, (0, 255, 0), 1)

                    tmp_label = (ctrl_pts * 1).astype(np.int32)
                    for ix, pt in enumerate(tmp_label):
                        cv2.putText(tmp_img, str(ix), (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
                        cv2.circle(tmp_img, (pt[0], pt[1]), 1, (0, 0, 255), 1)

                    cv2.imwrite(save_jpg_show, tmp_img)
            except:
                print('load {} error'.format(img_path))
                assert False

        # self.img_path = item.text()
        # label_path = os.path.splitext(self.img_path)[0] + '.pt137'
        # face_label_path = os.path.splitext(self.img_path)[0] + '.npy'
        # pickle_path = os.path.splitext(self.img_path)[0] + '.pickle'
        #
        # # open image
        # if self.item is not None:
        #     self.tmp_scene.removeItem(self.item)
        #     self.item = None
        #     self.resetCheck()
        # bg_pixel = QtGui.QPixmap(self.img_path)
        # self.item = QtWidgets.QGraphicsPixmapItem(bg_pixel)
        # self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        # self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        # self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        # self.item.scale_flag = 1.0
        # self.tmp_scene.addItem(self.item)
        # self.tmp_scene.setSceneRect(0, 0, bg_pixel.width(), bg_pixel.height())
        #
        # if os.path.exists(face_label_path) and not os.path.exists(pickle_path):
        #     self.label = np.load(face_label_path)
        #     self.pickle = ['v0', self.label, [1, 1]]
        #     with open(pickle_path, 'wb') as outfile:
        #         pickle.dump(self.pickle, outfile)
        # elif os.path.exists(pickle_path):
        #     with open(pickle_path, 'rb') as outfile:
        #         self.pickle = pickle.load(outfile)
        #         self.label = self.pickle[1]
        # else:
        #     self.label = np.loadtxt(label_path, skiprows=1, delimiter=' ')
        #     self.pickle = ['v0', self.label, [1, 1]]
        #
        # self.face_label = FaceFinal(self.label, self.pickle[2], self.item)
