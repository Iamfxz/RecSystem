# -*- coding:utf-8 -*-
"""
    Desc:
        基于标签计算歌曲相似度（jaccard）
"""
import json
import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'MusicRec.settings'
django.setup()


class SongSim:
    def __init__(self):
        # 歌曲id-标签set
        self.songTags = self.getSongTags()
        # print("总共:", self.songTags.keys().__len__()) # 114973
        # print(self.songTags)
        self.sim = self.getSongSim()
        # print(self.sim)
    
    @staticmethod
    # 应当提前利用注释里的代码删除tag中的空白，数据库同样处理
    def getSongTags():
        song_tags_dict = dict()
        # fw = open("newData/song_tag2.txt", "w", encoding="utf-8")
        for line in open("newData/song_tag.txt", "r", encoding="utf-8"):
            song_id, tag = line.strip().split(",")
            # if tag == '':
            #     continue
            # fw.write(line)
            song_tags_dict.setdefault(song_id, set())
            song_tags_dict[song_id].add(tag)
        # fw.close()
        return song_tags_dict
    
    # 耗时6h
    def getSongSim(self):
        sim = dict()
        if os.path.exists("newData/song_sim.json"):
            sim = json.load(open("newData/song_sim.json", "r", encoding="utf-8"))
        else:
            i = 0
            print("总共:", self.songTags.keys().__len__())
            for song1 in self.songTags.keys():
                sim[song1] = dict()
                for song2 in self.songTags.keys():
                    if song1 != song2:
                        j_len = len(self.songTags[song1] & self.songTags[song2])
                        if j_len != 0:
                            result = j_len / len(self.songTags[song1] | self.songTags[song2])
                            if sim[song1].__len__() < 20:
                                sim[song1][song2] = result
                            elif result > 0.8:
                                # 找到最小值 删除,并加入更大的值
                                minkey = min(sim[song1], key=sim[song1].get)
                                if result > sim[song1][minkey]:
                                    sim[song1][song2] = result
                                    # print(str(result) + '>' + str(sim[sing1][minkey]))
                                    # print("删除" + str(sim[sing1][minkey]))
                                    del sim[song1][minkey]
                i += 1
                print(str(i) + "\t" + song1)
            json.dump(sim, open("newData/song_sim.json", "w", encoding="utf-8"))
        print("歌曲相似度计算完毕！")
        return sim
    
    def transform(self):
        fw = open("newData/song_sim.txt", "w", encoding="utf-8")
        for s1 in self.sim.keys():
            for s2 in self.sim[s1].keys():
                fw.write(s1 + "," + s2 + "," + str(self.sim[s1][s2]) + "\n")
        fw.close()
        print("Over!")


if __name__ == "__main__":
    song = SongSim()
    song.transform()
