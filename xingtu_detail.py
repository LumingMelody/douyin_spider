import hashlib

import requests
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append([
    "uid", "用户链接", " 播放量", "互动率", "完播率", "预期CPM", "预期CPE", "粉丝增长量", "粉丝增长率", "近30天播放量环比", "近30天带组件视频播放量", "购物车点击率",
    "教育培训行业组件点击率", "工具类组件点击率", "3C电器点击率", "男性占比", "女性占比"
])

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "cookie": "MONITOR_WEB_ID=06071021-3c24-44cd-968c-e50c1f4de4c4; ttcid=d894af4d93b7433abf881d8430ad170432; tt_scid=nn.0gntv4qHPHEnnU9PoA6ptzI-wF-W3WAJMbIX4WOJPP0DgcRgYf8JSr6oMmDiv5d2c; csrftoken=2quuLHXlzEXss4T8xd7rV8PHiv4noq7S; tt_webid=7065236944129476109; passport_csrf_token_default=1a2ff6b63b96ae5ef50e536f327c60ce; passport_csrf_token=1a2ff6b63b96ae5ef50e536f327c60ce; s_v_web_id=verify_844530843a96600cbf81e9e634a61d7d; _tea_utm_cache_2018=undefined; uid_tt=c7d22752fe26b3612f680aaea4f6163c; uid_tt_ss=c7d22752fe26b3612f680aaea4f6163c; sid_tt=4a86061160c3cb37bce97098a4b7a2ba; sessionid=4a86061160c3cb37bce97098a4b7a2ba; sessionid_ss=4a86061160c3cb37bce97098a4b7a2ba; sid_ucp_v1=1.0.0-KDVjNzk4ZWRmNmQwZjc2MDFlYzUyNjg1MjMzMTJlMjcyM2I3ODUzYjMKFQj6wvTWhwMQzfvckAYY-hM4AUDrBxoCbGYiIDRhODYwNjExNjBjM2NiMzdiY2U5NzA5OGE0YjdhMmJh; ssid_ucp_v1=1.0.0-KDVjNzk4ZWRmNmQwZjc2MDFlYzUyNjg1MjMzMTJlMjcyM2I3ODUzYjMKFQj6wvTWhwMQzfvckAYY-hM4AUDrBxoCbGYiIDRhODYwNjExNjBjM2NiMzdiY2U5NzA5OGE0YjdhMmJh; sid_guard=4a86061160c3cb37bce97098a4b7a2ba%7C1645690317%7C5184000%7CMon%2C+25-Apr-2022+08%3A11%3A57+GMT; gftoken=NGE4NjA2MTE2MHwxNjQ1NjkwMzE3NjJ8fDAGBgYGBgY; star_sessionid=3827b4a0d5811682f1d01c7732790414; imagetoken=c607f74e49d5ce4ead07f3c174bdee5429227ae2; imagetoken_ss=c607f74e49d5ce4ead07f3c174bdee5429227ae2"
}

# 性价比sign
def GetAuthorCpInfo(u_id):
    m = hashlib.md5()
    str = f"o_author_id{u_id}platform_channel1platform_source1service_methodGetAuthorCpInfoservice_namedata.AdStarDataServicesign_strict1" + "e39539b8836fb99e1538974d3ac1fe98"
    m.update(str.encode())
    sign = m.hexdigest()
    # print(sign)
    return sign


# 传播sign
def GetAuthorSpreadInfo(u_id):
    m = hashlib.md5()
    str = f"o_author_id{u_id}platform_channel1platform_source1range2service_methodGetAuthorSpreadInfoservice_namedata.AdStarDataServicesign_strict1type1" + "e39539b8836fb99e1538974d3ac1fe98"
    m.update(str.encode())
    sign = m.hexdigest()
    # print(sign)
    return sign


# 合作sign
def GetAuthorCooperateInfo(u_id):
    m = hashlib.md5()
    str = f"o_author_id{u_id}platform_channel1platform_source1service_methodGetAuthorCooperateInfoservice_namedata.AdStarDataServicesign_strict1" + "e39539b8836fb99e1538974d3ac1fe98"
    m.update(str.encode())
    sign = m.hexdigest()
    # print(sign)
    return sign


# 成长sign
def GetAuthorDailyFansV2(u_id):
    m = hashlib.md5()
    str = f"author_type1end_date2022-02-23o_author_id{u_id}platform_source1service_methodGetAuthorDailyFansV2service_namedata.AdStarDataServicesign_strict1start_date2022-01-23" + "e39539b8836fb99e1538974d3ac1fe98"
    m.update(str.encode())
    sign = m.hexdigest()
    # print(sign)
    return sign


