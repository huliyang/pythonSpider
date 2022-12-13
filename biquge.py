# coding: UTF-8
import requests
from lxml import etree
import collections
import time
import os


base_url = 'https://www.bbiquge.net/book/131117/'
novel_url = base_url + 'index_1.html'
save_dir = "E:" + os.sep + "Program" + os.sep + "pyProjects" + os.sep + "novel"  # 保存的目录
header= {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
    'Referer': 'https://www.bbiquge.net/book/131117/'
}

if not os.path.exists(save_dir):
    os.makedirs(save_dir)


def download_url(url):
    response = requests.get(url=url,headers=header)
    response.encoding = 'gbk'
    data = etree.HTML(response.text)
    novel_title = data.xpath('//div[@class="zjbox"]/dl[@class="zjlist"]/dt[@class="ttname"]//text()') # 小说标题
    novel_hrefs = data.xpath('//div[@class="zjbox"]/dl[@class="zjlist"]/dd/a/@href') # 章节超链接
    novel_chapters = data.xpath('//div[@class="zjbox"]/dl[@class="zjlist"]/dd/a/text()') # 章节名称
    pages = data.xpath('//div[@class="zjbox"]//select/option/@value')
    download_dict = collections.OrderedDict()
    for chapter_href,novel_chapter in zip(novel_hrefs,novel_chapters):
        download_dict[novel_chapter] = base_url + chapter_href
    return novel_title[0], len(pages), download_dict


def save_novel(path, cont):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(cont)


def parse_data(dict):
    for key, value in dict.items():
        print(key + '==>' + value)
        html = requests.get(url=value, headers=header)
        time.sleep(5)
        html.encoding = 'gbk'
        data = etree.HTML(html.text)
        content = data.xpath('//div[@id="main"]/div[@id="readbox"]/div[@id="content"]/text()')
        save_novel(path + os.sep + key + '.txt', ''.join(content).replace('\\xa0\\xa0\\xa0\\xa0', '\\r\\n'))


if __name__ == '__main__':
    title, total, dict = download_url(novel_url)
    path = save_dir + os.sep + title
    if not os.path.exists(path):
        os.makedirs(path)
    parse_data(dict)
    for i in range(2,total):
        url = base_url + 'index_' + str(i) + '.html'
        _, __, dict2 = download_url(url)
        parse_data(dict2)
        time.sleep(5)