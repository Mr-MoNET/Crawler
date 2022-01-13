#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import requests
import json
import xlrd
import xlwt
from xlutils.copy import copy


# 网易云音乐信息 —— 我们都一样，张杰
# 网页请求
def get_one_comment(kwargs):
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_191252?' + 'offset=' + str(kwargs * 20) + '&limit=20'
    # url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token=a268524d07b6ed625deff380151c555b'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 Safari/537.36',
        'Referer': 'https://music.163.com/#/song?id=557583281',
        'Origin': 'http://music.163.com',
        'Host': 'music.163.com'
    }
    user_data = {
        'params': '6+IOWJgu6xVpizKpAgfXosl5qfKuvuQTn1xWijrGzr5cHwtoQNs6rnQKaNUE'
                  '/r7fqRgrx4dRiKF6LD9Z1YG3rgpRoqxMjurVgrv5q4lFK1KQ84XkLgUspxLLoei0GXNtWmlRXtKi3UkLB96xWx0h/tNbPFIPBy'
                  '+/FGlEC4AxyVGEm4waUPJ2jLOyXaDUCtNDzf55A+HusScFMSg7kfxK1Gjdf9GxgEMk1R0r8ThsLbhEPWg4gcNEjGX1RBK'
                  '/7qthr7+iRduHUBb3SXJDNH7HUamaTZQZ9AujSJ+Tf1m/DXfZtYYk+FIICfcnLelSdu4dFHC0ATUA6IgwWBzG5b5+uQqxsj'
                  '/Ib9saKhOtEDqQgN0=',
        'encSecKey': 'b9156061c3d63b4e587ea40d87a218029b937ea570dca57c19b43e0d46789182632556eea2b5996a29e51733c6eddcd50228d0dadf2c2b29b08244e431a155be25bd9621814b50aa983a3e5d88b52116221f65feeedfe49c2fa69f7334a205bcf0d95507385fed12a35982418192f6882ab84d13c7ad79dff15e122049587b20 '
    }
    try:
        response = requests.post(url, headers=headers, data=user_data)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print('出错啦！')
        return None


def parse_json_data(contents):
    if contents:
        # 编码格式转换
        contents = contents.decode('utf-8')
        # api接口返回的数据是json格式，把json格式转换为字典结构，获取评论信息
        comments = json.loads(contents)['comments']
        for comment in comments:
            content = comment['content']
            nickname = comment['user']['nickname']
            timeArray = time.localtime(comment['time'] / 1000)
            style_time = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
            dict = {'nickname': nickname, 'content': content, 'time': style_time}
            # print("时间: " + dict['time'] + "  用户: " + dict['nickname'] + "  评论: " + dict['content'])
            return dict


book_name_xls = '网易云评论.xls'
sheet_name_xls = '热评'
value_title = [["时间", "用户", "评论"], ]


def exchangeDataToxls(path, data):
    value = [[data['time'], data['nickname'], data['content']]]
    try:
        print(value)
        write_excel_xls_append(path, value)
    except IOError:
        print("文件不存在，请检查")
        exit()


def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


if __name__ == '__main__':
    for num in range(1, 100):
        response = get_one_comment(num)
        data = parse_json_data(response)
        exchangeDataToxls(book_name_xls, data)
