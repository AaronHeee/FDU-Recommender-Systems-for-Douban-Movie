import numpy as np
from svm import svm_problem, svm_parameter
from svmutil import svm_train, svm_predict, svm_read_problem
from sklearn.metrics import mean_squared_error


train_path = '../../douban.train'
valid_path = '../../douban.validation'


# 从符合 LIBSVM 指定格式的样本文件中读取数据
# y 是 Label 列表，x 是特征项列表
print("Reading data...")
y_train, x_train = svm_read_problem(train_path)
y_test, x_test = svm_read_problem(valid_path)

test_file = open(valid_path, 'r')
usr = []
for line in test_file:
    usr.append(line.split(' ',2)[1].split(':')[0])
test_file.close()

# 将训练出的分类模型保存为 m
print('Training...')
m = svm_train(y_train, x_train, '-c 4 -h 0')

# 使用分类模型 m 进行分类
print('Predicting..')
p_label, p_acc, p_val = svm_predict(y_test, x_test, m)

print('p_label: ', p_label)
print('p_acc: ', p_acc)
print('p_val: ', p_val)

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
        actual = self.dcg_score(y_value_true, y_value_score, k)
        best = self.dcg_score(y_value_true, y_value_true, k)
        if best:
            scores.append(actual / best)
    return np.mean(scores)

# 计算rmse分值
def rmse_score(y_true, y_pred):
    return  math.sqrt(mean_squared_error(y_true, y_pred))

y_true = np.array(y_test)
features = [[int(u)] for u in usr]
y_pred = np.clip(np.array(p_label), a_min=min(y_true), a_max=max(y_true))

np.save("y_true.npy", y_true)
np.save("x_user.npy", np.array(usr))
np.save("y_pred.npy", y_pred)

print("NDCG:", ndcg_score(features, y_true, y_pred, 10))
print("RMSE:", rmse_score(y_true, y_pred))
