# -*- coding: utf-8 -*-
"""
这个文件用于生成doc2vec的embedding，并且比较两个embedding的
"""
import logging
import multiprocessing
import os
import re

import gensim.corpora
import gensim.models
import gensim.models.word2vec
import gensim.models.doc2vec
import jieba
# import opencc  # pip install OpenCC
import six

model = gensim.models.Doc2Vec.load('simple_nlp_chinese-master/model/corpus.zhwiki.doc.model')

inferred_vector = model.infer_vector(jieba.cut(u"晚饭很好吃"))

similarity_1 = model.docvecs.similarity_unseen_docs(
    model, jieba.cut(
        u"1989年，位于缅因州的德里市，正被恐怖的阴影所笼罩。从上一年开始，儿童失踪案接连发生，似乎某个可怕的未知存在悄然来到了人们中间。痛失弟弟的少年比利（杰顿·李博赫 Jaeden Lieberher 饰），决定和艾迪、瑞奇、史丹利等伙伴利用暑假寻找弟弟乔治的下落。不久之后，遭小坏蛋们欺负的小胖子本、被疯传放荡的坏女孩贝弗莉以及父母死于大火的孤儿麦克相继加入这个受到嗤笑的窝囊废联盟。在这一过程中，他们经历了一连串的超自然的恐怖体验。少年们发现，在这个被诅咒的城市，每隔27年非正常死亡人数就会飙升。狞笑着的小丑（比尔·斯卡斯加德 Bill Skarsgård 饰），深入每个人的心底，挖掘他们最恐惧的部分"),
    jieba.cut(
        u'远离尘嚣的一座封闭谷仓内，安娜（劳拉·范德沃特 Laura Vandervoort 饰）、赖安（保罗·布朗斯坦 Paul Braunstein 饰）、米奇（曼德拉·范·皮布尔斯 Mandela Van Peebles 饰）和卡莉（布列塔尼·艾伦 Brittany Allen 饰）从昏迷中醒来。他们的头部被奇怪的装置束缚，颈上的铁链连接着安装了圆锯的铁门。在竖锯的指示下，他们将经历一场场痛彻骨髓的生死考验，并在死神的屠刀面前低头认罪。　　繁华都市中，以各种方式惨死的尸体接连出现，共同特征全部指向了拼图杀人案的制造者——本该在十年前死去的竖锯约翰·克莱默（托宾·贝尔 Tobin Bell 饰）。竖锯不死，给予背德者以至痛的责罚和审判'))

similarity_2 = model.docvecs.similarity_unseen_docs(
    model, jieba.cut(u"米娅（艾玛·斯通 Emma Stone 饰）渴望成为一名演员，但至今她仍旧只是片场咖啡厅里的一名平凡的咖啡师，尽管不停的参加着大大小小的试镜，但米娅收获的只有失败。某日，在一场派对之中，米娅邂逅了名为塞巴斯汀（瑞恩·高斯林 Ryan Gosling 饰）的男子，起初两人之间产生了小小的矛盾，但很快，米娅便被塞巴斯汀身上闪耀的才华以及他对爵士乐的纯粹追求所吸引，最终两人走到了一起。　　在塞巴斯汀的鼓励下，米娅辞掉了咖啡厅的工作，专心为自己写起了剧本，与此同时，塞巴斯汀为了获得一份稳定的收入，加入了一支流行爵士乐队，开始演奏自己并不喜欢的现代爵士乐，没想到一炮而红。随着时间的推移，努力追求梦想的两人，彼此之间的距离却越来越远，在理想和感情之间，他们必须做出选择。"),
    jieba.cut(u'远离尘嚣的一座封闭谷仓内，安娜（劳拉·范德沃特 Laura Vandervoort 饰）、赖安（保罗·布朗斯坦 Paul Braunstein 饰）、米奇（曼德拉·范·皮布尔斯 Mandela Van Peebles 饰）和卡莉（布列塔尼·艾伦 Brittany Allen 饰）从昏迷中醒来。他们的头部被奇怪的装置束缚，颈上的铁链连接着安装了圆锯的铁门。在竖锯的指示下，他们将经历一场场痛彻骨髓的生死考验，并在死神的屠刀面前低头认罪。　　繁华都市中，以各种方式惨死的尸体接连出现，共同特征全部指向了拼图杀人案的制造者——本该在十年前死去的竖锯约翰·克莱默（托宾·贝尔 Tobin Bell 饰）。竖锯不死，给予背德者以至痛的责罚和审判'))
print(similarity_1, similarity_2)

# import pickle
#
# with open('douban_plus_movie.p', 'rb') as file:
#     df = pickle.load(file)
# Number2vec = []
# Number2id = []
# for i in df.index:
#     Number2id.append(df.iloc[i].values[1])
#     Number2vec.append(model.infer_vector(jieba.cut(df.iloc[i].values[18])))
#
# import numpy as np
#
# Number2vec1 = np.array(Number2vec)
#
# with open("Number2vec_Number2id.pkl", "wb") as file:
#     pickle.dump((Number2vec1, Number2id), file)
#
# from sklearn.decomposition import PCA
#
# pca = PCA(n_components='mle', svd_solver='full')
# pca.fit(Number2vec1)
# # PCA(copy=True, n_components=2, whiten=False)
# print(pca.explained_variance_ratio_)
