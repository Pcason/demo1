# coding:utf-8
from datetime import datetime
import notify
import requests


def get_content():
    content = ""
    url = 'http://hnqndaxuexi.dahejs.cn/stw/product/list'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309001c) XWEB/6500",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "stw=8d56d00c-d275-4963-bbbd-095e5cdf5b7e",
    }
    data = {
        "pageNumber": "1",
        "pageSize": "10"
    }
    res = requests.post(url, data=data, headers=headers)
    if res.json().get('result') == 200:
        product_list = res.json().get('obj').get('list')
        for l in product_list:
            title = l.get('title')
            score = l.get('score')
            num = l.get('num')
            begin_time = l.get('beginTime')
            print(title, score, num, begin_time)
            target_time = datetime.strptime(begin_time, '%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()
            if current_time < target_time:
                content += f'{title}:\n积分：{score}\n数量：{num}\n开始时间：{begin_time}\n\n'
        return content
    print(res.json().get('msg'))


def main():
    content = get_content()
    if content != "":
        notify.pushplus_bot('学习通积分商城库存监控', content)
    print('暂无可兑换商品！')



if __name__ == '__main__':
    main()
