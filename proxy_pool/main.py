# -*- coding:utf-8 -*-


from multiprocessing import Process
from Schedule.ProxyRefreshSchedule import run as RefreshRun
from Schedule.ProxyValidSchedule import run as ValidRun
from Api.ProxyApi import run as ProxyApiRun


def run():
    p_list = list()
    p1 = Process(target=ValidRun, name='ValidRun')
    p_list.append(p1)
    p2 = Process(target=RefreshRun, name='RefreshRun')
    p_list.append(p2)
    p3 = Process(target=ProxyApiRun, name='ProxyApiRun')
    p_list.append(p3)

    for p in p_list:
        p.daemon = True
        p.start()

    for p in p_list:
        p.join()


if __name__ == '__main__':
    run()
