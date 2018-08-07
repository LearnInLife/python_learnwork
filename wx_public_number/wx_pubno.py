# -*- coding:utf-8 -*-

import requests
import json


class iciba(object):

    def __init__(self, wechat_config):
        self.appid = wechat_config['appid']
        self.appsecret = wechat_config['appsecret']
        self.template_id = wechat_config['template_id']
        self.access_token = ''

    # 获取access_token
    def get_access_token(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            self.appid, self.appsecret)

        r = requests.get(url)
        self.access_token = r.json()['access_token']
        return self.access_token

    def send_msg(self, openid, everday_words):
        msg = {
            'touser': openid,
            'template_id': self.template_id,
            'url': everday_words['fenxiang_img'],
            'data': {
                'content': {
                    'value': everday_words['content'],
                    'color': '#0000cd'
                },
                'note': {
                    'value': everday_words['note'],
                },
                'translation': {
                    'value': everday_words['translation'],
                }

            }
        }
        json_data = json.dumps(msg)
        if self.access_token == '':
            self.access_token = self.get_access_token()

        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % self.access_token

        r = requests.post(url, data=json_data)

        print(r.json())
        return r.json()

    def get_everyday_words(self):
        url = 'http://open.iciba.com/dsapi/'
        r = requests.get(url)
        content = r.json()['content']
        note = r.json()['note']
        print(content)
        print(note)
        return r.json()

    def send_everydat_words(self, openids):
        everday_words = self.get_everyday_words()
        for openid in openids:
            result = self.send_msg(openid, everday_words)
            if result['errcode'] == 0:
                print('[INFO] send to %s is success' % openid)
            else:
                print('[INFO] send to %s is error' % openid)


if __name__ == '__main__':
    wechat_config = {
        'appid': 'wx262420b1c43d2c9b',
        'appsecret': 'bbee792f3d825d61fec8cd508df994b2',
        'template_id': 'EhNQWtXecZhc9rTYHm3aHdgyMKDmDMPkipPIUnsaQ7k'
    }
    openid = [
        'oQjcd1D1NMEpPPffqOzoZqE3yUXA',
    ]

    i = iciba(wechat_config)
    i.send_everydat_words(openid)
