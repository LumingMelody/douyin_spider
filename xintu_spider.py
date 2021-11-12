#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@version: 1.0
@author: anne
@contact: thy.self@foxmail.com
@time: 2019/11/10 11:34
"""
import json
import random
import time
from pprint import pprint
from time import sleep
import pandas as pd
import requests
from openpyxl import Workbook
from selenium import webdriver
from urllib.parse import unquote
import hashlib

# driver = webdriver.Chrome()
# driver.get("https://star.toutiao.com/login?role=ad")
# driver.find_element_by_id("user-name").send_keys("julie.wang@51wom.com")
# driver.find_element_by_id("password").send_keys("PINDUODUO")
# driver.find_element_by_id("bytedance-SubmitStatic").click()
# sleep(10)
# cookies = driver.get_cookies()
# print(cookies)

headers = {
    "referer": "https://star.toutiao.com/ad/market",
    "sec-ch-ua-mobile": '?0',
    # "User-Agent": Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36
    "cookie": "gfpart_1.0.0.4796_38285=1; csrftoken=E9qPVeX3FJBxDXSf1RuRMYxJrQtnMsre; tt_webid=6932746184055326222; passport_csrf_token=906379ee5386bd53fb5ccdc9003cede9; passport_csrf_token_default=906379ee5386bd53fb5ccdc9003cede9; ttwid=1%7C0En6q_JuW18O5A1bPdaCPtnphJ0slIE4wS5t3nLT7f0%7C1614155802%7Cbcc166847b9724372b36d57c944e23d0f91dfe4c83ecad0fee7d5445cab3f83f; d_ticket=8a576e14dd58da4624c87902802566fb11f3f; passport_auth_status=771406bf4b0546a3512267b2a7a929f1%2C114a279a76b80b43995a21d936dcdafb; passport_auth_status_ss=771406bf4b0546a3512267b2a7a929f1%2C114a279a76b80b43995a21d936dcdafb; n_mh=9-mIeuD4wZnlYrrOvfzG3MuT6aQmCUtmr8FxV8Kl8xY; odin_tt=b5cd3788e3b3bbca41791b492fc2c92645e43eeebfa66ac7c33fe068894771676bd099e3fd7fb9caf1a740ed63b19e5e98aa4a117c03593067b1d5f418c50780; sid_guard=b734419e102af00aa94f2ca861de28c4%7C1614909066%7C5184000%7CTue%2C+04-May-2021+01%3A51%3A06+GMT; uid_tt=4bcaa82408c71bef138aad65ca70fa2e; uid_tt_ss=4bcaa82408c71bef138aad65ca70fa2e; sid_tt=b734419e102af00aa94f2ca861de28c4; sessionid=b734419e102af00aa94f2ca861de28c4; sessionid_ss=b734419e102af00aa94f2ca861de28c4; star_sessionid=33af4f8383c44065093007b8f451dff7; gftoken=YjczNDQxOWUxMHwxNjE0OTA5MDczNDl8fDAGBgYGBgY; MONITOR_WEB_ID=4232f5c1-9ef3-485d-ba39-5de45c3f2d45",
    "x-login-source": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "X-CSRFToken": "E9qPVeX3FJBxDXSf1RuRMYxJrQtnMsre",
}

wb = Workbook()
ws = wb.active
ws.append([
    "昵称",
    "省",
    "市",
    "性别",
    "mcn",
    "粉丝数",
    "标签",
    "预期cpm",
    "预期播放数",
    "作品互动率",
    "1-20s视频",
    "21-60s视频",
    "60s以上视频",
    "1-60s视频",
    "info详情信息"
])


# ws.append([nickname,'美妆教程',province,city,gender,fans_num,expected_cpm,expected_play_num,personal_interate_rate,origin_price1,origin_price2,origin_price3,origin_price4])
# for i in range(1, int(3372/20)+1)[112:]:
#     url = "https://star.toutiao.com/v/api/demand/author_list/?page={num}&limit=20&need_detail=true&platform_source=1" \
#           "&task_category=1&tag={tag}&fans_min=500000&fans_max=50000000&order_by=score".format(num=str(i),tag=str(72))
#
#     result = requests.get(url=url, headers=headers).text.replace("\\\\","\\")
#     print(i)
#     print(result)
#     info = json.dumps(json.loads(result), ensure_ascii=False)
#     with open("颜值达人.txt", "a+", encoding="utf-8") as f:
#         f.write(info+"\n")
#     sleep(random.randint(5, 10))


# for i in range(1, int(1103/20)+3)[51:]:
#     url = "https://star.toutiao.com/v/api/demand/author_list/?page={num}&limit=20&need_detail=true&platform_source=1" \
#           "&task_category=1&tag={tag}&fans_min=500000&fans_max=50000000&order_by=score".format(num=str(i),tag=str(48))
#
#     result = requests.get(url=url, headers=headers).text.replace("\\\\","\\")
#     print(i)
#     print(result)
#     info = json.dumps(json.loads(result), ensure_ascii=False)
#     with open("美食.txt", "a+", encoding="utf-8") as f:
#         f.write(info+"\n")
# for i in range(1, int(3398/20)+3)[50:60]:
#     url = "https://star.toutiao.com/v/api/demand/author_list/?page={num}&limit=20&need_detail=true&platform_source=1" \
#           "&task_category=1&tag={tag}&fans_min=500000&fans_max=50000000&order_by=score".format(num=str(i),tag=str(97))
#
#     result = requests.get(url=url, headers=headers).text.replace("\\\\","\\")
#     print(i)
#     print(result)
#     info = json.dumps(json.loads(result), ensure_ascii=False)
#     with open("剧情搞笑.txt", "a+", encoding="utf-8") as f:
#         f.write(info+"\n")
# for i in range(1, int(638/20)+3):

class DouyinSpider(object):
    requests.packages.urllib3.disable_warnings()

    @classmethod
    def get_sign(cls, id):
        url = unquote(
            "https://star.toutiao.com/h/api/gateway/handler_get/?o_author_id={id}&platform_source=1"
            "&platform_channel=1&recommend=false&service_name=author.AdStarAuthorService&service_method=GetAuthorBaseInfo").format(
            id=id)
        a = url.split("?")[1]
        b = [i.split("=")[0] + i.split("=")[1] if i.split("=")[1] != "false" else i.split("=")[0] + i.split("=")[0] for
             i in
             sorted(a.split("&"))]
        c = "".join(b) + "e39539b8836fb99e1538974d3ac1fe98"
        sign = hashlib.md5(c.encode("utf-8")).hexdigest()
        return sign

    @classmethod
    def douyin_spider(cls, douyin_account):
        url = "https://star.toutiao.com/v/api/demand/author_list/?page=1&limit=20&need_detail=true&" \
              "only_nick_name=true&platform_source=1&task_category=1&key={}&order_by=score".format(
            douyin_account)

        print(url)
        result = requests.get(url, headers=headers, verify=False).text.replace("\\\\", "\\")

        # print(result)
        info = json.loads(result)
        # pprint(info)
        authors = info['data']['authors']
        pprint(authors)
        for content in authors:
            # 省份
            province = content['province']

            # 地址
            city = content['city']

            # 性别
            gender = content['gender']

            # 抖音id
            douyin_id = content['core_user_id']

            # name
            douyin_name = content['nick_name']

            # 唯一id
            douyin_code = douyin_account

            # 粉丝数
            follower = content['follower']
            print(follower)

            # 头像
            douyin_img = content['avatar_uri']

            #
            douyin_type = content['tags_level_two']

            account_data = {
                'douyin_city': city,
                'douyin_code': douyin_code,
                'douyin_desc': '如果想要开心，你就关注唐唐吧！\n每天12:00更新！\n预告：情景喜剧即将出炉哟！',
                'douyin_id': douyin_id,
                'douyin_img': douyin_img,
                'douyin_name': douyin_name,
                'douyin_province': province,
                'douyin_type': douyin_type,
                'is_verified': '',
                'verified_info': ''
            }
        # # mongodb更新数据
        #     MongoDouyinAccount().update_many(
        #         query_filter={
        #             '_id': account_data['douyin_code']
        #         },
        #         update={'$set': account_data},
        #         upsert=True
        #     )

    @classmethod
    def get_douyin_info(cls):
        # for level in [2,3,4,5]:
        for page in range(1, 42):
            print(page)
            time.sleep(0.5)
            url = 'https://star.toutiao.com/v/api/demand/author_list/?limit=30&need_detail=true' \
                  '&page={page}&platform_source=1&task_category=1&tag=1&tag_level_two=5&order_by=follower' \
                  '&disable_replace_keyword=false&is_filter=true'.format(page=page)
            req = requests.get(url, headers=headers, verify=False).json()

            # pprint(req['data']['authors'][0])
            for data in req['data']['authors']:
                # time.sleep(1)
                try:
                    nickname = data['nick_name']
                    print(nickname)
                    gender = data['gender']
                    if gender == 2:
                        gender = '女'
                    elif gender == 1:
                        gender = '男'
                    else:
                        gender = '未知'

                    province = data['province']

                    # 地址
                    city = data['city']

                    fans_num = data['follower']

                    # 预期cpm
                    expected_cpm = data['expected_cpm']

                    # 预期播放量
                    expected_play_num = data['expected_play_num']

                    # 个人作品互动率
                    personal_interate_rate = data['personal_interate_rate']

                    price_info = data['price_info']
                    origin_price1 = 0
                    origin_price2 = 0
                    origin_price3 = 0
                    origin_price4 = 0
                    for info in price_info:
                        desc = info['desc']

                        if desc == '1-20s视频':
                            origin_price1 = price_info[0]['price']

                        # else:
                        #     origin_price1 = 0
                        # print(origin_price1)
                        #
                        if desc == '21-60s视频':
                            origin_price2 = price_info[1]['price']

                        # else:
                        #     origin_price2 = 0
                        # print(origin_price2)
                        #
                        if desc == '60s以上视频':
                            origin_price3 = price_info[2]['price']
                        # else:
                        #     origin_price3 = 0
                        # print(origin_price3)
                        #
                        if desc == '1-60s视频':
                            settlement_desc = info['settlement_desc']

                    tags = data['tags_relation']

                    tags_list = []
                    for values in tags.values():
                        for v in values:
                            tags_list.append(v)

                        # values.append(values)
                    # print(nickname,'美妆教程',province,city,gender,fans_num,expected_cpm,expected_play_num,personal_interate_rate,desc,origin_price)

                    id = data['id']

                    sign = cls.get_sign(id)

                    new_url = 'https://star.toutiao.com/h/api/gateway/handler_get/?o_author_id={id}&platform_source=1&platform_channel=1&recommend=false&service_name=author.AdStarAuthorService&service_method=GetAuthorBaseInfo&sign={sign}'.format(
                        id=id, sign=sign
                    )

                    new_req = requests.get(url=new_url, headers=headers, verify=False).json()
                    print(new_req)
                    if new_req['msg'] == 'Success':
                        mcn_name = new_req['data']['mcn_name']
                        print(mcn_name)
                    else:
                        mcn_name = ''

                    ws.append([nickname, province, city, gender, mcn_name, fans_num, str(tags_list), expected_cpm,
                               expected_play_num,
                               personal_interate_rate, origin_price1, origin_price2, origin_price3, '按播放量付费',
                               str(data)])
                except:
                    continue
            # if level == 2:
        wb.save('D:/douyin/美妆评测种草.xlsx')
        # elif level == 3:


if __name__ == '__main__':
    DouyinSpider.get_douyin_info()
    pd.read_excel("")
    # DouyinSpider.get_sign('6640245670529728516')


    # with open("生活.txt", "a+", encoding="utf-8") as f:
    #     f.write(info+"\n")
