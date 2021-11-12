#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import traceback

from urllib.parse import quote

# from src.commons.logging_helper import LoggingHelper

APP_NAME = 'whosecard_open_platform'
# logger = LoggingHelper.get_logger(APP_NAME)

BASE_URI = 'http://whosecard.com:8081'
APP_CONFIG = {
    'KEY': ''
}
XHS_API_PATH = {
    'search_notes': '/api/xiaohongshu/search/notes/v1',
    'note_detail': '/api/xiaohongshu/note/detail',
    'note_comments': '/api/xiaohongshu/note/comments',
    'note_sub_comments': '/api/xiaohongshu/note/sub_comments',
    'note_goods': '/api/xiaohongshu/note/goods',
    'user_notes': '/api/xiaohongshu/user/notes',
    'user_info': '/api/xiaohongshu/user/info',
    'user_followings': '/api/xiaohongshu/user/followings/v1',
    'user_followers': '/api/xiaohongshu/user/followers/v1',
    'note_liked': '/api/xiaohongshu/note/liked/v1',
    'note_faved': '/api/xiaohongshu/note/faved/v1',
    'store_items': '/api/xiaohongshu/store/items',
    'search_goods': '/api/xiaohongshu/search/goods',
    'search_user': '/api/xiaohongshu/search/user',
    'fe_api': '/api/xiaohongshu/fe_api'
}
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
KS_API_PATH = {
    'userIdInfo': '/api/kuaishou/userIdInfo',
    'userIdInfoFromPhoto': '/api/kuaishou/userIdInfoFromPhoto',
    'profile': '/api/kuaishou/profile',
    'profile_v2': '/api/kuaishou/photo/profile/v2',
    'profile_web_v1': '/api/kuaishou/photo/profile/web/v1',
    'grocery_product': '/api/kuaishou/grocery/product',
    'user_feeds': '/api/kuaishou/user/feeds',
    'tag_feeds': '/api/kuaishou/tag/feeds',
    'tag_info': '/api/kuaishou/tag/info',
    'location_poi': '/api/kuaishou/location/poi',
    'search': '/api/kuaishou/search'
}
WX_API_PATH = {
    'articles': '/api/wx/articles',
    'tmp2forever': '/api/url/transfer/tmp2forever',
    'short2long': '/api/url/transfer/short2long',
    'long2short': '/api/url/transfer/long2short',
    'info': '/api/account/info',
    'ext': '/api/msg/ext',
    'comment': '/api/msg/comment',
    'article': '/api/wx/article',
    'gzh_search': '/api/wx/gzh/search',
    'article_search': '/api/wx/article/search'
}
BZ_API_PATH = {
    'web': '/api/bilibili/web',
}
ZH_API_PATH = {
    'web': '/api/zhihu/web'
}


def get_data_from_api_url(api_url, params: dict):
    """
    获取接口数据
    :param api_url:
    :param params:
    :return:
    """
    params['key'] = APP_CONFIG['KEY']
    try:
        result = requests.get(api_url, params=params).json()
        if result.get('ok'):
            return result
        else:
            print(f'whosecard 返回值错误,返回值内容{result},请查看官网.')
            return None
    except Exception as e:
        print(f'whosecard 接口错误,错误内容{e},请查看官网.')
        return None


