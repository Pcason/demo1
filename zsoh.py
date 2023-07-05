# coding:utf-8
"""
项目名称：掌上瓯海APP
注册登录后设置登录密码为123456，填写手机号即可！介意者勿用！！！
环境变量ZSOH，多账号换行隔开
作者：cason
项目地址：https://github.com/Pcason/demo1/blob/main/zsoh.py
"""
import os
import time
import requests
import notify
import hashlib


class ZhangShangOHai:
    def __init__(self, phone):
        self.session_id = self.login(phone)

    @staticmethod
    def signature(str, str2, str3, str4, str5):
        SIGNATURE_SALT = "FR*r!isE5W"
        api_version = None
        if api_version and str.startswith(api_version):
            str = str.replace(api_version, '')
        signature_str = f"{str}&&{str2}&&{str3}&&{str4}&&{SIGNATURE_SALT}&&{str5}"
        signature_hash = hashlib.sha256(signature_str.encode()).hexdigest()
        return signature_hash

    def get_headers(self, url):
        headers = {
            'X-SESSION-ID': self.session_id,
            'X-REQUEST-ID': '9357add2-f91a-4dbb-8a77-988baae5b97d',
            'X-TIMESTAMP': str(int(time.time() * 1000)),
            'X-SIGNATURE': '',
            'X-TENANT-ID': '78',
            'User-Agent': '5.0.0;00000000-67e8-b8c7-0000-0000476ca5a0;Xiaomi M2012K11AC;Android;13;Release',
            'X-ACCOUNT-ID': '64643f2e2cd91836ea7e0954'
        }
        sign = self.signature(url.split('.com')[1], headers.get('X-SESSION-ID'), headers['X-REQUEST-ID'],
                              headers['X-TIMESTAMP'],
                              headers['X-TENANT-ID'])
        headers['X-SIGNATURE'] = sign
        return headers

    def like(self, id_list):
        url = 'https://vapp.tmuyun.com/api/favorite/like'
        for id in id_list:
            data = {
                'action': 'true',
                'id': str(id)
            }
            headers = self.get_headers(url)
            res = requests.post(url, data=data, headers=headers)
            print(res.json())

    def comment(self, id_list):
        url = 'https://vapp.tmuyun.com/api/comment/create'
        for id in id_list:
            data = {
                'channel_article_id': str(id),
                'content': 'good',
                'sort_type': "0"
            }
            headers = self.get_headers(url)
            res = requests.post(url, data=data, headers=headers)
            print(res.json())

    def service(self):
        url = 'https://vapp.tmuyun.com/api/user_mumber/doTask'
        data = {
            'memberType': '6',
            'member_type': '6',
        }
        headers = self.get_headers(url)
        res = requests.post(url, data=data, headers=headers)
        print(res.json())

    def share(self, id_list):
        url = 'https://vapp.tmuyun.com/api/user_mumber/doTask'
        for id in id_list:
            data = {
                'memberType': '3',
                'member_type': '3',
                'target_id': str(id)
            }
            headers = self.get_headers(url)
            res = requests.post(url, data=data, headers=headers)
            print(res.json())

    def read(self, id_list):
        url = 'https://vapp.tmuyun.com/api/article/detail'
        for id in id_list:
            params = {
                'id': str(id)
            }
            headers = self.get_headers(url)
            res = requests.get(url, params=params, headers=headers)
            if res.json().get('code') == 0:
                print('阅读成功！')
            else:
                print('阅读失败')

    def get_title_list(self):
        url = 'https://vapp.tmuyun.com/api/article/channel_list'
        params = {
            "channel_id": "643fb01979f6be441837aba9",
            "isDiFangHao": "false",
            "is_new": "true",
            "list_count": "0",
            "size": "20",
            "start": str(int(time.time() * 1000))
        }
        headers = self.get_headers(url)
        res = requests.get(url, params=params, headers=headers)
        article_list = res.json()["data"]["article_list"]
        id_list = [x['id'] for x in article_list]
        return id_list[0:10]

    def get_sign(self):
        url = 'https://vapp.tmuyun.com/api/user_mumber/sign'
        headers = self.get_headers(url)
        r = requests.get(url, headers=headers)
        if r.json().get('code') == 0:
            print('签到成功！')
        else:
            print('签到失败')

    def get_username(self):
        url = 'https://vapp.tmuyun.com/api/user_mumber/account_detail'
        headers = self.get_headers(url)
        res = requests.get(url, headers=headers)
        phone = res.json().get('data').get('rst').get('phone_number')
        points = res.json().get('data').get('rst').get('total_integral')
        return phone, points

    def login(self, phone):
        """
        登录
        Returns:
        """
        url = 'https://passport.tmuyun.com/web/oauth/credential_auth'
        data = {
            'client_id': '10032',
            'password': "OqGdlgP9MjbfnX5oHra/BvZN/FUAnAD3XE18HkEtiOemMpSbZL4MFgwkwreSx3CODMbvcPC4NV1g04hvWNnlYQW9zdaVeczdJxyYjuAtxUKJ18mVZc0imwGIR34tk5rG5l9mhZqDxYgH4I7BSA2n2ZL10GbbmHDSFmdP5VV/0Cc=",
            # encode_password('123456'),
            'phone_number': str(phone)
        }
        headers = {
            'User-Agent': 'ANDROID;13;10032;5.0.0;1.0;null;M2012K11AC',
            'X-REQUEST-ID': '1612a329-cd31-4fab-a08d-57cd3db0082d',
            'X-SIGNATURE': 'ffbc5dc4fb8e08cef7c549ebfb7f556a2998c1579809f6961cee749cd3176198',
            'COOKIE': 'SESSION=NWE5MTEwYzMtYzc0Mi00NGQyLTgzNzMtMWM2YWMxYzY4NThh; Path=/; HttpOnly; SameSite=Lax'
        }
        res = requests.post(url, data=data, headers=headers)
        code = res.json().get("data").get("authorization_code").get("code")
        url = "https://vapp.tmuyun.com/api/zbtxz/login"
        headers = {
            'X-SESSION-ID': "646b37cf7dee053719530a5f",
            'X-REQUEST-ID': '9357add2-f91a-4dbb-8a77-988baae5b97d',
            'X-TIMESTAMP': str(int(time.time() * 1000)),
            'X-SIGNATURE': '',
            'X-TENANT-ID': '78',
            'User-Agent': '5.0.0;00000000-67e8-b8c7-0000-0000476ca5a0;Xiaomi M2012K11AC;Android;13;Release',
            'X-ACCOUNT-ID': '64643f2e2cd91836ea7e0954'
        }
        sign = self.signature(url.split('.com')[1], headers.get('X-SESSION-ID'), headers['X-REQUEST-ID'],
                              headers['X-TIMESTAMP'],
                              headers['X-TENANT-ID'])
        headers['X-SIGNATURE'] = sign

        data = {
            'code': code,
            'type': '-1'
        }
        r = requests.post(url, data=data, headers=headers)
        session_id = r.json().get('data').get('session').get('id')
        return session_id


def main():
    content = ''
    phone_list = os.getenv('ZSOH').split('\n')
    for phone in phone_list:
        hai = ZhangShangOHai(phone)
        hai.get_sign()
        hai.service()
        id_list = hai.get_title_list()
        hai.read(id_list)
        hai.share(id_list)
        hai.comment(id_list)
        hai.like(id_list)
        phone, points = hai.get_username()
        content = content + f'用户{phone}的积分:{points}\n'
    notify.pushplus_bot('掌上瓯海', content)


if __name__ == '__main__':
    main()
