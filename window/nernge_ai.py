import os

from PyQt5 import Qt
from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui
import json
import time
import shutil

from function.func import *
from function.ai import *

data = json.loads(read(r'data\mainWindow.json'))


class ai(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(ai, self).__init__()
        self.message_ = None
        self.setWindowTitle('Nernge AI')
        self.setWindowIcon(gui.QIcon('data/images/favicon.ico'))
        self.setObjectName('mainWindow')
        self.loadStyle()

        self.input = widgets.QTextEdit(self)
        self.send = widgets.QPushButton(self)
        self.clear = widgets.QPushButton(self)
        self.message_box = widgets.QWidget(self)
        self.message_user_box = widgets.QWidget(self)
        self.icon = widgets.QLabel(self.message_box)
        self.title = widgets.QLabel(self.message_box)
        self.message = widgets.QTextBrowser(self.message_box)
        self.icon_user = widgets.QLabel(self.message_user_box)
        self.title_user = widgets.QLabel(self.message_user_box)
        self.message_user = widgets.QTextEdit(self.message_user_box)
        self.prior = widgets.QPushButton(self)
        self.next = widgets.QPushButton(self)

        self.mainWindow = mainWindow  # 主窗口类
        self.w = 800
        self.h = 600
        self.history = []
        self.cursor = -1
        self.act = None

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
            '@WH', str(int(widgets.QDesktopWidget().screenGeometry().width() * 15 / 1920)) + 'px'
        ))

    def initUI(self):
        self.input.setPlaceholderText('Ctrl + Enter 发送')

        self.send.setText('发送')
        self.clear.setText('清空上下文记忆')

        def clear():
            self.history = []
            self.cursor = -1
            self.act = None
            self.do_act()
            self.message_user.setPlainText('')
            self.message.setMarkdown('')
            widgets.QMessageBox.information(self, '清空上下文记忆', '已清空上下文记忆')

        self.clear.clicked.connect(clear)

        self.prior.setText('▲')
        self.next.setText('▼')

        self.do_act()

        def prior():
            self.act = True
            self.do_act()

        def next_():
            self.act = False
            self.do_act()

        self.prior.clicked.connect(prior)
        self.next.clicked.connect(next_)

        class react(QThread):
            signal = core.pyqtSignal(str)

            def __init__(self):
                super().__init__()
                self.message = ''
                self.history_message = ''

            def setMessage(self, message, history_message=''):
                self.message = message
                self.history_message = history_message

            def run(self):
                self.signal.emit('@Start')
                message_out = ''
                for i in chat(self.message, self.history_message, json.loads(read(r'data\nernge_ai.json'))['setting']):
                    self.signal.emit(i[0])
                    time.sleep(0.0001)
                    message_out = i[0]
                    exec(i[1])
                self.signal.emit('@Quit' + message_out)
                self.quit()

        react_ = react()
        react_.signal.connect(self.setMessage)

        def send_message():
            self.message.setMarkdown('...')
            receive_message = self.input.toPlainText()
            if receive_message:
                receive_message_temp = '以上是我们此前的对话记录：\n'
                for i in self.history:
                    user_, ai_ = i[0], i[1]
                    receive_message_temp += '我说：' + user_ + '\n你回答：' + ai_ + '\n'
                # receive_message_temp += '此对话记录是为了让你了解上下文内容，请不要在回答中提到与此相关的内容\n以下是我的正式对话内容：' + receive_message
                self.input.setText('')
                self.message_user.setPlainText(receive_message)
                react_.setMessage(receive_message, receive_message_temp)
                react_.start()
                self.message_ = receive_message

        self.send.clicked.connect(send_message)
        shortcut = gui.QKeySequence("Ctrl+Return")
        self.send.setShortcut(shortcut)

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

        self.input.setGeometry(size(50, 450, 700, 100))
        self.send.setGeometry(size(690, 515, 50, 25))
        self.clear.setGeometry(size(585, 515, 100, 25))
        self.prior.setGeometry(size(720, 320, 30, 30))
        self.next.setGeometry(size(720, 360, 30, 30))

        self.input.setFont(font(10))
        self.send.setFont(font(9))
        self.clear.setFont(font(9))
        self.prior.setFont(font(9))
        self.next.setFont(font(9))

        pixmap = gui.QPixmap('data/images/ai.png')
        pixmap.scaled(35, 35, core.Qt.IgnoreAspectRatio, core.Qt.SmoothTransformation)

        def shadow(_, __):
            effect = widgets.QGraphicsDropShadowEffect(self)
            effect.setColor(gui.QColor('#FFFFFF'))
            effect.setBlurRadius(_)
            effect.setOffset(__)
            return effect

        self.icon.setPixmap(pixmap)
        self.icon.setScaledContents(True)
        self.icon.setGeometry(size(0, 0, 35, 35))
        self.title.setText('Nernge AI - BT.Q')
        self.title.setGraphicsEffect(shadow(3, 1))
        self.title.setFont(font(12))
        self.title.setGeometry(size(40, 0, 410, 35))
        self.message.setGeometry(size(40, 35, 410, 210))
        self.message.setFont(font(10))
        self.message.setReadOnly(True)
        self.message.setObjectName('ReadOnly')
        self.message.setOpenExternalLinks(True)
        self.message.setMarkdown('''
## 你好！有什么可以帮助你的吗？
作为 **Nernge AI**，我可以提供多种功能来帮助你。以下是我可以做的一些事情：

**语言理解与交流**：我能够理解和回答中文和英文的问题，进行流畅的对话。

**信息检索**：我可以帮助你查找信息，无论是一般知识、新闻更新还是特定主题的资料。

**学习辅导**：如果你在学习中遇到困难，我可以提供解释和辅导，涵盖多个学科领域。

**生活建议**：我可以提供旅行建议、健康小贴士、饮食建议等日常生活相关的信息。

**技术支持**：如果你在使用电子设备或软件时遇到问题，我可以提供技术支持和故障排除建议。

**娱乐互动**：我可以参与轻松的对话，讲笑话，甚至参与一些简单的游戏。

**日程管理**：虽然我不能直接管理你的日程，但我可以提供建议和提醒，帮助你更好地规划时间。

**文本生成**：我可以帮助撰写或编辑文本，例如撰写邮件、报告或创意写作。

请注意，我会遵守道德和法律标准，拒绝回答涉及不当内容的问题。如果你有任何问题或需要帮助，随时可以告诉我！''')

        pixmap = gui.QPixmap('data/images/user.png')
        pixmap.scaled(35, 35, core.Qt.IgnoreAspectRatio, core.Qt.SmoothTransformation)
        self.icon_user.setPixmap(pixmap)
        self.icon_user.setScaledContents(True)
        self.icon_user.setGeometry(size(215, 0, 35, 35))
        self.title_user.setGeometry(size(0, 0, 210, 35))

        self.title_user.setText('我')
        self.title_user.setGraphicsEffect(shadow(3, 1))
        self.title_user.setAlignment(core.Qt.AlignRight | core.Qt.AlignVCenter)
        self.title_user.setFont(font(12))
        self.message_user.setGeometry(size(5, 35, 210, 60))
        self.message_user.setFont(font(10))
        self.message_user.setReadOnly(True)
        self.message_user.setObjectName('ReadOnly')

        self.message_box.setGeometry(size(50, 150, 450, 250))
        self.message_user_box.setGeometry(size(500, 50, 250, 100))

    def setMessage(self, message):
        if message == '@Start':
            self.send.setEnabled(False)
        elif message[:5] == '@Quit':
            self.history += [(self.message_, message[5:])]
            self.send.setEnabled(True)
            self.cursor += 1
            self.act = None
            self.do_act()
        else:
            self.message.setMarkdown(message)

    def do_act(self):
        if self.act is None:
            if self.cursor <= 0:
                self.prior.setEnabled(False)
            else:
                self.prior.setEnabled(True)
            if self.cursor >= len(self.history) - 1:
                self.next.setEnabled(False)
            else:
                self.next.setEnabled(True)
        else:
            if self.act:
                self.cursor -= 1
            else:
                self.cursor += 1
            if self.cursor == 0:
                self.prior.setEnabled(False)
            else:
                self.prior.setEnabled(True)
            if self.cursor == len(self.history) - 1:
                self.next.setEnabled(False)
            else:
                self.next.setEnabled(True)
            self.message.setMarkdown(self.history[self.cursor][1])
            self.message_user.setPlainText(self.history[self.cursor][0])

    def closeEvent(self, evt):
        if self.mainWindow.isVisible():
            evt.accept()
        else:
            self.hide()
            evt.ignore()
