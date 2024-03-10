from function.func import *
from function.ai import *

data = json.loads(read(r'data\mainWindow.json'))


class ui(widgets.QMainWindow):
    def __init__(self, mainWindow):
        super(ui, self).__init__()
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

    def closeEvent(self, evt):
        if self.mainWindow.isVisible():
            evt.accept()
        else:
            self.hide()
            evt.ignore()
