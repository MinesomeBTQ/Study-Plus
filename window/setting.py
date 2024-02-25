import os

from PyQt5 import Qt
from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui
import json
import shutil
import getpass

from function.func import *

create('data/static/color.json',
       '{"未来科技蓝": "#1e9fff", "活力橙": "#ff5722", "学习绿": "#39C839", "简约灰": "#aaaaaa", "古典红": "#87362b", '
       '"山水青": "#598AAA", "经典黑": "#333333", "自定义颜色": "#333333"}')
create('data/static/bg.json',
       '{"未来科技蓝": "bg_blue.png", "活力橙": "bg_orange.png", "学习绿": "bg_green.png", "简约灰": "bg_gray.png",'
       '"古典红": "bg_red.jpg", "现代深": "bg_black.jpg", "山水": "bg_mountain.png", "纯白": "bg_white.png",'
       '"自定义背景": "bg_white.png"}')
data = json.loads(read(r'data\mainWindow.json'))


class setting(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(setting, self).__init__()
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
        self.help = widgets.QLabel(self.tab_2)

        self.set_ai = widgets.QGroupBox(self.tab_3)
        self.edit_ai = widgets.QLineEdit(self.set_ai)

        self.mainWindow = mainWindow  # 主窗口类
        self.w = 600
        self.h = 450
        self.bg_list = json.loads(read('data/static/bg.json'))
        self.color_list = json.loads(read('data/static/color.json'))
        self.bg = data['background-image']

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
        ))

    def initUI(self):
        # 选项卡
        self.tab.addTab(self.tab_1, '外观设置')
        self.tab.addTab(self.tab_2, '悬浮球设置')
        self.tab.addTab(self.tab_3, 'AI设置')

        # 文本
        self.bg_setting.setTitle('设置背景')
        self.txt_bg.setText('选择默认背景：')
        self.txt_2_bg.setText('导入外部背景：')
        self.select_bg.addItems(self.bg_list)

        # 筛选选择背景选项
        try:
            self.select_bg.setCurrentText([k for k, v in self.bg_list.items() if v == self.bg][0])
        except IndexError:
            pass

        # 文本
        self.edit_bg.setEnabled(False)
        self.import_bg.setText('选择文件')
        self.import_bg.setObjectName('btn-b')
        self.tip_bg.setText('点击打开完整图片')

        def f5bg_view():
            self.view_bg.setStyleSheet(f'background-image: '
                                       f'url("data/images/{self.bg}");'
                                       f'border: 1px solid #d2d2d2;'
                                       f'background-attachment: scroll;')

        f5bg_view()
        self.view_bg.setCursor(Qt.Qt.PointingHandCursor)

        def preview():  # 点击图片事件
            try:
                os.startfile(os.getcwd() + fr'\data\images\{self.bg}')
            except FileNotFoundError:
                widgets.QMessageBox.warning(self, '找不到背景文件', '哎呀，找不到指定文件！可能该背景为纯色')

        self.view_bg.clicked.connect(preview)

        def import_image():  # 选择文件
            get = widgets.QFileDialog.getOpenFileName(
                self, '选择背景文件', None, '图片文件(*.png *.jpg)'
            )[0]
            if get:
                self.edit_bg.setText(get)
                filepath = ''.join(get.split('/')[-1])
                try:
                    shutil.copyfile(get, "data/images/" + filepath)
                except shutil.SameFileError:
                    pass
                self.bg = filepath
                data['background-image'] = filepath
                write(r'data\mainWindow.json', json.dumps(data))
                self.bg_list['自定义背景'] = filepath
                write(r'data\static\bg.json', json.dumps(self.bg_list))
                self.edit_bg.setText(os.getcwd() + '/data/images/' + self.bg)
                f5bg_view()
                self.mainWindow.loadStyle()

        self.import_bg.clicked.connect(import_image)

        def select_image():  # 选择背景
            get = self.select_bg.currentText()
            self.bg = self.bg_list[get]
            data['background-image'] = self.bg_list[get]
            write(r'data\mainWindow.json', json.dumps(data))
            f5bg_view()
            self.mainWindow.loadStyle()

        self.select_bg.currentTextChanged.connect(select_image)

        # 文本
        self.color_setting.setTitle('设置主题颜色')
        self.txt_color.setText('选择颜色')
        self.import_color.setText('其他颜色')
        self.import_color.setObjectName('btn-b')
        self.edit_color.addItems(self.color_list)

        # 筛选选择颜色选项
        try:
            self.edit_color.setCurrentText([k for k, v in self.color_list.items() if v == data['main-color']][0])
        except IndexError:
            pass

        def f5color_view():
            self.view_color.setStyleSheet(f'background: {data["main-color"]};'
                                          f'border: 1px solid #d2d2d2;'
                                          f'border-radius: 4px;')

        f5color_view()

        # 选择颜色
        def select_color():
            get = self.edit_color.currentText()
            data['main-color'] = self.color_list[get]
            write(r'data\mainWindow.json', json.dumps(data))
            self.mainWindow.loadStyle()
            f5color_view()

        self.edit_color.currentTextChanged.connect(select_color)

        # 其他颜色
        def import_color_():
            get = widgets.QColorDialog.getColor(parent=self)
            if get.isValid():
                get = get.name()
                data['main-color'] = get
                write(r'data\mainWindow.json', json.dumps(data))
                self.color_list['自定义颜色'] = get
                write(r'data\static\color.json', json.dumps(self.color_list))
                self.mainWindow.loadStyle()
                f5color_view()

        self.import_color.clicked.connect(import_color_)

        self.toolbox_op.setTitle('不透明度 - %')
        self.edit_op.setValue(data['opacity'])
        self.edit_op.setRange(0, 100)

        def set_op():
            data['opacity'] = self.edit_op.value()
            write(r'data\mainWindow.json', json.dumps(data))
            op = widgets.QGraphicsOpacityEffect(self)
            op.setOpacity(self.edit_op.value() / 100)
            self.mainWindow.toolbox_window.main_bg.setGraphicsEffect(op)

        self.edit_op.valueChanged.connect(set_op)

        self.toolbox_wh.setTitle('边长')
        self.edit_wh.setRange(10, 360)
        self.edit_wh.setValue(data['width-height'])

        def set_wh():
            data['width-height'] = self.edit_wh.value()
            write(r'data\mainWindow.json', json.dumps(data))
            self.mainWindow.toolbox_window.w = self.edit_wh.value()
            self.mainWindow.toolbox_window.h = self.edit_wh.value()
            self.mainWindow.toolbox_window.setupUI(wh=self.edit_wh.value())

        self.edit_wh.valueChanged.connect(set_wh)

        self.check_hide.setChecked(data['hide'])
        self.check_hide.setText('启动时隐藏主窗口')

        self.toolbox_show.setChecked(not data['toolbox'])
        self.toolbox_show.setText('隐藏悬浮球')

        def set_toolbox_show():
            if self.toolbox_show.isChecked():
                data['toolbox'] = False
                self.mainWindow.toolbox_window.hide()
            else:
                data['toolbox'] = True
                self.mainWindow.toolbox_window.show()
            write(r'data\mainWindow.json', json.dumps(data))

        self.toolbox_show.clicked.connect(set_toolbox_show)

        def set_hide():
            data['hide'] = self.check_hide.isChecked()
            write(r'data\mainWindow.json', json.dumps(data))

        self.check_hide.clicked.connect(set_hide)

        self.help.setText(
            '<a href="https://gitee.com/Nernge/studyplus" style="color: #666666;">获取 Study Plus 使用帮助</a>')
        self.help.setOpenExternalLinks(True)

        self.set_ai.setTitle('设置 API-Key')
        self.edit_ai.setText(read(r'data\static\api-key'))

        def edit_ai():
            write(r'data\static\api-key', self.edit_ai.text())

        self.edit_ai.textChanged.connect(edit_ai)

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

    def closeEvent(self, evt):
        if self.mainWindow.isVisible():
            evt.accept()
        else:
            self.hide()
            evt.ignore()
