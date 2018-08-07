# -*- coding: utf-8 -*-

from DB.DbClient import DbClient
from Util.GetConfig import GetConfig
from Util.LogHandler import LogHandler
from Util.UtilFunction import verifyProxyFormat
from ProxyGetter.GetFreeProxy import GetFreeProxy
from Util import EnvUtil
import random


class ProxyManager(object):

    def __init__(self):
        self.db = DbClient()
        self.config = GetConfig()
        self.raw_proxy_queue = 'raw_proxy'
        self.log = LogHandler('proxy_manager')
        self.useful_proxy_queue = 'useful_proxy'

    def refresh(self):
        """
        抓取代理地址存入DB中
        :return:
        """
        for proxyGetter in self.config.proxy_getter_functions:
            proxy_set = set()

            try:
                self.log.info("{func}:fetch proxy start".format(func=proxyGetter))
                proxy_iter = [_ for _ in getattr(GetFreeProxy, proxyGetter.strip())()]
            except Exception as e:
                self.log.error("{func}:fetch proxy fail".format(func=proxyGetter))
                continue
            for proxy in proxy_iter:
                proxy = proxy.strip()
                if proxy and verifyProxyFormat(proxy):
                    self.log.info("{func}:fetch proxy {proxy}".format(func=proxyGetter, proxy=proxy))
                    proxy_set.add(proxy)
                else:
                    self.log.info("{func}:fetch proxy {proxy} error".format(func=proxyGetter, proxy=proxy))

            # 存储到DB
            for proxy in proxy_set:
                self.db.changeTable(self.useful_proxy_queue)
                if self.db.exists(proxy):
                    continue
                self.db.changeTable(self.raw_proxy_queue)
                self.db.put(proxy)

    def get(self):
        """
        返回一个有用的代理
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        item_dict = self.db.getAll()
        if item_dict:
            if EnvUtil.PY3:
                return random.choice(list(item_dict.keys()))
            else:
                return random.choice(item_dict.keys())
        return None

    def delete(self, proxy):
        self.db.changeTable(self.useful_proxy_queue)
        self.db.delete(proxy)

    def getAll(self):
        self.db.changeTable(self.useful_proxy_queue)
        items = self.db.getAll()
        if EnvUtil.PY3:
            return list(items.keys()) if items else list()
        return items.key() if items else list()

    def getNumber(self):
        self.db.changeTable(self.raw_proxy_queue)
        total_raw_proxy = self.db.getNumber()
        self.db.changeTable(self.useful_proxy_queue)
        total_useful_proxy = self.db.getNumber()
        return {
            'raw_proxy': total_raw_proxy,
            'useful_proxy': total_useful_proxy
        }


if __name__ == "__main__":
    pp = ProxyManager()
    pp.refresh()
