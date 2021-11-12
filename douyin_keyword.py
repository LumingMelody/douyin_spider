import random
import time

import pandas as pd
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
# ws.append(['达人名称', '用户ID', '用户主页链接', '用户头像', '发布链接'])
ws.append([
    "达人名称",
    "粉丝数",
    "发布链接",
    "点赞量",
    "评论量",
    "转发量",
    "下载量",
    # "总互动量",
    "发布时间",
])
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


# 数据去重
def del_duplication(file_path):
    rd = pd.read_excel(file_path)
    rd.drop_duplicates(["昵称"], keep="last", inplace=True)
    # print(df)
    data = pd.DataFrame(rd)
    data.to_excel(file_path)


if __name__ == '__main__':
    file_path = r"D:\douyin\douyin_erp\douyin_11月\douyin_YSL夜皇后精华.xlsx"
    try:
        dy = WhosecardDySpider()
        cursor = 0
        for i in range(100):
            rs = dy.get_search(keyword="YSL夜皇后精华", cursor=cursor)
            # print(rs)
            while rs['result']['has_more']:
                rs = dy.get_search(keyword="YSL夜皇后精华", cursor=cursor)
                result = rs['result']
                result_list = result['aweme_list']
                for r in result_list:
                    # user_id = r['author_user_id']
                    # sec_uid = r['author']['sec_uid']
                    # uid = str(user_id) + "&sec_uid=" + str(sec_uid)
                    # user_url = "https://www.iesdouyin.com/share/user/{}".format(uid)
                    # user_img = r['author']['avatar_168x168']['url_list'][0]
                    # v_id = r['group_id']
                    # print(user_url)
                    user_name = r['author']['nickname']
                    fans = r['author']['follower_count']
                    # collect_count = r['statistics']['collect_count']
                    comment_count = r['statistics']['comment_count']
                    digg_count = r['statistics']['digg_count']
                    download_count = r['statistics']['download_count']
                    forward_count = r['statistics']['forward_count']
                    # share_count = r['statistics']['share_count']
                    # v_url = "https://www.iesdouyin.com/share/video/{}".format(v_id)
                    aweme_id = r['aweme_id']
                    v_url = f"https://www.douyin.com/video/{aweme_id}"
                    ts = r['create_time']
                    timeArray = time.localtime(ts)
                    create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    # total_interaction = int(digg_count) + int(comment_count) + int(forward_count), int(download_count)
                    ws.append([user_name, fans, v_url, digg_count, comment_count, forward_count,  download_count,
                               create_time])
                    print([user_name, fans, v_url, digg_count, comment_count, forward_count, download_count,
                           create_time])
                wb.save(file_path)
                cursor += 12
            else:
                break
            # if result['cursor'] == 12:

    except Exception as e:
        print(e)
    # del_duplication(file_path)

    # df = pd.read_excel("D:/douyin/douyin_erp/黑丝douyin_06_16.xlsx")
    # urls = df['发布链接']
    # for url in urls:
    #     v_id = url.split("/")[-1]
    #     rs = dy.get_comment(aweme_id=v_id)
    #     print(rs)
