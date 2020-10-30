# -*- coding: utf-8 -*-
from django.contrib import admin

from song.models import Song, SongLysic, SongTag, SongSim


class AdminSong(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("song_id", "song_name", "song_pl_id", "song_publish_time", 'song_sing_id', "song_total_comments",
                    "song_hot_comments",)
    # 添加search bar，在指定的字段中search
    search_fields = ("song_id", "song_name", "song_pl_id", "song_publish_time", 'song_sing_id', "song_total_comments",
                     "song_hot_comments",)
    # 页面右边会出现相应的过滤器选项
    # 排序
    ordering = ("-song_publish_time",)


admin.site.register(Song, AdminSong)


class AdminSongLysic(admin.ModelAdmin):
    list_display = ("song_id", "song_lysic",)
    search_fields = ("song_id", "song_lysic",)
    ordering = ("-song_id",)


admin.site.register(SongLysic, AdminSongLysic)


class AdminSongTag(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("song_id", "tag",)
    # 添加search bar，在指定的字段中searc
    search_fields = ("song_id", "tag",)
    # 页面右边会出现相应的过滤器选项
    list_filter = ("tag",)
    # 排序
    ordering = ("-song_id",)


admin.site.register(SongTag, AdminSongTag)


class AdminSongSim(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("song_id", "sim_song_id", "sim",)
    # 添加search bar，在指定的字段中searc
    search_fields = ("song_id", "sim_song_id", "sim",)
    # 排序
    ordering = ("-song_id",)


admin.site.register(SongSim, AdminSongSim)
