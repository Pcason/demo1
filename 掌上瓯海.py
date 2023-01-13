# coding:utf-8
import os

import requests
import json


def get_points(authorization):
    url = 'https://newsapi.wzrb.com.cn/api/Users/Info'
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Host': 'newsapi.wzrb.com.cn',
        'User-Agent': 'ohnews/4.0 (iPhone; iOS 14.8; Scale/2.00)',
        'Authorization': f'Bearer {authorization}',
        'Accept-Language': 'zh-Hans-CN;q=1, ja-CN;q=0.9'
    }
    r = requests.get(url, headers=headers)
    if r.json().get('code') != 0:
        return '', 'token失效'
    return r.json().get('data').get('mobile'), r.json().get('data').get('points')


def get_quests(authorization):
    url = 'https://newsapi.wzrb.com.cn/api/users/completed-quests'
    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'newsapi.wzrb.com.cn',
        'Authorization': f'Bearer {authorization}',
    }
    while True:
        n = 0
        for id in range(1, 31):
            data = json.dumps({"questId": id})
            r = requests.post(url, data=data, headers=headers)
            if r.json().get('status') != 200:
                print(id, r.json().get('msg'))
                n += 1
            else:
                print(id, r.json().get('data').get('quest').get('name'), '获得积分',
                      r.json().get('data').get('quest').get('score'))
        if n == 30:
            break
        else:
            n = 0


def main():
    token_list = os.getenv('ZSOH').split('@')
    for token in token_list:
        mobile, points = get_points(token)
        if mobile == '':
            print('用户token失效')
        else:
            print(f'用户{mobile}的积分:{points}')
        get_quests(token)
        mobile, points = get_points(token)
        print(f'用户{mobile}的积分:{points}')


if __name__ == '__main__':
    main()
