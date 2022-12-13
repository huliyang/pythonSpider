# coding: UTF-8

import requests
import re
import os

filename = 'music/'
if not os.path.exists(filename):
    os.makedirs(filename)

url = 'https://music.163.com/discover/toplist'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
}
response = requests.get(url=url,headers=headers)
html_data = re.findall('<li><a href="/song\?id=(\d+)">(.*?)</a></li>',response.text)


def change_title(t):
    pattern = re.compile(r"[\/\\\:\*\?\"\<\>\|]")  # '/ \ : * ? " < > |'
    new_title = re.sub(pattern, "_", title)  # 替换为下划线
    return new_title


for num_id,title in html_data:
    music_url = f'http://music.163.com/song/media/outer/url?id={num_id}.mp3'
    music_content = requests.get(url=music_url,headers=headers).content
    with open(filename + change_title(title) + '.mp3',mode='wb') as f:
        f.write(music_content)
    print(num_id,title)
