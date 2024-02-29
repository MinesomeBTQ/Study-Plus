import json

from function.func import *

init_setting = {
    r"data\mainWindow.json": {"background-image": "bg_blue.png", "main-color": "#1e9fff", "opacity": 80,
                              "width-height": 60, "hide": False, "toolbox": True},
    r'data\randoms.json': {"way": True, "num": [0, 50], "import": []},
    r'data\file_starter.json': {"func": True, "time": [0, 0, 0], "file": ""},
    r'data\schedule.json': {"time": [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                     [0, 0, 0], [0, 0, 0]], "1": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "",
                                                                  "6": "", "7": "", "8": ""},
                            "2": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "",
                                  "6": "", "7": "", "8": ""},
                            "3": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "",
                                  "6": "", "7": "", "8": ""},
                            "4": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "",
                                  "6": "", "7": "", "8": ""},
                            "5": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "",
                                  "6": "", "7": "", "8": ""},
                            "6": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "",
                                  "6": "", "7": "", "8": ""},
                            "7": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "",
                                  "6": "", "7": "", "8": ""}},
    r'data\schedule_func.json': {"text": "各位同学@N课要开始了，请大家做好准备", "message": [True, True]},
    r'data\nernge_ai.json': {"api-key": "", "setting": ""},
    r'data\static\color.json': {"未来科技蓝": "#1e9fff", "活力橙": "#ff5722", "学习绿": "#39C839", "简约灰": "#aaaaaa",
                                "古典红": "#87362b", "山水青": "#598AAA", "经典黑": "#333333", "自定义颜色": "#333333"},
    r'data\static\bg.json': {"未来科技蓝": "bg_blue.png", "活力橙": "bg_orange.png", "学习绿": "bg_green.png",
                             "简约灰": "bg_gray.png", "古典红": "bg_red.jpg", "现代深": "bg_black.jpg", "山水": "bg_mountain.png",
                             "纯白": "bg_white.png", "自定义背景": "bg_white.png"}
}

for filepath, data in zip(init_setting.keys(), init_setting.values()):
    if create(filepath, json.dumps(data)):
        old_data = json.loads(read(filepath))
        if old_data != data:
            for key, value in zip(data.keys(), data.values()):
                if key not in old_data:
                    old_data[key] = value
                key_need_del = []
                for old_key in old_data:
                    if old_key not in data.keys():
                        key_need_del.append(old_key)
                for key_del in key_need_del:
                    del old_data[key_del]
            with open(filepath, 'w+', encoding='utf-8') as file:
                file.write(json.dumps(old_data))

# mainWindow.json
# randoms.json
# file_starter.json
# schedule.json
# schedule_func.json
