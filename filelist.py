# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from typing import Union
import numpy as np
import cv2
import re
import os

class FileList(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(FileList, self).__init__(*args, **kwargs)

    def loadDir(self):
        print('loadDir')
        self.clear()
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open a folder', './')
        pattern = re.compile(r'((.*[jJ][pP][gG]$)|(.*[pP][nN][gG]$))')
        self.all_data_dict = dict()
        for dirpath, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                match = pattern.match(filename)
                if match:
                    img_file = os.path.join(dirpath, filename)
                    label_file = os.path.join(dirpath, os.path.splitext(filename)[0] + '_extract_137.pt')
                    if os.path.exists(img_file) and os.path.exists(label_file):
                        self.all_data_dict[img_file] = label_file
                        self.addItem(img_file)
