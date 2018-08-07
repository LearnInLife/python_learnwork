# -*- coding:utf-8 -*-

from Util.LogHandler import LogHandler
from ProxyGetter.GetFreeProxy import GetFreeProxy
from Util.UtilFunction import verifyProxyFormat
import inspect

log = LogHandler('check_proxy', file=False)


class CheckProxy(object):

    @staticmethod
    def checkAllGetProxyFunc():
        member_list = inspect.getmembers(GetFreeProxy, predicate=inspect.isfunction)
        proxy_count_dict = dict()
        for func_name, func in member_list:
            log.info("start run {}".format(func_name))
            try:
                proxy_list = [proxy for proxy in func() if verifyProxyFormat(proxy)]
                proxy_count_dict[func_name] = len(proxy_list)
            except Exception as e:
                log.info("get proxy func {} run error ".format(func_name))
                log.error(str(e))
        log.info("all func run over" + "***" * 5)
        for func_name, func in member_list:
            log.info("{n} completed, fetch proxy number: {c}".format(n=func_name, c=proxy_count_dict.get(func_name, 0)))

    @staticmethod
    def checkGetProxyFunc(func):
        """
                检查指定的getFreeProxy某个function运行情况
                Args:
                    func: getFreeProxy中某个可调用方法
                Returns:
                    None
        """
        func_name = getattr(func, '__name__', "None")
        log.info("start running func: {}".format(func_name))
        count = 0
        for proxy in func():
            if verifyProxyFormat(proxy):
                log.info("fetch proxy: {}".format(proxy))
                count += 1

        log.info("{n} completed, fetch proxy number: {c}".format(n=func_name, c=count))


if __name__ == "__main__":
    CheckProxy.checkAllGetProxyFunc()
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy5u)
