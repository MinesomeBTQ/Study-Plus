import os

from function.func import *
from window.setting.ui import *

data = json.loads(read(r'data\mainWindow.json'))


class setting(ui):
    def __init__(self, mainWindow):
        super(setting, self).__init__(mainWindow)

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
        self.bg_show_way.setText('背景显示方式：')
        self.bg_show_way_background.setText('平铺')
        self.bg_show_way_border.setText('拉伸')
        self.txt_widget_op.setText('控件透明度 - %：')

        self.bg_show_way_background.setChecked(True if data['bg_way'] == 'background-image' else False)
        self.bg_show_way_border.setChecked(True if data['bg_way'] == 'border-image' else False)

        def set_way():
            data['bg_way'] = 'background-image' if self.bg_show_way_background.isChecked() else 'border-image'
            write(r'data\mainWindow.json', json.dumps(data))
            self.mainWindow.loadStyle()

        self.bg_show_way_background.clicked.connect(set_way)
        self.bg_show_way_border.clicked.connect(set_way)

        self.widget_op.setRange(0, 100)
        self.widget_op.setValue(100 - data['widget_op'])

        def set_widget_op():
            data['widget_op'] = 100 - self.widget_op.value()
            write(r'data\mainWindow.json', json.dumps(data))
            self.mainWindow.loadStyle()

        self.widget_op.editingFinished.connect(set_widget_op)

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
                    os.remove(rf'data\images\{self.bg_list["自定义背景"]}')
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
            '<a href="https://gitee.com/Nernge/studyplus/blob/master/Help.md" style="color: #666666;">获取 Nernge AI '
            '使用帮助</a>')
        self.help.setOpenExternalLinks(True)

        self.set_ai.setTitle('设置 API-Key')
        self.edit_ai.setText(self.ai_data['api-key'])

        def edit_ai():
            self.ai_data['api-key'] = self.edit_ai.text()
            write(r'data\nernge_ai.json', json.dumps(self.ai_data))

        self.edit_ai.textChanged.connect(edit_ai)

        self.set_setting.setTitle('设置 AI 默认设定')
        self.edit_setting.setText(self.ai_data['setting'])

        def edit_setting():
            self.ai_data['setting'] = self.edit_setting.toPlainText()
            write(r'data\nernge_ai.json', json.dumps(self.ai_data))

        self.edit_setting.textChanged.connect(edit_setting)
