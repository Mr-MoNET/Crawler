import requests
from bs4 import BeautifulSoup
import docx
import re

# 正则表达式
# 找到新闻的超链接
findLink = re.compile(r'<a href="(.*?)"')

# 找到新闻的标题
findTitle = re.compile(r'<h1>(.*?)<', re.S)

# 找到新闻的内容
findContent = re.compile(r'<p>(.*?)<', re.S)

# 找到新闻栏数量
findNumber = re.compile(r'<ul class="(.*?)"')

# 实例化一个docx文档，更多使用功能请学习docx模块
doc = docx.Document()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/86.0.4240.111 ''Safari/537.36 ',
           'Connection': 'keep-alive'}


def requests_souhu():
    # 确定目标网页
    url = 'https://business.sohu.com/?spm=smpc.home.top-nav.4.1625025881214n1yDAK1'

    # 利用requests开始请求网页内容
    res = requests.get(url, headers=headers)
    # 检查状态码是否为200，以确认是否请求成功。
    if res.status_code == requests.codes.ok:
        print("---网页请求成功---\n---开始解析---")
    # 如果网页编码形式不一样，会造成网页内容部分乱码
    res.encoding = res.apparent_encoding
    # 使用lxml解析网页(推荐)
    soup = BeautifulSoup(res.text, 'lxml')
    # 使用find方法查找需要的内容
    news = soup.find_all('div', class_='z-main-1_mid')
    return news


def resolvePage(link):
    # 解析表达式中的所有链接
    link_new = re.findall(findLink, str(link))
    # 链接数组
    link_tuple = []

    for s in link_new:
        link_tuple.append(s)
        RequestContent = requests.get(url=s, headers=headers)
        RequestContent = RequestContent.content.decode('utf-8')
        # 解析标题
        soup = BeautifulSoup(RequestContent, 'lxml')
        content_title = soup.find_all('div', class_="text-title")
        title = re.findall(findTitle, str(content_title))
        if title:
            title = str(title[0]).replace(' ', '')
            # 解析内容
            long = []
            content_article = soup.find_all('article', class_="article")
            article = re.findall(findContent, str(content_article))
            article = str(article).replace('[', "")
            article = article.replace(']', "")
            long.append(article)
            print(long[0])
            # 将获取到的内容写入word文档中
            doc.add_paragraph(long)
            # 结束并保存word文档
            doc.save('搜狐新闻.docx')
            print("---写入成功---")


if __name__ == "__main__":
    response = requests_souhu()
    resolvePage(response)
