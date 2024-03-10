from window.randoms.ui import *

data = json.loads(read(r'data\mainWindow.json'))


class randoms(ui):
    def __init__(self, mainWindow):
        super(randoms, self).__init__(mainWindow)

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
        for i in self.data['import']:
            item = widgets.QListWidgetItem(i)
            item.setFlags(item.flags() | core.Qt.ItemIsEditable)
            self.list.addItem(item)
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
                item_ = widgets.QListWidgetItem(get[0])
                item_.setFlags(item_.flags() | core.Qt.ItemIsEditable)
                self.list.addItem(item_)
            statistic()

        def delete():
            try:
                item_ = self.list.takeItem(self.list.currentRow())
                if item_ is not None:
                    del item_
                    del self.data['import'][self.list.currentRow()]
                    write(r'data\randoms.json', json.dumps(self.data))
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
                    for c in content:
                        item_ = widgets.QListWidgetItem(c)
                        item_.setFlags(item_.flags() | core.Qt.ItemIsEditable)
                        self.list.addItem(item_)
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
                    for c in content:
                        item_ = widgets.QListWidgetItem(c)
                        item_.setFlags(item_.flags() | core.Qt.ItemIsEditable)
                        self.list.addItem(item_)
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
