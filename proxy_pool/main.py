# -*- coding:utf-8 -*-


from multiprocessing import Process
from Schedule.ProxyRefreshSchedule import run as RefreshRun
from Schedule.ProxyValidSchedule import run as ValidRun


def run():
    p_list = list()
    p1 = Process(target=ValidRun, name='ValidRun')
    p_list.append(p1)
    p2 = Process(target=RefreshRun, name='RefreshRun')
    p_list.append(p2)

    for p in p_list:
        p.daemon = True
        p.start()

    for p in p_list:
        p.join()


class A(object):
    def __init__(self):
        print('A')


class B(object):
    def __init__(self):
        print('B')


class C(A):
    def __init__(self):
        #super(C, self).__init__()
        print('C')


class D(C, B):
    def __init__(self):
        super(D, self).__init__()
        print('D')


if __name__ == '__main__':
    # run()
    D()
