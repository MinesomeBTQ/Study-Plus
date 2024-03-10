from function import setting_file
from function.func import *


if __name__ == '__main__':
    # core.QCoreApplication.setAttribute(core.Qt.AA_EnableHighDpiScaling)
    app = widgets.QApplication(sys.argv)
    app.path = os.path.basename(__file__)
    app.setStyleSheet(read(r'data\static\menu.qss').replace(
            '@WH', str(int(widgets.QDesktopWidget().screenGeometry().width() * 10 / 1920)) + 'px'
        ).replace(
            '@SM-WH', str(int(widgets.QDesktopWidget().screenGeometry().width() * 5 / 1920)) + 'px')
    )
    from window import mainWindow
    window = mainWindow.mainWindow(app)
    try:
        if not json.loads(read(r'data\mainWindow.json'))['hide']:
            window.show()
        else:
            window.close()
    except FileNotFoundError:
        window.show()
    sys.exit(app.exec_())
