# -*- coding: utf-8 -*-
import time

from django.http import JsonResponse

from playlist.models import PlayList
from user.models import User, UserBrowse, UserTag, UserSim
from user.rsaUtil import decrypt


def all(request):
    # 接口传入的tag参数
    tag = request.GET.get("tag")
    # 接口传入的page参数
    _page_id = int(request.GET.get("page"))
    _pagesize = int(request.GET.get("pagesize"))
    print("Tag : %s, page_id: %s" % (tag, _page_id))
    _list = list()
    # 全部用户
    if tag == "all":
        s_lists = User.objects.all().order_by("-u_id")
        # 拼接用户信息
        for one in s_lists[(_page_id - 1) * _pagesize:_page_id * _pagesize]:
            _list.append({
                "u_id": one.u_id,
                "u_name": one.u_name,
                "u_img_url": one.u_img_url
            })
    # 指定标签下的用户
    else:
        s_lists = UserTag.objects.filter(tag=tag).values("user_id").order_by("user_id").distinct()
        for sid in s_lists[(_page_id - 1) * _pagesize:_page_id * _pagesize]:
            one = User.objects.filter(u_id=sid["user_id"])
            if one.__len__() == 1:
                one = one[0]
            else:
                continue
            _list.append({
                "u_id": one.u_id,
                "u_name": one.u_name,
                "u_img_url": one.u_img_url
            })
    total = s_lists.__len__()
    return {"code": 1,
            "data": {
                "total": total,
                "sings": _list,
                "tags": getAllUserTags()
            }
            }


# 获取所有用户标签
def getAllUserTags():
    tags = set()
    for one in UserTag.objects.all().values("tag").distinct().order_by("user_id"):
        tags.add(one["tag"])
    return list(tags)


def one(request):
    u_id = request.GET.get("id")
    one = User.objects.filter(u_id=u_id)[0]
    writeBrowse(user_name=request.GET.get("username"), click_id=u_id, click_cate="5", user_click_time=getLocalTime(),
                desc="查看用户")
    return JsonResponse({
        "code": 1,
        "data": [
            {
                "u_id": one.u_id,
                "u_name": one.u_name,
                "u_birthday": one.u_birthday,
                "u_gender": one.u_gender,
                "u_province": one.u_province,
                "u_city": one.u_city,
                "u_tags": one.u_tags,
                "u_img_url": one.u_img_url,
                "u_sign": one.u_sign,
                "u_rec": getRecBasedOne(u_id),
                "u_playlist": getUserCreatePL(u_id)
            }
        ]
    })


# 获取单个用户的推荐
def getRecBasedOne(u_id):
    result = list()
    sim_users = UserSim.objects.filter(user_id=u_id).order_by("-sim").values("sim_user_id")[:10]
    for user in sim_users:
        one = User.objects.filter(u_id=user["sim_user_id"])[0]
        result.append({
            "id": one.u_id,
            "name": one.u_name,
            "img_url": one.u_img_url,
            "cate": "5"
        })
    return result


# 获取用户创建的歌单
def getUserCreatePL(uid):
    pls = PlayList.objects.filter(pl_creator__u_id=uid)
    result = list()
    for one in pls:
        result.append(
            {
                "pl_id": one.pl_id,
                "pl_name": one.pl_name,
                "pl_creator": one.pl_creator.u_name,
                "pl_create_time": one.pl_create_time,
                "pl_img_url": one.pl_img_url,
                "pl_desc": one.pl_desc
            }
        )
    return result


# 获取搜索匹配的列表,默认返回30个
def search(request):
    name = request.GET.get("search")
    users = User.objects.all().filter(u_name__contains=name)[:30]
    user_list = list()
    for one in users:
        # 前端使用el-autocomplete需要value字段且放置在前面
        user_list.append({
            "value": one.u_name,
            "id": one.u_id
        })
    return JsonResponse({
        "code": 1,
        "data": user_list
    })


def valid(user_name, cipher_text):
    """
        验证账号及密码是否 匹配或存在
    :param user_name: 用户名字，也是账号
    :param cipher_text: 用户密码，前端公钥加密
    :return:
    """
    users = User.objects.filter(u_name=user_name)
    if users.exists():
        user = users[0]
        if decrypt(user.u_password) == decrypt(cipher_text):
            return 200
        else:  # 密码错误
            return 203
    else:  # 用户不存在
        return 202


# 用户浏览信息进行记录
"""
    user_name = models.CharField(blank=False, max_length=64, verbose_name="用户名")
    click_id = models.CharField(blank=False, max_length=64, verbose_name="ID")
    click_cate = models.CharField(blank=False, max_length=64, verbose_name="类别")
    user_click_time = models.DateTimeField(blank=False, verbose_name="浏览时间")
    desc = models.CharField(blank=False, max_length=1000, verbose_name="备注",default="Are you ready!")
"""


def writeBrowse(user_name="", click_id="", click_cate="", user_click_time="", desc=""):
    UserBrowse(user_name=user_name,
               click_id=click_id,
               click_cate=click_cate,
               user_click_time=user_click_time,
               desc=desc).save()
    print("用户【 %s 】的行为记录【 %s 】写入数据库" % (user_name, desc))


# 获取当前格式化的系统时间
def getLocalTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
