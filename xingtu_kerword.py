import random
import time
import wsgiref.util
from concurrent.futures import ThreadPoolExecutor

import requests
import pandas as pd
from openpyxl import Workbook

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    # "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]

headers = {
    "referer": "https://star.toutiao.com/ad/market",
    "sec-ch-ua-mobile": '?0',
    "User-Agent": random.choice(USER_AGENTS),
    "cookie": "gfsitesid=MzY4NzhmZGY4OXwxNjIzNDAzNjMxMDd8fDEwNTE0MDUyNzQ4MgsLCwsLCwsLCwsL; passport_csrf_token_default=25454a94b73082db0078c86894451f11; passport_csrf_token=25454a94b73082db0078c86894451f11; csrftoken=c7MDzKh5jozJNIrtNbX7iubWJbewwaWG; tt_webid=6972461911858349604; uid_tt=1aec1a22fd51c90c4749eea3c46c4d1d; uid_tt_ss=1aec1a22fd51c90c4749eea3c46c4d1d; sid_tt=36878fdf89c56033dc5c7d6280d1de34; sessionid=36878fdf89c56033dc5c7d6280d1de34; sessionid_ss=36878fdf89c56033dc5c7d6280d1de34; sid_guard=36878fdf89c56033dc5c7d6280d1de34%7C1623403630%7C5184000%7CTue%2C+10-Aug-2021+09%3A27%3A10+GMT; star_sessionid=69e6008d5a1ffb0f12301e952df0d46e; gftoken=MzY4NzhmZGY4OXwxNjIzNDAzNjMxMDd8fDAGBgYGBgY; MONITOR_WEB_ID=7a9c76e8-8b54-4e62-a0b5-b6d0785aa1e4",
    "x-login-source": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "X-CSRFToken": "E9qPVeX3FJBxDXSf1RuRMYxJrQtnMsre",
}

# 代理服务器
proxyHost = "forward.apeyun.com"
proxyPort = "9082"
# 代理隧道验证信息
proxyUser = "2021040800226731834"
proxyPass = "pA7prxttyuCTFjwM"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

wb = Workbook()
ws = wb.active
# ws.append(["昵称", "1s-20s视频报价", "20s-60s视频报价", "60s以上视频报价"])
ws.append(["昵称", "详情页链接"])


def get_xingtu_keyword(d_url):
    resp = requests.get(url=d_url, headers=headers).json()
    try:
        author = resp['data']['authors'][0]
        print(author)
        nickname = author['nick_name']
        price_info = author['price_info']
        author_id = author['id']
        author_url = f"https://www.xingtu.cn/ad/creator/author/douyin/{author_id}"
        # if price_info[0]:
        #     one_to_twenty = price_info[0]['origin_price']
        # else:
        #     one_to_twenty = 0
        # if price_info[1]:
        #     twenty_to_sixty = price_info[1]['origin_price']
        # else:
        #     twenty_to_sixty = 0
        # if price_info[2]:
        #     more_than_sixty = price_info[2]['origin_price']
        # else:
        #     more_than_sixty = 0
        ws.append([nickname, author_url])
        wb.save("D:/douyin/07_30.xlsx")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # df = pd.read_excel("D:/douyin/douyin_erp/育婴师douyin_06_15.xlsx")
    df = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_07_29\dy_uid.xlsx")
    # pool = ThreadPoolExecutor(max_workers=10)
    user_names = df['昵称']
    for user_name in user_names:
        url = f"https://www.xingtu.cn/v/api/demand/author_list/?limit=20&need_detail=true&page=1&platform_source=1&key={user_name}&task_category=1&order_by=score&disable_replace_keyword=false&only_nick_name=false&is_filter=false"
        get_xingtu_keyword(url)
        time.sleep(2)
    #     pool.submit(get_xingtu_keyword, url)
    # pool.shutdown(wait=True)
