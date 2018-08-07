# -*- coding:utf-8 -*-


"""
    66ip.cn
    data5u.com
    xicidaili.com
    goubanjia.com
    xdaili.cn
    kuaidaili.com
    cn-proxy.com
    proxy-list.org
    www.mimiip.com to do

    免费抓取代理
"""
import requests
from Util.UtilFunction import getHtmlTree, getHtmlContent, getHtmlText
import re

requests.packages.urllib3.disable_warnings()


class GetFreeProxy(object):

    @staticmethod
    def freeProxy5u():
        """
               无忧代理 http://www.data5u.com/
               几乎没有能用的
        """
        url_list = [
            'http://www.data5u.com/',  # 首页提供的20个
            'http://www.data5u.com/free/gngn/index.shtml',  # 国内高匿
            'http://www.data5u.com/free/gnpt/index.shtml'  # 国内普通
        ]

        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath(".//ul[@class='l2']")
            for ul in ul_list:
                try:
                    proxy = ul.xpath(".//li/text()")[0:2]
                    yield ":".join(proxy)
                except Exception as e:
                    print(e)

    @staticmethod
    def freeProxy66ip(area=34, page=1):
        """
        代理66 http://www.66ip.cn/
        :param area: 抓取代理页数，areaindex_1北京代理页，areaindex_2上海代理页......
        :param page: 翻页
        :return:
        """
        area = 34 if area > 34 else area
        for areaindex in range(1, area + 1):
            for i in range(1, page + 1):
                url = "http://www.66ip.cn/areaindex_{}/{}.html".format(areaindex, i)
                html_tree = getHtmlTree(url)
                tr_list = html_tree.xpath(".//div[@id='footer']/div/table//tr[position()>1]")
                if len(tr_list) == 0:
                    continue
                for tr in tr_list:
                    try:
                        proxy = tr.xpath(".//td/text()")[0:2]
                        yield ":".join(proxy)
                    except Exception as e:
                        print(e)

    @staticmethod
    def freeProxyxici(page=2):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        print(e)

    @staticmethod
    def freeProxygouban():
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = getHtmlTree(url)
        proxy_list = tree.xpath(".//table//tr//td[@class='ip']")
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display:none'))
                                            and not(contains(@style, 'display: none'))
                                            and not(contains(@class, 'port'))
                                            ]/text()
                                    """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                yield '{}:{}'.format(ip_addr, port)
            except Exception as e:
                print(e)

    # @staticmethod
    # def freeProxyxun():
    #     """
    #     讯代理 http://www.xdaili.cn/
    #     :return:
    #     """
    #     url = 'http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10'
    #     request = WebRequest()
    #     try:
    #         res = request.get(url).json()
    #         for row in res['RESULT']['rows']:
    #             yield '{}:{}'.format(row['ip'], row['port'])
    #     except Exception as e:
    #         pass

    @staticmethod
    def freeProxykuai(pages=1):
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/{page}/',
            'https://www.kuaidaili.com/free/intr/{page}/'
        ]
        for url in url_list:
            for page in range(1, pages + 1):
                page_url = url.format(page=page)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table//tr')
                for tr in proxy_list[1:]:
                    yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxymimi(pages=1):
        """
        秘密代理 http://www.mimiip.com
        """
        url_list = [
            'http://www.mimiip.com/gngao/{page}',  # 国内高匿
            'http://www.mimiip.com/gnpu/{page}',  # 国内普匿
            'http://www.mimiip.com/gntou/{page}'  # 国内透明
        ]

        for url in url_list:
            for page in range(1, pages + 1):
                page_url = url.format(page=page)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath(".//table[@class='list']//tr")
                for tr in proxy_list[1:]:
                    yield ":".join(tr.xpath(".//td/text()")[0:2])

    @staticmethod
    def freeProxycoderbusy(pages=1):
        """
        码农代理 https://proxy.coderbusy.com/
        :return:
        """
        url = 'https://proxy.coderbusy.com/classical/country/cn.aspx?page={page}'
        for page in range(1, pages + 1):
            page_url = url.format(page=page)
            tree = getHtmlTree(page_url)
            proxy_list = tree.xpath(".//table[@class='table']//tr")
            for tr in proxy_list[1:]:
                td_list = tr.xpath(".//td/text()")
                ip = td_list[1].strip()
                host = td_list[3].strip()
                yield ":".join([ip, host])

    @staticmethod
    def freeProxyip3366(pages=1):
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = [
            'http://www.ip3366.net/free/?stype=1&page={page}',
            'http://www.ip3366.net/free/?stype=2&page={page}'
        ]
        for url in urls:
            for page in range(1, pages + 1):
                page_url = url.format(page=page)
                content = getHtmlContent(page_url, code='gbk')
                proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', content)
                for proxy in proxies:
                    yield ":".join(proxy)

    @staticmethod
    def freeProxyiphai():
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        for url in urls:
            r = getHtmlText(url)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxyjiangxianli(page_count=8):
        """
        guobanjia http://ip.jiangxianli.com/?page=
        免费代理库
        超多量
        :return:
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html_tree = getHtmlTree(url)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]

    # @staticmethod
    # def freeProxyWallFirst():
    #     """
    #     墙外网站 cn-proxy
    #     :return:
    #     """
    #     urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # @staticmethod
    # def freeProxyWallSecond():
    #     """
    #     https://proxy-list.org/english/index.php
    #     :return:
    #     """
    #     urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
    #     request = WebRequest()
    #     import base64
    #     for url in urls:
    #         r = request.get(url)
    #         proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
    #         for proxy in proxies:
    #             yield base64.b64decode(proxy).decode()
    #
    # @staticmethod
    # def freeProxyWallThird():
    #     urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)


if __name__ == "__main__":
    # GetFreeProxy.freeProxy5u()
    # GetFreeProxy.freeProxy66ip(1, 1)
    GetFreeProxy.freeProxyjiangxianli()
