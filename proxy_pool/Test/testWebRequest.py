# -*- coding:utf-8 -*-

from Util.WebRequest import WebRequest


def testWebRequest():
    wr = WebRequest()
    res = wr.get('https://www.baidu.com')
    assert res.status_code == 200


if __name__ == '__main__':
    testWebRequest()
