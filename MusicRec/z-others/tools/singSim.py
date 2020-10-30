# -*- coding:utf-8 -*-
"""
    Desc:
        基于标签计算歌手相似度（jaccard）
"""
import json
import os


class SingSim:
    def __init__(self):
        self.singTags = self.getSingTags()
        # print(self.singTags)
        self.sim = self.getSingSim()
        # print(self.sim)
    
    # sing_tag.txt来自tomysql中，并且删除tag为空的行，数据库同样处理
    @staticmethod
    def getSingTags():
        sing_tags_dict = dict()
        for line in open("newData/sing_tag.txt", "r", encoding="utf-8"):
            sing_id, tag = line.strip().split(",")
            sing_tags_dict.setdefault(sing_id, set())
            sing_tags_dict[sing_id].add(tag)
        return sing_tags_dict
    
    # 耗时预计0.5h
    def getSingSim(self):
        sim = dict()
        if os.path.exists("newData/sing_sim.json"):
            sim = json.load(open("newData/sing_sim.json", "r", encoding="utf-8"))
        else:
            i = 0
            for sing1 in self.singTags.keys():
                sim[sing1] = dict()
                for sing2 in self.singTags.keys():
                    if sing1 != sing2:
                        j_len = len(self.singTags[sing1] & self.singTags[sing2])
                        if j_len != 0:
                            result = j_len / len(self.singTags[sing1] | self.singTags[sing2])
                            if sim[sing1].__len__() < 20:
                                sim[sing1][sing2] = result
                            elif result > 0.8:
                                # 找到最小值 删除,并加入更大的值
                                minkey = min(sim[sing1], key=sim[sing1].get)
                                if result > sim[sing1][minkey]:
                                    sim[sing1][sing2] = result
                                    # print(str(result) + '>' + str(sim[sing1][minkey]))
                                    # print("删除" + str(sim[sing1][minkey]))
                                    del sim[sing1][minkey]
                            
                i += 1
                # print(str(i) + "\t" + sing1)
            json.dump(sim, open("newData/sing_sim.json", "w", encoding="utf-8"))
        print("歌手相似度计算完毕！")
        return sim
    
    def transform(self):
        fw = open("newData/sing_sim.txt", "w", encoding="utf-8")
        for s1 in self.sim.keys():
            for s2 in self.sim[s1].keys():
                fw.write(s1 + "," + s2 + "," + str(self.sim[s1][s2]) + "\n")
        fw.close()
        print("Over!")


if __name__ == "__main__":
    sing = SingSim()
    sing.transform()
