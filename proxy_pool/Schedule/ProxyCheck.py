# -*- coding:utf-8 -*-

from Manager.ProxyManager import ProxyManager
from threading import Thread
from Util.LogHandler import LogHandler
from Util.UtilFunction import validUsefulProxy

FAIL_COUNT = 1  # 校验失败次数，超过就删除代理


class ProxyCheck(ProxyManager, Thread):

    def __init__(self, queue, item_dict):
        ProxyManager.__init__(self)
        Thread.__init__(self)
        self.log = LogHandler('proxy_check', file=False)
        self.queue = queue
        self.item_dict = item_dict

    def run(self):
        self.db.changeTable(self.useful_proxy_queue)
        while self.queue.qsize():
            proxy = self.queue.get()
            count = self.item_dict[proxy]
            if validUsefulProxy(proxy):
                # 验证通过计数器减1
                if count and int(count) > 0:
                    self.db.put(proxy, num=int(count) - 1)

                self.log.info('proxycheck:{} validation pass'.format(proxy))
            else:
                self.log.info('proxycheck:{} validation fail'.format(proxy))
                if count and int(count) + 1 >= FAIL_COUNT:
                    self.log.info('proxycheck:{} fial too many,delete'.format(proxy))
                    self.db.delete(proxy)
                else:
                    self.db.put(proxy, num=int(count) - 1)
            self.queue.task_done()
