# -*- coding:utf-8 -*-
from datetime import datetime

from django.core.cache import cache
from django.http import JsonResponse

from sing.models import Sing
from song.models import Song, SongLysic, SongTag, SongSim
from user.views import writeBrowse, getLocalTime


def all(request):
    start = datetime.now()
    # 接口传入的tag参数
    tag = request.GET.get("tag")
    # 接口传入的page参数
    _page = int(request.GET.get("page"))
    _pagesize = int(request.GET.get('pagesize'))
    print("Tag : %s,page_id: %s" % (tag, _page))
    _list = list()
    # 全部歌曲
    if tag == "all":
        cache_song_tags_list = cache.get('song_tags_list', 'NOT_EXISTS')
        if cache_song_tags_list == 'NOT_EXISTS':
            song_tags_list = Song.objects.all().values("song_id", "song_name", "song_publish_time")
            cache.add('song_tags_list', song_tags_list, 24 * 60 * 60)
        else:
            song_tags_list = cache_song_tags_list
        # 拼接歌曲信息
        for one in song_tags_list[(_page - 1) * _pagesize:_page * _pagesize]:
            _list.append({
                "song_id": one["song_id"],
                "song_name": one["song_name"],
                "song_publish_time": one["song_publish_time"]
            })
        total = song_tags_list.__len__()
    # 指定标签下的歌曲
    else:
        song_tags_list = SongTag.objects.filter(tag=tag).values("song_id")
        # 转换成set去重复再转化回list
        song_ids_set = set()
        for song in song_tags_list:
            song_ids_set.add(song['song_id'])
        song_ids_set = sorted(song_ids_set)
        song_ids_list = list(song_ids_set)
        song_ids = song_ids_list[(_page - 1) * _pagesize:_page * _pagesize]
        # print(song_ids)
        songs_list = Song.objects.filter(song_id__in=song_ids).values("song_id", "song_name", "song_publish_time")
        print(songs_list.__len__())
        for one in songs_list:
            _list.append({
                "song_id": one["song_id"],
                "song_name": one["song_name"],
                "song_publish_time": one["song_publish_time"]
            })
        total = song_ids_list.__len__()
    end = datetime.now()
    print('歌曲页面时间：'+str(end - start))
    return {"code": 1,
            "data": {
                "total": total,
                "songs": _list,
                "tags": getAllSongTags()
            }
            }


def getAllSongTags():
    start = datetime.now()
    tags = set()
    cache_song_tags = cache.get('song_tags','NOT_EXISTS')
    if cache_song_tags == 'NOT_EXISTS':
        for one in SongTag.objects.all().values("tag").distinct().order_by("song_id"):
            tags.add(one["tag"])
        cache.add('song_tags', tags, 24*60*60)
    else:
        tags = cache_song_tags
    end = datetime.now()
    print('获取所有标签时间：'+str(end-start))
    return list(tags)


def one(request):
    song_id = request.GET.get("id")
    song = Song.objects.filter(song_id=song_id)[0]
    s_name = list()
    if song.song_sing_id.__contains__("#"):
        for s_one in song.song_sing_id.split("#"):
            if Sing.objects.filter(sing_id=s_one).exists():
                s_name.append(Sing.objects.filter(sing_id=s_one)[0].sing_name)
    else:
        s_name.append(Sing.objects.filter(sing_id=song.song_sing_id)[0].sing_name)
    song_lysic = SongLysic.objects.filter(song_id=song_id)[0]
    writeBrowse(user_name=request.GET.get("username"), click_id=song_id, click_cate="3", user_click_time=getLocalTime(),
                desc="查看歌曲")
    return JsonResponse({
        "code": 1,
        "data": [
            {
                "song_id": song.song_id,
                "song_name": song.song_name,
                "song_playlist": song.song_pl_id,
                "song_publish_time": song.song_publish_time,
                "song_sing": " / ".join(s_name),
                "song_total_comments": song.song_total_comments,
                "song_hot_comments": song.song_hot_comments,
                "song_url": song.song_url,
                "song_lysic": song_lysic.song_lysic,
                "song_rec": getRecBasedOne(song_id)
            }
        ]
    })


# 获取单首歌曲的推荐
def getRecBasedOne(song_id):
    result = list()
    songs = SongSim.objects.filter(song_id=song_id).order_by("-sim").values("sim_song_id")[:10]
    for song in songs:
        single = Song.objects.filter(song_id=song["sim_song_id"])[0]
        result.append({
            "id": single.song_id,
            "name": single.song_name,
            "publish_time": single.song_publish_time,
            "url": single.song_url,
            "cate": "3"
        })
    return result


# 获取搜索匹配的列表,默认返回30个
def search(request):
    name = request.GET.get("search")
    songs = Song.objects.all().filter(song_name__contains=name)[:30]
    song_list = list()
    for one in songs:
        # 前端使用el-autocomplete需要value字段且放置在前面
        song_list.append({
            "value": one.song_name,
            "id": one.song_id
        })
    return JsonResponse({
        "code": 1,
        "data": song_list
    })
