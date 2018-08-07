# -*- coding:utf-8 -*-

from Manager.ProxyManager import ProxyManager
from Schedule.ProxyCheck import ProxyCheck
from queue import Queue
import time


class ProxyValidSchedule(ProxyManager):

    def __init__(self):
        super(ProxyValidSchedule, self).__init__()
        self.queue = Queue()
        self.proxy_item = dict()

    def __validProxy(self, threads=10):
        """
        验证useful_proxy代理
        :param threads:
        :return:
        """
        thread_list = list()
        for index in range(threads):
            thread_list.append(ProxyCheck(self.queue, self.proxy_item))

        for thread in thread_list:
            thread.daemon = True
            thread.start()

        for thread in thread_list:
            thread.join()

    def putQueue(self):
        self.db.changeTable(self.useful_proxy_queue)
        self.proxy_item = self.db.getAll()
        print('useful_proxy:',self.proxy_item)
        for item in self.proxy_item:
            self.queue.put(item)

    def main(self):
        self.putQueue()
        while True:
            if not self.queue.empty():
                self.log.info('start valid useful proxy')
                self.__validProxy()
            else:
                self.log.info('valid complete! sleep 5 minutes')
                time.sleep(5 * 60)
                self.putQueue()


def run():
    p = ProxyValidSchedule()
    p.main()


if __name__ == '__main__':
    run()
