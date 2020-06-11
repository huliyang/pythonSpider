# coding:UTF-8

import selenium, selenium.webdriver
import time  # 进行延迟处理，访问过快容易被封
import re
import requests
import bs4
import os
import threading  # 多线程
import csv  # 下载的信息保存在csv格式的文件中

# URL = "https://movie.douban.com/typerank?type_name=剧情&type=11&interval_id=100:90&action="
BASE_URL = "https://movie.douban.com"  # 页面的根路径
CHART_URL = BASE_URL + "/chart"  # 入口地址
CHROME_DRIVER = "chromedriver.exe"  # 浏览器的驱动
driver = selenium.webdriver.Chrome(executable_path=CHROME_DRIVER)  # 浏览器的驱动
SAVE_DIR = "E:" + os.sep + "Program" + os.sep + "pyProjects" + os.sep + "sprider_data"  # 保存的目录
IMAGE_PATH = SAVE_DIR + os.sep + "images"  # 图片的保存路径

HTTP_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

CSV_HEADERS = ["type", "rank", "name", "rating", "comment", "img", "crew", "url"]  # csv标题

if not os.path.exists(IMAGE_PATH):
    os.mkdirs(IMAGE_PATH)


class Movie:  # 保存电影信息的类
    def __init__(self, type):
        self.img = None  # 电影图片
        self.name = None  # 电影名称
        self.type = type  # 电影分类
        self.rank = None  # 电影评分
        self.crew = None  # 演员列表
        self.rating = None  # 平均分
        self.comment = None  # 评论人数
        self.url = None  # 影片路径

    def __repr__(self) -> str:
        return "【电影信息】分类：%s、名次：%d、名称：%s、评分：%f、评论人数：%d、图片：%s、演员列表：%s、影片路径：%s" % \
               (self.type, self.rank, self.name, self.rating, self.comment, self.img, self.crew, self.url)

    def get(self):  # 保存影片信息到本地
        return [self.type, self.rank, self.name, self.rating, self.comment, self.img, self.crew, self.url]


def download_img(url, image_name):  # url:图片路径 image_name:保存名称
    image_path = IMAGE_PATH + os.sep + image_name
    response = requests.get(url)
    with open(file=image_path, mode="bw") as file:
        file.write(response.content)  # 获取二进制数据


def download_type(type, url):
    driver.get(url=url)  # 访问的加载路径
    for item in range(2):  # 加载2次
        target = driver.find_element_by_id("footer")  # 此元素定义在页面尾部，访问它来模拟鼠标下滑操作
        driver.execute_script("arguments[0].scrollIntoView();", target)  # 进行滚动
        time.sleep(4)  # 4秒滚动一次

    time.sleep(4)  # 因为异步加载需要时间，所以等待2秒
    count = 0  # 抓取计数，最多抓取50次内容
    save_path = SAVE_DIR + os.sep + type + ".csv"
    with open(file=save_path, mode="w", newline="", encoding="UTF-8") as file:
        csv_file = csv.writer(file)  # 创建csv文件对象
        csv_file.writerow(CSV_HEADERS)
        try:
            for content in driver.find_elements_by_xpath("//div[@class='movie-content']"):
                time.sleep(0.2)  # 延迟
                movie = Movie(type)
                movie.url = content.find_element_by_tag_name("a").get_property("href")  # 获取影片路径
                image_url = content.find_element_by_class_name("movie-img").get_property("src")  # 图片地址
                if image_url:  # 有图片，加载后续元素
                    movie.img = image_url[image_url.rfind("/") + 1:]  # 获取图片名称
                    movie.name = content.find_element_by_class_name("movie-name-text").text  # 获取电影名称
                    threading.Thread(target=download_img, args=(image_url, movie.img)).start()  # 启动图片的下载线程
                    movie.rank = int(content.find_element_by_class_name("rank-num").text)
                    movie.crew = content.find_element_by_class_name("movie-crew").text.split("/")  # 存放为列表
                    movie.rating = float(content.find_element_by_class_name("rating_num").text)
                    movie.comment = int(re.sub("\D", "", content.find_element_by_class_name("comment-num").text))
                    csv_file.writerow(movie.get())  # 获取列表信息进行写入
                    print(movie)
                    count += 1
                    if count >= 50:  # 达到抓取上限
                        raise Exception("超过抓取次数")
        except Exception as e:
            print(e)


def main():
    request = requests.get(url=CHART_URL, headers=HTTP_HEADERS)  # 发出get请求
    request.encoding = "UTF-8"
    soup = bs4.BeautifulSoup(markup=request.text, features="lxml")
    typerank_list = soup.find_all("a", href=re.compile("^/typerank"))
    for type in typerank_list:
        type_title = type.contents[0]  # 获取文字
        download_type(type_title, BASE_URL + type["href"])
        print("【%s】访问路径：%s" % (type_title, BASE_URL + type["href"]))


if __name__ == "__main__":
    main()
