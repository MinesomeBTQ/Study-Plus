from PyQt5 import Qt
from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui
import json
import webbrowser
import time as _time
import requests

from PyQt5.QtWidgets import QAction

from function.func import *

create(r'data\mainWindow.json', '{"background-image": "bg_blue.png", "main-color": "#1e9fff", "opacity": 60, '
                                '"width-height": 60, "hide": false, "toolbox": true}')
# 记得更改配置文件检测

from window import setting, randoms, toolbox, schedule, file_starter, nernge_ai

data = json.loads(read(r'data\mainWindow.json'))

__version__ = __true_version__ = 'v1.1.0'


class mainWindow(widgets.QMainWindow):
    def __init__(self, app):
        super(mainWindow, self).__init__()
        self.setWindowTitle('Study Plus')
        self.setObjectName('mainWindow')
        self.setWindowIcon(gui.QIcon('data/images/favicon.ico'))
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.loadStyle()

        self.title = widgets.QLabel(self)  # 标题
        self.subtitle = widgets.QLabel(self)  # 小标题
        self.random_btn = widgets.QPushButton(self)  # 随机数设置
        self.schedule_btn = widgets.QPushButton(self)  # 课程表设置
        self.file_starter_btn = widgets.QPushButton(self)  # 文件定时启动设置
        self.setting_btn = widgets.QPushButton(self)  # 设置
        self.ai_btn = widgets.QPushButton(self)  # Nernge AI

        self.w = 800
        self.h = 600
        self.app = app
        self.tray_icon = widgets.QSystemTrayIcon(gui.QIcon("data/images/favicon.ico"), self)
        self.tray_icon.hide()

        global data
        try:
            type([data['background-image'], data['main-color'], data['opacity'], data['hide'], data['width-height'],
                  data['toolbox']])
        except KeyError:
            write(r'data\mainWindow.json',
                  '{"background-image": "bg_blue.png", "main-color": "#1e9fff", "opacity": 60, '
                  '"width-height": 60, "hide": false, "toolbox": true}')
            data = json.loads(read(r'data\mainWindow.json'))
            widgets.QMessageBox.information(self, 'Study Plus', '检测到部分配置文件为旧版本或损坏，已经为您重置该配置文件')

        self.screen().logicalDotsPerInchChanged.connect(self.setupUI)
        self.resizeEvent = self.setupUI
        self.initUI()
        self.setupUI()

        self.setting_window = setting.setting(self)
        self.randoms_window = randoms.randoms(self)
        self.schedule_window = schedule.schedule(self)
        self.file_starter_window = file_starter.file_starter(self)
        self.toolbox_window = toolbox.toolbox(self)
        self.ai_window = nernge_ai.ai(self)
        if data['toolbox']:
            self.toolbox()
        self.tray()

        self.thread_run = True
        self.thread_schedule = QThread(self)

        def run():
            while self.thread_run:
                try:
                    data_ = json.loads(read(r'data\schedule.json'))
                    data_func = json.loads(read(r'data\schedule_func.json'))
                    if data_func['func']:
                        time_now = _time.localtime(_time.time())
                        week = time_now.tm_wday
                        if [time_now.tm_hour, time_now.tm_min, time_now.tm_sec] in data_['time']:
                            lst = []
                            for time_, i in zip(data_['time'], range(9)):
                                if [time_now.tm_hour, time_now.tm_min, time_now.tm_sec] == time_:
                                    lst += [i]
                            for i in lst:
                                if ''.join(data_[str(week + 1)][str(i)].split(' ')):
                                    self.tray_icon.showMessage('课堂提醒',
                                                               data_func['text'].replace('@N', data_[str(week + 1)][
                                                                   str(i)]))
                            _time.sleep(1.1)
                except json.decoder.JSONDecodeError:
                    pass
                if self.thread_run:
                    _time.sleep(0.01)

        self.thread_schedule.run = run
        self.thread_schedule.start()

        self.thread_file_starter = QThread(self)

        def file_start():
            while self.thread_run:
                try:
                    data_ = json.loads(read(r'data\file_starter.json'))
                    if data_['func'] and data_['file']:
                        time_now = _time.localtime(_time.time())
                        if [time_now.tm_hour, time_now.tm_min, time_now.tm_sec] == data_['time']:
                            os.startfile(data_['file'])
                            _time.sleep(1.1)
                except json.decoder.JSONDecodeError:
                    pass
                if self.thread_run:
                    _time.sleep(0.01)

        self.thread_file_starter.run = file_start
        self.thread_file_starter.start()

        class get_version(QThread):
            signal = core.pyqtSignal(str)

            def __init__(self):
                super().__init__()

            def run(self):
                try:
                    global __true_version__
                    __true_version__ = (requests.get('https://gitee.com/Nernge/studyplus/raw/master/README.md')
                                        .text.split('\n')[0].replace('#', '').replace('Study Plus', '')
                                        .replace(' ', ''))
                    if __version__ != __true_version__:
                        self.signal.emit('run')
                    self.quit()
                except requests.exceptions.ConnectionError:
                    self.quit()

        self.getVersion = get_version()
        self.getVersion.signal.connect(self.message)
        self.getVersion.start()

    def loadStyle(self):
        global data
        data = json.loads(read(r'data\mainWindow.json'))
        self.setStyleSheet(read(r'data\static\style.qss').replace(
            '@BACKGROUND-IMAGE', data['background-image']
        ).replace(
            '@MAIN-COLOR', data['main-color']
        ))
        try:
            self.setting_window.loadStyle()
            self.randoms_window.loadStyle()
            self.toolbox_window.loadStyle()
            self.schedule_window.loadStyle()
            self.file_starter_window.loadStyle()
            self.ai_window.loadStyle()
        except AttributeError:
            pass

    def initUI(self):
        self.title.setObjectName('title')
        self.title.setText('Study Plus')
        self.title.setAlignment(core.Qt.AlignCenter)

        self.subtitle.setObjectName('subtitle')
        self.subtitle.setText(__version__ + ' By BT.Q')
        self.subtitle.setAlignment(core.Qt.AlignCenter)

        self.random_btn.setText('随 机 抽 号')
        self.random_btn.setObjectName('btn-b')
        self.random_btn.setCursor(Qt.Qt.PointingHandCursor)
        self.random_btn.clicked.connect(self.randoms)

        self.schedule_btn.setText('课 程 表')
        self.schedule_btn.setObjectName('btn-b')
        self.schedule_btn.setCursor(Qt.Qt.PointingHandCursor)
        self.schedule_btn.clicked.connect(self.schedule)

        self.file_starter_btn.setText('文件定时启动')
        self.file_starter_btn.setObjectName('btn-b')
        self.file_starter_btn.setCursor(Qt.Qt.PointingHandCursor)
        self.file_starter_btn.clicked.connect(self.file_starter)

        self.setting_btn.setText('设 置')
        self.setting_btn.setObjectName('btn-b')
        self.setting_btn.setCursor(Qt.Qt.PointingHandCursor)
        self.setting_btn.clicked.connect(self.setting)

        self.ai_btn.setText('Nernge AI')
        self.ai_btn.setObjectName('btn-b')
        self.ai_btn.setCursor(Qt.Qt.PointingHandCursor)
        self.ai_btn.clicked.connect(self.ai)

    def setupUI(self, evt=None):
        screen = widgets.QDesktopWidget().screenGeometry()
        w, h = screen.width() * self.w / 1920, screen.height() * self.h / 1080
        if type(evt) is float or evt is None:
            self.resize(int(w), int(h))
            self.setMinimumSize(int(w * 0.8), int(h * 0.8))
            self.setMaximumSize(int(w * 1.2), int(h * 1.2))
        dpi = self.screen().logicalDotsPerInch() / 96

        def font(size_):
            f = gui.QFont()
            f.setPointSizeF((size_ * w / (self.w * dpi) + size_ * h / (self.h * dpi)) / 2)
            return f

        w, h = self.width(), self.height()
        size = lambda x1, y1, x2, y2: core.QRect(int(x1 * w / self.w), int(y1 * h / self.h), int(x2 * w / self.w),
                                                 int(y2 * h / self.h))
        self.title.setGeometry(size(50, 0, 325, 200))
        self.subtitle.setGeometry(size(50, 125, 325, 75))
        self.random_btn.setGeometry(size(50, 200, 325, 250))
        self.schedule_btn.setGeometry(size(420, 50, 325, 150))
        self.file_starter_btn.setGeometry(size(420, 225, 325, 150))
        self.setting_btn.setGeometry(size(50, 475, 325, 75))
        self.ai_btn.setGeometry(size(420, 400, 325, 150))

        self.title.setFont(font(40))
        self.subtitle.setFont(font(10))
        self.random_btn.setFont(font(18))
        self.schedule_btn.setFont(font(18))
        self.file_starter_btn.setFont(font(18))
        self.setting_btn.setFont(font(18))
        self.ai_btn.setFont(font(18))

    def setting(self):
        self.setting_window.close()
        self.setting_window.show()

    def randoms(self):
        self.randoms_window.close()
        self.randoms_window.show()

    def schedule(self):
        self.schedule_window.close()
        self.schedule_window.show()

    def file_starter(self):
        self.file_starter_window.close()
        self.file_starter_window.show()

    def toolbox(self):
        self.toolbox_window.show()

    def ai(self):
        self.ai_window.close()
        self.ai_window.show()

    def tray(self):
        menu = widgets.QMenu()
        act_show = QAction("打开主窗口 (&O)", self)
        act_exit = QAction("退出 Study Plus (&E)", self)
        act_randoms = QAction('随机抽号 (&R)', self)
        act_schedule = QAction('课程表 (&S)', self)
        act_file_starter = QAction('文件定时启动（&F）', self)
        act_ai = QAction('Nernge AI（&N）', self)
        act_setting = QAction('设置 (&S)', self)
        act_help = QAction('帮助 (&H)', self)

        def get_menu(evt):
            if evt == act_show:
                self.tray_icon.hide()
                self.show()
            if evt == act_randoms:
                self.randoms()
            if evt == act_schedule:
                self.schedule()
            if evt == act_setting:
                self.setting()
            if evt == act_file_starter:
                self.file_starter()
            if evt == act_ai:
                self.ai()
            if evt == act_help:
                webbrowser.open('https://gitee.com/Nernge/studyplus')
            if evt == act_exit:
                self.thread_run = False
                _time.sleep(0.01)
                self.thread_schedule.quit()
                self.thread_file_starter.quit()
                self.app.quit()

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
        menu.addAction(act_exit)

        def tray_icon_clicked(reason):
            if reason == Qt.QSystemTrayIcon.Trigger:
                self.tray_icon.hide()
                self.show()

        self.tray_icon.activated.connect(tray_icon_clicked)
        self.tray_icon.setToolTip('Study Plus')
        menu.triggered[widgets.QAction].connect(get_menu)
        self.tray_icon.setContextMenu(menu)

    def closeEvent(self, evt):
        self.tray_icon.show()
        self.hide()
        evt.ignore()

    def message(self, info):
        if info == 'run' and self.isVisible():
            if widgets.QMessageBox.information(self, 'Study Plus %s 更新至 %s' % (__version__, __true_version__),
                                               '检测到有可供安装的新版本，是否前往更新？',
                                               widgets.QMessageBox.Yes | widgets.QMessageBox.No) == 16384:
                webbrowser.open(
                    'https://gitee.com/Nernge/studyplus/blob/master/Study%20Plus%20Installer.exe')
