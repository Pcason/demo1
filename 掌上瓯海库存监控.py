# coding:utf-8
import requests
import notify


def get_content():
    content=""
    url='http://lwintegral.wznbw.com/addons/leescore/index/ajaxGoodlist?appid=2'
    res=requests.get(url)
    good_list=res.json().get('data')
    for good in good_list:
        name=good.get('name')
        stock=good.get('stock')
        if stock != 0:
            content += f'{name}：库存剩余{stock}\n'
    return content


def main():
    content = get_content()
    if content != "":
        notify.pushplus_bot('掌上瓯海积分商城库存监控', content)
    else:
        print('暂无可兑换商品！')


if __name__ == '__main__':
    main()