# -*- coding:utf-8 -*-


import redis
import json
import random
from Util.EnvUtil import *


class RedisClient(object):
    """
    reids client
    """

    def __init__(self, name, host, port):
        self.name = name
        self.__conn = redis.Redis(host=host, port=port, db=0)

    def get(self, key):
        if key:
            rkey = self.__conn.hgetall(self.name, key)
            if isinstance(rkey, bytes):
                return rkey.decode('utf-8')
            else:
                return rkey
        else:
            keys = self.__conn.hgetall(self.name)
            # return random.choice(key.keys()) if key else None
            # key.keys()在python3中返回dict_keys，不支持index，不能直接使用random.choice
            # 另：python3中，redis返回为bytes,需要解码
            rkey = random.choice(list(keys.keys())) if keys else None

            if isinstance(rkey, bytes):
                return rkey.decode('utf-8')
            else:
                return rkey

    def put(self, key):
        key = json.dumps(key) if isinstance(key, (dict, list)) else key
        return self.__conn.hincrby(self.name, key, 1)

    def getvalue(self, key):
        value = self.__conn.hget(self.name, key)
        return value if value else None

    def pop(self):
        key = self.get()
        if key:
            self.__conn.hdel(self.name, key)

        return key

    def delete(self, key):
        self.__conn.hdel(self.name, key)

    def inckey(self, key, value):
        self.__conn.hincrby(self.name, key, value)

    def getAll(self):
        # return self.__conn.hgetall(self.name).keys()
        # python3 redis返回bytes类型,需要解码
        if PY3:
            return [key.decode('utf-8') for key in self.__conn.hgetall(self.name).keys()]
        else:
            return self.__conn.hgetall(self.name).keys()

    def get_status(self):
        return self.__conn.hlen(self.name)

    def changeTable(self, name):
        self.name = name


if __name__ == '__main__':
    redis_con = RedisClient('proxy', '127.0.0.1', 6379)
    # redis_con.put('abc')
    # redis_con.put('123')
    # redis_con.put('123.115.235.221:8800')
    # redis_con.put(['123', '115', '235.221:8800'])
    print(redis_con.getAll())
    # redis_con.delete('abc')
    # print(redis_con.getAll())

    # print(redis_con.getAll())
    # redis_con.changeTable('raw_proxy')
    # redis_con.pop()

    # redis_con.put('132.112.43.221:8888')
    # redis_con.changeTable('proxy')
    # print(redis_con.get_status())
    # print(redis_con.getAll())
