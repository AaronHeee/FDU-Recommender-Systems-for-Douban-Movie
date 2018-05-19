# @Time        : 2018/5/18
# @Author      : Zhankui (Aaron) He
# @File        : ndcg.py
# @Description : ndcg test

import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.utils import check_X_y


def dcg_score(y_true, y_score, k=5):
    order = np.argsort(y_score)[::-1]
    y_true = np.take(y_true, order[:k])
    gain = 2 ** y_true - 1
    discounts = np.log2(np.arange(len(y_true)) + 2)
    return np.sum(gain / discounts)

def ndcg_score(y_true, y_score, k=5):
    y_score, y_true = check_X_y(y_score, y_true)

    # Make sure we use all the labels (max between the length and the higher
    # number in the array)
    lb = LabelBinarizer()
    lb.fit(np.arange(max(np.max(y_true) + 1, len(y_true))))
    binarized_y_true = lb.transform(y_true)
    print(binarized_y_true)
    if binarized_y_true.shape != y_score.shape:
        raise ValueError("y_true and y_score have different value ranges")

    scores = []

    # Iterate over each y_value_true and compute the DCG score
    for y_value_true, y_value_score in zip(binarized_y_true, y_score):
        actual = dcg_score(y_value_true, y_value_score, k)
        best = dcg_score(y_value_true, y_value_true, k)
        # print(best)
        scores.append(actual / best)
    return np.mean(scores)


# NDCG Scorer function
# sklearn 的 NDCG 对二维的计算有点问题，可以转化为三分类问题
y_true = [0, 1, 0]
y_score = [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
print(ndcg_score(y_true, y_score, k=2))
