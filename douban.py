# -*- codeing = utf-8 -*-

import re  # 正则表达式，进行文字匹配
import requests
import xlwt  # 进行excel操作
from bs4 import BeautifulSoup  # 网页解析，获取数据

# 正则表达式
# 影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式）
# 影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 让换行符包含在字符中
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 豆瓣电影Top250
# 请求网页
def post_douban(kwargs):
    url = 'https://movie.douban.com/top250?start=' + str(kwargs * 25)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 Safari/537.36',
        'Connection': 'keep-alive',
        'Host': 'movie.douban.com',
    }
    try:
        # 注意请求方式是post还是get
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print('出错啦！')
        return None


# 利用BeautifulSoup4解析请求回来的html文件
def resolvingHtml(response):
    html = response.decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    # 元组tuple存放字典，字典dict用于存放影片相关信息
    tuple = []
    dict = {"title": "", "image": "", "link": "", "judge": ""}
    for item in soup.find_all('div', class_="item"):
        item = str(item)
        # 影片的标题 图片 连接 评分人数
        dict['title'] = re.findall(findTitle, item)
        dict['image'] = re.findall(findImgSrc, item)
        dict['link'] = re.findall(findLink, item)
        dict['judge'] = re.findall(findJudge, item)
        print(dict)
        tuple.append(dict)
    return tuple


if __name__ == '__main__':
    for num in range(0, 10):
        print(resolvingHtml(post_douban(num)))
