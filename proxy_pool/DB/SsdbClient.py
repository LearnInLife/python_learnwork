# -*- coding:utf-8 -*-

from Util.EnvUtil import *

from redis.connection import BlockingConnectionPool
import redis
import random


class SsdbClient(object):
    """
       SSDB client
       SSDB中代理存放的容器为hash：
           原始代理存放在name为raw_proxy的hash中，key为代理的ip:port，value为为None,以后扩展可能会加入代理属性；
           验证后的代理存放在name为useful_proxy的hash中，key为代理的ip:port，value为一个计数,初始为1，每校验失败一次减1；
    """

    def __init__(self, name, host, port):
        self.name = name
        self.__conn = redis.Redis(connection_pool=BlockingConnectionPool(host=host, port=port))

    def get(self, proxy):
        data = self.__conn.hget(self.name, key=proxy)

        if data:
            return data.decode('utf-8') if PY3 else data
        else:
            return None

    def put(self, key, num=1):
        data = self.__conn.hset(self.name, key, num)
        return data

    def delete(self, key):
        self.__conn.hdel(self.name, key)

    def update(self, key, value):
        self.__conn.hincrby(self.name, key, value)

    def pop(self):
        keys = self.__conn.hkeys(self.name)
        if keys:
            proxy = random.choice(keys)
            value = self.__conn.hget(self.name, proxy)
            self.delete(proxy)
            return {
                'proxy': proxy.decode('utf-8') if PY3 else proxy,
                'value': value.decode('utf-8') if PY3 and value else None,
            }
        return None

    def exists(self, key):
        return self.__conn.hexists(self.name, key)

    def getAll(self):
        item_dics = self.__conn.hgetall(self.name)
        if PY3:
            return {
                key.decode('utf-8'): value.decode('utf-8') for key, value in item_dics.items()
            }
        else:
            return item_dics

    def getNumber(self):
        return self.__conn.hlen(self.name)

    def changeTable(self, name):
        self.name = name
