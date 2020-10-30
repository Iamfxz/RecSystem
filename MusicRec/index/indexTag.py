# -*- coding:utf-8 -*-
import datetime

from django.core.cache import cache

from playlist.models import PlayListToTag
from sing.models import SingTag
from song.models import SongTag
from user.models import UserBrowse

# 首页 推荐标签
"""
    由于标签个数原因，且歌单、歌手、歌曲公用一套标签，所以这里的标签推荐基于
        1、用户在站内产生的点击行为
        2、热门标签进行补数
"""


def GetHotTags(request):
    user_name = request.GET.get("username")
    # 歌手标签
    sings_tags = getSingRecTags(user_name)
    # 歌曲,歌单标签
    songs_tags, pl_tags = getSongAndPlRecTags(user_name)
    return {
        "code": 1,
        "data": {
            "playlist": {"cateid": 2, "tags": list(pl_tags)},
            "song": {"cateid": 3, "tags": list(songs_tags)},
            "sing": {"cateid": 4, "tags": list(sings_tags)},
        }
    }


# 获得歌手标签推荐
def getSingRecTags(user_name):
    start = datetime.datetime.now()
    a_day_ago = start - datetime.timedelta(hours=23, minutes=59, seconds=59)  # 获取当前时间的一天之前
    sings_tags = list()
    # 根据用户一天内的足迹进行标签推荐
    click_sings = UserBrowse.objects.filter(user_name=user_name, click_cate="4",
                                            user_click_time__gt=a_day_ago).values("click_id")
    if click_sings.__len__() != 0:
        for one in click_sings:
            filter_one = SingTag.objects.filter(sing_id=one["click_id"])
            if filter_one.__len__() != 0 and filter_one[0].tag not in sings_tags:
                sings_tags.append(filter_one[0].tag)
    print("歌手标签推荐: %s" % sings_tags)
    # 如果 click 和 choose的tag不够 以 hot来补充
    cache_tag_dict_sing = cache.get('tag_dict_sing', 'NOT_EXISTS')  # 缓存不存在则返回True
    # print(cache_tag_dict_sing)
    if cache_tag_dict_sing == 'NOT_EXISTS':
        if sings_tags.__len__() < 15:
            hot_tag_dict = dict()
            for one in SingTag.objects.all():
                hot_tag_dict.setdefault(one.tag, 0)
                hot_tag_dict[one.tag] += 1
            tag_dict_sing = sorted(hot_tag_dict.items(), key=lambda k: k[1], reverse=True)[:15 - sings_tags.__len__()]
            for tag_count in tag_dict_sing:
                if tag_count[0] not in sings_tags:
                    sings_tags.append(tag_count[0])
            cache.add('tag_dict_sing', tag_dict_sing, 30 * 60)
            # print("sings_tags_by_hot: %s" % sings_tags_by_hot)
    else:
        for tag_count in cache_tag_dict_sing:
            if tag_count[0] not in sings_tags:
                sings_tags.append(tag_count[0])
    end = datetime.datetime.now()
    print('计算歌手标签时间：' + str(end - start))
    return sings_tags


# 获得歌曲、歌单标签推荐
def getSongAndPlRecTags(user_name):
    start = datetime.datetime.now()
    a_day_ago = start - datetime.timedelta(hours=23, minutes=59, seconds=59)  # 获取当前时间的一天之前
    song_tags = list()
    pl_tags = list()
    # 根据用户一天内的足迹进行标签推荐
    click_pls = UserBrowse.objects.filter(user_name=user_name, click_cate="2",
                                          user_click_time__gt=a_day_ago).values("click_id")
    click_songs = UserBrowse.objects.filter(user_name=user_name, click_cate="3",
                                            user_click_time__gt=a_day_ago).values("click_id")
    if click_songs.__len__() != 0:
        for one in click_songs:
            filter_one = SongTag.objects.filter(song_id=one["click_id"])
            if filter_one.__len__() != 0 and filter_one[0].tag not in song_tags:
                song_tags.append(filter_one[0].tag)
    if click_pls.__len__() != 0:
        for one in click_pls:
            pl_one = PlayListToTag.objects.filter(pl_id=one["click_id"])
            if pl_one.__len__() != 0:
                for pl_tag_one in pl_one:
                    if pl_tag_one.tag not in pl_tags:
                        pl_tags.append(pl_tag_one.tag)
    print("推荐歌单标签 %s" % pl_tags)
    print("推荐歌曲标签： %s" % song_tags)
    # 如果tag不够 以 hot来补充
    cache_tag_dict_song = cache.get('tag_dict_song', 'NOT_EXISTS')
    # print(cache_tag_dict_song)
    if cache_tag_dict_song == 'NOT_EXISTS':
        if song_tags.__len__() < 15:
            hot_tag_dict = dict()
            for one in SongTag.objects.all():
                hot_tag_dict.setdefault(one.tag, 0)
                hot_tag_dict[one.tag] += 1
            tag_dict_song = sorted(hot_tag_dict.items(), key=lambda k: k[1], reverse=True)[:15 - song_tags.__len__()]
            for one in tag_dict_song:
                if one[0] not in song_tags:
                    song_tags.append(one[0])
            cache.add('tag_dict_song', tag_dict_song, 30 * 60)
            # print("songs_tags_by_hot: %s" % songs_tags_by_hot)
    else:
        for one in cache_tag_dict_song:
            if one[0] not in song_tags:
                song_tags.append(one[0])
    end = datetime.datetime.now()
    # 如果 click 和 choose的tag不够 以 hot来补充
    cache_tag_dict_pl = cache.get('tag_dict_pl', 'NOT_EXISTS')
    # print(cache_tag_dict_pl)
    if cache_tag_dict_pl == 'NOT_EXISTS':
        if pl_tags.__len__() < 15:
            hot_tag_dict = dict()
            for one in PlayListToTag.objects.all():
                hot_tag_dict.setdefault(one.tag, 0)
                hot_tag_dict[one.tag] += 1
            tag_dict_pl = sorted(hot_tag_dict.items(), key=lambda k: k[1], reverse=True)[:15 - pl_tags.__len__()]
            for one in tag_dict_pl:
                if one[0] not in pl_tags:
                    pl_tags.append(one[0])
            cache.add('tag_dict_pl', tag_dict_pl, 30 * 60)
            # print("pl_tags_by_hot: %s" % pl_tags_by_hot)
    else:
        for one in cache_tag_dict_pl:
            if one[0] not in pl_tags:
                pl_tags.append(one[0])
    
    print('计算歌曲歌单标签时间：' + str(end - start))
    return song_tags, pl_tags
