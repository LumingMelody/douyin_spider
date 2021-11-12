import random

import pandas as pd
import requests
from openpyxl import Workbook
from whosecard_open_platform import WhosecardDySpider

BASE_URI = 'http://whosecard.com:8081'
DY_API_PATH = {
    'post': '/api/douyin/aweme/post',
    'favorite': '/api/douyin/aweme/favorite',
    'challenge': '/api/douyin/aweme/challenge',
    'user_detail': '/api/douyin/aweme/user/detail',
    'challenge_detail': '/api/douyin/aweme/challenge/detail',
    'challenge_related': '/api/douyin/aweme/poi/challenge/related',
    'detail': '/api/douyin/aweme/detail',
    'comment': '/api/douyin/aweme/comment',
    'comment_reply': '/api/douyin/aweme/comment/reply',
    'promotion': '/api/douyin/aweme/promotion',
    'product_item': '/api/douyin/haohuo/product/item',
    'search': '/api/douyin/aweme/search',
    'poi_detail': '/api/douyin/aweme/poi/detail',
    'poi_aweme': '/api/douyin/aweme/poi/aweme',
    'user_follower_list': '/api/douyin/aweme/user/follower/list',
    'user_following_list': '/api/douyin/aweme/user/following/list',
    'hotsearch_brand_category': '/api/douyin/aweme/hotsearch/brand/category',
    'hotsearch_brand_weekly_list': '/api/douyin/aweme/hotsearch/brand/weekly/list',
    'hotsearch_brand_billboard': '/api/douyin/aweme/hotsearch/brand/billboard',
    'hotsearch_brand_detail': '/api/douyin/aweme/hotsearch/brand/detail'
}

wb = Workbook()

ws = wb.active
ws.append(['手机号', '达人名称', '用户ID', '达人主页链接', '评论', '点赞', '分享'])

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

cookie = ""
headers = {
    "User-Agent": random.choice(USER_AGENTS),
    "cookie": cookie,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'Connection': 'close'
}


def short_url_to_long_url(short_url):
    """

    :param short_url:
    :return:
    """
    res = requests.get(short_url, headers=headers, allow_redirects=False)
    long_url = res.headers.get('location')
    return long_url


if __name__ == '__main__':
    file_path = r"D:\red_book\red_book_51wom\red_book_10月\red_book_10_26\douyin_urls.xlsx"
    dy = WhosecardDySpider()
    df = pd.read_excel(file_path)
    urls = df['发布链接']
    phones = df['手机号']
    for index, url in enumerate(urls):
        # print(url)
        l_url = short_url_to_long_url(url)
        # print(l_url)
        # awe_id = url.split("/")[-1]
        awe_id = l_url.split("/")[-2]
        print(awe_id)
        result = dy.get_detail(awe_id)
        print(result)
        if result is not None:
            aweme_detail = result['result']['aweme_detail']
            author_name = aweme_detail['author']['nickname']
            author_sec_uid = aweme_detail['author']['sec_uid']
            author_id = aweme_detail['author_user_id']
            author_url = f"https://www.douyin.com/user/{author_sec_uid}?&author_id={author_id}"
            comment_count = aweme_detail['statistics']['comment_count']
            digg_count = aweme_detail['statistics']['digg_count']
            share_count = aweme_detail['statistics']['share_count']
            ws.append([phones[index], author_name, author_id, author_url, comment_count, digg_count, share_count])
    wb.save(r"D:\red_book\red_book_51wom\red_book_10月\red_book_10_26\douyin_10_26_result.xlsx")


