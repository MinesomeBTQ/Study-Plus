from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class ui(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(ui, self).__init__()
        self.signal = False
        self.bg_self = None
        self.setWindowTitle('Study Plus - 随机抽号')
        self.setWindowIcon(gui.QIcon('data/images/favicon.ico'))
        self.loadStyle()

        self.choose_way = widgets.QGroupBox(self)
        self.set_num = widgets.QGroupBox(self)
        self.txt_1 = widgets.QLabel(self.set_num)
        self.txt_2 = widgets.QLabel(self.set_num)
        self.choose_way_num = widgets.QRadioButton(self.choose_way)
        self.choose_way_import = widgets.QRadioButton(self.choose_way)
        self.get_num_min = widgets.QSpinBox(self.set_num)
        self.get_num_max = widgets.QSpinBox(self.set_num)
        self.import_ = widgets.QGroupBox(self)
        self.list = widgets.QListWidget(self.import_)
        self.btn_add = widgets.QPushButton(self.import_)
        self.btn_del = widgets.QPushButton(self.import_)
        self.btn_import_replace = widgets.QPushButton(self.import_)
        self.btn_import_add = widgets.QPushButton(self.import_)
        self.btn_clear = widgets.QPushButton(self.import_)
        self.statistic_txt = widgets.QLabel(self.import_)

        self.mainWindow = mainWindow  # 主窗口类
        self.w = 450
        self.h = 600
        self.data = json.loads(read(r'data\randoms.json'))

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

        self.choose_way.setGeometry(size(25, 15, 400, 70))
        self.choose_way_num.setGeometry(size(25, 0, 175, 75))
        self.choose_way_import.setGeometry(size(200, 0, 175, 75))
        self.set_num.setGeometry(size(25, 95, 400, 70))
        self.txt_1.setGeometry(size(25, 25, 50, 25))
        self.get_num_min.setGeometry(size(75, 25, 100, 25))
        self.txt_2.setGeometry(size(200, 25, 50, 25))
        self.get_num_max.setGeometry(size(250, 25, 100, 25))
        self.import_.setGeometry(size(25, 175, 400, 405))
        self.list.setGeometry(size(25, 35, 175, 345))
        self.btn_add.setGeometry(size(225, 35, 150, 25))
        self.btn_del.setGeometry(size(225, 70, 150, 25))
        self.btn_import_replace.setGeometry(size(225, 105, 150, 50))
        self.btn_import_add.setGeometry(size(225, 165, 150, 50))
        self.btn_clear.setGeometry(size(225, 225, 150, 25))
        self.statistic_txt.setGeometry(size(225, 355, 150, 25))

        self.choose_way.setFont(font(10))
        self.choose_way_num.setFont(font(10))
        self.choose_way_import.setFont(font(10))
        self.set_num.setFont(font(10))
        self.txt_1.setFont(font(10))
        self.txt_2.setFont(font(10))
        self.get_num_min.setFont(font(8))
        self.get_num_max.setFont(font(8))
        self.list.setFont(font(9))
        self.btn_add.setFont(font(9))
        self.btn_del.setFont(font(9))
        self.import_.setFont(font(10))
        self.btn_import_replace.setFont(font(9))
        self.btn_import_add.setFont(font(9))
        self.btn_clear.setFont(font(9))
        self.statistic_txt.setFont(font(8))

    def closeEvent(self, evt):
        if self.mainWindow.isVisible():
            evt.accept()
        else:
            self.hide()
            evt.ignore()
