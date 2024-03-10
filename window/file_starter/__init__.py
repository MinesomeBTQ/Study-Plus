from window.file_starter.ui import *
from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class file_starter(ui):
    def __init__(self, mainWindow):
        super(file_starter, self).__init__(mainWindow)
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

    def initUI(self):
        self.txt_1.setText('启用文件定时启动')
        self.on.setText('启用')
        self.off.setText('禁用')
        self.txt_2.setText('文件路径')
        self.edit.setText(self.data['file'])
        self.txt_3.setText('启动时间')
        self.edit_time.setObjectName('timeEdit')
        self.edit_time.setDisplayFormat("hh:mm:ss")
        self.edit_time.setTime(core.QTime(self.data['time'][0], self.data['time'][1], self.data['time'][2]))

        self.on.setChecked(self.data['func'])
        self.off.setChecked(not self.data['func'])

        def check():
            if self.on.isChecked():
                self.data['func'] = True
            else:
                self.data['func'] = False
            write(r'data\file_starter.json', json.dumps(self.data))

        self.on.clicked.connect(check)
        self.off.clicked.connect(check)

        def set_file(evt):
            type(evt)
            path = widgets.QFileDialog.getOpenFileName(self, '选择文件路径', None, '所有文件(*.*)')[0]
            if path:
                self.edit.setText(path)
                self.data['file'] = path
                write(r'data\file_starter.json', json.dumps(self.data))

        self.edit.mousePressEvent = set_file

        def set_time():
            self.data['time'] = [self.edit_time.time().hour(), self.edit_time.time().minute(),
                                 self.edit_time.time().second()]
            write(r'data\file_starter.json', json.dumps(self.data))

        self.edit_time.timeChanged.connect(set_time)
