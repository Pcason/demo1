# coding:utf-8
import os

import requests

import notify


def get_details(token):
    url = 'https://tree-prod.graylog.chimps.cn/player/re-enter'
    headers = {
        'Authorization': token
    }
    r = requests.get(url, headers=headers)
    # print(r.json())
    water=r.json().get('data').get('tree').get('water')
    energy=r.json().get('data').get('energy')
    nutrient=r.json().get('data').get('tree').get('nutrient')
    fruit=r.json().get('data').get('tree').get('fruit').get('1')
    fertilizer = r.json().get('data').get('tree').get('fertilizer')
    return water,energy, nutrient, fruit, fertilizer


def sign_roll(token):
    url = 'https://tree-prod.graylog.chimps.cn/sign-roll/roll'
    headers = {
        'Authorization': token
    }
    data_list = [
        {
            'rewardType': 'login'
        },
        {
            'rewardType': 'share'
        },
        {
            'rewardType': 'video'
        },
        {
            'rewardType': 'video'
        }
    ]
    for data in data_list:
        while True:
            r = requests.post(url, data=data, headers=headers)
            errcode = r.json().get('errcode')
            if errcode == 40002:
                print(r.json().get('errmsg'))
                break
            else:
                print('抽奖获得成功!')


def daily_tasks(token):
    url = 'https://tree-prod.graylog.chimps.cn/free/reward'
    headers = {
        'Authorization': token
    }
    params_list = [
        {
            'type': 'login',
            'rewardType': ''
        },
        {
            'type': 'viewManor',
            'rewardType': ''
        },
        {
            'type': 'shareGold',
            'rewardType': ''
        },
        {
            'type': 'videoWater',
            'rewardType': ''
        },
        {
            'type': 'wxNotify',
            'rewardType': ''
        },
        {
            'type': 'subscribe',
            'rewardType': ''
        }
    ]
    for params in params_list:
        while True:
            r = requests.get(url, params=params, headers=headers)
            errcode = r.json().get('errcode')
            if errcode == 40002:
                print(r.json().get('errmsg'))
                break
            else:
                print('完成任务获得水滴: ', r.json().get('data').get('rewards')[0].get('water'))


def play_video(token):
    url='https://tree-prod.graylog.chimps.cn/player/add-reward'
    headers = {
        'Authorization': token
    }
    data={
        'reason':'dailyFreeWaterAgain',
        'rewardTpye':'video'
    }
    for i in range(3):
        r = requests.post(url, data=data, headers=headers)
        errcode = r.json().get('errcode')
        if errcode == 40002:
            print(r.json().get('errmsg'))
            break
        else:
            print('看视频获得水滴: 10')


def reward_share_friend(token):
    url='https://tree-prod.graylog.chimps.cn/free/reward-share-friend'
    headers = {
        'Authorization': token
    }
    data={
        'rewardType':'share'
    }
    for i in range(5):
        r=requests.post(url, data=data, headers=headers)
        errcode = r.json().get('errcode')
        if errcode == 40002:
            print(r.json().get('errmsg'))
            break
        else:
            print('分享获得水滴: ', r.json().get('data').get('rewards').get('water'))


def share_friend_big(token):
    url='https://tree-prod.graylog.chimps.cn/free/reward-share-friend-big'
    headers = {
        'Authorization': token
    }
    data_list=[
        {
            'idx':'2'
        },
        {
            'idx': '5'
        }
    ]
    for data in data_list:
        r=requests.post(url, data=data, headers=headers)
        errcode = r.json().get('errcode')
        if errcode == 40002:
            print(r.json().get('errmsg'))
            break
        else:
            print('礼包领取成功!')

def add_rewards(token):
    url='https://tree-prod.graylog.chimps.cn/player/add-reward'
    headers = {
        'Authorization': token
    }
    data={
        'reason':'rewardBalloon'
    }
    while True:
        r = requests.post(url, data=data, headers=headers)
        errcode = r.json().get('errcode')
        if errcode == 40002:
            print(r.json().get('errmsg'))
            break
        else:
            print('获得水滴: 10')


