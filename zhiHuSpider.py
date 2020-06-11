# coding:UTF-8

import requests
import re
import os
import time

URL = "https://www.zhihu.com/question/26037846"
HEADERS = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }


class Spider(object):
    def __init__(self, question_id=26037846):
        self.__session=requests.session()
        self.url = "https://www.zhihu.com/question/{}".format(question_id)
        self.faq_id = question_id

    def get_answer(self,limit=10):
        # 加载数据时，浏览器请求的网址
        url = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=content,voteup_count&limit={1}&offset={2}"
        pic_reg = re.compile('<noscript>.*?data-original="(.*?)".*?</noscript>', re.S)
        flag = False
        offset = 0
        # 记录图片数量
        pic_num = 0
        while not flag:
            resp = self.__session.get(url.format(self.faq_id, limit, offset), headers=HEADERS)
            time.sleep(0.2)
            data = resp.json()
            if data.get("paging").get("is_end")==True:  # 判断是否还有回答
                flag = True
            else:
                content_data_list = data.get("data")
                for data in content_data_list:
                    content = data.get("content")
                    author = data.get("author")  # 从返回的JSON中取出author标签下的数据
                    name = author.get("name")  # 取得答主姓名
                    pic_urls = re.findall(pic_reg, content)  # 图片url
                    # 将回答的所有图片写入url.txt
                    for i in pic_urls:
                        pic_num += 1
                        with open('url.txt','a',encoding='utf-8') as f :
                            f.write(i + '\t' + name + '\n')
            print(f'已获取前 {offset + limit} 个回答，当前图片总数为 {pic_num}')
            if flag:
                print('爬取完毕')
                break
            offset += limit

    def download(self):
        img_info = []
        total = 1
        try:
            with open('url.txt','r',encoding='utf-8') as f:
                for i in f:
                    img = i.replace('\n','').split('\t')
                    img_info.append(img)
                    total += 1
        except FileNotFoundError as e:
            print(e)
        print('----------------------  开始下载  ---------------------- 图片总数：%d' % total)
        num = 0
        for i in img_info:
            img_url = i[0]
            img_author_name = i[1]
            # 获取当前文件所在目录
            path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'zhihuPic'
            # 创建文件夹 用来存抓取的图片
            if not os.path.exists(path):
                os.makedirs(path)
            num += 1
            filename = path + os.sep + img_author_name + '_' + str(num) + '.jpg'
            resp = requests.get(img_url)
            time.sleep(0.2)
            with open(file=filename,mode='bw') as f:
                f.write(resp.content)
            print(f'图片 {img_url} 下载完成..({num} / {total})')


def main():
    s = Spider()
    s.get_answer()
    # s.download()


if __name__ == "__main__":
    main()
