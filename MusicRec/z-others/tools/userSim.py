# -*- coding:utf-8 -*-
"""
    Desc:
        基于标签计算用户相似度（jaccard）
"""
import json
import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'MusicRec.settings'
django.setup()
from user.models import UserTag


class UserSim:
    def __init__(self):
        self.userTags = self.getUserTags()
        print(self.userTags)
        self.sim = self.getUserSim()
        print(self.sim)
    
    @staticmethod
    def getUserTags():
        user_tags_dict = dict()
        for one in UserTag.objects.all():
            user_tags_dict.setdefault(one.user_id, set())
            user_tags_dict[one.user_id].add(one.tag)
        return user_tags_dict
    
    # 计算用户相似度，由于全量用户存储数据量大且无用
    # 所以这里只存储了每个用户的相近20个用户，后续添加要求相似度大于0.8且不超过20个
    # result =  两个用户的标签交集数 / 两个用户的标签并集数
    # 这里采用的是Jaccard系数来计算相似度
    def getUserSim(self):
        sim = dict()
        if os.path.exists("newData/user_sim.json"):
            sim = json.load(open("newData/user_sim.json", "r", encoding="utf-8"))
        else:
            i = 0
            for use1 in self.userTags.keys():
                sim[use1] = dict()
                for use2 in self.userTags.keys():
                    if use1 != use2:
                        j_len = len(self.userTags[use1] & self.userTags[use2])
                        if j_len != 0:
                            result = j_len / len(self.userTags[use1] | self.userTags[use2])
                            if sim[use1].__len__() < 20:
                                sim[use1][use2] = result
                            elif result > 0.8:
                                # 找到最小值 删除,并加入更大的值
                                minkey = min(sim[use1], key=sim[use1].get)
                                if result > sim[use1][minkey]:
                                    sim[use1][use2] = result
                                    print(str(result) + '>' + str(sim[use1][minkey]))
                                    print("删除" + str(sim[use1][minkey]))
                                    del sim[use1][minkey]
                i += 1
                # print(str(i) + "\t" + use1)
            json.dump(sim, open("newData/user_sim.json", "w", encoding="utf-8"))
        print("用户相似度计算完毕！")
        return sim
    
    # 将计算出的相似度转成导入mysql的格式
    def transform(self):
        fw = open("newData/user_sim.txt", "w", encoding="utf-8")
        for u1 in self.sim.keys():
            for u2 in self.sim[u1].keys():
                fw.write(u1 + "," + u2 + "," + str(self.sim[u1][u2]) + "\n")
        fw.close()
        print("Over!")


if __name__ == "__main__":
    user = UserSim()
    user.transform()
