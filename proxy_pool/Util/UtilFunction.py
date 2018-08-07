# -*- coding: utf-8 -*-


import re
import time
from lxml import etree
from Util.WebRequest import WebRequest
import requests


def getHtmlTree(url, **kwargs):
    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }

    wr = WebRequest()

    time.sleep(2)

    content = wr.get(url, header=header).content
    return etree.HTML(content)


def getHtmlContent(url, code='utf-8', **kwargs):
    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }

    wr = WebRequest()

    time.sleep(2)

    content = wr.get(url, header=header).content
    return content.decode(code, errors='ignore')


def getHtmlText(url):
    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }

    wr = WebRequest()

    time.sleep(2)

    text = wr.get(url, header=header).text
    return text


def verifyProxyFormat(proxy):
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


def validUsefulProxy(proxy):
    """
    检查代理是否可用
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')

    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    try:
        r = requests.get(url='http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200:
            return True

    except Exception as e:
        return False


def tcpConnect(proxy):
    """
    TCP三次握手
    :param proxy:
    :return:
    """
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    ip, port = proxy.split(":")
    r = s.connect_ex((ip, port))
    return True if r == 0 else False
