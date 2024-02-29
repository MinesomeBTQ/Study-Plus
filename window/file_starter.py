import os

from PyQt5 import Qt
from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui
import json
import shutil

from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class file_starter(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(file_starter, self).__init__()
        self.bg_self = None
        self.setWindowTitle('Study Plus - 文件定时启动')
        self.setWindowIcon(gui.QIcon('data/images/favicon.ico'))
        self.loadStyle()

        self.txt_1 = widgets.QLabel(self)
        self.txt_2 = widgets.QLabel(self)
        self.txt_3 = widgets.QLabel(self)
        self.on = widgets.QRadioButton(self)
        self.off = widgets.QRadioButton(self)
        self.edit = widgets.QLineEdit(self)
        self.edit_time = widgets.QTimeEdit(self)

        self.mainWindow = mainWindow  # 主窗口类
        self.w = 400
        self.h = 250
        self.data = json.loads(read(r'data\file_starter.json'))

        self.screen().logicalDotsPerInchChanged.connect(self.setupUI)
        self.resizeEvent = self.setupUI
        self.initUI()
        self.setupUI()

    def loadStyle(self):
        global data
        data = json.loads(read(r'data\mainWindow.json'))
        self.setStyleSheet(read(r'data\static\style.qss').replace(
            '@BACKGROUND-IMAGE', data['background-image']
        ).replace(
            '@MAIN-COLOR', data['main-color']
        ).replace(
            '@WH', str(int(widgets.QDesktopWidget().screenGeometry().width() * 15 / 1920))+'px'
        ))

    def initUI(self):
        self.txt_1.setText('启用文件定时启动')
        self.on.setText('启用')
        self.off.setText('禁用')
        self.txt_2.setText('文件路径')
        self.edit.setText(self.data['file'])
        self.txt_3.setText('启动时间')
        self.edit_time.setDisplayFormat("hh:mm:ss")
        self.edit_time.setTime(core.QTime(self.data['time'][0], self.data['time'][1], self.data['time'][2]))

        self.on.setChecked(self.data['func'])
        self.off.setChecked(not self.data['func'])

        def check():
            if self.on.isChecked():
                self.data['func'] = True
            else:
                self.data['func'] = False
            write(r'data\file_starter.json', json.dumps(self.data))

        self.on.clicked.connect(check)
        self.off.clicked.connect(check)

        def set_file(evt):
            type(evt)
            path = widgets.QFileDialog.getOpenFileName(self, '选择文件路径', None, '所有文件(*.*)')[0]
            if path:
                self.edit.setText(path)
                self.data['file'] = path
                write(r'data\file_starter.json', json.dumps(self.data))

        self.edit.mousePressEvent = set_file

        def set_time():
            self.data['time'] = [self.edit_time.time().hour(), self.edit_time.time().minute(),
                                 self.edit_time.time().second()]
            write(r'data\file_starter.json', json.dumps(self.data))

        self.edit_time.timeChanged.connect(set_time)

    def setupUI(self, evt=None):
        screen = widgets.QDesktopWidget().screenGeometry()
        w, h = screen.width() * self.w / 1920, screen.height() * self.h / 1080
        if type(evt) is float or evt is None:
            self.setFixedSize(int(w), int(h))
        dpi = self.screen().logicalDotsPerInch() / 96

        def font(size_):
            f = gui.QFont()
            f.setPointSizeF((size_ * w / (self.w * dpi) + size_ * h / (self.h * dpi)) / 2)
            return f

        w, h = self.width(), self.height()
        size = lambda x1, y1, x2, y2: core.QRect(int(x1 * w / self.w), int(y1 * h / self.h), int(x2 * w / self.w),
                                                 int(y2 * h / self.h))

        self.txt_1.setGeometry(size(25, 25, 350, 25))
        self.on.setGeometry(size(25, 50, 175, 25))
        self.off.setGeometry(size(200, 50, 175, 25))
        self.txt_2.setGeometry(size(25, 100, 350, 25))
        self.edit.setGeometry(size(25, 125, 350, 25))
        self.txt_3.setGeometry(size(25, 175, 350, 25))
        self.edit_time.setGeometry(size(25, 200, 350, 25))

        self.txt_1.setFont(font(10))
        self.txt_2.setFont(font(10))
        self.txt_3.setFont(font(10))
        self.on.setFont(font(10))
        self.off.setFont(font(10))
        self.edit.setFont(font(9))

    def closeEvent(self, evt):
        if self.mainWindow.isVisible():
            evt.accept()
        else:
            self.hide()
            evt.ignore()
