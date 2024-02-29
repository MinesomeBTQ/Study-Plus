import json
import os
import openai
from function.func import *


def chat(content, history_message='', setting=''):
    api_key = json.loads(read(r'data\nernge_ai.json'))['api-key']
    if not api_key:
        api_key = ""  # API Key，请自行替换
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1",
    )

    try:
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {
                    "role": "system",
                    "content": "你是 Nernge AI，由 BT.Q"
                               "提供的人工智能助手，目前在 Study Plus (项目地址 https://gitee.com/Nernge/studyplus) 上运行， "
                               "你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一些涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Nernge AI"
                               "为专有名词，不可翻译成其他语言。为了方便阅读，你输出的内容可以为Markdown格式或TML格式，它会被翻译并显示给我。"
                               + "\n" + setting + "\n" + history_message,
                },
                {"role": "user", "content": content},
            ],
            temperature=0.3,
            stream=True,
        )
    except openai.APIConnectionError:
        yield '## 连接错误，请检查互联网连接', ''
        return '## 连接错误，请检查互联网连接', ''
    except Exception as e:
        error = eval(e.args[0][18:])['error']
        if error['message'] == 'auth failed':
            out = ('## 您设置的api-key有误', '')
        elif error['type'] == 'rate_limit_reached_error':
            out = ('## 您的对话太频繁了。请稍等。', 'time.sleep(3)')
        elif error['type'] == 'exceeded_current_quota_error':
            out = ("## AI额度不足\n请前往 [帮助文档](https://gitee.com/Nernge/studyplus/blob/master/Help.md) 解决", '')
        else:
            out = ("出现错误：" + str(e) + (
                "\n\n可能是 **AI额度不足** ，请前往 [帮助文档](https://gitee.com/Nernge/studyplus/blob/master/Help"
                ".md) 解决"), '')
        yield out
        return out
    collected_messages = []
    for idx, chunk in enumerate(response):
        chunk_message = chunk.choices[0].delta
        if not chunk_message.content:
            continue
        collected_messages.append(chunk_message)
        yield ''.join([m.content for m in collected_messages]), ''
