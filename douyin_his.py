import time

import pandas as pd
from openpyxl import Workbook

from whosecard_open_platform import WhosecardDySpider

wb = Workbook()
ws = wb.active
ws.append([
    "用户名",
    "用户ID",
    "用户签名",
    "用户粉丝",
    "用户关注数",
    "用户获赞数",
    "用户作品ID",
    "用户作品链接",
    "用户作品标题",
    "用户作品评论数",
    "用户作品点赞数",
    "用户作品下载数",
    "用户作品分享数",
    "用户作品转发数",
    "用户作品发布时间",
])


# def main(u_id, user, fan, follower, like_count):
def main():
    dy = WhosecardDySpider()
    result = dy.get_post(user_id=4437277056436583, max_cursor=0)
    # result = dy.get_post(user_id=u_id, max_cursor=0)
    print(result)
    if result is not None:
        while 'max_cursor' in result['result'].keys():
            print(result)
            aweme_list = result['result']['aweme_list']
            for aweme in aweme_list:
                user_name = aweme['author']['nickname']
                uid = aweme['author']['uid']
                sign = aweme['author']['signature']
                user = "安森的话事酒馆"
                fans = 6083761
                follower = 8
                like_count = 64278965
                # user_url = "https://www.douyin.com/user/MS4wLjABAAAASnmoVotBsVhd4vE1FxuawkL75r_Hc8PQynaM5UAqUvE?enter_method=video_title&author_id=98289525851&group_id=6916409351733366019&log_pb=%7B%22impr_id%22%3A%22021625638344237fdbddc0100fff0030a0a1a880000002020eba6%22%7D&enter_from=video_detail"
                aweme_id = aweme['aweme_id']
                aweme_url = f"https://www.douyin.com/video/{aweme_id}"
                desc = aweme['desc']
                comment_count = aweme['statistics']['comment_count']
                digg_count = aweme['statistics']['digg_count']
                download_count = aweme['statistics']['download_count']
                forward_count = aweme['statistics']['forward_count']
                share_count = aweme['statistics']['share_count']
                ts = aweme['create_time']
                timeArray = time.localtime(ts)
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                # if ts <= 1577808000:
                #     return
                print([user_name, uid, sign, fans, follower, like_count, aweme_url, aweme_id, desc,
                       comment_count, digg_count, download_count, share_count, forward_count, create_time])
                ws.append([user_name, uid, sign, fans, follower, like_count, aweme_id, aweme_url, desc,
                           comment_count, digg_count, download_count, share_count, forward_count, create_time])
            max_cursor = result['result']['max_cursor']
            result = dy.get_post(user_id=4437277056436583, max_cursor=max_cursor)
            # wb.save(f"D:/douyin/douyin_erp/douyin_8月/douyin_08_04/{user}.xlsx")
            wb.save("D:/douyin/douyin_erp/douyin_8月/douyin_08_04/安森的话事酒馆.xlsx")
        else:
            print("没有更多作品")
    else:
        print("作品抓取失败")


if __name__ == '__main__':
    # df = pd.read_excel(r"D:\douyin\douyin_erp\douyin_8月\douyin_08_04\douyin_ids.xlsx")
    # ids = df['用户ID']
    # users = df['用户名']
    # fans = df['粉丝数']
    # followers = df['关注数']
    # like_counts = df['获赞总数']
    # for index, id in enumerate(ids):
    #     user = users[index]
    #     fan = fans[index]
    #     follower = followers[index]
    #     like_count = like_counts[index]
    #     main(id, user, fan, follower, like_count)
    main()