class WhosecardDySpider(object):
    """ whosecard 抖音 spider

    """

    @classmethod
    def get_data_from_api_name(cls, api_name, params: dict):
        """
        获取接口数据
        :param api_name:
        :param params:
        :return:
        """
        api_url = f'{BASE_URI}{DY_API_PATH[api_name]}'
        return get_data_from_api_url(api_url, params)

    @classmethod
    def get_search(cls, keyword, cursor=None, search_source='video_search', sort_type=0, publish_time=0):
        """
        获取关键词搜索结果
        :param keyword:
        :param cursor: 上一页会返回下一页的cursor值
        :param search_source: search_source为搜索类型，目前支持以下取值：
  video_search: 搜索视频
  poi: 搜索地点
  user: 搜索用户，此时keyword建议填用户的short_id(抖音号)
  challenge: 搜索话题/挑战
        :param sort_type: sort_type: 对结果排序，取值为 0（综合排序），1（最多点赞），2（最新发布）
        :param publish_time: 限制发布时间，取值为 0（不限），1（一天内），7（一周内），182（半年内）
        :return:
        """
        params = dict()
        params['keyword'] = keyword
        params['cursor'] = cursor
        params['search_source'] = search_source
        params['sort_type'] = sort_type
        params['publish_time'] = publish_time
        return cls.get_data_from_api_name('search', params)

    @classmethod
    def get_post(cls, user_id, max_cursor=None):
        """
        实时获取用户发布的视频列表（按时间排序）
        :param user_id:
        :param max_cursor:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['max_cursor'] = max_cursor
        return cls.get_data_from_api_name('post', params)

    @classmethod
    def get_favorite(cls, user_id, max_cursor=None):
        """
        实时获取用户喜欢（点赞）的视频列表（按时间排序）
        :param user_id:
        :param max_cursor:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['max_cursor'] = max_cursor
        return cls.get_data_from_api_name('favorite', params)

    @classmethod
    def get_challenge(cls, ch_id, is_commerce=1, cursor=None):
        """
        实时获取话题/挑战视频列表（按热度排序）
        :param ch_id:
        :param is_commerce: 参数is_commerce不能为空，此值是从话题/挑战详情接口里获取到的，如果is_commerce=1则表示为商业话题，传0则为普通话题
如果要翻页，需要传入cursor参数（这里的参数跟前面的max_cursor不一样，不要搞混了），此参数在前一页的请求中会返回，每次翻页都会更新。
此接口返回的视频个数可能不固定，具体以实际为准。
        :param cursor:
        :return:
        """
        params = dict()
        params['ch_id'] = ch_id
        params['is_commerce'] = is_commerce
        params['cursor'] = cursor
        return cls.get_data_from_api_name('post', params)

    @classmethod
    def get_user_detail(cls, user_id):
        """
        获取抖音用户详情页
        :param user_id:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        return cls.get_data_from_api_name('user_detail', params)

    @classmethod
    def get_challenge_detail(cls, ch_id):
        """
        获取话题/挑战详情页
        :param ch_id:
        :return:
        """
        params = dict()
        params['ch_id'] = ch_id
        return cls.get_data_from_api_name('challenge_detail', params)

    @classmethod
    def get_challenge_related(cls, ch_id):
        """
        获取话题/挑战的相关地点
        :param ch_id:
        :return:
        """
        params = dict()
        params['ch_id'] = ch_id
        return cls.get_data_from_api_name('challenge_related', params)

    @classmethod
    def get_detail(cls, aweme_id):
        """
        实时获取单个抖音视频detail信息（不包含播放量）
        :param aweme_id:
        :return:
        """
        params = dict()
        params['aweme_id'] = aweme_id
        return cls.get_data_from_api_name('detail', params)

    @classmethod
    def get_comment(cls, aweme_id, cursor=None):
        """
        获取视频评论列表
        :param aweme_id:
        :param cursor:
        :return:
        """
        params = dict()
        params['aweme_id'] = aweme_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('comment', params)

    @classmethod
    def get_comment_reply(cls, aweme_id, comment_id, cursor=None):
        """
        获取视频评论回复列表
        :param aweme_id:
        :param comment_id:
        :param cursor:
        :return:
        """
        params = dict()
        params['aweme_id'] = aweme_id
        params['comment_id'] = comment_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('comment_reply', params)

    @classmethod
    def get_promotion(cls, user_id, cursor=None):
        """
        获取抖音用户商品橱窗列表
        :param user_id:
        :param cursor: 每次返回10个商品信息，如果要翻页，则需要传入cursor参数，第一次请求时cursor为0，之后每次翻页传的cursor都要加10。
