# encoding=utf-8
import requests
import json
import csv
import time
import jieba
import numpy
from PIL import Image
from wordcloud import WordCloud


# 网页请求
def get_one_comment(offset):
    headers = {
        'Cookie': '_iuqxldmzr_=32; _ntes_nnid=bdaab01e87ee929b3a9a91ea44b5cd45,1534172699282; '
                  '_ntes_nuid=bdaab01e87ee929b3a9a91ea44b5cd45; __utmc=94650624; '
                  'WM_TID=M4E4ToHGUg4EetTbOjxEC5J%2BuODh%2B0jj; abt=66; '
                  'WM_NI=cRw1E4mJtjv9dwKem8xCMaYzUgNNyu8qqM25igmzBYDj%2FJGjHnYTJFFFqen2XIq%2FlCdRUdQxmdIvxSl84'
                  '%2BvraOwnH1lJboEwOdL6UrZhnx030tzRng9NfOIBNXgIUx7GMUI%3D; '
                  'WM_NIKE'
                  '=9ca17ae2e6ffcda170e2e6eeb6b15cf88bb8ade56a8eb48291f97ca5b9e1d2c45bf6ed9cb9e659b1be8e89ca2af0fea7c3b92aa18eb9d2c840af96bc8bf533a8a98586f034bc9d8382dc7297b982affc7ffcafbfaeb13fabb9a39bc15388b6e1abc6628cb297b5c94e869abf86ed3a9c97bfd0ef49a88e9b85d474afbc8797fb59b0e8fcccf57aa391b98fcb3bb096ae90c87d8dbc84d7d87a9ab8a299b339f4acb6b3ed6dfb92aab0cc4a8e88a9aad874f59983b6cc37e2a3; __utma=94650624.827593374.1534172700.1535852507.1535857189.3; __utmz=94650624.1535857189.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; JSESSIONID-WYYY=kgbbgMKEcRf18SvvxZVqNTmWZD%2Fdn8BpA%2F7aMH7vv4mSpiDaE%5CfkC5xPu5hFv0nk5X7PpvlEJJ97%2BC3WyE5Qv50EW%2FdNPQQPenibqq%2F5IyHkuuMlCTkpkb7TRMl9oBEdFi68ktMI8m%2F5Ilyub4P204bpG0qBv4yx9vvw8CmCJ%2B9vCaSd%3A1535859527007; __utmb=94650624.7.10.1535857189',
        'Referer': 'https://music.163.com/song?id=1299557768',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.99 Safari/537.36 '
    }
    # 字符串拼接
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_1299557768?offset=' + str(offset) + '&limit=20'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print('出错啦！')
        return None


# 解析数据
def parse_json_data(contents):
    if contents:
        # 编码格式转换
        contents = contents.decode('utf-8')
        # api接口返回的数据是json格式，把json格式转换为字典结构，获取评论信息
        comments = json.loads(contents)['comments']
        print(comments)
        for comment in comments:
            content = comment['content']
            nickname = comment['user']['nickname']
            timeArray = time.localtime(comment['time'] / 1000)
            style_time = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
            dict = {'nickname': nickname, 'content': content, 'time': style_time}
            print("时间: " + dict['time'] + "  用户: " + dict['nickname'] + "  评论: " + dict['content'])
            yield {
                'time': style_time,
                'nickname': nickname,
                'comment': content
            }
        # print(nickname+','+content+','+style_time)


# csv保存数据
def save_csv_comments(messages, i):
    # encoding=utf_8_sig只能转换中文乱码和字母乱码，不能支持数字的乱码
    with open('comment_csv.csv', 'a', encoding='utf_8_sig', newline='')as f:
        csvFile = csv.writer(f)
        if i == 0:
            csvFile.writerow(['评论时间', '昵称', '评论内容'])
        csvdatas = []
        for message in messages:
            csvdata = []
            csvdata.append(message['time'])
            csvdata.append(message['nickname'])
            csvdata.append(message['comment'].replace('\n', ''))
            csvdatas.append(csvdata)
        csvFile.writerows(csvdatas)


# 读取csv文件的评论内容的一列
def read_csvFile(fileName):
    with open(fileName, 'r') as f:
        # 因为此csv文件并非二进制文件， 只是一个文本文件
        readerCSV = csv.reader(f)
        comment_column = [row[2] for row in readerCSV]
        return comment_column


# 词云生成
def make_word_cloud(text):
    comment_text = jieba.cut(''.join(text[1:]))
    print(comment_text)
    # list类型转换为str类型
    comment_text = ''.join(comment_text)
    animal = numpy.array(Image.open('timg_meitu_1.jpg'))
    wc = WordCloud(font_path='C:/Windows/Fonts/simsun.ttc', background_color="white", width=913, height=900,
                   max_words=2000, mask=animal)
    # 生成词云
    wc.generate(comment_text)
    # 保存到本地
    wc.to_file("animal.png")


# 程序主入口
def main(offset, i):
    parse_json_data(get_one_comment(offset))
    # save_csv_comments(parse_json_data(get_one_comment(offset)), i)


# if __name__=="__main__":
# 	for i in range(100):
# 		main(i*20,i)
# make_word_cloud(read_csvFile('comment_csv.csv'))

if __name__ == "__main__":
    for i in range(100):
        main(i * 20, i)
