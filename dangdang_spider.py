# coding:UTF-8
import requests
import re

HTTP_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}


def main(page):
    url = "http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-" + str(page)
    html = request_dangdang(url)
    items = parse_result(html)
    for item in items:
        print(item)


def request_dangdang(url):
    try:
        response = requests.get(url,headers=HTTP_HEADERS)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def parse_result(html):
    str_pattern = '<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>'
    pattern = re.compile(str_pattern,re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'range': item[0],
            'image': item[1],
            'title': item[2],
            'recommand': item[3],
            'author': item[4],
            'times': item[5],
            'price':item[6]
        }


if __name__ == "__main__":
    for i in range(1,4):
        main(i)