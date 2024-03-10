import time as _time

from function.func import *

from window import setting, randoms, toolbox, schedule, file_starter, nernge_ai

data = json.loads(read(r'data\mainWindow.json'))

__version__ = __true_version__ = 'v1.1.3'


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
        self.message_window = None
        if data['toolbox']:
            self.toolbox()
        self.tray()

        self.thread_run = True

        class thread_schedule(core.QThread):
            show_message = core.pyqtSignal(str)

            def __init__(self, parent):
                super().__init__()
                self.parent = parent

            def run(self):
                while self.parent.thread_run:
                    try:
                        data_ = json.loads(read(r'data\schedule.json'))
                        data_func = json.loads(read(r'data\schedule_func.json'))
                        if data_func['message'][0] or data_func['message'][1]:
                            time_now = _time.localtime(_time.time())
                            week = time_now.tm_wday
                            if [time_now.tm_hour, time_now.tm_min, time_now.tm_sec] in data_['time']:
                                lst = []
                                for time_, i in zip(data_['time'], range(data_func['class_num'])):
                                    if [time_now.tm_hour, time_now.tm_min, time_now.tm_sec] == time_:
                                        lst += [i]
                                for i in lst:
                                    if ''.join(data_[str(week + 1)][str(i)].split(' ')):
                                        if data_func['message'][0]:
                                            self.parent.tray_icon.showMessage('课程提醒 - '+data_[str(week + 1)][str(i)],
                                                                              data_func['text'].replace('@N',
                                                                                                        data_
                                                                                                        [str(week + 1)]
                                                                                                        [str(i)]))
                                        if data_func['message'][1]:
                                            self.show_message.emit(data_[str(week + 1)][str(i)])
                                _time.sleep(1.1)
                    except json.decoder.JSONDecodeError:
                        pass
                    if self.parent.thread_run:
                        _time.sleep(0.01)

        self.thread_schedule = thread_schedule(self)
        self.thread_schedule.show_message.connect(self.show_message)
        self.thread_schedule.start()

        self.thread_file_starter = core.QThread(self)

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

        class get_version(core.QThread):
            signal = core.pyqtSignal(str)

            def __init__(self, main_window):
                super().__init__()
                self.mainWindow = main_window

            def run(self):
                try:
                    global __true_version__
                    __true_version__ = (requests.get('https://gitee.com/Nernge/studyplus/raw/master/README.md')
                                        .text.split('\n')[0].replace('#', '').replace('Study Plus', '')
                                        .replace(' ', ''))
                    if __version__ != __true_version__:
                        have_shown = False
                        while not have_shown:
                            if self.mainWindow.isVisible():
                                self.signal.emit('run')
                                have_shown = True
                            _time.sleep(0.1)
                        self.quit()

                except requests.exceptions.ConnectionError:
                    self.quit()

        self.getVersion = get_version(self)
        self.getVersion.signal.connect(self.message)
        self.getVersion.start()

    def loadStyle(self):
        global data
        data = json.loads(read(r'data\mainWindow.json'))
        self.setStyleSheet(get_style())
        try:
            self.setting_window.loadStyle()
            self.randoms_window.loadStyle()
            self.toolbox_window.loadStyle()
            self.schedule_window.loadStyle()
            self.file_starter_window.loadStyle()
            self.ai_window.loadStyle()
            self.message_window.loadStyle()
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
        self.random_btn.clicked.connect(self.randoms)

        self.schedule_btn.setText('课 程 表')
        self.schedule_btn.setObjectName('btn-b')
        self.schedule_btn.clicked.connect(self.schedule)

        self.file_starter_btn.setText('文件定时启动')
        self.file_starter_btn.setObjectName('btn-b')
        self.file_starter_btn.clicked.connect(self.file_starter)

        self.setting_btn.setText('设 置')
        self.setting_btn.setObjectName('btn-b')
        self.setting_btn.clicked.connect(self.setting)

        self.ai_btn.setText('Nernge AI')
        self.ai_btn.setObjectName('btn-b')
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
        act_show = widgets.QAction("打开主窗口 (&O)", self)
        act_exit = widgets.QAction("退出 Study Plus (&E)", self)
        act_randoms = widgets.QAction('随机抽号 (&R)', self)
        act_schedule = widgets.QAction('课程表 (&S)', self)
        act_file_starter = widgets.QAction('文件定时启动（&F）', self)
        act_ai = widgets.QAction('Nernge AI（&N）', self)
        act_setting = widgets.QAction('设置 (&S)', self)
        act_help = widgets.QAction('帮助 (&H)', self)
        act_toolbox = widgets.QAction('关闭/打开悬浮球 (&T)', self)

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
            if evt == act_toolbox:
                if self.toolbox_window.isVisible():
                    self.toolbox_window.hide()
                else:
                    self.toolbox_window.show()
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
        menu.addAction(act_toolbox)
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
                    'https://gitee.com/Nernge/studyplus/raw/master/Study%20Plus%20Installer.exe')

    def show_message(self, evt):
        self.message_window = schedule.message(self)
        self.message_window.class_name = evt
        self.message_window.show()
