# coding:UTF-8
import requests
import bs4
import os
import time

# 先运行get_url()函数，将获得的url保存在文件中
# 再运行download()函数，获取小说内容

headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

url = 'http://www.shencou.com/read/0/743/'


def get_url():
    response = requests.get(url=url,headers=headers)
    response.encoding = 'gbk'
    soup = bs4.BeautifulSoup(markup=response.text, features="lxml")
    chapter_list = soup.find_all(class_='ttname')
    content_list = soup.find_all(class_='zjlist4')
    for chapter, content in zip(chapter_list,content_list):
        a_list = content.find_all(name='a')
        for a in a_list:
            print(url + a['href'], a.string, end='\n')
            with open(file='href.txt',mode='a',encoding='gbk') as f:
                f.write(url + a['href'] + '\t' + a.string + '\n')


def download():
    url_info = []
    total = 0
    with open(file='href.txt',mode='r',encoding='gbk') as f:
        for i in f:
            url = i.replace('\n','').split('\t')
            url_info.append(url)
            total += 1
    print('----------------------  开始下载  ---------------------- 总数：%d' % total)
    num = 0
    for i in url_info:
        href = i[0]
        chapter_name = i[1]
        # 获取当前文件所在目录
        path = os.path.dirname(os.path.abspath(__file__)) + os.sep + '八男？别闹了！'
        if not os.path.exists(path):
            os.makedirs(path)
        num += 1
        filename = path + os.sep + chapter_name + '.txt'
        resp = requests.get(href)
        time.sleep(0.2)
        with open(file=filename, mode='wb') as f:
            f.write(resp.content)
        print(f'章节 {url} 下载完成..({num} / {total})')


def main():
    # get_url()
    download()


if __name__ == "__main__":
    main()