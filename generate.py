import json
import os
import jieba
import stylecloud

def main(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        for file in files:
            data = readDatas(file_dir+'/'+file)
            userRank = analyseUserTop(data)
            # print(userTop)
            timeline = analyseTime(data)
            # print(time)
            pie = analysePie(userRank)
            wordcloud(file, data)
            save2Js(file, userRank, timeline, pie)

def save2Js(filename, userRank, timeline, pie):
    result = {}
    filename = filename[13:21] + '.json'
    outputPath = './output/'
    result['user_rank'] = userRank
    result['timeline'] = timeline
    result['pie'] = pie
    jsonStr = json.dumps(result)
    fullpath = outputPath+filename
    file = open(fullpath, 'w')
    file.write(jsonStr)
    file.close()
    print(fullpath + '文件已经创建')


def readDatas(file):
    with open(file, 'r', encoding='utf-8') as lines:
        array = lines.readlines()  #返回的是一个列表，该列表每一个元素是txt文件的每一行
        datas = [] #使用一个新的列表来装去除换行符\n后的数据
        for i in array: #遍历array中的每个元素
            dict = {}
            time = i[4:9]
            dict['time'] = time
            nicknameStart = i.find(' : ') + 3
            nicknameEnd = i.find(' 说：')
            nickname = i[nicknameStart:nicknameEnd]
            dict['nickname'] = nickname
            content = i[nicknameEnd+3:]
            dict['content'] = content
            datas.append(dict)
        return datas

def analyseUserTop(datas):
    result = {}
    analyse = {}
    skipNickname = ['伊利专属智能助手', '原来我不是白羊座']
    for data in datas:
        if data['nickname'] in skipNickname:
            continue
        isIn = data['nickname'] in analyse.keys()
        if not isIn:
            analyse[data['nickname']] = 0
    for data in datas:
        if data['nickname'] in skipNickname:
            continue
        isIn = data['nickname'] in analyse.keys()
        if isIn:
            analyse[data['nickname']] += 1
        else:
            analyse[data['nickname']] = 0
    d_order = sorted(analyse.items(), key=lambda x: x[1], reverse=True)
    sortedDict = dict(d_order)
    result['label'] = list(sortedDict.keys())
    result['value'] = list(sortedDict.values())
    return result

def analyseTime(datas):
    res = {}
    result = {}
    for item in range(24):
            result[str(item)+':00'] = 0
    for data in datas:
        hour = data['time'][0:2]+':00'
        isIn = hour in result.keys()
        if isIn:
            result[hour] += 1
        else:
            result[hour] = 0
    res['label'] = list(result.keys())
    res['value'] = list(result.values())
    return res

def analysePie(userRank):
    result = []
    for index, item in enumerate(userRank['label']):
        row = {}
        limit = 3
        if index > limit-1:
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
    filename = filename[13:21] + '.png'
    outputPath = './wordcloud/'
    allContent = ''
    skipNickname = ['伊利专属智能助手', '原来我不是白羊座']
    for data in datas:
        if data['content'].find('我就是天选之人') >= 0:
            continue
        if data['content'].find('点点红包抽礼物') >= 0:
            continue
        if data['nickname'] in skipNickname:
            continue
        allContent += data['content']
    # print(allContent)
    word_list = jieba.cut(allContent)
    result = " ".join(word_list)  # 分词用空格隔开
    result = result.replace('的', '').replace('我', '').replace('你', '').replace('啊', '').replace('了', ''). \
        replace('就', '').replace('是', '').replace('这', '').replace('不', '').replace('都', '').replace('好', ''). \
        replace('有', '').replace('要', '').replace('没', '').replace('还', '').replace('也', '').replace('个', '').\
        replace('那', '')
    stylecloud.gen_stylecloud(
        text=result,  # 上面分词的结果作为文本传给text参数
        size=512,
        font_path='STHeiti Light.ttc',  # 字体设置
        palette='cartocolors.qualitative.Pastel_7',  # 调色方案选取，从palettable里选择
        gradient='horizontal',  # 渐变色方向选了垂直方向
        icon_name='fas fa-heart',  # 蒙版选取，从Font Awesome里选
        output_name=outputPath+filename)  # 输出词云图


dataPath = './data'
main(dataPath)