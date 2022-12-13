# coding: UTF-8
import os
import wordcloud
import jieba.analyse
import matplotlib.pyplot as plt


def each_file(file_path):
    path_dir = os.listdir(file_path)
    total = 0
    child = []
    for all_dir in path_dir:
        child.append(os.path.join('%s%s' % (file_path,all_dir)))
        total += 1
    return total, child


def read_file(file_name):
    fopen = open(file_name,'r',encoding='utf-8')
    for file in fopen:
        return file
    fopen.close()


if __name__ == '__main__':
    dir = 'E:\\Program\\pyProjects\\novel\\龙王殿章节目录\\'
    total, path = each_file(dir)
    keywords = dict()
    for tmp_path in path:
        tmp_file = read_file(tmp_path)
        result = jieba.analyse.textrank(tmp_file, topK=100, withWeight=True)
        for i in result:
            keywords[i[0]] = i[1]
    print(keywords)
    color_mask = plt.imread('./img.png')
    cloud = wordcloud.WordCloud(
        font_path = 'C:\\Windows\\Fonts\\simfang.ttf',
        background_color='white',
        mask=color_mask,
        random_state=30,
        scale=5
    )
    word_cloud = cloud.generate_from_frequencies(keywords)
    word_cloud.to_file('img2.png')
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()

