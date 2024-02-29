import os

from PyQt5 import Qt
from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui
import json
import shutil

from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class schedule(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(schedule, self).__init__()
        self.bg_self = None
        self.setWindowTitle('Study Plus - 课程表')
        self.setWindowIcon(gui.QIcon('data/images/favicon.ico'))
        self.loadStyle()

        self.table = widgets.QTableWidget(self)
        self.txt_1 = widgets.QLabel(self)
        self.txt_2 = widgets.QLabel(self)
        self.system_msg = widgets.QCheckBox(self)
        self.window_msg = widgets.QCheckBox(self)
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
        self.setStyleSheet(read(r'data\static\style.qss').replace(
            '@BACKGROUND-IMAGE', data['background-image']
        ).replace(
            '@MAIN-COLOR', data['main-color']
        ).replace(
            '@WH', str(int(widgets.QDesktopWidget().screenGeometry().width() * 15 / 1920))+'px'
        ))

    def initUI(self):
        self.table.setColumnCount(8)
        self.table.setRowCount(9)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(widgets.QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(widgets.QHeaderView.Stretch)
        self.table.setSelectionBehavior(widgets.QAbstractItemView.SelectItems)
        # self.table.setEditTriggers(widgets.QAbstractItemView.NoEditTriggers)

        self.table.setHorizontalHeaderLabels(
            ['开始时间', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日', ])
        self.table.setVerticalHeaderLabels(
            ['第一节', '第二节', '第三节', '第四节', '第五节', '第六节', '第七节', '第八节', '第九节'])
        for r, ri in zip(self.data.keys(), range(8)):
            try:
                for c, ci in zip(list(self.data.values())[ri].values(), range(9)):
                    item = widgets.QTableWidgetItem(c)
                    item.setTextAlignment(core.Qt.AlignCenter)
                    self.table.setItem(ci, ri, item)
            except AttributeError:
                for i in range(9):
                    '''print(""" time_item_NUM = widgets.QTimeEdit(self) time_item_NUM.setDisplayFormat("hh:mm:ss") 
                    time_item_NUM.setTime(core.QTime(self.data['time'][NUM][0], self.data['time'][NUM][1], 
                    self.data['time'][NUM][2]))

                    def set_time(): time = [time_item_NUM.time().hour(), time_item_NUM.time().minute(), 
                    time_item_NUM.time().second()] self.data['time'][NUM] = time write(r'data\\schedule.json', 
                    json.dumps(self.data))

                    time_item_NUM.timeChanged.connect(set_time)
                    self.table.setCellWidget(NUM, ri, time_item_NUM)
                    """.replace('NUM', str(i)))
                    '''

                    time_item_0 = widgets.QTimeEdit(self)
                    time_item_0.setDisplayFormat("hh:mm:ss")
                    time_item_0.setTime(
                        core.QTime(self.data['time'][0][0], self.data['time'][0][1], self.data['time'][0][2]))

                    def set_time():
                        time = [time_item_0.time().hour(), time_item_0.time().minute(), time_item_0.time().second()]
                        self.data['time'][0] = time
                        write(r'data\schedule.json', json.dumps(self.data))

                    time_item_0.timeChanged.connect(set_time)
                    self.table.setCellWidget(0, ri, time_item_0)

                    time_item_1 = widgets.QTimeEdit(self)
                    time_item_1.setDisplayFormat("hh:mm:ss")
                    time_item_1.setTime(
                        core.QTime(self.data['time'][1][0], self.data['time'][1][1], self.data['time'][1][2]))

                    def set_time():
                        time = [time_item_1.time().hour(), time_item_1.time().minute(), time_item_1.time().second()]
                        self.data['time'][1] = time
                        write(r'data\schedule.json', json.dumps(self.data))

                    time_item_1.timeChanged.connect(set_time)
                    self.table.setCellWidget(1, ri, time_item_1)

                    time_item_2 = widgets.QTimeEdit(self)
                    time_item_2.setDisplayFormat("hh:mm:ss")
                    time_item_2.setTime(
                        core.QTime(self.data['time'][2][0], self.data['time'][2][1], self.data['time'][2][2]))

                    def set_time():
                        time = [time_item_2.time().hour(), time_item_2.time().minute(), time_item_2.time().second()]
                        self.data['time'][2] = time
                        write(r'data\schedule.json', json.dumps(self.data))

                    time_item_2.timeChanged.connect(set_time)
                    self.table.setCellWidget(2, ri, time_item_2)

                    time_item_3 = widgets.QTimeEdit(self)
                    time_item_3.setDisplayFormat("hh:mm:ss")
                    time_item_3.setTime(
                        core.QTime(self.data['time'][3][0], self.data['time'][3][1], self.data['time'][3][2]))

                    def set_time():
                        time = [time_item_3.time().hour(), time_item_3.time().minute(), time_item_3.time().second()]
                        self.data['time'][3] = time
                        write(r'data\schedule.json', json.dumps(self.data))

                    time_item_3.timeChanged.connect(set_time)
                    self.table.setCellWidget(3, ri, time_item_3)

                    time_item_4 = widgets.QTimeEdit(self)
                    time_item_4.setDisplayFormat("hh:mm:ss")
                    time_item_4.setTime(
                        core.QTime(self.data['time'][4][0], self.data['time'][4][1], self.data['time'][4][2]))

                    def set_time():
                        time = [time_item_4.time().hour(), time_item_4.time().minute(), time_item_4.time().second()]
                        self.data['time'][4] = time
                        write(r'data\schedule.json', json.dumps(self.data))

                    time_item_4.timeChanged.connect(set_time)
                    self.table.setCellWidget(4, ri, time_item_4)

                    time_item_5 = widgets.QTimeEdit(self)
                    time_item_5.setDisplayFormat("hh:mm:ss")
                    time_item_5.setTime(
                        core.QTime(self.data['time'][5][0], self.data['time'][5][1], self.data['time'][5][2]))

                    def set_time():
                        time = [time_item_5.time().hour(), time_item_5.time().minute(), time_item_5.time().second()]
                        self.data['time'][5] = time
                        write(r'data\schedule.json', json.dumps(self.data))

                    time_item_5.timeChanged.connect(set_time)
                    self.table.setCellWidget(5, ri, time_item_5)

                    time_item_6 = widgets.QTimeEdit(self)
                    time_item_6.setDisplayFormat("hh:mm:ss")
                    time_item_6.setTime(
                        core.QTime(self.data['time'][6][0], self.data['time'][6][1], self.data['time'][6][2]))

                    def set_time():
                        time = [time_item_6.time().hour(), time_item_6.time().minute(), time_item_6.time().second()]
                        self.data['time'][6] = time
                        write(r'data\schedule.json', json.dumps(self.data))

                    time_item_6.timeChanged.connect(set_time)
                    self.table.setCellWidget(6, ri, time_item_6)

                    time_item_7 = widgets.QTimeEdit(self)
                    time_item_7.setDisplayFormat("hh:mm:ss")
                    time_item_7.setTime(
                        core.QTime(self.data['time'][7][0], self.data['time'][7][1], self.data['time'][7][2]))

                    def set_time():
                        time = [time_item_7.time().hour(), time_item_7.time().minute(), time_item_7.time().second()]
                        self.data['time'][7] = time
                        write(r'data\schedule.json', json.dumps(self.data))

                    time_item_7.timeChanged.connect(set_time)
                    self.table.setCellWidget(7, ri, time_item_7)

                    time_item_8 = widgets.QTimeEdit(self)
                    time_item_8.setDisplayFormat("hh:mm:ss")
                    time_item_8.setTime(
                        core.QTime(self.data['time'][8][0], self.data['time'][8][1], self.data['time'][8][2]))

                    def set_time():
                        time = [time_item_8.time().hour(), time_item_8.time().minute(), time_item_8.time().second()]
                        self.data['time'][8] = time
                        write(r'data\schedule.json', json.dumps(self.data))

                    time_item_8.timeChanged.connect(set_time)
                    self.table.setCellWidget(8, ri, time_item_8)

        def set_table(row, col):
            self.data[str(col)][str(row)] = self.table.item(row, col).text()
            write(r'data\schedule.json', json.dumps(self.data))

        self.table.cellChanged.connect(set_table)

        self.txt_1.setText('课程表定时通知方式')
        self.system_msg.setText('系统通知')
        self.window_msg.setText('弹窗通知')
        self.system_msg.setChecked(self.data_func['message'][0])
        self.window_msg.setChecked(self.data_func['message'][1])

        def check():
            if self.window_msg.isChecked() and self.edit.toPlainText().count('@N') > 1:
                widgets.QMessageBox.warning(self, '错误', '若设置了 弹窗通知 ，通知内容中最多包含一个“@N”')
                return False
            else:
                return True

        def on():
            self.data_func['message'][0] = self.system_msg.isChecked()
            write(r'data\schedule_func.json', json.dumps(self.data_func))

        def off():
            if check():
                self.data_func['message'][1] = self.window_msg.isChecked()
                write(r'data\schedule_func.json', json.dumps(self.data_func))
            else:
                self.window_msg.setChecked(False)

        self.system_msg.clicked.connect(on)
        self.window_msg.clicked.connect(off)

        self.txt_2.setText('通知内容：')
        self.edit.setPlainText(self.data_func['text'])
        self.edit.setPlaceholderText('课程名称使用 @N 代替')
        self.edit.setFocus()

        def edit():
            if check():
                self.data_func['text'] = self.edit.toPlainText()
                write(r'data\schedule_func.json', json.dumps(self.data_func))
            else:
                self.edit.setPlainText(self.data_func['text'])

        self.edit.textChanged.connect(edit)

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
        self.txt_2.setGeometry(size(250, 525, 100, 50))
        self.edit.setGeometry(size(350, 525, 425, 50))

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
