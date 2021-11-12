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
    "cookie": "ttcid=a6090f76dd5c44fbbec4a168e40d834328; _tea_utm_cache_2018=undefined; MONITOR_DEVICE_ID=8c84e3d2-3e8b-4656-8c54-c5c2cb130771; tt_webid=7028866373770692127; csrftoken=fPGSy36I8BeD3WQbbMZ5CvvgnZrbK01c; passport_csrf_token_default=07aa241118dabb872e93c5ec839b6688; passport_csrf_token=07aa241118dabb872e93c5ec839b6688; _tea_utm_cache_1581=undefined; _tea_utm_cache_2925=undefined; MONITOR_WEB_ID=20edb3f9-47ce-4d74-910c-3b610af9e378; tt_scid=40ZuvR0Uh65qrApAvCSArpbtB.U6aWqy9nDx1LCLxlM4eAeXDEghWMyU5jCJqk7k43bd; s_v_web_id=verify_2a02307c944b749b3b8732a7d07c2cf0; uid_tt=487c48d51c8a293c72d2df360639dd53; uid_tt_ss=487c48d51c8a293c72d2df360639dd53; sid_tt=46013a8742ea58a290c398699ced54bb; sessionid=46013a8742ea58a290c398699ced54bb; sessionid_ss=46013a8742ea58a290c398699ced54bb; sid_ucp_v1=1.0.0-KDAxYTU5MGE3YmU1YTk2YzQ0NGE2NjBiNTNhMDQ1YmRkZDk0M2M1MjcKFQj6wvTWhwMQkpyyjAYY-hM4AUDrBxoCbGYiIDQ2MDEzYTg3NDJlYTU4YTI5MGMzOTg2OTljZWQ1NGJi; ssid_ucp_v1=1.0.0-KDAxYTU5MGE3YmU1YTk2YzQ0NGE2NjBiNTNhMDQ1YmRkZDk0M2M1MjcKFQj6wvTWhwMQkpyyjAYY-hM4AUDrBxoCbGYiIDQ2MDEzYTg3NDJlYTU4YTI5MGMzOTg2OTljZWQ1NGJi; sid_guard=46013a8742ea58a290c398699ced54bb%7C1636601362%7C5184000%7CMon%2C+10-Jan-2022+03%3A29%3A22+GMT; star_sessionid=d11fad1b3418a892797754a166a812b0; gftoken=NDYwMTNhODc0MnwxNjM2NjAxMzYzOTV8fDAGBgYGBgY",

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


def get_pagetop_sign(mcn_id):
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
        page_top_sign = get_pagetop_sign(mcn_id)
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
