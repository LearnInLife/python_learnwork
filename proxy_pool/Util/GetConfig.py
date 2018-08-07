# -*- coding:utf-8 -*-


import os
from Util.UtilClass import ConfigParse
from Util.UtilClass import LazyProperty


class GetConfig(object):

    def __init__(self):
        # 获得该文件的文件夹路径
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        # 配置文件的路径
        self.config_path = os.path.join(os.path.split(self.pwd)[0], 'Config.ini')
        self.config_file = ConfigParse()
        self.config_file.read(self.config_path)

    @LazyProperty
    def db_type(self):
        return self.config_file.get('DB', 'type')

    @LazyProperty
    def db_name(self):
        return self.config_file.get('DB', 'name')

    @LazyProperty
    def db_host(self):
        return self.config_file.get('DB', 'host')

    @LazyProperty
    def db_port(self):
        return self.config_file.get('DB', 'port')

    @LazyProperty
    def proxy_getter_functions(self):
        return self.config_file.options('ProxyGetter')

    @LazyProperty
    def host_ip(self):
        return self.config_file.get('HOST', 'ip')

    @LazyProperty
    def host_port(self):
        return int(self.config_file.get('HOST', 'port'))


if __name__ == '__main__':
    g = GetConfig()
    print(g.db_type)
    print(g.db_name)
    print(g.db_host)
    print(g.db_port)
    print(g.proxy_getter_functions)
    print(g.host_ip)
    print(g.host_port)
