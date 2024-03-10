from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class ui(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(ui, self).__init__()
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
        self.setStyleSheet(get_style())

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
