#!/usr/bin/python3
import json
import time
from bilibili_api import live, sync

# configs
# live room ID
config_liveroom_id = 3314896
config_danmaku_savepath = './danmaku/'

room = live.LiveDanmaku(config_liveroom_id)


@room.on('DANMU_MSG')
async def on_danmaku(event):
    # 收到弹幕
    content = event['data']['info'][1]
    sender_uid = event['data']['info'][2][0]
    sender_nickname = event['data']['info'][2][1]
    image_height = event['data']['info'][0][13]['height'] if event['data']['info'][0][13] != "{}" else ''
    image_width = event['data']['info'][0][13]['width'] if event['data']['info'][0][13] != "{}" else ''
    image_url = event['data']['info'][0][13]['url'] if event['data']['info'][0][13] != "{}" else ''
    sender_medal_level = event['data']['info'][3][0] if len(event['data']['info'][3]) > 0 else ''
    sender_medal_medal_name = event['data']['info'][3][1] if len(event['data']['info'][3]) > 0 else ''
    sender_medal_medal_upper_nickname = event['data']['info'][3][2] if len(event['data']['info'][3]) > 0 else ''
    sender_medal_medal_upper_liveroom = event['data']['info'][3][3] if len(event['data']['info'][3]) > 0 else ''
    sender_medal_medal_upper_uid = event['data']['info'][3][-1] if len(event['data']['info'][3]) > 0 else ''
    danmu = {
        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'content': content,
        'image': {
            'height': image_height,
            'width': image_width,
            'url': image_url
        },
        'sender': {
            'uid': sender_uid,
            'nickname': sender_nickname
        },
        'medal': {
            'level': sender_medal_level,
            'name': sender_medal_medal_name,
            'upper': {
                'uid': sender_medal_medal_upper_uid,
                'nickname': sender_medal_medal_upper_nickname,
                'liveroom': sender_medal_medal_upper_liveroom
            }
        }
    }
    data = json.dumps(danmu, ensure_ascii=False)
    print(data)
    record_and_append_danmaku(data)


def record_and_append_danmaku(danmu):
    now_date = time.strftime("%Y-%m-%d", time.localtime())
    fo = open(config_danmaku_savepath + now_date + ".txt", "a+")
    fo.write(danmu + "\n")
    fo.close()


sync(room.connect())
