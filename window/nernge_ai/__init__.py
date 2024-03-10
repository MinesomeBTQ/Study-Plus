from function.func import *
from function.ai import *
from window.nernge_ai.ui import *

data = json.loads(read(r'data\mainWindow.json'))


class ai(ui):
    def __init__(self, mainWindow):
        super(ai, self).__init__(mainWindow)

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

        class react(core.QThread):
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
            receive_message = self.input.toPlainText()
            if receive_message:
                self.message.setMarkdown('...')
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
