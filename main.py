from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
import sys
import json
import os
from function import func


if __name__ == '__main__':
    # core.QCoreApplication.setAttribute(core.Qt.AA_EnableHighDpiScaling)
    app = widgets.QApplication(sys.argv)
    app.path = os.path.basename(__file__)
    app.setStyleSheet(func.read(r'data\static\menu.qss'))
    from window import mainWindow
    window = mainWindow.mainWindow(app)
    try:
        if not json.loads(func.read(r'data\mainWindow.json'))['hide']:
            window.show()
        else:
            window.close()
    except FileNotFoundError:
        window.show()
    sys.exit(app.exec_())