# 受众sign
def GetAuthorWatchedDistribution(u_id):
    m = hashlib.md5()
    str = f"o_author_id{u_id}platform_channel1platform_source1service_methodGetAuthorWatchedDistributionservice_namedata.AdStarDataServicesign_strict1type1" + "e39539b8836fb99e1538974d3ac1fe98"
    m.update(str.encode())
    sign = m.hexdigest()
    # print(sign)
    return sign


# 种草sign
def GetAuthorEcomDetai(u_id):
    m = hashlib.md5()
    str = f"author_id{u_id}day_count30platform_channel1service_methodGetAuthorEcomDetailservice_namedata.AdStarDataServicesign_strict1" + "e39539b8836fb99e1538974d3ac1fe98"
    m.update(str.encode())
    sign = m.hexdigest()
    # print(sign)
    return sign


def get_user_detail(uid):
    # 传播
    sign = GetAuthorSpreadInfo(uid)
    resp = requests.get(
        f"https://www.xingtu.cn/h/api/gateway/handler_get/?o_author_id={uid}&platform_source=1&platform_channel=1&range=2&type=1&service_name=data.AdStarDataService&service_method=GetAuthorSpreadInfo&sign_strict=1&sign={sign}", headers=headers).json()
    print(resp)
    sp_data = resp['data']
    # 播放量数
    play_num = sp_data['play_mid']
    # 互动率
    interact_rate = sp_data['interact_rate']['value'] / 100
    # 完播率
    play_over_rate = sp_data['play_over_rate']['value'] / 100
    # 预期cpm
    expect_cpm = sp_data['expect_cpm']['cpm_21_60'] / 100
    # 预期cpe
    expect_cpe = sp_data['expect_cpe']['cpe_21_60'] / 100

    # 成长
    sign = GetAuthorDailyFansV2(uid)
    resp_data = requests.get(
        f"https://www.xingtu.cn/h/api/gateway/handler_get/?o_author_id={uid}&platform_source=1&start_date=2022-01-23&end_date=2022-02-23&author_type=1&service_name=data.AdStarDataService&service_method=GetAuthorDailyFansV2&sign_strict=1&sign={sign}", headers=headers).json()
    fans_data = resp_data['data']
    # 粉丝增长量
    fans_growth = fans_data['fans_growth']
    # 粉丝增长率
    fans_growth_rate = fans_data['fans_growth_rate'] * 100
    # 近30天播放量环比
    raw_play_rate = fans_data['raw_play_rate']['value'] / 100

    # 种草
    sign = GetAuthorEcomDetai(uid)
    ed_data = requests.get(
        f"https://www.xingtu.cn/h/api/gateway/handler_get/?author_id={uid}&platform_channel=1&day_count=30&service_name=data.AdStarDataService&service_method=GetAuthorEcomDetail&sign_strict=1&sign={sign}", headers=headers).json()
    video_data = ed_data['data']['video_data']
    # 近30天带组件视频播放量
    component_item_play = video_data['component_item_play']['value']
    # 购物车点击率
    ecom_shop_score = (video_data['ecom_video_score'] / video_data['ecom_video_vv_medium']) * 1000
    # 教育培训行业组件点击率
    education_score = video_data['industry_component_ctr'][0]['value'] / 100
    # 工具类组件点击率
    tool_score = video_data['industry_component_ctr'][1]['value'] / 100
    # 3C电器点击率
    electric_score = video_data['industry_component_ctr'][2]['value'] / 100

    # 性别
    sign = GetAuthorWatchedDistribution(uid)
    response = requests.get(
        f" https://www.xingtu.cn/h/api/gateway/handler_get/?o_author_id={uid}&platform_source=1&platform_channel=1&type=1&service_name=data.AdStarDataService&service_method=GetAuthorWatchedDistribution&sign_strict=1&sign={sign}", headers=headers).json()
    gender_data = response['data']['distributions'][1]['distribution_list']
    male = int(gender_data[0]['distribution_value'])
    female = int(gender_data[1]['distribution_value'])
    gender_count = int(male) + int(female)
    # 男性占比
    male_score = (male / gender_count) * 100
    # 女性占比
    female_score = (female / gender_count) * 100
    # 用户链接
    user_url = f"https://www.xingtu.cn/ad/creator/author/douyin/{uid}"
    ws.append(
        [uid, user_url, play_num, interact_rate, play_over_rate, expect_cpm, expect_cpe, fans_growth, fans_growth_rate,
         raw_play_rate,
         component_item_play, ecom_shop_score, education_score, tool_score, electric_score, male_score, female_score])
    wb.save(r'./xingtu_detail.xlsx')


if __name__ == '__main__':
    get_user_detail('6918288919846977547')
