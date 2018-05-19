from svm import svm_problem, svm_parameter
from svmutil import svm_train, svm_predict, svm_read_problem


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