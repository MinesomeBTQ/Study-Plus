from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class ui(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(ui, self).__init__()
        self.bg_self = None
        self.setWindowTitle('Study Plus - 课程表')
        self.setWindowIcon(gui.QIcon('data/images/favicon.ico'))
        self.loadStyle()

        self.table = widgets.QTableWidget(self)
        self.txt_1 = widgets.QLabel(self)
        self.txt_2 = widgets.QLabel(self)
        self.txt_3 = widgets.QLabel(self)
        self.system_msg = widgets.QCheckBox(self)
        self.window_msg = widgets.QCheckBox(self)
        self.edit_class_num = widgets.QSpinBox(self)
        self.edit = widgets.QTextEdit(self)

        self.mainWindow = mainWindow  # 主窗口类
        self.w = 800
        self.h = 600
        self.data = json.loads(read(r'data\schedule.json'))
        self.data_func = json.loads(read(r'data\schedule_func.json'))
        self.time_items = []

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

        self.table.setGeometry(size(0, 0, 800, 500))
        self.txt_1.setGeometry(size(25, 525, 200, 25))
        self.system_msg.setGeometry(size(25, 550, 100, 25))
        self.window_msg.setGeometry(size(125, 550, 100, 25))
        self.txt_2.setGeometry(size(375, 525, 100, 50))
        self.edit.setGeometry(size(450, 525, 325, 50))
        self.txt_3.setGeometry(size(250, 525, 200, 25))
        self.edit_class_num.setGeometry(size(250, 550, 100, 25))

        self.table.setFont(font(9))
        self.txt_1.setFont(font(10))
        self.system_msg.setFont(font(10))
        self.window_msg.setFont(font(10))
        self.txt_2.setFont(font(10))
        self.edit.setFont(font(9))
        self.table.horizontalHeader().setFont(font(9))
        self.table.verticalHeader().setFont(font(9))

    def closeEvent(self, evt):
        if self.mainWindow.isVisible():
            evt.accept()
        else:
            self.hide()
            evt.ignore()
