# -*- coding:utf-8 -*-

import os
import logging
from logging.handlers import TimedRotatingFileHandler

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')


class LogHandler(logging.Logger):

    def __init__(self, name, level=logging.DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        super(LogHandler, self).__init__(name, level)

        if stream:
            self.__setStreamHandler__()

        if file:
            self.__setFileHandler__()

    def __setStreamHandler__(self, level=None):

        stream_handler = logging.StreamHandler()
        # 设置格式
        formatter = logging.Formatter('%(asctime)s: %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        # 告诉handler使用这个格式
        stream_handler.setFormatter(formatter)
        if level:
            stream_handler.setLevel(level)
        else:
            stream_handler.setLevel(self.level)
        self.addHandler(stream_handler)

    def __setFileHandler__(self, level=None):

        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))
        # 设置定时循环日志，保存在log目录，一天保存一个文件，保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
        file_handler.suffix = '%Y%m%d.log'
        if level:
            file_handler.setLevel(level)
        else:
            file_handler.setLevel(self.level)

        formatter = logging.Formatter('%(asctime)s: %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def resetName(self, name):
        self.name = name
        self.removeHandler(self.file_handler)
        self.__setFileHandler__()


if __name__ == '__main__':
    log = LogHandler('test')
    log.info('this is test msg')
