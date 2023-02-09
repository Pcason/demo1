# coding:utf-8
"""
项目名称:打水果赚钱微信小游戏
抓包https://api.xyx.bkdau.cn/?c=emnew&a=getSelfInfo 的请求体加密内容（oxr9uhUQ...==）
环境变量dsgck 多账号换行分开，每天1~2次
作者：cason
项目地址：https://github.com/Pcason/demo1
"""
import json
import os
import random
import time
import requests
import base64
from Crypto.Cipher import AES
import notify


class Fruit:
    def __init__(self, token):
        self.token = token
        self.headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; M2012K11AC Build/N6F26Q)'}

    @staticmethod
    def AES_Encrypt(data):
        key = '<690>!?&^gkg4k5M'
        vi = '!k&H)f8^75(*?<29'
        BLOCK_SIZE = 16  # Bytes
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                        chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
        data = pad(data)
        # 字符串补位
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
        encryptedbytes = cipher.encrypt(data.encode('utf8'))
        # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
        encodestrs = base64.b64encode(encryptedbytes)
        # 对byte字符串按utf-8进行解码
        enctext = encodestrs.decode('utf8')
        return enctext

    @staticmethod
    def AES_Decrypt(data):
        key = '<690>!?&^gkg4k5M'
        vi = '!k&H)f8^75(*?<29'
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        data = data.encode('utf8')
        encodebytes = base64.decodebytes(data)
        # 将加密数据转换位bytes类型数据
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
        text_decrypted = cipher.decrypt(encodebytes)
        # 去补位
        text_decrypted = unpad(text_decrypted)
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted

    def get_info(self):
        url = 'https://api.xyx.bkdau.cn/?c=emnew&a=getSelfInfo'
        data = self.token
        r = requests.post(url, data=data, headers=self.headers)
        detext = self.AES_Decrypt(r.text)
        if json.loads(detext).get('msg') == 'success':
            cash = json.loads(detext).get('ret').get('cash')
            stage = json.loads(detext).get('ret').get('stage')
            print('当前金额为：', cash)
            print('当前关卡：', stage)
            return cash
        else:
            print('查询失败：', json.loads(detext).get('msg'))

    def stage(self):
        start_url = 'https://api.xyx.bkdau.cn/?c=emdsg&a=startStage'
        finish_url = 'https://api.xyx.bkdau.cn/?c=emdsg&a=stageFinish'
        proopen_url = 'https://api.xyx.bkdau.cn/?c=emdsg&a=preOpenStageRp'
        doopen_url = 'https://api.xyx.bkdau.cn/?c=emdsg&a=doOpenStageRp'
        svlog_url = 'https://api.xyx.bkdau.cn/?c=emnew&a=svLog'
        marquee_url = 'https://api.xyx.bkdau.cn/?c=emnew&a=getMarquee'
        preboss_url = 'https://api.xyx.bkdau.cn/?c=emdsg&a=preOpenScBoss'
        doboss_url = 'https://api.xyx.bkdau.cn/?c=emdsg&a=doOpenScBoss'
        svlog_data = json.loads(self.AES_Decrypt(self.token))
        svlog_data['log_type'] = 2
        svlog_data = self.AES_Encrypt(json.dumps(svlog_data))
        start_data = json.loads(self.AES_Decrypt(self.token))
        start_data['id'] = 1000
        start_data = self.AES_Encrypt(json.dumps(start_data))
        # 开始游戏
        start_res = requests.post(start_url, data=start_data, headers=self.headers)
        if json.loads(self.AES_Decrypt(start_res.text)).get('msg') == 'success':
            stage = json.loads(self.AES_Decrypt(start_res.text)).get('ret').get('stage')
            print('开始闯关：', stage)
            open_data = json.loads(self.AES_Decrypt(self.token))
            open_data['stage'] = stage
            open_data = self.AES_Encrypt(json.dumps(open_data))
            # 第一次领取
            propen_res = requests.post(proopen_url, data=open_data, headers=self.headers)
            if json.loads(self.AES_Decrypt(propen_res.text)).get('msg') == 'success':
                # 红包领取
                preboss_res = requests.post(preboss_url, data=open_data, headers=self.headers)
                if json.loads(self.AES_Decrypt(preboss_res.text)).get('msg') == 'success':
                    doboss_res = requests.post(doboss_url, data=open_data, headers=self.headers)
                    r_cash = json.loads(self.AES_Decrypt(doboss_res.text)).get('ret').get('r_cash')
                    t_cash = json.loads(self.AES_Decrypt(doboss_res.text)).get('ret').get('t_cash')
                    print('领取闯关红包，获得金额：', r_cash, '元，当前总金额：', t_cash, '元')
                else:
                    print('闯关红包领取失败：', json.loads(self.AES_Decrypt(preboss_res.text)).get('msg'))
                time.sleep(random.randint(3, 5) + random.random())  # 随机等待3~5秒
                # 第二次领取
                doopen_res = requests.post(doopen_url, data=open_data, headers=self.headers)
                if json.loads(self.AES_Decrypt(doopen_res.text)).get('msg') == 'success':
                    r_cash = json.loads(self.AES_Decrypt(doopen_res.text)).get('ret').get('r_cash')
                    t_cash = json.loads(self.AES_Decrypt(doopen_res.text)).get('ret').get('t_cash')
                    print('闯关成功，获得金额：', r_cash, '元，当前总金额：', t_cash, '元')
                    requests.post(marquee_url, data=open_data, headers=self.headers)
                    requests.post(marquee_url, data=open_data, headers=self.headers)
                    svlog_res = requests.post(svlog_url, data=svlog_data, headers=self.headers)
                    requests.post(marquee_url, data=open_data, headers=self.headers)
                    requests.post(marquee_url, data=open_data, headers=self.headers)
                    print(json.loads(self.AES_Decrypt(svlog_res.text)).get('msg'))
                else:
                    # print(json.loads(self.AES_Decrypt(doopen_res.text)))
                    print('1闯关金币领取失败：', json.loads(self.AES_Decrypt(doopen_res.text)).get('msg'))
            else:
                # print(json.loads(self.AES_Decrypt(propen_res.text)))
                print('2闯关金币领取失败：', json.loads(self.AES_Decrypt(propen_res.text)).get('msg'))
            # 结束游戏
            finish_res = requests.post(finish_url, data=open_data, headers=self.headers)
            if json.loads(self.AES_Decrypt(finish_res.text)).get('msg') == 'success':
                print('结束闯关')
            else:
                print('结束闯关出错：', json.loads(self.AES_Decrypt(finish_res.text)).get('msg'))
        else:
            print('闯关出错：', json.loads(self.AES_Decrypt(start_res.text)).get('msg'))

    def sign(self):
        sign_url = 'https://api.xyx.bkdau.cn/?c=emnew&a=doRpTask'
        prize_url = 'https://api.xyx.bkdau.cn/?c=emnew&a=oRpTaskPrize'
        sign_data = json.loads(self.AES_Decrypt(self.token))
        stage_data = sign_data
        stage_data['task_id'] = 40001
        stage_data = self.AES_Encrypt(json.dumps(stage_data))
        sign_data['task_id'] = 10001
        sign_data = self.AES_Encrypt(json.dumps(sign_data))
        sign_res = requests.post(sign_url, data=sign_data, headers=self.headers)
        if json.loads(self.AES_Decrypt(sign_res.text)).get('msg') == '任务更新成功':
            prize_res = requests.post(prize_url, data=sign_data, headers=self.headers)
            if json.loads(self.AES_Decrypt(prize_res.text)).get('msg') == 'success':
                r_cash = json.loads(self.AES_Decrypt(prize_res.text)).get('ret').get('r_cash')
                t_cash = json.loads(self.AES_Decrypt(prize_res.text)).get('ret').get('t_cash')
                print('签到成功，获得金额：', r_cash, '元，当前总金额：', t_cash, '元')
            else:
                print('签到奖励领取失败：', json.loads(self.AES_Decrypt(prize_res.text)).get('msg'))
        else:
            print('签到失败：', json.loads(self.AES_Decrypt(sign_res.text)).get('msg'))
        prize_res = requests.post(prize_url, data=stage_data, headers=self.headers)
        if json.loads(self.AES_Decrypt(prize_res.text)).get('msg') == 'success':
            r_cash = json.loads(self.AES_Decrypt(prize_res.text)).get('ret').get('r_cash')
            t_cash = json.loads(self.AES_Decrypt(prize_res.text)).get('ret').get('t_cash')
            print('闯关任务完成，获得金额：', r_cash, '元，当前总金额：', t_cash, '元')
        else:
            print('闯关奖励领取失败：', json.loads(self.AES_Decrypt(prize_res.text)).get('msg'))


