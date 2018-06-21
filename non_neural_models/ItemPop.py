# @Time        : 2018/5/20
# @Author      : Zhankui (Aaron) He
# @File        : ItemPop.py
# @Description : Popularity algorithm for recommendation

import numpy as np
import math
from sklearn.metrics import mean_squared_error

def ItemPop(path):
    with open(path, "r") as f:
        lines = f.readlines()
        y_true, x_user, y_pred = [], [], []
        for line in lines:
            items = line.split(" ")
            y_true.append(float(items[0]))
            x_user.append([int(items[1].split(":")[0])])
            item_id = int(items[2].split(":")[0])
            for item in items[1:]:
                idx, val = item.split(":")
                idx, val = int(idx), float(val)
                if idx == item_id + 41785:
                    y_pred.append(val)

    print(rmse_score(y_true, y_pred))
    print(ndcg_score(x_user, y_true, y_pred, 10))

# 收集同一个user的评分向量
def user_detect(features, y_true, y_score):
    y_true_dict, y_score_dict = {}, {}
    for (f, y_t, y_s) in zip(features, y_true, y_score):
        user = f[0]
        if user in y_true_dict:
            y_true_dict[user].append(y_t)
            y_score_dict[user].append(y_s)
        else:
            y_true_dict[user] = [y_t]
            y_score_dict[user] = [y_s]

    return y_true_dict, y_score_dict

# 计算dcg分值
def dcg_score(y_true, y_score, k=5):
    order = np.argsort(y_score)[::-1]
    y_true = np.take(y_true, order[:k])
    gain = 2 ** y_true - 1
    discounts = np.log2(np.arange(len(y_true)) + 2)
    return np.sum(gain / discounts)

# 计算ndcg分值
def ndcg_score(features, y_true, y_score, k=5):
    scores = []
    y_true_dict, y_score_dict = user_detect(features, y_true, y_score)

    # Iterate over each y_value_true and compute the DCG score
    for key in y_true_dict.keys():
        y_value_true, y_value_score = y_true_dict[key], y_score_dict[key]
        actual = dcg_score(y_value_true, y_value_score, k)
        best = dcg_score(y_value_true, y_value_true, k)
        if best:
            scores.append(actual / best)
    return np.mean(scores)

# 计算rmse分值
def rmse_score(y_true, y_pred):
    return  math.sqrt(mean_squared_error(y_true, y_pred))

path = "/Users/aaronhe/Documents/NutStore/Aaron He/FDU/Social-Media-Analysis/Recommender-Systems-for-Douban-Movie/neural_factorization_machine/data/douban-plus-3-06-08/douban-plus-3-06-08.train.libfm"
ItemPop(path)
