# -*- coding:UTF-8 -*-

import socks
import socket
import requests
import time
import os
from lxml import etree


# socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1080)
# socket.socket = socks.socksocket


class Spider(object):
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

    def start_request(self):
        for i in range(1, 10):
            if i == 1:
                response = requests.get('https://www.meitulu.com/item/20591.html', headers=self.headers)
            else:
                response = requests.get('https://www.meitulu.com/item/20591_' + str(i) + '.html', headers=self.headers)
            html = etree.HTML(response.content.decode())
            self.xpath_data(html)

    def xpath_data(self, html):
        src_list = html.xpath('//div[@class="content"]/center/img/@src')
        alt_list = html.xpath('//div[@class="content"]/center/img/@alt')
        for src, alt in zip(src_list, alt_list):
            time.sleep(5)
            file_name = alt + '.jpg'
            response = requests.get(src, headers=self.headers)
            print("正在抓取图片：" + file_name)
            try:
                with open('images/' + file_name, "wb") as f:
                    f.write(response.content)
            except:
                print('==========文件名有误！==========')


spider = Spider()
spider.start_request()
