#!/usr/bin/python3
import json
import os

import jieba
import stylecloud
from numpy.core.defchararray import isdigit

danmaku_path = './danmaku/'
config_output_path = './output/'
skip_nickname = []
skip_sentenses = []


def main(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        for file in files:
            data = read_datas(file_dir + file)
            # calc_stenses_nums(data)
            user_rank = analyse_user_top(data)
            # print(userTop)
            timeline = analyse_time(data)
            # print(time)
            pie = analyse_pie(user_rank)
            wordcloud(file, data)
            save_json(file, user_rank, timeline, pie)


def calc_stenses_nums(datas):
    sentens = {}
    for data in datas:
        content = data['content']
        if content in sentens.keys():
            sentens[content] = sentens[content] + 1
        else:
            sentens[content] = 1
    print('相同弹幕次数查重：\n')
    d_order = sorted(sentens.items(), key=lambda x: x[1], reverse=True)
    sorted_dict = dict(d_order)
    for senten, num in sorted_dict.items():
        print('次数：%d，%s' % (num, senten))


def save_json(filename, user_rank, timeline, pie):
    result = {}
    filename = filename.replace('-', '').replace('.txt', '.json')
    result['user_rank'] = user_rank
    result['timeline'] = timeline
    result['pie'] = pie
    json_str = json.dumps(result)
    fullpath = config_output_path + filename
    file = open(fullpath, 'w')
    file.write(json_str)
    file.close()
    print(fullpath + '文件已经创建')


def read_datas(file):
    with open(file, 'r', encoding='utf-8') as lines:
        lines = lines.readlines()
        datas = []
        for line in lines:
            data = json.loads(line)
            datas.append(data)
        return datas


def analyse_user_top(datas):
    result = {}
    analyse = {}
    for data in datas:
        nickname = data['sender']['nickname']
        if nickname in skip_nickname:
            continue
        is_in = nickname in analyse.keys()
        if not is_in:
            analyse[nickname] = 0
    for data in datas:
        nickname = data['sender']['nickname']
        if nickname in skip_nickname:
            continue
        is_in = nickname in analyse.keys()
        if is_in:
            analyse[nickname] += 1
        else:
            analyse[nickname] = 0
    d_order = sorted(analyse.items(), key=lambda x: x[1], reverse=True)
    sorted_dict = dict(d_order)
    result['label'] = list(sorted_dict.keys())
    result['value'] = list(sorted_dict.values())
    result['json'] = sorted_dict
    return result


def analyse_time(datas):
    res = {}
    result = {}
    for item in range(24):
        if item < 10:
            result['0' + str(item) + ':00'] = 0
        else:
            result[str(item) + ':00'] = 0
    for data in datas:
        hour = data['time'][12:14]
        if hour == "" or (not isdigit(hour)):
            continue
        hour = hour + ':00'
        is_in = hour in result.keys()
        if is_in:
            result[hour] += 1
        else:
            result[hour] = 0
    res['label'] = list(result.keys())
    res['value'] = list(result.values())
    res['json'] = result
    # print(result)
    return res


def analyse_pie(userRank):
    result = []
    for index, item in enumerate(userRank['label']):
        row = {}
        limit = 10
        if index > limit - 1:
            if len(result) == limit:
                row['name'] = '其他用户'
                row['value'] = userRank['value'][index]
                result.append(row)
            else:
                result[limit]['name'] = '其他用户'
                result[limit]['value'] = result[limit]['value'] + userRank['value'][index]
            continue
        row['name'] = userRank['label'][index]
        row['value'] = userRank['value'][index]
        result.append(row)
    return result


def wordcloud(filename, datas):
    filename = filename.replace('-', '').replace('.txt', '.png')
    all_content = ''
    for data in datas:
        nickname = data['sender']['nickname']
        if nickname in skip_nickname:
            continue
        if data['content'] in skip_sentenses:
            continue
        all_content += data['content'] + '。'
    # print(allContent)
    word_list = jieba.cut(all_content)
    result = " ".join(word_list)  # 分词用空格隔开
    stylecloud.gen_stylecloud(
        text=result,  # 上面分词的结果作为文本传给text参数
        size=512,
        font_path='./font.ttf',  # 字体设置
        palette='cartocolors.qualitative.Pastel_7',  # 调色方案选取，从palettable里选择
        gradient='horizontal',  # 渐变色方向选了垂直方向
        icon_name='fas fa-heart',  # 蒙版选取，从Font Awesome里选
        output_name=config_output_path + filename,
        background_color='#0E1B4B'
    )  # 输出词云图


main(danmaku_path)
