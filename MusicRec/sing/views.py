# -*- coding:utf-8 -*-
from django.core.cache import cache
from django.http import JsonResponse

from sing.models import Sing, SingTag, SingSim, SingSong
from song.models import Song
from user.views import writeBrowse, getLocalTime


def all(request):
    # 接口传入的tag参数
    tag = request.GET.get("tag")
    # 接口传入的page参数
    _page_id = int(request.GET.get("page"))
    _pagesize = int(request.GET.get('pagesize'))
    print("Tag : %s, page_id: %s" % (tag, _page_id))
    _list = list()
    # 全部歌手
    if tag == "all":
        cache_sing_tags_list = cache.get('sing_tags_list', 'NOT_EXISTS')
        if cache_sing_tags_list == 'NOT_EXISTS':
            sing_tags_list = Sing.objects.all().values("sing_id", "sing_name", "sing_url").order_by("-sing_id")
            cache.add('sing_tags_list', sing_tags_list, 24*60*60)
        else:
            sing_tags_list = cache_sing_tags_list
        # 拼接歌曲信息
        for one in sing_tags_list[(_page_id - 1) * _pagesize:_page_id * _pagesize]:
            _list.append({
                "sing_id": one["sing_id"],
                "sing_name": one["sing_name"],
                "sing_url": one["sing_url"]
            })
    # 指定标签下的歌手
    else:
        sing_tags_list = SingTag.objects.filter(tag=tag).values("sing_id").order_by("sing_id")
        sing_ids = [s_one["sing_id"] for s_one in sing_tags_list[(_page_id - 1) * _pagesize:_page_id * _pagesize]]
        sings_list = Sing.objects.filter(sing_id__in=sing_ids).values("sing_id", "sing_name", "sing_url")
        for one in sings_list:
            _list.append({
                "sing_id": one["sing_id"],
                "sing_name": one["sing_name"],
                "sing_url": one["sing_url"]
            })
    total = sing_tags_list.__len__()
    return {"code": 1,
            "data": {
                "total": total,
                "sings": _list,
                "tags": getAllSingTags()
            }
            }


# 获取所有歌手标签
def getAllSingTags():
    tags = set()
    cache_sing_tags = cache.get('sing_tags', 'NOT_EXISTS')
    if cache_sing_tags == 'NOT_EXISTS':
        sing_tags = SingTag.objects.all().values("tag").distinct().order_by("sing_id")
        for one in sing_tags:
            tags.add(one["tag"])
        cache.add('sing_tags', tags)
    else:
        tags = cache_sing_tags
    return list(tags)


def one(request):
    sing_id = request.GET.get("id")
    writeBrowse(user_name=request.GET.get("username"), click_id=sing_id, click_cate="4", user_click_time=getLocalTime(),
                desc="查看歌手")
    one = Sing.objects.filter(sing_id=sing_id)[0]
    return JsonResponse({
        "code": 1,
        "data": [
            {
                "sing_id": one.sing_id,
                "sing_name": one.sing_name,
                "sing_music_num": one.sing_music_num,
                "sing_mv_num": one.sing_mv_num,
                "sing_album_num": one.sing_album_num,
                "sing_url": one.sing_url,
                "sing_rec": getRecBasedOne(sing_id),
                "sing_songs": getSingerSong(sing_id)
            }
        ]
    })


# 获取单个歌手的推荐
def getRecBasedOne(sing_id):
    result = list()
    sings = SingSim.objects.filter(sing_id=sing_id).order_by("-sim").values("sim_sing_id")[:10]
    for sing in sings:
        one = Sing.objects.filter(sing_id=sing["sim_sing_id"])[0]
        result.append({
            "id": one.sing_id,
            "name": one.sing_name,
            "img_url": one.sing_url,
            "cate": "4"
        })
    return result


# 获取单个歌手的歌曲
def getSingerSong(sid):
    result = list()
    query_set = SingSong.objects.filter(sing_id=sid)
    for one in query_set:
        for song in Song.objects.filter(song_id=one.song_id):
            result.append({
                "song_id": song.song_id,
                "song_name": song.song_name,
                "song_publish_time": song.song_publish_time,
            })
    return result


# 获取搜索匹配的列表,默认返回前30个
def search(request):
    # print(request.GET)
    name = request.GET.get("search")
    sings = Sing.objects.all().filter(sing_name__contains=name)[:30]
    sing_list = list()
    for one in sings:
        # 前端使用el-autocomplete需要value字段且放置在前面
        sing_list.append({
            "value": one.sing_name,
            "id": one.sing_id
        })
    return JsonResponse({
        "code": 1,
        "data": sing_list
    })