def main():
    content = ''
    token_list = os.getenv('dsgck').split('\n')
    # token_list = ['']
    print('=====检测到' + str(len(token_list)) + '个账号======')
    for num,token in enumerate(token_list):
        num += 1
        print(f'\n=======开始账号【{num}】========\n')
        # token='oxr9uhUQtGDQm9/aw0SHFw9qb4X7CyXejNd8W7srOYjCFqkUDq+yLfSeyHkWqF95iYikifWaLbTghB15BGfRTt6g4nUNjY4X2uVrTT8i+3cji58TDZXcB/iMlAHAuBIZjQPBI+HJXJImalx2j/kCyDI5w7qM7b6L08PWKyPGK3Ykox0aWCcjc+C4mS/D7L/HTM5qGt3s6l6Lhtpw8mT6npyx9Q4i3L0FuYIhbVYq9ZggtJI9tB7iqVHReYlR0fj5ts4ZIWDoB1pKzpV+mSzXVXGjK6RyCZnUx3+9uOllD911olCCHjUr4RfzjdW+/kbAoqt3bfYw0evHnPhpvXDJTA=='
        fruit = Fruit(token)
        fruit.get_info()
        for i in range(50):
            fruit.stage()
        fruit.sign()
        cash=fruit.get_info()
        content += f'账号{num}，当前金额为：{cash}\n'
    notify.pushplus_bot('打水果赚钱小游戏', content)


if __name__ == '__main__':
    main()
