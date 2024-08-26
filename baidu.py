# -*- coding:utf-8 -*-
import re
import requests

word = input("请输入关键词: ")
z = input("请输入大小（z=9特大尺寸，z=3大尺寸，z=2中等尺寸，z=1小尺寸，z=0所有尺寸):")

i = 1
pn = 0

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.231"
}


def dowmloadPic(html, keyword):
    global i
    global pic_url
    pic_url = re.findall('"middleURL":"(.*?)",', html, re.S)
    print('找到关键词:' + keyword + '的图片，现在开始下载图片...')
    for each in pic_url:
        print('正在下载第' + str(i) + '张图片，图片地址:' + str(each))
        try:
            pic = requests.get(each, headers=headers)
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载')
            i += 1
            continue

        dir = './images/' + keyword + '_' + str(i) + '.jpg'
        # dir = './images/' + str(each)
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1

check = 1

if __name__ == '__main__':
    while i == check:
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip&rn=60&pn=' + str(
            pn) + '&z=' + str(z)
        result = requests.get(url)
        dowmloadPic(result.text, word)
        pn = pn + 60
        check = check+60
    print('已下载全部图片')