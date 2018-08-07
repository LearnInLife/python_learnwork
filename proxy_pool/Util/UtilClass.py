# -*- coding:utf-8 -*-


class LazyProperty(object):
    """
    可以使方法像属性那样调用
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class Singleton(type):
    """
    单例元类
    """
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._inst[cls]


try:
    from configparser import ConfigParser  # py3
except:
    pass


class ConfigParse(ConfigParser):

    def __init__(self):
        super(ConfigParser, self).__init__()

    def optionxform(self, optionstr):
        """用于在解析时，optionstr无论大小写，都会转换成小写"""
        return optionstr

# class A(object, metaclass=Singleton):
#
#     def __init__(self, *args, **kwargs):
#         print('A', args, kwargs)
#
#
# a = A()
# print('a is', a)
#
# b = A([1, 2, 3], {'a': 'a'})
# print('b is', b)
