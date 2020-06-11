# coding:UTF-8
import requests
import time
import os
from bs4 import BeautifulSoup

url = 'https://www.umei.cc/meinvtupian/meinvxiezhen/'
path = 'images/'

headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def main():
    create_dir(path)
    response = requests.get(url, headers=headers)
    response.encoding = "UTF-8"
    main_page = BeautifulSoup(response.text, "html.parser")
    alist = main_page.find("div", attrs={"class": "TypeList"}).find_all("a", attrs={"class": "TypeBigPics"})
    for a in alist:
        time.sleep(3)
        href = a.get("href")
        child_resp = requests.get(href, headers=headers)  # 请求子页面
        child_resp.encoding = 'UTF-8'
        child_page = BeautifulSoup(child_resp.text, "html.parser")
        img = child_page.find("div", attrs={"class": "ImageBody"}).find("img")
        print(img.get("src"))
        # 下载图片
        title = img.get("alt")
        f = open(path + "%s.jpg" % title, mode="wb")
        f.write(requests.get(img.get("src")).content)



if __name__ == "__main__":
    main()

