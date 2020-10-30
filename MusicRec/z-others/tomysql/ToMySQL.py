# -*- coding: utf-8 -*-
"""
    Author: Thinkgamer
    Desc:
        代码12-3  把数据写入数据库
"""
import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = "MusicRec.settings"
django.setup()
"""
 上边import 解决错误：
 django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS, but settings are not 
 django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
"""

import pymysql
import json
from MusicRec.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWD, DB_NAME
from playlist.models import PlayListToSongs, PlayListToTag, PlayList
from song.models import SongLysic, Song, SongTag
from user.models import User, UserTag
from sing.models import Sing, SingTag, SingSim, SingSong
from datetime import datetime
from django.utils import timezone


class ToMySQL:
    def __init__(self):
        self.db = self.__connect()
        self.cursor = self.db.cursor()
    
    # 连接mysql数据库
    @staticmethod
    def __connect():
        db = pymysql.Connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT, charset='utf8')
        return db
    
    # 将歌曲信息写入数据库 OK
    """
        song_id = models.CharField(blank=False, max_length=64, verbose_name="歌曲ID", unique=True)
        song_name = models.CharField(blank=False, max_length=100, verbose_name="歌曲名字")
        song_pl_id = models.CharField(blank=False, max_length=64, verbose_name="专辑ID")
        song_publish_time = models.DateTimeField(blank=True, verbose_name="出版时间")
        song_sing_id = models.CharField(blank=False, max_length=100, verbose_name="歌手ID")
        song_total_comments = models.IntegerField(blank=True,verbose_name="歌曲总的评论数")
        song_hot_comments = models.IntegerField(blank=True,verbose_name="歌曲热门评论数")
        song_url = models.CharField(blank=True, max_length=1000, verbose_name="歌曲链接")
    """
    
    def SongMessToMySQL(self):
        for line in open("newData/song_mess_all.txt", "r", encoding="utf-8"):
            _list = line.split(" |+| ")
            if _list.__len__() == 9:
                song_id, song_name, song_pl_id, song_publish_time, song_sing_id, song_total_comments, \
                song_hot_comments, size, song_url = line.split(" |+| ")
                s = Song(
                    song_id=song_id,
                    song_name=song_name,
                    song_pl_id=song_pl_id,
                    song_publish_time=self.TransFormTime(int(song_publish_time) / 1000),
                    song_sing_id=song_sing_id,
                    song_total_comments=song_total_comments,
                    song_hot_comments=song_hot_comments,
                    song_url=song_url
                )
                try:
                    s.save()
                except Exception as e:
                    # 发现重复的歌曲的时候，直接跳过
                    if e.args[0] == 1062:
                        continue
                    print(e)
                    print(song_id)
                    pass
            else:
                print(line)
        print("Over!")
    
    # 歌词信息写入数据库 ok
    """
        song_id = models.CharField(blank=False, max_length=64, verbose_name="歌曲ID", unique=True)
        song_lysic = models.TextField(blank=True, verbose_name="歌词")
    """
    
    @staticmethod
    def SongLysicToMySQL():
        i = 0
        for line in open("newData/song_lyric_mess_all.txt", "r", encoding="utf-8"):
            _list = line.strip().split("\t")
            if _list.__len__() > 1:
                song_id = _list[0]
                lyric = _list[1]
                if lyric == "null":
                    lyric = "暂无歌词提供！"
            else:
                song_id = _list[0]
                lyric = "暂无歌词提供！"
            try:
                SongLysic(song_id=song_id, song_lysic=lyric).save()
                i += 1
                print(i)
            except Exception as e:
                if e.args[0] == 1062:
                    # 更新歌曲的歌词(有一部分歌曲是重复的)
                    SongLysic.objects.filter(song_id=song_id).update(song_lysic=lyric)
                    print(str(i) + "更新歌词，id:" + song_id)
                else:
                    print("Error: {} ,{}".format(song_id, e))
        print("歌词信息写入数据库完成！")
    
    # 歌手信息写入数据库 ok
    """
        sing_id = models.CharField(blank=False, max_length=64, verbose_name="歌手ID", unique=True)
        sing_name = models.CharField(blank=False, max_length=100, verbose_name="歌手名字")
        sing_music_num = models.IntegerField(blank=False, verbose_name="音乐数目")
        sing_mv_num = models.IntegerField(blank=False, verbose_name="MV数目")
        sing_album_num = models.IntegerField(blank=False, verbose_name="专辑数目")
        sing_url = models.CharField(blank=True, max_length=1000, verbose_name="歌手图片")
    """
    
    def SingMessToMySQL(self):
        have_write_sing = list()
        i = 0
        for line in open("newData/sing_mess_all.txt", "r", encoding="utf-8"):
            _list = line.strip().split(",")
            if _list[0] in have_write_sing:
                continue
            if _list.__len__() == 6:
                sing_id, sing_name, sing_music_num, sing_mv_num, sing_album_num, sing_url = line.strip().split(",")
                s = Sing(
                    sing_id=sing_id,
                    sing_name=sing_name,
                    sing_music_num=sing_music_num,
                    sing_mv_num=sing_mv_num,
                    sing_album_num=sing_album_num,
                    sing_url=sing_url
                )
                try:
                    s.save()
                except Exception as e:
                    print(e)
                    print(sing_id)
                    pass
                have_write_sing.append(sing_id)
            # 歌手名字中带有逗号‘，’
            elif _list.__len__() == 7:
                sing_id, sing_name1, sing_name2, sing_music_num, sing_mv_num, sing_album_num, sing_url \
                    = line.strip().split(",")
                s = Sing(
                    sing_id=sing_id,
                    sing_name=sing_name1 + "," + sing_name2,
                    sing_music_num=sing_music_num,
                    sing_mv_num=sing_mv_num,
                    sing_album_num=sing_album_num,
                    sing_url=sing_url
                )
                try:
                    s.save()
                except Exception as e:
                    print(e)
                    print(sing_id)
                    pass
                have_write_sing.append(sing_id)
            else:
                print(_list)
                print(_list.__len__())
                print('名字中带有逗号较多的数据可手动插入数据库，默认不插入')
        print("Over!")
    
    # 用户信息写入数据库 ok
    """
        u_id = models.CharField(blank=False, max_length=64, verbose_name="用户ID", unique=True)
        u_name = models.CharField(blank=False, max_length=150, verbose_name="用户昵称")
        u_birthday = models.DateField(blank=True, verbose_name="生日")
        u_gender = models.IntegerField(blank=True,verbose_name="用户性别")
        u_province = models.CharField(blank=True, max_length=20, verbose_name="用户省份")
        u_city = models.CharField(blank=True, max_length=20, verbose_name="用户城市")
        u_type = models.CharField(blank=True, max_length=10, verbose_name="用户类型")
        u_tags = models.CharField(blank=True, max_length=1000, verbose_name="用户标签")
        u_img_url = models.CharField(blank=True, max_length=1000, verbose_name="头像链接")
        u_auth_status = models.CharField(blank=True, max_length=10, verbose_name="用户状态")
        u_account_status = models.CharField(blank=True, max_length=10, verbose_name="账号状态")
        u_dj_status = models.CharField(blank=True, max_length=10, verbose_name="DJ状态")
        u_vip_type = models.CharField(blank=True, max_length=10, verbose_name="VIP状态")
        u_sign = models.TextField(blank=True, verbose_name="用户签名")
    """
    
    def userMessToMySQL(self):
        i = 0
        uid_list = list()
        for line in open("newData/user_mess_all.txt", "r", encoding="utf-8").readlines():
            if line.split(" |=| ").__len__() < 14:
                continue
            u_id, u_name, u_birthday, u_gender, u_province, u_city, u_type, u_tags, u_img_url, u_auth_status, \
            u_account_status, u_dj_status, u_vip_type, u_sign = line.split(" |=| ")
            # print(u_id, u_name, u_birthday, u_gender, u_province, u_city, u_type, u_tags, u_img_url, u_auth_status,
            #       u_account_status, u_dj_status, u_vip_type, u_sign)
            if u_id in uid_list:
                continue
            else:
                uid_list.append(u_id)
            user = User(
                u_id=u_id,
                u_name=u_name,
                u_birthday=self.TransFormTime(float(int(u_birthday) / 1000)),
                u_gender=int(u_gender),
                u_province=u_province,
                u_city=u_city,
                u_type=u_type,
                u_tags=u_tags.replace("[", "").replace("]", ""),
                u_img_url=u_img_url,
                u_auth_status=u_auth_status,
                u_account_status=u_account_status,
                u_dj_status=u_dj_status,
                u_vip_type=u_vip_type,
                u_sign='秘密' if u_sign == "\n" else u_sign
            )
            try:
                user.save()
                i += 1
                print(i)
            except Exception as e:
                i += 1
                print(i)
                print("Error: {} ,{}".format(u_id, e))
                # 字符集编码错误，u_sign中有表情包等（尚未解决，故强制更改）
                if e.args[0] == 1366:
                    print('强制插入')
                    user.u_sign = '秘密'
                    user.save()
    
    # 歌单信息写入数据库  ok
    """
        pl_id = models.CharField(blank=False, max_length=64, verbose_name="ID", unique=True)
        pl_creator = models.ForeignKey(User, related_name="创建者信息", on_delete=models.DO_NOTHING)
        pl_name = models.CharField(blank=False, max_length=64, verbose_name="歌单名字")
        pl_create_time = models.DateTimeField(blank=True, verbose_name="创建时间")
        pl_update_time = models.DateTimeField(blank=True, verbose_name="更新时间")
        pl_songs_num = models.IntegerField(blank=True,verbose_name="包含音乐数")
        pl_listen_num = models.IntegerField(blank=True,verbose_name="播放次数")
        pl_share_num = models.IntegerField(blank=True,verbose_name="分享次数")
        pl_comment_num = models.IntegerField(blank=True,verbose_name="评论次数")
        pl_follow_num = models.IntegerField(blank=True,verbose_name="收藏次数")
        pl_tags = models.CharField(blank=True, max_length=1000, verbose_name="歌单标签")
        pl_img_url = models.CharField(blank=True, max_length=1000, verbose_name="歌单封面")
        pl_desc = models.TextField(blank=True, verbose_name="歌单描述")
    """
    
    def playListMessToMysql(self):
        i = 0
        for line in open("newData/pl_mess_all.txt", "r", encoding="utf-8"):
            pl_id, pl_creator, pl_name, pl_create_time, pl_update_time, pl_songs_num, pl_listen_num, \
            pl_share_num, pl_comment_num, pl_follow_num, pl_tags, pl_img_url, pl_desc = line.split(" |=| ")
            try:
                user = User.objects.filter(u_id=pl_creator)[0]
            except Exception as e:
                print(e)
                user = User.objects.filter(u_id=pl_creator)[0]
            pl = PlayList(
                pl_id=pl_id,
                pl_creator=user,
                pl_name=pl_name,
                pl_create_time=self.TransFormTime(int(pl_create_time) / 1000),
                pl_update_time=self.TransFormTime(int(pl_update_time) / 1000),
                pl_songs_num=int(pl_songs_num),
                pl_listen_num=int(pl_listen_num),
                pl_share_num=int(pl_share_num),
                pl_comment_num=int(pl_comment_num),
                pl_follow_num=int(pl_follow_num),
                pl_tags=str(pl_tags).replace("[", "").replace("]", "").replace("\'", ""),
                pl_img_url=pl_img_url,
                pl_desc=pl_desc
            )
            pl.save()
            i += 1
            print(i)
    
    # 歌单和歌曲（此处用sing）的id对应信息写入数据库 ok
    """
        pl_id = models.ForeignKey(PlayList, related_name="歌单ID", on_delete=models.DO_NOTHING)
        song_id = models.ForeignKey(Song, related_name="歌曲ID", on_delete=models.DO_NOTHING)
    """
    
    def playListSingMessToMySQL(self):
        i = 0
        for line in open("newData/pl_sing_id.txt", "r", encoding="utf-8"):
            pid, sids = line.strip().split("\t")
            for sid in str(sids).split(","):
                try:
                    pls = PlayListToSongs(pl_id=pid, song_id=sid)
                    pls.save()
                    i += 1
                    print(i)
                except Exception as e:
                    print(e, pid, sid)
        print("歌单和歌曲ID对应信息写完毕！")
    
    # 歌单和歌单tag写入数据库  ok
    def playListTagMessToMySQL(self):
        i = 0
        for line in open("newData/pl_mess_all.txt", "r", encoding="utf-8"):
            _list = line.split(" |=| ")
            pl_id = _list[0]
            tags = _list[10].replace("[", "").replace("]", "")
            tag_list = tags.split(",")
            if tag_list.__len__() > 1:
                for tag in tag_list:
                    PlayListToTag(pl_id=pl_id, tag=tag.replace("\'", "").replace(" ", "")).save()
                i += 1
                print(i)
            else:
                PlayListToTag(pl_id=pl_id, tag=tags.replace("\'", "").replace(" ", "")).save()
                i += 1
                print(i)
        print("Over !")
    
    # 歌手-标签、歌曲-标签 写入数据库 和 写入文件
    @staticmethod
    def SingAndTagMessToMySQL():
        # 1、歌手id(key) -> 歌曲id(list)；
        sing_song_dict = dict()
        for sing in Sing.objects.all().values('sing_id'):
            sing_song_dict.setdefault(sing['sing_id'], list())
        for one in Song.objects.all().values("song_id", "song_sing_id"):
            if "#" in one["song_sing_id"]:
                for sing_id in one["song_sing_id"].split("#"):
                    if sing_id not in sing_song_dict:
                        sing_song_dict.setdefault(sing_id, list())
                    sing_song_dict[sing_id].append(one["song_id"])
            else:
                if one["song_sing_id"] not in sing_song_dict:
                    sing_song_dict.setdefault(one["song_sing_id"], list())
                sing_song_dict[one["song_sing_id"]].append(one["song_id"])
        print(sing_song_dict)
        json.dump(sing_song_dict, open("sing_song.json", "w", encoding="utf-8"))
        # 旧方法,存在bug,一个歌手只有一首歌
        # sing_song_dict = dict()
        # if os.path.exists("newData/sing_song.json"):
        #     sing_song_dict = json.load(open("newData/sing_song.json", "r", encoding="utf-8"))
        # else:
        #     for one in Song.objects.all().values("song_id", "song_sing_id"):
        #         if "#" in one["song_sing_id"]:
        #             for sing in one["song_sing_id"].split("#"):
        #                 sing_song_dict[sing] = one["song_id"]
        #         else:
        #             sing_song_dict[one["song_sing_id"]] = one["song_id"]
        #     json.dump(sing_song_dict, open("newData/sing_song.json", "w", encoding="utf-8"))
        
        # 2、歌曲id(key) -> 歌单 -> 标签(value)；生成 歌曲-标签 的对应文件
        song_playlist_tag_dict = dict()
        if os.path.exists("newData/song_tag.json"):
            song_playlist_tag_dict = json.load(open("newData/song_tag.json", "r", encoding="utf-8"))
        else:
            for one in PlayListToSongs.objects.all():
                pl_tags = PlayList.objects.filter(pl_id=one.pl_id).values("pl_tags")
                if one.song_id in song_playlist_tag_dict.keys():
                    song_playlist_tag_dict[one.song_id] += ", " + pl_tags[0]["pl_tags"]
                else:
                    song_playlist_tag_dict[one.song_id] = pl_tags[0]["pl_tags"]
            json.dump(song_playlist_tag_dict, open("newData/song_tag.json", "w", encoding="utf-8"))
        # print(song_playlist_tag_dict)
        
        # 3. 将歌曲 -> 标签 写入 数据库 和 文件 ；较为耗时（完成）
        fw = open("newData/song_tag.txt", "w", encoding="utf-8")
        for song in song_playlist_tag_dict.keys():
            # print(song)
            song_have_write = list()
            for tag in song_playlist_tag_dict[song].split(","):
                tag = tag.replace(" ", "")
                if tag not in song_have_write:
                    # 写入文件
                    fw.write(song + "," + tag + "\n")
                    song_have_write.append(tag)
                # 写入数据库
                SongTag(song_id=song, tag=tag.replace(" ", "")).save()
        fw.close()
        print("歌曲-标签 写入 Over !")
        
        # 已被步骤3合并 4. 将歌曲 -> 标签 写入 新建文件 song_tag.txt 用于后面相似度计算
        # fw = open("./newData/song_tag.txt", "w", encoding="utf-8")
        # for song in song_playlist_tag_dict.keys():
        #     # print(song)
        #     song_have_write = list()
        #     for tag in song_playlist_tag_dict[song].split(","):
        #         tag = tag.replace(" ", "")
        #         if tag not in song_have_write:
        #             fw.write(song + "," + tag + "\n")
        #             song_have_write.append(tag)
        # fw.close()
        # print("歌曲-标签 写入文件 Over !")
        
        # 5. 将歌手 -> 标签；写入数据库 写入文件
        fw1 = open("newData/sing_tag.txt", "w", encoding="utf-8")
        for sing in sing_song_dict.keys():
            # print(sing)
            songId = sing_song_dict[sing]
            sing_have_write = list()
            for tag in song_playlist_tag_dict[songId].split(","):
                tag = tag.replace(" ", "")
                if tag not in sing_have_write:
                    # 写入文件
                    fw1.write(sing + "," + tag + "\n")
                    sing_have_write.append(tag)
                # 写入数据库
                SingTag(sing_id=sing, tag=tag).save()
        fw1.close()
        print("歌手-标签 写入 Over !")
        
        # 已被步骤5合并 6.将歌曲-标签；写入 新建文件 sing_tag.txt 用于后面相似度计算
        # fw1 = open("./newData/sing_tag.txt", "w", encoding="utf-8")
        # for sing in sing_song_dict.keys():
        #     # print(sing)
        #     songId = sing_song_dict[sing]
        #     sing_have_write = list()
        #     for tag in song_playlist_tag_dict[songId].split(","):
        #         tag = tag.replace(" ", "")
        #         if tag not in sing_have_write:
        #             fw1.write(sing + "," + tag + "\n")
        #             sing_have_write.append(tag)
        # fw1.close()
        # print("歌手-标签 写入文件 Over !")
    
    # 将用户 -> 标签写入数据库
    @staticmethod
    def UserTagMessToMySQL():
        i = 0
        for one in PlayList.objects.all():
            i += 1
            print(str(i) + ":" + str(one))
            for tag in one.pl_tags.split(","):
                UserTag(user_id=one.pl_creator.u_id, tag=tag.replace(" ", "")).save()
        print("Over !")
    
    # 太慢了，可以直接用navicat导入数据各个sim表格
    @staticmethod
    def singSimToMySQL():
        i = 0
        fw = open("../tools/newData/sing_sim.txt", 'r', encoding='utf-8')
        for line in fw:
            sing_id, sim_sing_id, sim = line.strip().split(",")
            try:
                SingSim(sing_id=sing_id, sim_sing_id=sim_sing_id, sim=sim).save()
                i += 1
            except Exception as e:
                print(e)
        
        print("总共存入singsim表%d个数据" % i)
        fw.close()
    
    # 13位时间戳转换为时间
    @staticmethod
    def TransFormTime(t1):
        try:
            dt = datetime.fromtimestamp(t1, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print("%s, %s " % (t1, e))
            dt = datetime.fromtimestamp(0, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        return dt
    
    #
    # # 修改部分歌词格式错误例如以\n开头
    # def Fix(self):
    #     fw = open('./newData/song_lyric_mess_all.txt', "a", encoding="utf-8")
    #     for line in open("./newData/song_lyric_mess_all(wrong).txt", "r", encoding="utf-8"):
    #         _list = line.strip().split("\t")
    #         if _list[0].startswith('\\n'):
    #             fw.writelines(line.strip())
    #             continue
    #         else:
    #             fw.writelines('\n' + line.strip())
    #     fw.close()
    @staticmethod
    def singSongToMySQL():
        if os.path.exists("sing_song.json"):
            sing_song_dict = json.load(open("sing_song.json", "r", encoding="utf-8"))
            # print(sing_song_dict)
            for sing, song_list in sing_song_dict.items():
                # print(sing)
                for song in song_list:
                    try:
                        # print(sing, song)
                        SingSong(sing_id=sing, song_id=song).save()
                    except Exception as e:
                        print(e)
        else:
            print("先生成sing_song.json文件")


if __name__ == "__main__":
    tomysql = ToMySQL()
    # 可分开逐个运行
    # tomysql.userMessToMySQL()  # 2
    # tomysql.playListMessToMysql() # 2
    # tomysql.SingMessToMySQL()  # 2
    # tomysql.SongMessToMySQL()  # 2
    # tomysql.playListSingMessToMySQL()  # 2
    # tomysql.SongLysicToMySQL()  # 2
    # tomysql.playListTagMessToMySQL() # 2
    # tomysql.SingAndTagMessToMySQL()  # 2
    # tomysql.UserTagMessToMySQL()  # 2
    # tomysql.singSimToMySQL() # 2 后续未添加的表格通过navicat导入
    # tomysql.singSongToMySQL()
    # tomysql.singSongToMySQL()
    QuerySet = SingSong.objects.filter(sing_id=100210)
    for one in QuerySet:
        print(one.song_id)
        for song in Song.objects.filter(song_id=one.song_id):
            print(song.song_name)