比如当cursor=0时，返回第1-10条商品信息。
比如当cursor=10时，返回第11-20条商品信息。
以此类推，每次请求结果可以根据返回的has_more参数判断是否需要翻页。
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('promotion', params)

    @classmethod
    def get_product_item(cls, url):
        """
        从haohuo获取单个商品详情
        :param url: url参数需要urlencode编码，此参数来自于【获取抖音用户商品橱窗列表】接口的商品链接url字段。
如：https://haohuo.snssdk.com/views/product/item2?id=3320163565905801015&origin_type=3002002000&origin_id=95899249695_3320163565905801015

⚠️ url必须是https://haohuo.snssdk.com开头，否则此接口请求无效（如果是其它链接，如淘宝商品链接，则不要请求此接口）。

        :return:
        """
        params = dict()
        params['url'] = url
        return cls.get_data_from_api_name('product_item', params)

    @classmethod
    def get_poi_detail(cls, poi_id):
        """
        获取根据poi_id获取地点详情页数据
        :param poi_id:
        :return:
        """
        params = dict()
        params['poi_id'] = poi_id
        return cls.get_data_from_api_name('poi_detail', params)

    @classmethod
    def get_poi_aweme(cls, poi_id, cursor=None):
        """
        获取根据poi_id获取地点发布的视频列表
        :param poi_id:
        :param cursor: cursor在翻页时会用到，初始默认为0，如果前一页请求返回的has_more=1，取cursor返回值可获取下一页数据
        :return:
        """
        params = dict()
        params['poi_id'] = poi_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('poi_aweme', params)

    @classmethod
    def get_user_follower_list(cls, user_id, max_time=None):
        """
        获取获取用户粉丝列表
        :param user_id:
        :param max_time: 如果要翻页，需要传入max_time参数，此参数可从前一页的返回值min_time获取（⚠️这里是min_time，不是max_time），每次翻页都会更新。
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['max_time'] = max_time
        return cls.get_data_from_api_name('user_follower_list', params)

    @classmethod
    def get_user_following_list(cls, user_id, max_time=None):
        """
        获取获取用户关注列表
        :param user_id:
        :param max_time: 如果要翻页，需要传入max_time参数，此参数可从前一页的返回值min_time获取（⚠️这里是min_time，不是max_time），每次翻页都会更新。
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['max_time'] = max_time
        return cls.get_data_from_api_name('user_following_list', params)

    @classmethod
    def get_hotsearch_brand_category(cls):
        """
        获取品牌热DOU榜 - 品牌分类列表
        :return:
        """
        params = dict()
        return cls.get_data_from_api_name('hotsearch_brand_category', params)

    @classmethod
    def get_hotsearch_brand_weekly_list(cls, category_id):
        """
        获取品牌热DOU榜 - 指定品牌分类下的历史榜单
        :param category_id:category_id为品牌分类id，从【品牌热DOU榜 - 品牌分类列表】接口获取
        :return:
        """
        params = dict()
        params['category_id'] = category_id
        return cls.get_data_from_api_name('hotsearch_brand_weekly_list', params)

    @classmethod
    def get_hotsearch_brand_billboard(cls, category_id, start_date=''):
        """
        获取品牌热DOU榜 - 指定品牌分类下的指定某一期榜单信息
        :param category_id: category_id为品牌分类id，从【品牌热DOU榜 - 品牌分类列表】接口获取
        :param start_date: start_date为指定某一期榜单，如果为空字符串则取最近一期，可选值从【品牌热DOU榜 - 指定品牌分类下的历史榜单】接口获取
        :return:
        """
        params = dict()
        params['category_id'] = category_id
        params['start_date'] = start_date
        return cls.get_data_from_api_name('hotsearch_brand_billboard', params)

    @classmethod
    def get_hotsearch_brand_detail(cls, category_id, brand_id):
        """
        获取品牌热DOU榜 - 获取单个品牌的详情数据
        :param category_id: category_id为品牌分类id，从【品牌热DOU榜 - 品牌分类列表】接口获取
        :param brand_id: brand_id为品牌id，从【品牌热DOU榜 - 指定品牌分类下的指定某一期榜单信息】接口获取
        :return:
        """
        params = dict()
        params['category_id'] = category_id
        params['brand_id'] = brand_id
        return cls.get_data_from_api_name('hotsearch_brand_detail', params)

    @classmethod
    def share_url_to_normal_url(cls, url):
        """
        分享链接转换
        :param url:
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
        if 'sec_uid' in url:
            user_id = url.split('?')[0].split('/')[-1]
            return {
                'retCode': 0,
                'ok': True,
                'result': {
                    'user_id': user_id
                }
            }
        try:
            res = requests.get(url, headers=headers, allow_redirects=False)
        except:
            return {
                'retCode': 1,
                'ok': False,
                'result': {}
            }
        normal_url = res.headers.get('location')
        user_id = normal_url.split('?')[0].split('/')[-1]
        return {
            'retCode': 0,
            'ok': True,
            'result': {
                'user_id': user_id
            }
        }


if __name__ == '__main__':
    result = WhosecardDySpider.get_search("口红")
    import json

    print(json.dumps(result))

    # print(WhosecardKsSpider.get_userIdInfo('https%3a%2f%2ff.kuaishou.com%2fsnK21'))
