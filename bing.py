import os
from time import sleep
import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.231"
}


def request_download(PictureList, url, dir='upload_pic'):
    print("下载Bing图片: %s" % url)
    r = requests.get(url)
    sleep(0.5)
    filename = url.split("/")[-1]
    filename = filename.split("?")[0]

    PictureList.append(filename+'.jpg')
    with open('./' + dir + '/' + filename + '.jpg', 'wb') as f:
        f.write(r.content)


def download(path, query='', final=10):
    first = 0
    count = 35
    results = []

    result = os.path.exists(path)
    if not result:
        os.mkdir(path)

    while count <= 35:
        params = (
            ('q', query),
            ('first', str(first)),
            ('count', str(count)),
            ('cw', '1177'),
            ('ch', '912'),
            ('relp', '35'),
            ('tsc', 'ImageBasicHover'),
            ('datsrc', 'I'),
            ('layout', 'RowBased_Landscape'),
            ('mmasync', '1'),
            ('dgState', 'x*643_y*1362_h*180_c*2_i*36_r*8'),
            ('IG', '50728F4EDAA0464EAEA130852983A4D5'),
            ('SFX', '2'),
            ('iid', 'images.5534'),
        )

        try:
            response = requests.get(
                'https://cn.bing.com/images/async', headers=headers, params=params)
            # print(response.text)
            html = etree.HTML(response.text)
            # print(html)
            ret = html.xpath("//img[@class='mimg']/@src")
            results += ret
        except Exception as e:
            print("网络请求出错 %s" % str(e))

        first = count
        count += 35

    temp = set(results)
    PictureList = []
    count = 0
    for url in temp:
        try:
            request_download(PictureList=PictureList, url=url, dir=path)
        except Exception as e:
            print("图片下载出错 url: %s error: %s" % (url, str(e)))
        if count >= final:
            break


if __name__ == '__main__':
    print("start")
    download("./store_path", "关键字", 100)