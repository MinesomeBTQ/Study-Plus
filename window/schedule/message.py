from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class message(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(message, self).__init__()
        self.class_name = ''
        self.mainWindow = mainWindow
        self.setObjectName('mainWindow')
        self.setWindowTitle('课程提醒')
        self.setWindowIcon(gui.QIcon('data/images/favicon.ico'))

        def shadow(_, __):
            effect = widgets.QGraphicsDropShadowEffect(self)
            effect.setColor(gui.QColor('#FFFFFF'))
            effect.setBlurRadius(_)
            effect.setOffset(__)
            return effect

        self.txt_top = widgets.QLabel(self)
        self.txt_bottom = widgets.QLabel(self)
        self.txt_center = widgets.QLabel(self)
        self.close_btn = widgets.QPushButton(self)

        self.txt_top.setGraphicsEffect(shadow(3, 1))
        self.txt_bottom.setGraphicsEffect(shadow(3, 1))
        self.txt_center.setGraphicsEffect(shadow(3, 1))
        self.txt_top.setAlignment(core.Qt.AlignBottom | core.Qt.AlignHCenter)
        self.txt_bottom.setAlignment(core.Qt.AlignTop | core.Qt.AlignHCenter)
        self.txt_center.setAlignment(core.Qt.AlignCenter)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setText('关闭')

        self.screen().logicalDotsPerInchChanged.connect(self.setupUI)
        self.resizeEvent = self.setupUI

        self.loadStyle()

    def loadStyle(self):
        global data
        data = json.loads(read(r'data\mainWindow.json'))
        self.setStyleSheet(get_style())

    def setupUI(self, evt=None):
        screen = widgets.QDesktopWidget().screenGeometry()
        wh = 600
        w, h = screen.width() * wh / 1920, screen.height() * wh / 1080
        if type(evt) is float or evt is None:
            self.setFixedSize(int(w), int(h))
        dpi = self.screen().logicalDotsPerInch() / 96
        self.setFixedSize(
            int(widgets.QDesktopWidget().screenGeometry().width() * 600 / 1920),
            int(widgets.QDesktopWidget().screenGeometry().height() * 600 / 1080))

        def font(size_):
            f = gui.QFont()
            f.setPointSizeF(
                (size_ * w / (wh * dpi) + size_ * h / (wh * dpi)) / 2)
            return f

        w, h = self.width(), self.height()
        size = lambda x1, y1, x2, y2: core.QRect(int(x1 * w / wh), int(y1 * h / wh),
                                                 int(x2 * w / wh), int(y2 * h / wh))

        self.txt_top.setGeometry(size(100, 0, 400, 100))
        self.txt_bottom.setGeometry(size(100, 350, 400, 100))
        self.txt_center.setGeometry(size(0, 100, 600, 250))
        self.close_btn.setGeometry(size(225, 475, 150, 75))

        self.txt_top.setFont(font(20))
        self.txt_bottom.setFont(font(20))
        self.txt_center.setFont(font(int(120/max(math.sqrt(len(self.class_name.encode())/3), 1))))
        self.close_btn.setFont(font(20))

    def showEvent(self, a0):
        self.txt_center.setFocus()
        data_func = json.loads(read(r'data\schedule_func.json'))
        self.txt_top.setText(data_func['text'].split('@N')[0])
        self.txt_bottom.setText(data_func['text'].split('@N')[1])
        self.txt_center.setText(self.class_name)

    def closeEvent(self, evt):
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), int(newTop))
        """
        if self.mainWindow.isVisible():
            evt.accept()
        else:
            self.hide()
            evt.ignore()
