# -*- coding: utf-8 -*-
from django.contrib import admin

from playlist.models import PlayList, PlayListToSongs, PlayListToTag


class AdminPlaylist(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = (
        "pl_id", "pl_creator", "pl_name", "pl_tags", "pl_create_time", 'pl_update_time', "pl_songs_num", "pl_listen_num",
        "pl_share_num", "pl_comment_num", 'pl_follow_num',)
    # 添加search bar，在指定的字段中searc
    search_fields = (
        "pl_id", "pl_creator", "pl_name", "pl_tags" "pl_create_time", 'pl_update_time', "pl_songs_num", "pl_listen_num",
        "pl_share_num", "pl_comment_num", 'pl_follow_num',)
    # 排序
    ordering = ("-pl_create_time",)


admin.site.register(PlayList, AdminPlaylist)


class AdminPlaylistToSongs(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("pl_id", "song_id",)
    # 添加search bar，在指定的字段中searc
    search_fields = ("pl_id", "song_id",)
    # 页面右边会出现相应的过滤器选项
    # 排序
    ordering = ("-pl_id",)


admin.site.register(PlayListToSongs, AdminPlaylistToSongs)


class AdminPlaylistToTag(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("pl_id", "tag",)
    # 添加search bar，在指定的字段中searc
    search_fields = ("pl_id", "tag",)
    # 页面右边会出现相应的过滤器选项
    list_filter = ("tag",)
    # 排序
    ordering = ("-pl_id",)


admin.site.register(PlayListToTag, AdminPlaylistToTag)