def answer(token):
    while True:
        answer_url= 'https://tree-prod.graylog.chimps.cn/player/unlock'
        headers = {
            'Authorization': token
        }
        data={}
        r=requests.post(answer_url, data=data, headers=headers)
        errcode = r.json().get('errcode')
        if errcode == 40002:
            print(r.json().get('errmsg'))
            break
        else:
            answer_pass_url='https://tree-prod.graylog.chimps.cn/player/pass'
            data={
                'rangeTime': '30'
            }
            r2=requests.post(answer_pass_url, data=data, headers=headers)
            print('答题成功，获得水滴: ',r2.json().get('data').get('addWater'))


def watering(token):
    while True:
        url='https://tree-prod.graylog.chimps.cn/tree/water'
        headers = {
            'Authorization': token
        }
        data={}
        r=requests.post(url, data=data, headers=headers)
        errcode = r.json().get('errcode')
        if errcode == 40002:
            errmsg = r.json().get('errmsg')
            if errmsg == '您的土壤养分不足，快去施肥吧':
                fertilizer(token)
                use_fertilizer(token)
                continue
            elif errmsg == '已到最高等级，赶紧收集水果吧':
                got_fruit(token)
                continue
            elif errmsg == '请先播种':
                sowing(token)
                continue
            print(errmsg)
            break
        print('浇水成功，剩余水滴: ',r.json().get('data').get('tree').get('water'))


def fertilizer(token):
    url='https://tree-prod.graylog.chimps.cn/player/add-reward'
    headers = {
        'Authorization': token
    }
    data={
        'reason':'dailyFertilizerByVideo',
        'rewardType':'video'
    }
    r=requests.post(url, data=data, headers=headers)
    errcode = r.json().get('errcode')
    if errcode == 40002:
        print(r.json().get('errmsg'))
    else:
        print('领取成功，目前肥料数量: ',r.json().get('data').get('fertilizer'))

def use_fertilizer(token):
    url='https://tree-prod.graylog.chimps.cn/tree/use-fertilizer'
    headers = {
        'Authorization': token
    }
    data={}
    while True:
        r = requests.post(url, data=data, headers=headers)
        errcode = r.json().get('errcode')
        if errcode == 40002:
            print(r.json().get('errmsg'))
            break
        else:
            print('施肥成功')
            print('目前养分: ', r.json().get('data').get('tree').get('nutrient'))
            print('目前剩余肥料数量: ', r.json().get('data').get('tree').get('fertilizer'))



def got_fruit(token):
    url='https://tree-prod.graylog.chimps.cn/tree/got-fruit'
    headers = {
        'Authorization': token
    }
    data_list=[
        {
            'idx':'2'
        },
        {
            'idx':'1'
        }
    ]
    for data in data_list:
        r=requests.post(url, data=data, headers=headers)
        errcode = r.json().get('errcode')
        if errcode == 40002:
            print(r.json().get('errmsg'))
        else:
            print('领取成功，目前果实数量: ', r.json().get('data').get('tree').get('fruit').get('1'))


def sowing(token):
    url='https://tree-prod.graylog.chimps.cn/tree/sowing'
    headers = {
        'Authorization': token
    }
    data={
        'type':'1'
    }
    r=requests.post(url, data=data, headers=headers)
    errcode = r.json().get('errcode')
    if errcode == 40002:
        print(r.json().get('errmsg'))
    else:
        print('播种成功')


def main():
    content = ''
    token_list = os.getenv('cygy').split('\n')
    for num, token in enumerate(token_list):
        num = num+1
        sign_roll(token)
        daily_tasks(token)
        play_video(token)
        reward_share_friend(token)
        share_friend_big(token)
        add_rewards(token)
        answer(token)
        watering(token)
        water, energy, nutrient, fruit, fertilizer = get_details(token)
        print(f'账号[{num}]当前水滴数量: ', water)
        print(f'账号[{num}]当前体力值: ', energy)
        print(f'账号[{num}]当前养分: ', nutrient)
        print(f'账号[{num}]当前肥料数量: ', fertilizer)
        print(f'账号[{num}]当前果实数量: ', fruit)
        content += f'=========账号[ {num} ]=========\n账号[{num}]当前水滴数量: {water}\n账号[{num}]当前体力值: {energy}\n账号[{num}]当前养分: {nutrient}\n账号[{num}]当前肥料数量: {fertilizer}\n账号[{num}]当前果实数量: {fruit}\n\n'
    notify.pushplus_bot('成语果园', content)


if __name__ == '__main__':
    main()
