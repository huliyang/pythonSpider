# coding: UTF-8
import requests
from lxml import etree
import time

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}
URL = 'https://www.huya.com/g/4079'


def main():
    response = requests.get(url=URL, headers=HEADERS)
    data = etree.HTML(response.text)
    girls = data.xpath('//img[@class="pic"]')
    for girl in girls:
        img_url = girl.xpath('./@data-original')[0]  # 缩小后的图片
        time.sleep(1)
        img_url = img_url.split('?')[0]  # 原图
        name = girl.xpath('./@alt')[0]
        image = requests.get(url=img_url, headers=HEADERS)
        with open('./girl/%s.jpg' % name, 'wb') as f:
            f.write(image.content)
        print('《%s》下载完成' % name)


if __name__ == '__main__':
    main()