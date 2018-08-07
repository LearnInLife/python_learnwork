# -*- coding:utf-8 -*-

from Manager.ProxyManager import ProxyManager
from Util.LogHandler import LogHandler
from Util.UtilFunction import validUsefulProxy
from threading import Thread
from apscheduler.schedulers.blocking import BlockingScheduler

import time


class ProxyRefreshSchedule(ProxyManager):
    """
    代理定时刷新
    """

    def __init__(self):
        super(ProxyRefreshSchedule, self).__init__()
        self.log = LogHandler('refresh_schedule')

    def validProxy(self):
        """
        验证raw_proxy中的代理，将可用的代理放入useful_proxy中
        :return:
        """
        self.db.changeTable(self.raw_proxy_queue)
        raw_proxy_item = self.db.pop()
        self.log.info('proxyrefreshschedule: %s start validProxy' % time.ctime())
        # 已经验证过的代理集合
        remaining_proxies = self.getAll()
        while raw_proxy_item:
            raw_proxy = raw_proxy_item.get('proxy')
            if isinstance(raw_proxy, bytes):
                raw_proxy = raw_proxy.decode('utf8')

            if (raw_proxy not in remaining_proxies) and validUsefulProxy(raw_proxy):
                self.db.changeTable(self.useful_proxy_queue)
                self.db.put(raw_proxy)
                self.log.info('raw_proxy %s validation pass' % raw_proxy)
            else:
                self.log.info('raw_proxy %s validation fail' % raw_proxy)
            self.db.changeTable(self.raw_proxy_queue)
            raw_proxy_item = self.db.pop()
            remaining_proxies = self.getAll()
        self.log.info('proxyrefreshschedule: %s validProxy complete' % time.ctime())


def refreshPool():
    pp = ProxyRefreshSchedule()
    pp.validProxy()


def main(process_num=30):
    p = ProxyRefreshSchedule()
    # 获取代理
    p.refresh()

    # 检验新代理
    pl = []
    for num in range(process_num):
        proc = Thread(target=refreshPool, args=())
        pl.append(proc)

    for num in range(process_num):
        pl[num].daemon = True
        pl[num].start()

    for num in range(process_num):
        pl[num].join()


def run():
    main()
    sch = BlockingScheduler()
    sch.add_job(main, 'interval', minutes=10)  # 每10分钟抓取一次
    sch.start()


if __name__ == '__main__':
    run()
