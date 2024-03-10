from window.schedule.ui import *
from window.schedule.message import *
from function.func import *

data = json.loads(read(r'data\mainWindow.json'))


class schedule(ui):
    def __init__(self, mainWindow):
        super(schedule, self).__init__(mainWindow)

    def initUI(self):
        def f5table():
            self.table.setColumnCount(8)
            self.table.setAlternatingRowColors(True)
            self.table.horizontalHeader().setSectionResizeMode(widgets.QHeaderView.Stretch)
            self.table.verticalHeader().setSectionResizeMode(widgets.QHeaderView.Stretch)
            self.table.setSelectionBehavior(widgets.QAbstractItemView.SelectItems)
            # self.table.setEditTriggers(widgets.QAbstractItemView.NoEditTriggers)

            def num2cn(num_):
                num2cn_list_t = {1: "十", 2: "二十", 3: "三十", 4: "四十", 5: "五十", 6: "六十", 7: "七十", 8: "八十", 9: "九十", 0: ""}
                num2cn_list = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九", 0: ""}
                return f'{num2cn_list_t[int(num_ // 10)] + num2cn_list[int(num_ % 10)]}'

            num = self.data_func['class_num']
            self.table.setRowCount(num)
            self.table.setHorizontalHeaderLabels(
                ['开始时间', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'])
            self.table.setVerticalHeaderLabels(
                [f'第{num2cn(i)}节' for i in range(1, num+1)])
            for r, ri in zip(self.data.keys(), range(8)):

                try:
                    for c, ci in zip(list(self.data.values())[ri].values(), range(num)):
                        item = widgets.QTableWidgetItem(c)
                        item.setTextAlignment(core.Qt.AlignCenter)
                        self.table.setItem(ci, ri, item)
                except AttributeError:
                    for i in range(num):
                        time_item = widgets.QTimeEdit(self)
                        time_item.setDisplayFormat("hh:mm:ss")
                        time_item.setObjectName(str(i))
                        time_item.setTime(core.QTime(self.data['time'][i][0], self.data['time'][i][1], self.data['time'][i][2]))

                        def set_time():
                            item_ = self.sender()
                            time_ = [item_.time().hour(), item_.time().minute(), item_.time().second()]
                            self.data['time'][int(item_.objectName())] = time_
                            write(r'data\\schedule.json', json.dumps(self.data))

                        time_item.timeChanged.connect(set_time)
                        self.table.setCellWidget(i, ri, time_item)

            def set_table(row, col):
                self.data[str(col)][str(row)] = self.table.item(row, col).text()
                write(r'data\schedule.json', json.dumps(self.data))

            self.table.cellChanged.connect(set_table)

        f5table()

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

        self.txt_3.setText('课程数量：')
        self.edit_class_num.setRange(5, 99)
        self.edit_class_num.setValue(self.data_func['class_num'])

        def edit_class_num():
            class_num = self.edit_class_num.value()
            data_num = self.data_func['class_num']
            if class_num > data_num:
                for i in range(0, class_num-data_num):
                    try:
                        self.data['time'][data_num+i]
                    except IndexError:
                        self.data['time'].append([0, 0, 0])
                    for col in tuple(self.data.keys())[1:]:
                        try:
                            self.data[col][str(data_num+i)]
                        except KeyError:
                            self.data[col][str(data_num+i)] = ""
            if class_num != data_num:
                self.data_func['class_num'] = class_num
                write(r'data\schedule.json', json.dumps(self.data))
                write(r'data\schedule_func.json', json.dumps(self.data_func))
                f5table()

        self.edit_class_num.editingFinished.connect(edit_class_num)
