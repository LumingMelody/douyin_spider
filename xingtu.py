import hashlib
import json
import time
from urllib.parse import unquote
import queue
from openpyxl import Workbook

import requests

headers = {
    "authority": "star.toutiao.com",
    "x-login-source": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "X-CSRFToken": "E9qPVeX3FJBxDXSf1RuRMYxJrQtnMsre",
    "sec-ch-ua-mobile": '?0',
    "method": "GET",
    "scheme": "https",
    "cache-control": "max-age=0",
    "cookie": "MONITOR_WEB_ID=06071021-3c24-44cd-968c-e50c1f4de4c4; ttcid=d894af4d93b7433abf881d8430ad170432; tt_scid=nn.0gntv4qHPHEnnU9PoA6ptzI-wF-W3WAJMbIX4WOJPP0DgcRgYf8JSr6oMmDiv5d2c; csrftoken=2quuLHXlzEXss4T8xd7rV8PHiv4noq7S; tt_webid=7065236944129476109; passport_csrf_token_default=1a2ff6b63b96ae5ef50e536f327c60ce; passport_csrf_token=1a2ff6b63b96ae5ef50e536f327c60ce; s_v_web_id=verify_844530843a96600cbf81e9e634a61d7d; _tea_utm_cache_2018=undefined; uid_tt=c7d22752fe26b3612f680aaea4f6163c; uid_tt_ss=c7d22752fe26b3612f680aaea4f6163c; sid_tt=4a86061160c3cb37bce97098a4b7a2ba; sessionid=4a86061160c3cb37bce97098a4b7a2ba; sessionid_ss=4a86061160c3cb37bce97098a4b7a2ba; sid_ucp_v1=1.0.0-KDVjNzk4ZWRmNmQwZjc2MDFlYzUyNjg1MjMzMTJlMjcyM2I3ODUzYjMKFQj6wvTWhwMQzfvckAYY-hM4AUDrBxoCbGYiIDRhODYwNjExNjBjM2NiMzdiY2U5NzA5OGE0YjdhMmJh; ssid_ucp_v1=1.0.0-KDVjNzk4ZWRmNmQwZjc2MDFlYzUyNjg1MjMzMTJlMjcyM2I3ODUzYjMKFQj6wvTWhwMQzfvckAYY-hM4AUDrBxoCbGYiIDRhODYwNjExNjBjM2NiMzdiY2U5NzA5OGE0YjdhMmJh; sid_guard=4a86061160c3cb37bce97098a4b7a2ba%7C1645690317%7C5184000%7CMon%2C+25-Apr-2022+08%3A11%3A57+GMT; gftoken=NGE4NjA2MTE2MHwxNjQ1NjkwMzE3NjJ8fDAGBgYGBgY; star_sessionid=3827b4a0d5811682f1d01c7732790414; imagetoken=6a5a248139c4c4ca43e0ca5d228109e3924adcdc; imagetoken_ss=6a5a248139c4c4ca43e0ca5d228109e3924adcdc",
    "referer": "https://star.toutiao.com/ad/cart/settlement?_route_from=from_module%3Dnavigator",
}

# url = "https://www.xingtu.cn/v/api/demand/author_list/?limit=20&need_detail=true&page=1&platform_source=1&task_category=1&tag={}&order_by=score&disable_replace_keyword=false&is_filter=true"
# url = "https://www.xingtu.cn/v/api/demand/author_list/?limit=20&need_detail=true&page={page}&platform_source=1&task_category=1&tag=72&price_max={min}&price_min={max}&is_filter=true"

# url = "https://www.xingtu.cn/v/api/demand/author_list/?limit=20&need_detail=true&page=1&platform_source=1&task_category=1&tag=97&order_by=score&disable_replace_keyword=false&is_filter=true"
wb = Workbook()
ws = wb.active
ws.append(["用户名",
           "省份",
           "城市",
           "性别",
           "粉丝数",
           "用户标签",
           "预期cpm",
           "预期播放量",
           "个人作品互动率",
           "0-20秒视频报价",
           "21-60秒视频报价",
           "60秒以上视频报价",
           ])


