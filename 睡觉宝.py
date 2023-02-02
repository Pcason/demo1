# coding:utf-8
import os
import random
import time
import requests
import notify


class SleepBody:
    def __init__(self, ua):
        self.headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; M2012K11AC Build/N6F26Q)',
            'ua': ua
        }
        self.now_time = int(time.strftime('%H', time.localtime(time.time())))

    def login(self):
        url = 'https://mapi.shuijiaobao.cn/login/code'
        data = {
            "versionName": "2.0.5",
            "pName": "ql_sleep",
            "channel": "sl_ali",
            "userId": "920404"
        }
        r = requests.post(url, headers=self.headers, data=data)
        if r.json().get('msg') == '成功':
            user_name = r.json().get('data').get('userInfo').get('name')
            token = r.json().get('data').get('userInfo').get('accessToken')
            return user_name, token
        else:
            print(r.json().get('msg'))

    def sign(self):
        if self.now_time in [7, 8, 9]:
            url = 'https://mapi.shuijiaobao.cn/home/sign'
            r = requests.post(url, headers=self.headers)
            print(r.json())
        else:
            print('今日已签到')

    def sleep(self):
        start_url = 'https://mapi.shuijiaobao.cn/sleep/createOrderSleep'
        end_url = 'https://mapi.shuijiaobao.cn/sleep/clickWakeUp'
        gold_url = 'https://mapi.shuijiaobao.cn/sleep/collectSleepGoldAll'
        if self.now_time in [12, 13, 14, 20, 21, 22]:
            res = requests.post(start_url, headers=self.headers)
            if res.json().get('msg') == '成功':
                print('开始睡觉了。。。')
            else:
                print(res.json().get('msg'))
        elif self.now_time in [15, 16, 17, 7, 8, 9]:
            res = requests.post(end_url, headers=self.headers)
            if res.json().get('msg') == '成功':
                print('睡醒了！')
                r = requests.post(gold_url, headers=self.headers)
                if r.json().get('msg') == '成功':
                    print('领取金币：', r.json().get('data').get('number'))
                else:
                    print(r.json().get('msg'))
            else:
                print(res.json().get('msg'))
        else:
            print('未到睡觉时间。')

    def feed(self):
        url = 'https://mapi.shuijiaobao.cn/sleep/dinnerCreate'
        r = requests.post(url, self.headers)
        if self.now_time in [7, 8, 9, 12, 13, 14, 17, 18, 20, 21, 22]:
            if r.json().get('msg') == '成功':
                print('吃饭领取金币：', r.json().get('data').get('gold_number'))
            else:
                print(r.json().get('msg'))
        else:
            print('未到吃饭时间。')

    def view_video(self):
        url = 'https://mapi.shuijiaobao.cn/task/dayReward'
        data = {
            'type': '155'
        }
        if self.now_time in [7, 8, 9]:
            for i in range(1, 9):
                r = requests.post(url, headers=self.headers, data=data)
                if r.json().get('msg') == '成功':
                    print(f'第{i}次看视频领取金币：', r.json().get('data').get('user_info').get('add_gold_coin'))
                else:
                    print(r.json().get('msg'))
                time.sleep(random.randint(10, 15) + random.random())
        else:
            print('今日已观看视频')

    def user_gold(self):
        url = 'https://mapi.shuijiaobao.cn/user/userContent'
        r = requests.post(url, headers=self.headers)
        if r.json().get('msg') == '成功':
            userGold = r.json().get('data').get('userGold')
            print('用户当前金币数量；', userGold)
            return userGold
        else:
            print(r.json().get('msg'))


def main():
    content = ''
    ua_list = os.getenv('sjbck').split('\n')
    print(ua_list)
    print('=====检测到' + str(len(ua_list)) + '个账号======')
    for ua in ua_list:
        sleep_body = SleepBody(ua)
        user_name, token = sleep_body.login()
        print(f'\n=======开始账号【{user_name}】========\n')
        sleep_body.sign()
        sleep_body.sleep()
        sleep_body.feed()
        sleep_body.view_video()
        gold = sleep_body.user_gold()
        print('当前账户积分：', gold)
        content += f'账号{user_name},当前积分为{gold}\n'
    notify.pushplus_bot('睡觉宝', content)


if __name__ == '__main__':
    main()
