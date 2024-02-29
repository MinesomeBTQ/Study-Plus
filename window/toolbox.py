import os

from PyQt5 import Qt
from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui
import json
import shutil
import webbrowser
import time as _time

from PyQt5.QtWidgets import QWidget

from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class toolbox(widgets.QWidget):
    def __init__(self, mainWindow):
        super(toolbox, self).__init__()
        self._startPos = None
        self._isTracking = None
        self._endPos = None
        self.bg_self = None
        self.setWindowTitle('Study Plus')
        self.loadStyle()

        self.main_bg = QWidget(self)
        self.main_bg.setObjectName('toolbox-bg')
        op = widgets.QGraphicsOpacityEffect(self)
        op.setOpacity(data['opacity'] / 100)
        self.main_bg.setGraphicsEffect(op)
        self.main = QWidget(self)
        self.main.setObjectName('toolbox')
        self.main.setCursor(Qt.Qt.PointingHandCursor)
        self.text = widgets.QLabel(self.main)

        self.mainWindow = mainWindow
        self.move(int(widgets.QDesktopWidget().screenGeometry().width() * 100 / 1920),
                  int(widgets.QDesktopWidget().screenGeometry().width() * 100 / 1920))
        self.setAttribute(core.Qt.WA_TranslucentBackground)
        self.setWindowFlags(core.Qt.FramelessWindowHint | core.Qt.SplashScreen | core.Qt.WindowStaysOnTopHint)
        self.w = data['width-height']
        self.h = data['width-height']

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
        self.text.setAlignment(core.Qt.AlignCenter)
        self.text.setWordWrap(True)
        self.text.setText('双击\n抽号')

        def random_(evt):
            type(evt)
            self.text.setText((get_random()))

        self.main.mouseDoubleClickEvent = random_

        menu = widgets.QMenu(self)
        act_show = widgets.QAction("打开主窗口 (&O)", self)
        act_exit = widgets.QAction("退出 Study Plus (&E)", self)
        act_randoms = widgets.QAction('随机抽号 (&R)', self)
        act_schedule = widgets.QAction('课程表 (&S)', self)
        act_file_starter = widgets.QAction('文件定时启动（&F）', self)
        act_ai = widgets.QAction('Nernge AI（&N）', self)
        act_setting = widgets.QAction('设置 (&S)', self)
        act_help = widgets.QAction('帮助 (&H)', self)
        act_hide = widgets.QAction('关闭悬浮球 (&C)', self)

        def get_menu(evt):
            if evt == act_show:
                self.mainWindow.tray_icon.hide()
                self.mainWindow.show()
            if evt == act_randoms:
                self.mainWindow.randoms()
            if evt == act_schedule:
                self.mainWindow.schedule()
            if evt == act_setting:
                self.mainWindow.setting()
            if evt == act_file_starter:
                self.mainWindow.file_starter()
            if evt == act_ai:
                self.mainWindow.ai()
            if evt == act_help:
                webbrowser.open('https://gitee.com/Nernge/studyplus')
            if evt == act_hide:
                self.hide()
            if evt == act_exit:
                self.mainWindow.thread_run = False
                _time.sleep(0.01)
                self.mainWindow.thread_schedule.quit()
                self.mainWindow.thread_file_starter.quit()
                self.mainWindow.app.quit()

        menu.addAction(act_show)
        menu.addSeparator()
        menu.addAction(act_randoms)
        menu.addAction(act_schedule)
        menu.addAction(act_file_starter)
        menu.addAction(act_ai)
        menu.addAction(act_setting)
        menu.addSeparator()
        menu.addAction(act_help)
        menu.addSeparator()
        menu.addAction(act_hide)
        menu.addAction(act_exit)
        menu.triggered[widgets.QAction].connect(get_menu)

        def show_menu():
            menu.popup(gui.QCursor.pos())

        self.main.setContextMenuPolicy(core.Qt.CustomContextMenu)
        self.main.customContextMenuRequested.connect(show_menu)

    def setupUI(self, evt=None, wh=0):
        global data
        data = json.loads(read(r'data\mainWindow.json'))
        screen = widgets.QDesktopWidget().screenGeometry()
        w, h = screen.width() * self.w / 1920, screen.height() * self.h / 1080
        if type(evt) is float or evt is None:
            self.resize(int(self.w * (screen.width() + screen.height()) / 3000),
                        int(self.h * (screen.width() + screen.height()) / 3000))
        dpi = self.screen().logicalDotsPerInch() / 96

        def font(size_):
            f = gui.QFont()
            f.setPointSizeF(((size_ * w / (self.w * dpi) + size_ * h / (self.h * dpi)) / 2) * self.w / 60)
            return f

        w, h = self.width(), self.height()
        size = lambda x2, y2: core.QRect(0, 0, int(x2 * (screen.width() + screen.height()) / 3000),
                                         int(y2 * (screen.width() + screen.height()) / 3000))

        if wh == 0:
            self.main_bg.setGeometry(size(self.w, self.h))
            self.main.setGeometry(size(self.w, self.h))
            self.text.setGeometry(size(self.w, self.h))
        else:
            self.main_bg.setGeometry(size(wh, wh))
            self.main.setGeometry(size(wh, wh))
            self.text.setGeometry(size(wh, wh))

        self.text.setFont(font(12))

    def mouseMoveEvent(self, e):
        try:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except TypeError:
            pass

    def mousePressEvent(self, e):
        if e.button() == core.Qt.LeftButton:
            self._isTracking = True
            self._startPos = core.QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e):
        if e.button() == core.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def closeEvent(self, evt):
        if self.mainWindow.isVisible():
            evt.accept()
        else:
            self.hide()
            evt.ignore()
