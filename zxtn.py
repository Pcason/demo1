# coding:utf-8
"""
项目名称：掌心潼南APP
新版本打不开下载旧版本，登录密码设置为123456abc
手机号填入环境变量zxtn，换行分割
每天一次即可
作者：cason
项目地址：https://github.com/Pcason/demo1/blob/main/zxtn.py
"""
import os
import requests
import notify

headers = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; M2012K11AC Build/N6F26Q)'
}


def login(phone):
    """
    登录
    Args:
    phone: 手机号
    Returns:

    """
    url = 'https://api.cqliving.com//login.html'
    data = {
        'appId': '37',
        'loginName': phone,
        'pwd': 'df10ef8509dc176d733d59549e7dbfaf',
        'hashSign': '63adc2327c81f59c276a15aa34f92688',
        'sessionId': '6df56b8ccb2e4935a225a6d4ffb8da85'
    }
    res = requests.post(url, data=data, headers=headers)
    try:
        token = res.json().get('data').get('token')
        print('登陆成功')
        return token
    except Exception as e:
        print('登录失败！', e)
        exit()


def praise(token):
    url = 'https://h5.cqliving.com//info/doPraise.html'
    for i in range(5298670, 5298680):
        data = {
            'appId': '37',
            'sourceId': str(i),
            'sourceType': '1',
            'sessionId': '6df56b8ccb2e4935a225a6d4ffb8da85',
            'token': token,
            'type': '0'
        }
        res = requests.post(url, data=data, headers=headers)
        if res.json().get('code') == 0:
            print('点赞成功，获得{}积分'.format(res.json().get('data').get('point')))
        else:
            print("点赞失败", res.json().get('message'))


def reading(token):
    url = 'https://api.cqliving.com/point/read/addPoint.html'
    for i in range(5298671, 5298680):
        data = {
            'appId': '37',
            'v': '1',
            'sessionId': '6df56b8ccb2e4935a225a6d4ffb8da85',
            'token': token,
            'informationId': str(i),
            'sourceType': '1'
        }
        res = requests.post(url, data=data, headers=headers)
        if res.json().get('code') == 0:
            print('阅读成功，获得{}积分'.format(res.json().get('data').get('point')))
        else:
            print("阅读失败", res.json().get('message'))
    for i in range(5298688, 5298699):
        data = {
            'appId': '37',
            'v': '1',
            'sessionId': '6df56b8ccb2e4935a225a6d4ffb8da85',
            'token': token,
            'informationId': str(i),
            'sourceType': '1'
        }
        res = requests.post(url, data=data, headers=headers)
        if res.json().get('code') == 0:
            print('阅读成功，获得{}积分'.format(res.json().get('data').get('point')))
        else:
            print("阅读失败", res.json().get('message'))


def comment(token):
    url = 'https://api.cqliving.com/commentSave.html'
    for i in range(5298660, 5298665):
        data = {
            'appId': '37',
            'sourceId': str(i),
            'sourceType': '1',
            'sessionId': '6df56b8ccb2e4935a225a6d4ffb8da85',
            'token': token,
            'v': '1',
            'content': '666',
            'isAnonymous': 'false'
        }
        res = requests.post(url, data=data, headers=headers)
        if res.json().get('code') == 1:
            print('评论成功，获得{}积分'.format(res.json().get('data').get('point')))
        else:
            print("评论失败", res.json().get('message'))


def share(token):
    url = 'https://api.cqliving.com//shareLog.html'
    for i in range(5298660, 5298680):
        data = {
            'appId': '37',
            'sourceId': str(i),
            'sourceType': '1',
            'sessionId': '6df56b8ccb2e4935a225a6d4ffb8da85',
            'token': token,
            'v': '1',
            'platform': '1'
        }
        res = requests.post(url, data=data, headers=headers)
        if res.json().get('code') == 0:
            print('分享成功，获得{}积分'.format(res.json().get('data').get('point')))
        else:
            print("分享失败", res.json().get('message'))


def sign(token):
    url = 'https://h5.cqliving.com/point/doSign.html'
    data = {
        'v': '1',
        'appId': '37',
        'token': token,
        'sessionId': '6df56b8ccb2e4935a225a6d4ffb8da85'
    }
    res = requests.post(url, data=data, headers=headers)
    if res.json().get('code') == 0:
        print('签到成功')
    else:
        print("签到失败", res.json().get('message'))


def point_info(token):
    url = 'https://api.cqliving.com/point/myInfo.html'
    data = {
        'v': '1',
        'appId': '37',
        'token': token,
        'sessionId': '6df56b8ccb2e4935a225a6d4ffb8da85'
    }
    res = requests.post(url, data=data, headers=headers)
    if res.json().get('code') == 0:
        currentPoint = res.json().get('data').get('currentPoint')
        return currentPoint
    else:
        print("查询积分失败", res.json().get('message'))


def main():
    content = ''
    phone_list = os.getenv('zxtn').split('\n')
    print('=====检测到' + str(len(phone_list)) + '个账号======')
    for num, phone in enumerate(phone_list):
        print(f'=======开始账号[{num}]========')
        num += 1
        token = login(phone)
        sign(token)
        reading(token)
        praise(token)
        comment(token)
        share(token)
        currentPoint = point_info(token)
        print(f'账号[ {num} ]当前积分：', currentPoint)
        content += f'账号{phone}当前积分：{currentPoint}\n'
    notify.pushplus_bot('掌心潼南', content)


if __name__ == '__main__':
    main()
