# coding:utf-8
"""
项目名称：悦马星空APP
抓包appapi.changan-mazda.com.cn域名下Authorization值，只要Bearer 后面的部分。
青龙环境变量ymsk，多账号换行隔开
作者：cason
项目地址：https://github.com/Pcason/demo1/blob/main/ymsk.py
"""
import json
import os
import notify
import requests


def get_point(token, memberid):
    '''
    查询积分值
    :param token: 
    :param memberid: 
    :return: 
    '''
    url = 'https://appapi.changan-mazda.com.cn/api-user/point/getUserPointInfo'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    data = json.dumps({"memberId": memberid})
    r = requests.post(url, data=data, headers=headers)
    return r.json().get('data')[0].get('usablePoint')


def send_releaseCount(token):
    '''
    发布文章
    :param token: 
    :return: 
    '''
    url = 'https://appapi.changan-mazda.com.cn/api-content/dynamic/publishDynamic'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    data = json.dumps(
        {"mvUrl": "", "content": "<p>哈哈哈哈<\/p>", "isMv": "false", "contentStr": "哈哈哈哈", "contentUrl": [], "latitude": 0,
         "longitude": 0, "quoteTopic": [], "topicId": "", "userls": [], "isReward": "false"})
    r = requests.post(url, data=data, headers=headers)
    return r.json().get('code')


def releaseCount_total(userid):
    '''
    统计已发布文章总数
    :param userid: 
    :return: 
    '''
    url = 'https://appapi.changan-mazda.com.cn/api-user/user/focus/focusAndFansCount?userId=' + userid
    r = requests.get(url)
    return r.json().get('data').get('releaseCount')


def send_comment(token):
    '''
    发布评论
    :param token: 
    :return: 响应码
    '''
    url = 'https://appapi.changan-mazda.com.cn/api-content/comment/addComment'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    data = json.dumps(
        {"commentOffsetVos": [], "parentId": "-1", "contentId": "1a91b3e74207c9de46ff01f3c0e22e0b", "contentType": "3",
         "content": "哈哈哈", "isReplyMain": 1, "avatar": "", "nickname": "粉丝1613422230716170241",
         "userId": "1613422229692977153", "replyUserId": "", "userLs": [], "replyUserName": ""})
    r = requests.post(url, data=data, headers=headers)
    return r.json().get('code')


def get_userid(token):
    '''
    获取用户基本信息
    :param token: 
    :return: 用户id，memberId，memberId
    '''
    url = 'https://appapi.changan-mazda.com.cn/api-auth/oauth/current/user'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    r = requests.get(url, headers=headers)
    return r.json().get('data').get('id'), r.json().get('data').get('memberId'), r.json().get('data').get('memberId')


def signin(token, userid):
    '''
    签到
    :param token: 
    :param userid: 
    :return: 
    '''
    url = 'https://appapi.changan-mazda.com.cn/api-user/user/signin'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    data = json.dumps({"userId": userid})
    r = requests.post(url, headers=headers, data=data)
    return r.json().get('code')


def main():
    content = ''
    token_list = os.getenv('ymsk').split('\n')
    # token_list=['8e3a0f1f-2f73-45f2-aaf3-eaa8076717c4']
    print('=====检测到'+str(len(token_list))+'个账号======')
    for token in token_list:
        userid, memberid, username = get_userid(token)
        signin_code = signin(token, userid)
        if signin_code == 200:
            print('签到成功')
        count_code = send_releaseCount(token)
        if count_code == 200:
            print('文章发表成功!')
        for i in range(1, 11):
            comment_code = send_comment(token)
            if comment_code == 200:
                print('评论成功!')
        release_count = releaseCount_total(userid)
        point = get_point(token, memberid)
        print(username, '文章发表总数:', release_count)
        print(username, '目前积分:', point)
        content += username+'目前积分: '+str(point)+'\n'
    notify.pushplus_bot('悦马星空', content)


if __name__ == '__main__':
    main()
