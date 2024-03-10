from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class ui(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(ui, self).__init__()
        self.bg_self = None
        self.setWindowTitle('Study Plus - 设置')
        self.setWindowIcon(gui.QIcon('data/images/favicon.ico'))
        self.loadStyle()

        self.tab = widgets.QTabWidget(self)
        self.tab_1 = widgets.QWidget(self)
        self.tab_2 = widgets.QWidget(self)
        self.tab_3 = widgets.QWidget(self)

        self.bg_setting = widgets.QGroupBox(self.tab_1)
        self.txt_bg = widgets.QLabel(self.bg_setting)
        self.txt_2_bg = widgets.QLabel(self.bg_setting)
        self.select_bg = widgets.QComboBox(self.bg_setting)
        self.edit_bg = widgets.QLineEdit(self.bg_setting)
        self.import_bg = widgets.QPushButton(self.bg_setting)
        self.view_bg = widgets.QPushButton(self.bg_setting)
        self.tip_bg = widgets.QLabel(self.bg_setting)
        self.bg_show_way = widgets.QLabel(self.bg_setting)
        self.bg_show_way_background = widgets.QRadioButton(self.bg_setting)
        self.bg_show_way_border = widgets.QRadioButton(self.bg_setting)
        self.txt_widget_op = widgets.QLabel(self.bg_setting)
        self.widget_op = widgets.QSpinBox(self.bg_setting)

        self.color_setting = widgets.QGroupBox(self.tab_1)
        self.txt_color = widgets.QLabel(self.color_setting)
        self.edit_color = widgets.QComboBox(self.color_setting)
        self.view_color = widgets.QPushButton(self.color_setting)
        self.import_color = widgets.QPushButton(self.color_setting)

        self.toolbox_op = widgets.QGroupBox(self.tab_2)
        self.toolbox_wh = widgets.QGroupBox(self.tab_2)
        self.edit_op = widgets.QSpinBox(self.toolbox_op)
        self.edit_wh = widgets.QSpinBox(self.toolbox_wh)
        self.check_hide = widgets.QCheckBox(self.tab_2)
        self.toolbox_show = widgets.QCheckBox(self.tab_2)
        self.help = widgets.QLabel(self.tab_3)

        self.set_ai = widgets.QGroupBox(self.tab_3)
        self.edit_ai = widgets.QLineEdit(self.set_ai)
        self.set_setting = widgets.QGroupBox(self.tab_3)
        self.edit_setting = widgets.QTextEdit(self.set_setting)

        self.mainWindow = mainWindow  # 主窗口类
        self.w = 600
        self.h = 450
        self.bg_list = json.loads(read('data/static/bg.json'))
        self.color_list = json.loads(read('data/static/color.json'))
        self.bg = data['background-image']
        self.ai_data = json.loads(read(r'data\nernge_ai.json'))

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

        self.tab.setGeometry(size(0, 0, 600, 450))

        self.bg_setting.setGeometry(size(25, 5, 550, 250))
        self.txt_bg.setGeometry(size(25, 25, 250, 25))
        self.txt_2_bg.setGeometry(size(25, 75, 250, 25))
        self.select_bg.setGeometry(size(25, 50, 250, 25))
        self.edit_bg.setGeometry(size(25, 100, 170, 25))
        self.import_bg.setGeometry(size(200, 100, 75, 25))
        self.view_bg.setGeometry(size(300, 25, 225, 190))
        self.tip_bg.setGeometry(size(300, 215, 225, 20))
        self.bg_show_way.setGeometry(size(25, 125, 250, 25))
        self.bg_show_way_background.setGeometry(size(25, 150, 125, 25))
        self.bg_show_way_border.setGeometry(size(150, 150, 125, 25))
        self.txt_widget_op.setGeometry(size(25, 175, 250, 25))
        self.widget_op.setGeometry(size(25, 200, 250, 25))

        self.color_setting.setGeometry(size(25, 265, 550, 140))
        self.txt_color.setGeometry(size(25, 25, 550, 25))
        self.edit_color.setGeometry(size(25, 50, 500, 25))
        self.view_color.setGeometry(size(25, 95, 245, 25))
        self.import_color.setGeometry(size(280, 95, 245, 25))

        self.toolbox_op.setGeometry(size(25, 5, 550, 75))
        self.edit_op.setGeometry(size(25, 30, 500, 25))
        self.toolbox_wh.setGeometry(size(25, 90, 550, 75))
        self.edit_wh.setGeometry(size(25, 30, 500, 25))
        self.toolbox_show.setGeometry(size(25, 175, 500, 25))
        self.check_hide.setGeometry(size(25, 200, 500, 25))

        self.help.setGeometry(size(25, 400, 550, 25))

        self.set_ai.setGeometry(size(25, 5, 550, 75))
        self.edit_ai.setGeometry(size(25, 30, 500, 25))
        self.set_setting.setGeometry(size(25, 105, 550, 175))
        self.edit_setting.setGeometry(size(25, 30, 500, 125))

        self.tab.setStyleSheet('QTabBar::title{background: #FFFFFF;font-size: %spt;}'
                               'height: %s;' % (
                                   int((9 * w / (self.w * dpi) + 9 * h / (self.h * dpi)) / 2),
                                   int(20 * h / self.h)
                               ))

        self.bg_setting.setFont(font(10))
        self.txt_bg.setFont(font(10))
        self.txt_2_bg.setFont(font(10))
        self.select_bg.setFont(font(9))
        self.edit_bg.setFont(font(9))
        self.import_bg.setFont(font(9))
        self.tip_bg.setFont(font(8))
        self.bg_show_way.setFont(font(10))
        self.bg_show_way_background.setFont(font(10))
        self.bg_show_way_border.setFont(font(10))
        self.txt_widget_op.setFont(font(10))
        self.widget_op.setFont(font(9))

        self.color_setting.setFont(font(10))
        self.txt_color.setFont(font(10))
        self.edit_color.setFont(font(9))
        self.import_color.setFont(font(9))

        self.toolbox_op.setFont(font(10))
        self.toolbox_wh.setFont(font(10))
        self.edit_op.setFont(font(9))
        self.edit_wh.setFont(font(9))
        self.check_hide.setFont(font(10))
        self.toolbox_show.setFont(font(10))
        self.help.setFont(font(10))

        self.set_ai.setFont(font(10))
        self.edit_ai.setFont(font(9))
        self.set_setting.setFont(font(10))
        self.edit_setting.setFont(font(9))

    def closeEvent(self, evt):
        if self.mainWindow.isVisible():
            evt.accept()
        else:
            self.hide()
            evt.ignore()
