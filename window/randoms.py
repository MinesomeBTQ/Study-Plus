from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui

from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class randoms(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(randoms, self).__init__()
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
        self.setStyleSheet(read(r'data\static\style.qss').replace(
            '@BACKGROUND-IMAGE', data['background-image']
        ).replace(
            '@MAIN-COLOR', data['main-color']
        ).replace(
            '@WH', str(int(widgets.QDesktopWidget().screenGeometry().width() * 15 / 1920))+'px'
        ))

    def initUI(self):
        self.choose_way.setTitle('抽号方式')
        self.choose_way_num.setText('数字抽号')
        self.choose_way_import.setText('自定义抽号')
        if self.data['way']:
            self.choose_way_num.setChecked(True)
        else:
            self.choose_way_import.setChecked(True)

        def way_num():
            self.data['way'] = True
            write(r'data\randoms.json', json.dumps(self.data))
            self.set_num.setEnabled(True)
            self.import_.setEnabled(False)

        def way_import():
            self.data['way'] = False
            write(r'data\randoms.json', json.dumps(self.data))
            self.set_num.setEnabled(False)
            self.import_.setEnabled(True)

        self.choose_way_num.clicked.connect(way_num)
        self.choose_way_import.clicked.connect(way_import)

        self.set_num.setTitle('数字抽号')
        if not self.data['way']:
            self.set_num.setEnabled(False)
        else:
            self.import_.setEnabled(False)
        self.txt_1.setText('最小值：')
        self.txt_2.setText('最大值：')

        def get_num_min():
            self.data['num'][0] = self.get_num_min.value()
            write(r'data\randoms.json', json.dumps(self.data))
            if self.signal:
                self.get_num_max.setMinimum(self.get_num_min.value())

        def get_num_max():
            self.data['num'][1] = self.get_num_max.value()
            write(r'data\randoms.json', json.dumps(self.data))
            if self.signal:
                self.get_num_min.setMaximum(self.get_num_max.value())
                self.signal = True

        self.get_num_min.valueChanged.connect(get_num_min)
        self.get_num_max.valueChanged.connect(get_num_max)
        self.get_num_min.setValue(self.data['num'][0])
        self.get_num_max.setValue(self.data['num'][1])
        self.import_.setTitle('自定义抽号')
        self.list.addItems(self.data['import'])
        self.btn_add.setText('添加')
        self.btn_del.setText('删除')
        self.btn_import_replace.setText('从文件导入\n(替换原内容)')
        self.btn_import_add.setText('从文件导入\n(在原内容上添加)')
        self.btn_clear.setText('清除')

        def statistic():
            self.statistic_txt.setText('共 %s 项' % str(self.list.count()))

        statistic()

        def add():
            get = widgets.QInputDialog.getText(self, '输入添加内容', '输入添加内容')
            if get[1]:
                self.data['import'] += [get[0]]
                write(r'data\randoms.json', json.dumps(self.data))
                self.list.addItem(get[0])
            statistic()

        def delete():
            try:
                del self.data['import'][self.list.currentRow()]
                write(r'data\randoms.json', json.dumps(self.data))
                item = self.list.takeItem(self.list.currentRow())
                type(item)
                del item
            except IndexError:
                pass
            finally:
                statistic()

        def import_replace():
            get = widgets.QFileDialog.getOpenFileName(self, '选择导入文件', None, '文本文件(*.txt)')[0]
            if get:
                text = read(get)
                get = widgets.QInputDialog.getText(self, '输入分隔符号', '输入分隔符号（如为回车则直接点击OK）')
                if get[1]:
                    if get[0]:
                        content = text.split(get[0].replace('\\n', '\n'))
                    else:
                        content = text.split('\n'.replace('\\n', '\n'))
                    self.list.clear()
                    self.list.addItems(content)
                    self.data['import'] = content
                    write(r'data\randoms.json', json.dumps(self.data))
            statistic()

        def import_add():
            get = widgets.QFileDialog.getOpenFileName(self, '选择导入文件', None, '文本文件(*.txt)')[0]
            if get:
                text = read(get)
                get = widgets.QInputDialog.getText(self, '输入分隔符号', '输入分隔符号（如为回车则直接点击OK）')
                if get[1]:
                    if get[0]:
                        content = text.split(get[0].replace('\\n', '\n'))
                    else:
                        content = text.split('\n'.replace('\\n', '\n'))
                    self.list.addItems(content)
                    self.data['import'] += content
                    write(r'data\randoms.json', json.dumps(self.data))
            statistic()

        def clear():
            if (widgets.QMessageBox.question(self, '清除', '是否要清除所有内容？',
                                             widgets.QMessageBox.Yes | widgets.QMessageBox.No) == 16384):
                self.list.clear()
                self.data['import'] = []
                write(r'data\randoms.json', json.dumps(self.data))
            statistic()

        self.statistic_txt.setAlignment(core.Qt.AlignBottom)
        self.btn_add.clicked.connect(add)
        self.btn_del.clicked.connect(delete)
        self.btn_import_replace.clicked.connect(import_replace)
        self.btn_import_add.clicked.connect(import_add)
        self.btn_clear.clicked.connect(clear)

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
