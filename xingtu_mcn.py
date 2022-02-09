import time

import requests
import hashlib
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append([
    "mcn名称", "所属公司名称", " 博主数", "总粉丝量", "机构简介", "达人概览"
])

"limit20order_byauthor_numpage1service_methodDemanderMcnListservice_namemcn.AdStarMcnServicesign_strict1"
"1b5eba10695170762751e7fb02e8eda6"

"mcn_id6685143170927296524service_methodMcnMainPageTopAuthorsservice_namemcn.AdStarMcnServicesign_strict1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "cookie": "ttcid=a6090f76dd5c44fbbec4a168e40d834328; tt_webid=7028866373770692127; csrftoken=fPGSy36I8BeD3WQbbMZ5CvvgnZrbK01c; MONITOR_WEB_ID=20edb3f9-47ce-4d74-910c-3b610af9e378; tt_scid=PKtaZ1hhrrV8P9Aa0lqxMGVzQZd66uEwc92JHuHAOKj87lnKfPQC6cDCmx.RnyKP78ba; s_v_web_id=verify_c4b49711dcfc8e4ed4c30637cfcd4cce; _tea_utm_cache_2018=undefined; MONITOR_DEVICE_ID=a6316cfd-9602-4267-a3f6-39ab328ad7d5; passport_csrf_token_default=3f66dd371a88187dc2a01febbe91a09a; sid_guard=43757967bd797f38e9c740dad96b01b9%7C1644372282%7C5184000%7CSun%2C+10-Apr-2022+02%3A04%3A42+GMT; uid_tt=b1a267c19c8c5ed4e49910e7ad6e56b6; uid_tt_ss=b1a267c19c8c5ed4e49910e7ad6e56b6; sid_tt=43757967bd797f38e9c740dad96b01b9; sessionid=43757967bd797f38e9c740dad96b01b9; sessionid_ss=43757967bd797f38e9c740dad96b01b9; sid_ucp_v1=1.0.0-KDZhZmZmYzBkYzIyZjU2MDYwMDQzODBlYjlkOTg2NGE1YjE1Y2UxMTMKFQj6wvTWhwMQusKMkAYY-hM4AUDrBxoCbGYiIDQzNzU3OTY3YmQ3OTdmMzhlOWM3NDBkYWQ5NmIwMWI5; ssid_ucp_v1=1.0.0-KDZhZmZmYzBkYzIyZjU2MDYwMDQzODBlYjlkOTg2NGE1YjE1Y2UxMTMKFQj6wvTWhwMQusKMkAYY-hM4AUDrBxoCbGYiIDQzNzU3OTY3YmQ3OTdmMzhlOWM3NDBkYWQ5NmIwMWI5; passport_csrf_token=3f66dd371a88187dc2a01febbe91a09a; _tea_utm_cache_1581=undefined; _tea_utm_cache_2925=undefined; star_sessionid=3619e9dba4cfb836563836c87b4c5cd1; gftoken=NDM3NTc5NjdiZHwxNjQ0MzcyMjg1NzB8fDAGBgYGBgY"
}


def get_list_sign(page_num):
    m = hashlib.md5()
    str = f"limit20order_byauthor_numpage{page_num}service_methodDemanderMcnListservice_namemcn.AdStarMcnServicesign_strict1" + "e39539b8836fb99e1538974d3ac1fe98"
    m.update(str.encode())
    sign = m.hexdigest()
    # print(sign)
    return sign


def get_public_sign(mcn_id):
    m = hashlib.md5()
    str = f"mcn_id{mcn_id}service_methodMcnGetPublicInfoservice_namemcn.AdStarMcnServicesign_strict1" + "e39539b8836fb99e1538974d3ac1fe98"
    m.update(str.encode())
    sign = m.hexdigest()
    # print(sign)
    return sign


def get_page_top_sign(mcn_id):
    # "mcn_id6685143170927296524service_methodMcnMainPageTopAuthorsservice_namemcn.AdStarMcnServicesign_strict1"
    m = hashlib.md5()
    str = f"mcn_id{mcn_id}service_methodMcnMainPageTopAuthorsservice_namemcn.AdStarMcnServicesign_strict1" + "e39539b8836fb99e1538974d3ac1fe98"
    m.update(str.encode())
    sign = m.hexdigest()
    # print(sign)
    return sign


def get_mcn(pageNum):
    list_sign = get_list_sign(pageNum)
    list_url = f"https://www.xingtu.cn/h/api/gateway/handler_get/?page={pageNum}&limit=20&order_by=author_num&service_name=mcn.AdStarMcnService&service_method=DemanderMcnList&sign_strict=1&sign={list_sign}"
    response = requests.get(url=list_url, headers=headers).json()
    # print(response)
    mcns = response['data']['mcns']
    for mcn in mcns:
        mcn_id = mcn['user_id']
        # print(mcn_id)
        public_sign = get_public_sign(mcn_id)
        # print(public_sign)
        public_url = f"https://www.xingtu.cn/h/api/gateway/handler_get/?mcn_id={mcn_id}&service_name=mcn.AdStarMcnService&service_method=McnGetPublicInfo&sign_strict=1&sign={public_sign}"
        resp = requests.get(url=public_url, headers=headers).json()
        result = resp['data']['public_info']
        mcn_name = result['name']
        company_name = result['company_name']
        author_num = result['author_num']
        introduction = result['introduction']
        sum_follower = result['sum_follower']
        page_top_sign = get_page_top_sign(mcn_id)
        page_top_url = f"https://www.xingtu.cn/h/api/gateway/handler_get/?mcn_id={mcn_id}&service_name=mcn.AdStarMcnService&service_method=McnMainPageTopAuthors&sign_strict=1&sign={page_top_sign}"
        res = requests.get(url=page_top_url, headers=headers).json()
        top_follower_authors = res['data']['top_follower_authors']
        lst = []
        for top_follower_author in top_follower_authors:
            nick_name = top_follower_author['nick_name']
            tags = top_follower_author['tags']
            tag = nick_name + ":" + str(tags)
            lst.append(tag)
        # print(lst)
        print([mcn_name, company_name, author_num, sum_follower, introduction, str(lst)])
        ws.append([mcn_name, company_name, author_num, sum_follower, introduction, str(lst)])
    wb.save(r"D:\douyin\douyin_erp\douyin_11月\mcn_douyin_1.xlsx")


if __name__ == '__main__':
    for i in range(27, 69):
        get_mcn(i)
        time.sleep(3)
