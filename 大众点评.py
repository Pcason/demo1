# coding:utf-8
import random
import time

import requests
from lxpy import lxml_check
from lxml import etree
import re


def get_html(url):
    # url='https://www.dianping.com/shop/l2Rgc2sSL0P7wCTY/review_all'
    headers = {
        'Cookie': 'fspop=test; cy=1209; cye=xinzheng; _lxsdk_cuid=18387ccfc5a66-0f47235bde904e-26021c51-149c48-18387ccfc5bc8; _lxsdk=18387ccfc5a66-0f47235bde904e-26021c51-149c48-18387ccfc5bc8; _hc.v=869908c4-43e4-92ca-d7b7-dcede0b9f6a9.1664430702; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1664430702; s_ViewType=10; WEBDFPID=9zyzxu8z623v501319yu20502y6983zx81612xw17x19795849y18812-1979790736379-1664430735851MUSCSCGfd79fef3d01d5e9aadc18ccd4d0c95078555; aburl=1; _lx_utm=utm_source%3Dbaidu%26utm_medium%3Dorganic%26utm_term%3D%25E5%25A4%25A7%25E4%25BC%2597%25E7%2582%25B9%25E8%25AF%2584; dplet=7f7afa3664281db8892b8f2303446b8c; dper=82b11f539615280ffa376f964141a180bedde223a43be4f0d22a157c20b0e63540ec2f735bcaa46aa47feee9e91df6913555264ed103a541efb00df727630373f16ade48759b8687f3ce74d2c7f70424cf2bb813cf753bcaf5e95db6e9bd1236; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_0432557552; ctu=7e2f41e1eded339a8b528417a04b91ac95ecc0b393a43e6103750530447e269f; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1664458411; _lxsdk_s=18389707f07-5fb-c62-ef8%7C%7C295',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    # with open('大众点评/dazhongdainpin.html', 'r', encoding='utf-8')as f:
    #     text=f.read()
    shopId = url.split('/')[-2]
    r_xml = etree.HTML(r.text)
    html = r.text
    return r_xml, html, shopId


# 解密手机号
def explain_phone(css_text, svg_text):
    parse_dict = {}  # {'css密文y':'id'}
    css_list = re.findall(r'\.(.*?){background:-(.+)\.0px -(.+)\.0px;', '\n'.join(css_text.split('}')))
    x_text = re.findall(r'<text x="(.*?)" y="(.*?)">(.*?)</text>', svg_text)
    x_list = x_text[0][0].split()
    y_list = x_text[0][1]
    text = x_text[0][2]
    # print(css_list)
    for c in css_list:
        if int(c[2]) <= int(y_list):
            for x in x_list:
                if int(c[1]) <= int(x):
                    parse_dict[c[0]] = x_list.index(x)
                    break
    svg_value = list(parse_dict.values())
    svg_key = list(parse_dict.keys())
    num_list = []
    for i in svg_value:
        try:
            num = text[i]
            num_list.append(num)
        except:
            num = ''
            num_list.append(num)
    parse_dict_2 = dict(zip(svg_key, num_list))
    # print(parse_dict_2)
    return parse_dict_2


# 解密文本
def explain(css_text, svg_text):
    parse_dict = {}  # {'id':'css密文y'}
    parse_dict_2 = {}  # {'id':'svg1密文'}
    # 这一步得到的列表内容为css中class的名字及其对应的偏移量
    css_list = re.findall(r'\.(.*?){background:-(.+)\.0px -(.+)\.0px;', '\n'.join(css_text.split('}')))
    # print(css_list)
    # print(svg_text)
    key_list = re.findall(r'<path\sid="(.*?)"\sd="..\s(.*?)\s...."/>', svg_text)
    if key_list != []:
        for c in css_list:
            for k in key_list:
                if int(k[1]) >= int(c[2]):
                    parse_dict[c[0]] = [k[0], c[1]]
                    break
        con_list = re.findall(r'<textPath xlink:href="#(.*?)" textLength=".*">(.*?)</textPath>', svg_text)

    else:
        y_list = re.findall(r'<text x="0" y="(.*?)">', svg_text)

        for c in css_list:
            for y in y_list:
                if int(y) >= int(c[2]):
                    parse_dict[c[0]] = [y, c[1]]
                    break
        con_list = re.findall(r'<text x="0" y="(.*?)">(.*?)</text>', svg_text)

    # print(parse_dict)
    id_x_list = list(parse_dict.values())
    dict1_key_list = list(parse_dict.keys())
    text_list = []
    for j in con_list:
        parse_dict_2[j[0]] = j[1]
    # print(parse_dict_2)
    # print(id_x_list)
    for id_x in id_x_list:
        # print(list(id_x)[0])
        num = int(list(id_x)[1]) // 14
        try:
            text = parse_dict_2.get(id_x[0])[num]
            text_list.append(text)
        except:
            text_list.append('')
    parse_dict = dict(zip(dict1_key_list, text_list))  # {'css密文':'解密文字'}
    return parse_dict


# 得到解密结果
def parse_html(xml):
    css_url = 'https:' + xml.xpath('/html/head/link[4]/@href')[0]
    css_text = requests.get(css_url).text
    # with open('css.txt','r',encoding='utf-8')as f1:
    #     css_text=f1.read()
    svg_url_1 = 'https:' + re.findall(r'background-image: url\((.*?)\)', css_text)[0]
    svg_url_2 = 'https:' + re.findall(r'background-image: url\((.*?)\)', css_text)[1]
    svg_url_3 = 'https:' + re.findall(r'background-image: url\((.*?)\)', css_text)[2]
    text_1 = requests.get(svg_url_1).text
    text_2 = requests.get(svg_url_2).text
    text_3 = requests.get(svg_url_3).text
    # with open('大众点评/svg1.html', 'r', encoding='utf-8')as f3:
    #     svg_text_1=f3.read()
    # with open('大众点评/svg2.html', 'r', encoding='utf-8')as f4:
    #     svg_text_2=f4.read()
    # with open('大众点评/svg3.html', 'r', encoding='utf-8')as f2:
    #     svg_text_3=f2.read()
    if text_1.count('text') > 50:
        svg_text_3 = text_1
    elif text_2.count('text') > 50:
        svg_text_3 = text_2
    else:
        svg_text_3 = text_3
    if 5 < text_1.count('text') < 50:
        svg_text_2 = text_1
    elif 5 < text_2.count('text') < 50:
        svg_text_2 = text_2
    else:
        svg_text_2 = text_3
    if text_1.count('text') < 6:
        svg_text_1 = text_1
    elif text_2.count('text') < 6:
        svg_text_1 = text_2
    else:
        svg_text_1 = text_3

    parse_dict_1 = explain_phone(css_text, svg_text_1)
    parse_dict_2 = explain(css_text, svg_text_2)
    parse_dict_3 = explain(css_text, svg_text_3)
    return parse_dict_1, parse_dict_2, parse_dict_3


# 店铺基本信息
def stort_obj(xml,html,parse_dict_1,parse_dict_2):
    star_score_list = re.findall(r'<div class="star_score score_(.*?)">(.*?)</div>', html)
    store_star = '.'.join(star_score_list[0][0])
    store_score = star_score_list[0][1]
    content_num = xml.xpath('//*[@id="review-list"]/div[2]/div[1]/div[2]/span[1]/text()')[0]
    people_money = xml.xpath('//*[@id="review-list"]/div[2]/div[1]/div[2]/span[2]/text()')[0]
    details_score = xml.xpath('//*[@id="review-list"]/div[2]/div[1]/div[2]/span[3]//text()')
    shop_name = xml.xpath('//*[@id="review-list"]/div[2]/div[1]/div[1]/h1/text()')[0]
    print('店铺名称:' + shop_name)
    print('店铺星级:' + store_star)
    print('店铺评分:' + store_score)
    print(people_money, details_score[1], details_score[3], details_score[5])
    print('评价数量:' + content_num)

    content_list_2 = re.findall(r'class="address-info">(.*?)</div>', html, re.DOTALL)[0]
    address = re.sub(r'(&nbsp;)|(<bb class=")|("></bb>)|(\s)', '', content_list_2)
    for i in parse_dict_2:
        check_html = re.search(i, address)
        if check_html != None:
            address = re.sub(i, parse_dict_2[i], address)
    print(address)
    content_list_3 = re.findall(r'class="phone-info">(.*?)</div>', html, re.DOTALL)[0]
    phone = re.sub(r'(&nbsp;)|(<cc class=")|("></cc>)|(\s)', '', content_list_3)
    # print(phone)
    for j in parse_dict_2:
        check_html = re.search(j, phone)
        if check_html != None:
            phone = re.sub(j, parse_dict_1[j], phone)
    print(phone)


# 评论信息
def get_parse_obj(html, xml, shopId, parse_dict_3):
    '''
    :param parse_dict_1: 电话
    :param parse_dict_2: 地址
    :param parse_dict_3: 评论
    :return:
    '''
    content_list = re.findall(
        r'<div class="review-words Hide">(.*?)<div class="misc-info clearfix">|<div class="review-words">(.*?)<div class="misc-info clearfix">',
        html, re.DOTALL)
    n = 1
    for con in content_list:
        # 评价内容
        cont_tup = re.sub(r'(<divclass="less-words".*</div>)', '', re.sub(
            r'(<svgmtsi class=")|("></svgmtsi>)|(<ul>.*?</ul>)|(<img class="emoji-img" src=".*?alt=""/>)|(\s)|(<div class="less-words">.*</div>)|(\\n)|(<div class="review-pictures">.*?</div>)|(\\t)|(<div class="review-recommend">.*?</div>)|(&#x0A;)|(</div>)|(&#x20;)',
            '', str(con)))
        if eval(cont_tup)[0] != '':
            content = eval(cont_tup)[0]
        else:
            content = eval(cont_tup)[1]
        # print(content)
        for i in parse_dict_3:
            check_html = re.search(i, content)
            if check_html != None:
                content = re.sub(i, parse_dict_3[i], content)
        print('客户评论:' + content)
        # 评价图片
        img_list = xml.xpath(f'//*[@id="review-list"]//li[{n}]//ul//img/@data-big')
        # print(img_list)

        if img_list != []:
            img_num = 1
            for img in img_list:
                print(f'评价图片{img_num}:{img}')
                if img_num < len(img_list):
                    img_num += 1
        else:
            print('无评论图片!')
        # 好评星级
        star_listt = re.findall(r'<span class="sml-rank-stars sml-str(.*?) star"></span>', html)
        if len(star_listt[n - 1]) == 2:
            star = '.'.join(star_listt[n - 1])
            print('星级:' + star + '星')
        else:
            print('星级:0.5星')
        # 评论时间
        pj_time = xml.xpath('//*[@id="review-list"]//span[@class="time"]/text()')
        try:
            print('评论时间:' + pj_time[n - 1].split()[0] + ' ' + pj_time[n].split()[1])
        except:
            print('评论时间:' + pj_time[n - 1].split()[0])
        # 商家回复
        reply_list = xml.xpath(f'//*[@id="review-list"]//li[{n}]//div[@class="shop-reply"]/p/text()')
        reply_time_list = xml.xpath(
            f'//*[@id="review-list"]//li[{n}]//div[@class="shop-reply"]//span[@class="date"]/text()')
        if reply_list != []:
            print('商家回复:' + reply_list[0].split()[0])
            print('商家回复时间:' + reply_time_list[0])
        else:
            print('该评论暂无商家回复!')
        # add_review(html,shopId)

        if n <= len(content_list):
            n += 1


# 追评信息
def add_review(html,shopId):
    # 追评
    UserId_list = re.findall(r'data-user-id="(.*?)"', html)
    headers = {
        'Cookie': 'fspop=test; cy=1209; cye=xinzheng; _lxsdk_cuid=18387ccfc5a66-0f47235bde904e-26021c51-149c48-18387ccfc5bc8; _lxsdk=18387ccfc5a66-0f47235bde904e-26021c51-149c48-18387ccfc5bc8; _hc.v=869908c4-43e4-92ca-d7b7-dcede0b9f6a9.1664430702; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1664430702; s_ViewType=10; WEBDFPID=9zyzxu8z623v501319yu20502y6983zx81612xw17x19795849y18812-1979790736379-1664430735851MUSCSCGfd79fef3d01d5e9aadc18ccd4d0c95078555; aburl=1; _lx_utm=utm_source%3Dbaidu%26utm_medium%3Dorganic%26utm_term%3D%25E5%25A4%25A7%25E4%25BC%2597%25E7%2582%25B9%25E8%25AF%2584; dplet=7f7afa3664281db8892b8f2303446b8c; dper=82b11f539615280ffa376f964141a180bedde223a43be4f0d22a157c20b0e63540ec2f735bcaa46aa47feee9e91df6913555264ed103a541efb00df727630373f16ade48759b8687f3ce74d2c7f70424cf2bb813cf753bcaf5e95db6e9bd1236; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_0432557552; ctu=7e2f41e1eded339a8b528417a04b91ac95ecc0b393a43e6103750530447e269f; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1664458411; _lxsdk_s=18389707f07-5fb-c62-ef8%7C%7C295',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    reviewUserId_list = re.findall(r'<a class="link fold" data-userid="(.*?)"', html)
    uid_num = 0
    for UserId in UserId_list:
        try:
            if UserId == reviewUserId_list[uid_num]:
                for reviewUserId in reviewUserId_list:
                    add_parse_url = f'https://www.dianping.com/ajax/json/review/subReviewAction?reviewUserId={reviewUserId}&shopId={shopId}'
                    res = requests.get(add_parse_url, headers=headers)
                    text_2 = res.json().get('msg')
                    add_parse_list = re.findall(r'class="desc">(.*?)</p>', text_2, re.DOTALL)
                    if add_parse_list != []:
                        print('追评:' + re.sub(r'(&#x20;)|(&#x0A;)|(<img.*?alt=""/>)', '', add_parse_list[0]))
                    add_star_list = re.findall(r'"sml-rank-stars sml-str(.*?)\">', text_2)
                    # print(add_star_list)
                    if add_star_list != []:
                        if len(add_star_list[0]) == 2:
                            star = '.'.join(add_star_list[0])
                            print('追评星级:' + star + '星')
                        else:
                            print('追评星级:0.5星')
                        add_time = re.search(r'class=\"time\">(.*?)<', text_2, re.DOTALL).group(1).split()[0]
                        print('追评时间:' + add_time)
                if uid_num < len(reviewUserId_list) - 1:
                    uid_num += 1
        except:
            pass


def main():
    for i in range(1,4): # 爬取的页数
        url = f'https://www.dianping.com/shop/k4Qg61fIdYfcXFNN/review_all/p{i}'
        xml, html, shopId = get_html(url)
        parse_dict_1, parse_dict_2, parse_dict_3 = parse_html(xml)
        get_parse_obj(html, xml, shopId, parse_dict_3)
        time.sleep(random.randint(3,5))
        print('---------------------------')
    stort_obj(xml,html, parse_dict_1, parse_dict_2)

if __name__ == '__main__':
    main()
