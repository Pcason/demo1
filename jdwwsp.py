# coding:utf-8
import os
import time
import notify
import requests


def main():
    content = ''
    ck_list = os.getenv('jdck').split('\n')
    print('=====检测到' + str(len(ck_list)) + '个账号======')
    for num, ck in enumerate(ck_list):
        num = num + 1
        url = 'https://api.m.jd.com/'
        headers = {
            "Cookie": ck,
            "Origin": "https://h5platform.jd.com",
            'User-Agent': 'jdltapp;android;4.9.0;;;appBuild/2394;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1679034000534%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22EG%3D%3D%22%2C%22ad%22%3A%22DJHsDwGmEJHvYwVuYtYmCm%3D%3D%22%2C%22od%22%3A%22%22%2C%22ov%22%3A%22Ctq%3D%22%2C%22ud%22%3A%22DJHsDwGmEJHvYwVuYtYmCm%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jd.jdlite%22%7D;Mozilla/5.0 (Linux; Android 9; M2012K11AC Build/PQ3A.190801.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            "functionId": "runningPrizeDraw",
            "body": "{\"linkId\":\"L-sOanK_5RJCz7I314FpnQ\",\"type\":1,\"level\":3}",
            "t": str(int(time.time() * 1000)),
            "appid": "activities_platform",
            "client": "android",
            "clientVersion": "4.9.0",
            "cthr": "1",
            "uuid": "5343266346039343-5626564626630333",
            "build": "2394",
            "screen": "393*873",
            "networkType": "wifi",
            "d_brand": "Redmi",
            "d_model": "M2012K11AC",
            "lang": "zh_CN",
            "osVersion": "9",
            "partner": "xiaomi",
            "eid": "eidA084d81228bs4VFw7AdV9THaSrfmQZpQLlFRcPIjDtiS3h3Uwsantbf9pbMW94Qg9NVNtpfZlIEWqgCKpLeBUBTvbXJdmSX0XERDkCcFV4uaV9Bg2"
        }
        for i in range(50):
            res = requests.post(url, data=data, headers=headers)
            print(res.json())
            if res.json().get('success') == 'Ture':
                content += res.text + '\n'
                break
        if content == '':
            content = '抱歉，没抢到！'
    notify.pushplus_bot('旺旺赛跑', content)


if __name__ == '__main__':
    main()
