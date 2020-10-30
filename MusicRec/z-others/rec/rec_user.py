# -*- coding: utf-8 -*-

"""
        基于用户的协同过滤算法 给用户推荐用户
"""
import math


class RecUser:
    def __init__(self):
        self.file = "../tomysql/newData/pl_mess_all.txt"
        
        self.total_user = 0 # 用户总数
        self.user_tags_count_dict = dict()  # 用户对标签的次数统计
        self.load_data()

        self.tags_users = dict()
        self.avg_r_u = dict()   # avg_r_u[tag]:所有用户对于tag的平均分
        self.C = dict()  # 相似度的分子部分，C[U][V]:用户u和v的交集经过计算连加的评分
        self.N = dict()  # 对
        self.W = dict()  # 相似度矩阵
        self.UserSimilarityBest()
    
    # 加载数据
    def load_data(self):
        for line in open(self.file, "r", encoding="utf-8"):
            pl_mess_list = line.strip().split(" |=| ")
            playlist_id, user_id, tags = (
                pl_mess_list[0],
                pl_mess_list[1],
                str(pl_mess_list[10]).replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
            )
            self.total_user += 1
            # print(playlist_id, user_id, tags)
            self.user_tags_count_dict.setdefault(user_id, {})
            for tag in tags.split(","):
                if tag is not '':   # 数据预处理上的空值问题，部分歌单标签为空
                    self.user_tags_count_dict[user_id].setdefault(tag, 0)
                    self.user_tags_count_dict[user_id][tag] += 1
        print("用户打标签统计完成 ！")
    
    # 计算用户之间的相似度
    def UserSimilarityBest(self):
        """
        计算用户之间的相似度，采用惩罚热门商品和优化算法复杂度的算法
        :return: dict
        """
        # 构建倒排表tags_users
        for user_id, tags in self.user_tags_count_dict.items():
            for tag in tags.keys():
                self.tags_users.setdefault(tag, set())
                if self.user_tags_count_dict[user_id][tag] > 0:
                    self.tags_users[tag].add(user_id)
        # 构建N(i)--对i有行为的数量，这里i为用户
        # 构建C--相似度分子，用户u和v并集的计算后的数值
        for tags, users in self.tags_users.items():     # 含有共同标签的用户
            self.avg_r_u[tags] = len(users)/self.total_user
            for u in users:
                self.N.setdefault(u, 0)
                self.N[u] += 1
                self.C.setdefault(u, {})
                for v in users:
                    self.C[u].setdefault(v, 0)
                    if u == v:
                        continue
                    # 惩罚热门商品 todo 减去平均分
                    self.C[u][v] += 1 / math.log(1 + len(users) - self.avg_r_u[tags])
        # 构建相似度矩阵W
        for u, related_users in self.C.items():
            self.W.setdefault(u, {})
            for v, cuv in related_users.items():
                if u == v:
                    continue
                self.W[u].setdefault(v, 0.0)
                self.W[u][v] = cuv / math.sqrt(self.N[u] * self.N[v])
    
    # 保存每个用户最相似的20个用户在文件中
    def write_to_file(self):
        fw = open("newData2/user_user_prefer.txt", "w", encoding="utf-8")
        for user_id in self.W.keys():
            sorted_result = sorted(self.W[user_id].items(), key=lambda one: one[1], reverse=True)
            for one in sorted_result[:20]:
                fw.write(user_id + "," + one[0] + "," + str(one[1]) + "\n")
        fw.close()
        print("保存到文件完成 ！")


if __name__ == "__main__":
    rec_user = RecUser()
    rec_user.write_to_file()
