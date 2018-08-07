# -*- coding:utf-8 -*-

import requests
from wxpy import *
from threading import Timer

bot = Bot()


def get_news():
    """获取每日一句"""
    url = 'http://open.iciba.com/dsapi/'
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    print(content)
    print(note)
    return content, note


def send_news():
    try:
        contents = get_news()

        # 获取朋友的微信名称
        my_friend = bot.friends().search('acer')[0]
        my_friend.send(contents[0])
        my_friend.send(contents[1])
        my_friend.send(u'Have a good one!')

        # 每隔86400秒，发送一次
        t = Timer(86400, send_news)
        t.start()
    except:

        my_friend = bot.friends().search(u'治君')[0]
        my_friend.send(u'今天发送失败')


if __name__ == '__main__':
    send_news()
