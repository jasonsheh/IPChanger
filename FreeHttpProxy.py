#!/usr/bin/python
# __author__ = 'JasonSheh'
# __email__ = 'qq3039344@gmail.com'
# -*- coding:utf-8 -*-

import re
import requests
import time
import threading
import queue


class FreeHttpProxy:
    def __init__(self):
        self.http_connection_test_url = "http://www.baidu.com"
        self.https_connection_test_url = "https://www.baidu.com"
        self.required_ip_count = 5
        self.http_proxy = {}
        self.thread_num = 15
        self.q = queue.Queue()

    def get_proxy_from_66ip(self):
        pattern = re.compile("\n.*?\t(.*?)<br />", re.S)
        url = 'http://www.66ip.cn/nmtq.php?getnum=&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=0&api=66ip'
        resp = requests.get(url).text
        resp = re.findall(pattern, resp)
        for proxy in resp:
            proxy = proxy.strip()
            if proxy:
                proxy = re.sub(re.compile('<.*?>'), '', proxy)
                self.q.put_nowait({'http': 'http://' + proxy})

    def get_proxy_from_kuaidaili(self):
        ip_pattern = re.compile('<td data-title="IP">(.*?)</td>', re.S)
        port_pattern = re.compile('<td data-title="PORT">(.*?)</td>', re.S)
        type_pattern = re.compile('<td data-title="类型">(.*?)</td>', re.S)
        url = 'https://www.kuaidaili.com/free/inha/1/'
        resp = requests.get(url).text
        ip = re.findall(ip_pattern, resp)
        port = re.findall(port_pattern, resp)
        type = re.findall(type_pattern, resp)

        resp = zip(ip, port, type)
        for ip, port, _type in resp:
            proxy = {_type.lower(): '{}://{}:{}'.format(_type.lower(), ip, port)}
            self.q.put_nowait(proxy)

    def get_proxy_from_89ip(self):
        pattern = re.compile('</script>\n(.*)<br>')
        url = 'http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp='
        resp = requests.get(url).text
        resp = re.findall(pattern, resp)
        for proxy in resp[0].split('<br>'):
            self.q.put_nowait({'http': 'http://' + proxy})

    def get_all_proxy(self):
        self.get_proxy_from_66ip()
        # self.get_proxy_from_kuaidaili()
        self.get_proxy_from_89ip()

    def http_proxy_speed_test(self):
        while not self.q.empty():
            proxy = self.q.get()
            start_time = time.time()
            try:
                r = requests.get(self.http_connection_test_url, proxies=proxy, timeout=5)
            except requests.exceptions.ProxyError:
                continue
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.ReadTimeout:
                continue
            except requests.exceptions.ChunkedEncodingError:
                continue
            finish_time = time.time()
            spend_time = finish_time - start_time
            self.http_proxy[spend_time] = proxy

    def proxy_connection_test(self):
        self.get_all_proxy()

        threads = []
        for i in range(self.thread_num):
            t = threading.Thread(target=self.http_proxy_speed_test)
            threads.append(t)
        for item in threads:
            item.start()
        for item in threads:
            item.join()

        self.http_proxy = sorted(self.http_proxy.items(), key=lambda x: x[0])

    def get(self):
        self.proxy_connection_test()
        return [_[1] for _ in self.http_proxy]


if __name__ == '__main__':
    print(FreeHttpProxy().get())