def get_sign(id):
    url = unquote(
        "https://star.toutiao.com/h/api/gateway/handler_get/?o_author_id={id}&platform_source=1"
        "&platform_channel=1&recommend=false&service_name=author.AdStarAuthorService&service_method=GetAuthorBaseInfo").format(
        id=id)
    a = url.split("?")[1]
    b = [i.split("=")[0] + i.split("=")[1] if i.split("=")[1] != "false" else i.split("=")[0] + i.split("=")[0] for
         i in
         sorted(a.split("&"))]
    print(b)
    c = "".join(b) + "e39539b8836fb99e1538974d3ac1fe98"
    print(c)
    sign = hashlib.md5(c.encode("utf-8")).hexdigest()
    return sign


def get_douyin_content(dy_url):
    twenty_one_to_sixty = ""
    zero_to_twenty = ""
    over_sixty = ""
    user_tag = ""
    id = dy_url.split('/')[-1]
    sign = get_sign(id)
    response = requests.get(headers=headers, url=dy_url, verify=False)
    print(dy_url)
    if response:
        resp = response.content.decode('utf-8')
        rp_json = json.loads(resp)
        # print(rp_json)
        data = rp_json["data"]
        # print(data)
        authors = data["authors"]
        print(authors)
        for a in authors:
            print(a)
            # 用户名
            nick_name = a["nick_name"]
            # 省份
            province = a["province"]
            # 城市
            city = a["city"]
            # 性别 男1 女2
            gender = a["gender"]
            if gender == 1:
                gender = '男'
            elif gender == 2:
                gender = '女'
            # 粉丝数
            follower = a["follower"]
            uid = a["unique_id"]
            # 标签
            # tags = a["tags_relation"]["美妆"][0]
            tags = a["tags_relation"]
            for tag in tags:
                user_tag = tag
            # 预期cpm
            expected_cpm = a["expected_cpm"]
            # 预期播放
            expected_play_num = a["expected_play_num"]
            # 个人作品互动率
            personal_interate_rate = a["personal_interate_rate"]
            price_info = a["price_info"]
            for info in price_info:
                try:
                    desc = info["desc"]
                    # 0-20秒视频报价
                    if desc == "1-20s视频":
                        zero_to_twenty = a["price_info"][0]["price"]
                    # 21-60秒视频报价
                    if desc == "21-60s视频":
                        twenty_one_to_sixty = a["price_info"][1]["price"]
                    # 60秒以上视频报价
                    if desc == "60s以上视频":
                        over_sixty = a["price_info"][2]["price"]
                except Exception as err:
                    print(err)
            uid = a["id"]
            # personal = "https://star.toutiao.com/ad/author/douyin/{}/1?recommend=false&version=v2".format(uid)
            # print(uid)
            sign = get_sign(uid)
            info_url = f"https://www.xingtu.cn/h/api/gateway/handler_get/?o_author_id={uid}&platform_source=1&platform_channel=1&recommend=true&service_name=author.AdStarAuthorService&service_method=GetAuthorBaseInfo&sign={sign}"
            user_rsp = requests.get(headers=headers, url=info_url).json()
            # # print(user_rsp)
            # if user_rsp['msg'] == 'Success':
            #     mcn_name = user_rsp['data']['mcn_name']
            #     print(mcn_name)
            # else:
            #     mcn_name = ''

            ws.append([nick_name, province, city, gender,  follower, user_tag, expected_cpm, expected_play_num,
                       personal_interate_rate, zero_to_twenty, twenty_one_to_sixty, over_sixty])
            # ws.append([nick_name, uid, follower])

        wb.save(r"./xingtu.xlsx")


if __name__ == '__main__':
    # i = 1
    # min_price = 100000
    # max_price = 100000
    # # url里面的tag为分类标识
    # # 分类标识 美妆教程=2 妆容展示=3 护肤保养=4 美妆评测种草=5  时尚： 穿搭=7 街拍=8 造型=9
    #
    # url = f"https://www.xingtu.cn/v/api/demand/author_list/?limit=20&need_detail=true&page={i}&platform_source=1&task_category=1&tag=72&order_by=score&price_max={max_price}&price_min={min_price}&fans_min=5000000&fans_max=10000000&is_filter=true"
    # while True:
    #     if i < 5:
    #         get_douyin_content(url.format(page=i, min_price=min_price, max_price=max_price))
    #         i += 1
    #         time.sleep(3)
    #     else:
    #         break
    print(get_sign(6870166593343586312))

