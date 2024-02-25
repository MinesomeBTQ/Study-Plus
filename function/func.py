import os
import random
import json
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon


def create(filepath, content=''):
    if not os.path.exists(filepath):
        with open(filepath, 'w+', encoding='utf-8') as file:
            file.write(content)


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
