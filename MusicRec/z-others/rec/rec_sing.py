# -*- coding: utf-8 -*-

"""
    Desc:
        基于物品的协同过滤推荐算法 ，给用户推荐歌手
    Step:
        1、得到用户和歌手的对应关系
        2、计算歌手与歌手相似度
        3、计算用户对歌手的喜欢程度
"""

import json
import math
import os


class RecSing:
    
    def __init__(self):
        self.playlist_mess_file = "../tomysql/newData/pl_mess_all.txt"  # 无重复
        self.playlist_song_mess_file = "../tomysql/newData/pl_sing_id.txt"  # 无重复
        self.song_mess_file = "../tomysql/newData/song_mess_all.txt"  # 有重复歌曲信息
        
        # 用户-歌手list，歌手list
        self.user_singer_dict, self.singer_list = self.load_data()
        # 歌手相似度
        self.sing_sim = self.ItemSimilarityBest()
        
        # 用户对歌手的评分 {user_id:{sing_id:score}}
        self.user_singer_score_dict = self.recommend_singer()
    
    # 加载数据
    def load_data(self):
        # 所有歌手
        singers_list = list()
        # 歌曲和歌手对应关系
        song_singer_dict = dict()
        for line in open(self.song_mess_file, "r", encoding="utf-8"):
            one_mess_list = line.strip().split(" |+| ")
            try:
                song_id, singer_id = one_mess_list[0], one_mess_list[4]
                song_singer_dict[song_id] = singer_id
                for i in singer_id.split("#"):
                    if i not in singers_list and i != "0":  # 网易云部分歌手格式为0表示此歌手不存在
                        singers_list.append(i)
            except Exception as e:
                print(e)
        # print(song_singer_dict)
        print("歌曲和歌手对应关系构建完成！")
        
        # 歌单(key)和歌手(list)对应关系
        playlist_singer_dict = dict()
        for line in open(self.playlist_song_mess_file, "r", encoding="utf-8"):
            # 歌单 \t 歌曲s
            playlist_id, song_ids = line.strip().split("\t")
            playlist_singer_dict.setdefault(playlist_id, list())
            for song_id in song_ids.split(","):
                try:
                    if song_singer_dict[song_id].__contains__("#"):
                        for singer_one in song_singer_dict[song_id].split("#"):
                            if singer_one == "0":
                                continue
                            playlist_singer_dict[playlist_id].append(singer_one)
                    else:
                        playlist_singer_dict[playlist_id].append(song_singer_dict[song_id])
                except Exception as e:
                    print("Error: {} ,{}".format(song_id, e))
        # print(playlist_sing_dict)
        print("歌单和歌手对应关系构建完成！")
        
        # 用户(key)和歌手{singer_id:count}对应关系
        # 用户创建歌单，歌单中的歌曲都是用户喜欢的，多个歌单中的多首歌，喜欢次数为count
        user_singer_dict = dict()
        for line in open(self.playlist_mess_file, "r", encoding="utf-8"):
            pl_mess_list = line.strip().split(" |=| ")
            playlist_id, user_id = pl_mess_list[0], pl_mess_list[1]
            user_singer_dict.setdefault(user_id, {})
            for singer_id in playlist_singer_dict[playlist_id]:
                user_singer_dict[user_id].setdefault(singer_id, 0)
                user_singer_dict[user_id][singer_id] += 1
        # print(user_singer_dict)
        print("用户和歌手对应信息统计完毕 ！")
        
        return user_singer_dict, singers_list
    
    # 计算歌手（物品）相似度
    def ItemSimilarityBest(self):
        item_sim = dict()
        if os.path.exists("newData/singer_sim_singer.json"):
            item_sim = json.load(open("newData/singer_sim_singer.json", "r", encoding="utf-8"))
            print("歌手相似从文件中加载")
            return item_sim
        item_user_count = dict()  # 物品-用户产生过行为
        count = dict()  # 共现矩阵 key:sing_id; value:{sing_id:count}
        for user, item in self.user_singer_dict.items():
            for i in item.keys():  # item {singer_id:count} i是用户喜欢的歌手id
                item_user_count.setdefault(i, 0)
                if self.user_singer_dict[user][i] > 0.0:
                    item_user_count[i] += 1  # 1代表喜欢
                for j in item.keys():
                    count.setdefault(i, {}).setdefault(j, 0)
                    if self.user_singer_dict[user][i] > 0.0 and self.user_singer_dict[user][j] > 0.0 and i != j:
                        count[i][j] += 1  # 同时喜欢歌手，且这个物品不相同
        # 共现矩阵 -> 相似度矩阵
        for i, related_items in count.items():
            item_sim.setdefault(i, dict())
            for j, cuv in related_items.items():  # cuv为共现矩阵中的值
                item_sim[i].setdefault(j, 0)
                # 余弦相似度 = 同时喜欢物品i和喜欢物品j的用户数/ 对i和对j有行为的两个数的积的开平方
                item_sim[i][j] = cuv / math.sqrt(item_user_count[i] * item_user_count[j])
        
        for key1, val1 in item_sim.items():
            for key2, val2 in val1.items():
                if item_sim[key1][key2] == 0:
                    del item_sim[key1][key2]
        json.dump(item_sim, open("newData/singer_sim_singer.json", "w", encoding="utf-8"))
        print("歌手相似计算完毕！")
        return item_sim
    
    # 为每个用户推荐歌手
    def recommend_singer(self):
        # 记录用户对歌手的评分
        user_singer_score_dict = dict()
        if os.path.exists("newData/user_singer_prefer.json"):
            user_singer_score_dict = json.load(open("newData/user_singer_prefer.json", "r", encoding="utf-8"))
            print("用户对歌手的偏好从文件加载完毕！")
            return user_singer_score_dict
        for user in self.user_singer_dict.keys():
            print(user)
            user_singer_score_dict.setdefault(user, {})
            # 遍历所有用户未评分歌手
            for singer in self.singer_list:
                if singer in self.user_singer_dict[user].keys():
                    continue
                score = 0.0
                for singer_sim in self.sing_sim[singer].keys():
                    if singer_sim == singer or singer_sim not in self.user_singer_dict[user].keys() \
                            or singer_sim not in self.sing_sim[singer].keys():
                        continue
                    score += self.sing_sim[singer][singer_sim] * self.user_singer_dict[user][singer_sim]
                user_singer_score_dict[user][singer] = score
        json.dump(user_singer_score_dict, open("newData/user_singer_prefer.json", "w", encoding="utf-8"))
        print("用户对歌手的偏好计算完成！")
        return user_singer_score_dict
    
    # 写入文件
    def write_to_file(self):
        fw = open("newData/user_singer_prefer.txt", "w", encoding="utf-8")
        for user_id in self.user_singer_score_dict.keys():
            sort_user_singer_prefer = sorted(self.user_singer_score_dict[user_id].items(),
                                             key=lambda x: x[1], reverse=True)
            for i in sort_user_singer_prefer[:100]:
                fw.write(user_id + "," + i[0] + "," + str(i[1]) + "\n")
        fw.close()
        print("写入文件完成！")


if __name__ == "__main__":
    rec_sing = RecSing()
    rec_sing.write_to_file()
