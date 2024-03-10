import sys
import os
import random
import json
import time
import shutil
import webbrowser
import requests
import math

from PyQt5 import QtWidgets as widgets
from PyQt5 import QtCore as core
from PyQt5 import QtGui as gui
from PyQt5 import Qt


def create(filepath, content=''):
    if not os.path.exists(filepath):
        with open(filepath, 'w+', encoding='utf-8') as file:
            file.write(content)
        return False
    else:
        return True


def read(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def write(filepath, content=''):
    with open(filepath, 'w+', encoding='utf-8') as file:
        file.write(content)


def get_random():
    data = json.loads(read(r'data\randoms.json'))
    if data['way']:
        return str(random.randint(data['num'][0], data['num'][1]))
    else:
        try:
            result = random.choice(data['import'])
            if len(result) == 4 and result.upper() == result.lower():
                result = result[:2] + '\n' + result[-2:]
            return result
        except IndexError:
            return ''


def get_style():
    data = json.loads(read(r'data\mainWindow.json'))
    return read(r'data\static\style.qss').replace(
            '@BACKGROUND-IMAGE', data['background-image']
        ).replace(
            '@MAIN-COLOR', data['main-color']
        ).replace(
            '@WH', str(widgets.QDesktopWidget().screenGeometry().width() * 15 / 1920) + 'px'
        ).replace(
            '@SM-WH', str(widgets.QDesktopWidget().screenGeometry().width() * 12.5 / 1920) + 'px'
        ).replace(
            '@BG-WAY', data['bg_way']
        ).replace(
            '@OP+1', str(min((110 - data['widget_op']) / 100, 1))
        ).replace(
            '@OP+2', str(min((120 - data['widget_op']) / 100, 1))
        ).replace(
            '@OP', str((100 - data['widget_op']) / 100)
    )


class QPushButton(widgets.QPushButton):
    def __init__(self, parent=None):
        super(QPushButton, self).__init__(parent)
        self.setCursor(Qt.Qt.PointingHandCursor)


widgets.QPushButton = QPushButton
