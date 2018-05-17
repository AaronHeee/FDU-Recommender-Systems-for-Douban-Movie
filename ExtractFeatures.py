import pandas as pd
import numpy as np
import random
from sqlalchemy import create_engine

"""
Format: 

user_id : 5
item_id : 10
rates: {key: rating} + average_rating[item]
year: year - 1900
type: 4
ground truth: 3

==>

3 5:1 10+1000:1 key+2000:rating 3001: year 3001+type: 1
"""


def connectSql():
    engine = create_engine('mysql://root:qwert12345@localhost:3306/douban', convert_unicode=True, encoding='utf-8',
                           connect_args={"charset": "utf8"})
    df_movie = pd.read_sql('movie', engine, index_col='number')
    df_user = pd.read_sql('user', engine, index_col='user_id')
    return df_movie, df_user


def preprocess(df_movie, df_user):
    print('Preprocessing...')

    # Idx = 1,2,3... Id = Movie Id
    # 记录Movie的Id到Idx 方便后面对接用户
    # 记录电影的所有Type
    MovieId2Idx = {}
    AllType = []
    for idx, row in df_movie.iterrows():
        MovieId2Idx[row['id']] = idx
        AllType.extend(row['type'].split(','))
    AllType = list(set(AllType))
    TypeDict = {AllType[i]: i for i in range(len(AllType))}

    return MovieId2Idx, TypeDict


def pos_sample(df_movie, df_user, MovieId2Idx, TypeDict, bias, path):
    file = open(path + '.pos', 'w')

    for ur_idx, (_, row) in enumerate(df_user.iterrows()):
        print('Pos Sampling Processing: ' + str(ur_idx), end='\r')

        # 对每一个用户 将他评分过的电影的Id:rate的字典转成Idx:rate
        rates = eval(row['rates'])
        MovieIdx2rate = {}
        for id in rates.keys():
            if id in MovieId2Idx:
                MovieIdx2rate[MovieId2Idx[id]] = rates[id]

        # 利用idx去使用dataframe
        # 取电影的year, average rate, type信息
        MovieIdx2yr = {}
        MovieIdx2avrate = {}
        MovieIdx2type = {}
        for idx in MovieIdx2rate.keys():
            MovieIdx2yr[idx] = df_movie.loc[idx]['year']
            MovieIdx2avrate[idx] = float(df_movie.loc[idx]['rate'])/2   # /2是因为有10分和五星的区别
            tps = df_movie.loc[idx]['type'].split(',')
            MovieIdx2type[idx] = [TypeDict[tp] for tp in tps]

        # 对该用户评价过的每一个电影 生成一个特征
        for idx in MovieIdx2rate.keys():
            # 将正在生成特征的这个电影的用户评分换成电影的平均分数
            rates = {idx: MovieIdx2rate[idx] for idx in MovieIdx2rate.keys()}
            rates[idx] = MovieIdx2avrate[idx]

            features = []
            # add ground truth
            features.append(MovieIdx2rate[idx])
            # add user
            features.append(str(ur_idx) + ':1')  # features.append(ur_idx)
            # add item
            features.append(str(bias[0] + int(idx)) + ':1')     # features.append(idx)
            # add rates
            for mv_idx in rates.keys():
                features.append(str(bias[1] + int(mv_idx)) + ':' + str(rates[mv_idx]))
            # add movie year
            # add movie year
            if MovieIdx2yr[idx] != '':
                features.append(str(bias[2]) + ':' + MovieIdx2yr[idx])
            else:
                features.append(str(bias[2]) + ':0')
            # add movie type
            for i in MovieIdx2type[idx]:
                features.append(str(bias[3] + i) + ':' + '1')

            file.write(' '.join(features) + '\n')

    file.close()


def neg_sample(df_movie, df_user, MovieId2Idx, TypeDict, bias, path):
    file = open(path + '.neg', 'w')

    for ur_idx, (_, row) in enumerate(df_user.iterrows()):
        print('Neg Sampling Processing: ' + str(ur_idx), end='\r')

        # 对每一个用户 将他评分过的电影的Id:rate的字典转成Idx:rate
        rates = eval(row['rates'])
        MovieIdx2rate = {}
        for id in rates.keys():
            if id in MovieId2Idx:
                MovieIdx2rate[MovieId2Idx[id]] = rates[id]

        # 生成没有评价过的电影列表
        unrates = set(df_movie.index) - set(MovieIdx2rate.keys())

        # 对该用户评价过的每一个电影
        # 利用idx去索引dataframe
        # 取电影的year, average rate, type信息
        MovieIdx2yr = {}
        # MovieIdx2avrate = {}
        MovieIdx2type = {}
        for idx in unrates:
            MovieIdx2yr[idx] = df_movie.loc[idx]['year']
            # MovieIdx2avrate[idx] = float(df_movie.loc[idx]['rate'])/2
            tps = df_movie.loc[idx]['type'].split(',')
            MovieIdx2type[idx] = [TypeDict[tp] for tp in tps]

        # 对该用户没评价过的每一个电影 生成一个特征
        for idx in unrates:
            # 将正在生成特征的这个电影的用户评分换成电影的平均分数
            # rates = {idx: MovieIdx2rate[idx] for idx in MovieIdx2rate.keys()}
            # rates[idx] = MovieIdx2avrate[idx]

            features = []
            # add ground truth
            features.append('0')
            # add user
            features.append(str(ur_idx) + ':1')  # features.append(ur_idx)
            # add item
            features.append(str(bias[0] + int(idx)) + ':1')     # features.append(idx)
            # 加入这个没评价过的电影的平均分数
            features.append(str(bias[1] + int(idx)) + ':' + str(float(df_movie.loc[idx]['rate'])/2))
            # add rates
            for mv_idx in MovieIdx2rate.keys():
                features.append(str(bias[1] + int(mv_idx)) + ':' + str(MovieIdx2rate[mv_idx]))
            # add movie year
            if MovieIdx2yr[idx] != '':
                features.append(str(bias[2]) + ':' + MovieIdx2yr[idx])
            else:
                features.append(str(bias[2]) + ':0')
            # add movie type
            for i in MovieIdx2type[idx]:
                features.append(str(bias[3] + i) + ':' + '1')

            file.write(' '.join(features) + '\n')

    file.close()

def my_write(path, list):
    print("Hold on plz. I'm writing to " + path)
    file = open(path, 'w')
    for line in list:
        file.write(line)
    file.close()

def split_dataset(path):
    pos_file = open(path + '.pos', 'r')
    neg_file = open(path + '.neg', 'r')

    pos_line = []
    ur_range_pos = {}    # 记录每一个用户对应的正样本长度区间
    before_line, ur = 0, '0'
    for (num, line) in enumerate(pos_file.readlines()):
        pos_line.append(line)

        if ur != line.split()[1].split(':')[0] and (num-1) - before_line > 2:
            ur_range_pos[ur] = [before_line, num-1]
            before_line = num
            ur = line.split()[1].split(':')[0]
        elif num - before_line > 2 and ur == '999':
            ur_range_pos[ur] = [before_line, num]      # 加入最后一个用户
    pos_file.close()

    neg_line = []
    ur_range_neg = {}  # 记录每一个用户对应的负样本长度区间
    before_line, ur = 0, '0'
    for (num, line) in enumerate(neg_file.readlines()):
        neg_line.append(line)

        if ur != line.split()[1].split(':')[0] and (num-1) - before_line > 2:
            ur_range_neg[ur] = [before_line, num - 1]
            before_line = num
            ur = line.split()[1].split(':')[0]
        elif num - before_line > 2 and ur == '999':
            ur_range_neg[ur] = [before_line, num]      # 加入最后一个用户
    neg_file.close()

    # print(len(ur_range_pos))   # 989
    # print(len(ur_range_neg))   # 1000

    test = []
    valid = []
    train = []

    for ur in ur_range_pos.keys():
        print('Split Dataset Processing: ' + ur, end='\r')
        posL, posR = ur_range_pos[ur]
        negL, negR = ur_range_neg[ur]

        posUr = [x for x in pos_line[posL:posR]]   # 生成新列表 防止后面的del操作改变pos_line
        negUr = [x for x in neg_line[negL:negR]]

        random.seed(55)
        tst, vld = random.sample(range(len(posUr)), 2)
        test.append(posUr[tst])
        valid.append(posUr[vld])
        del posUr[tst]
        del posUr[vld-1]         # 由于此时已经删除了一个元素 后面所有元素都往前移 所以角标-1
        train.extend(posUr)      # 加入除test和valid之外的所有正样本

        k, j = 99, 4
        tst = random.sample(range(len(negUr)), k)       # 每个用户取了k个负样本加入测试集和验证集
        vld = random.sample(range(len(negUr)), k)
        trn = random.sample(range(len(negUr)), j)       # 每个用户取了j个负样本加入训练集
        for i in range(len(negUr)):
            if i in tst:
                test.append(negUr[i])
            if i in vld:
                valid.append(negUr[i])
            if i in trn:
                train.append(negUr[i])

    my_write(path + '.train', train)
    my_write(path + '.test', test)
    my_write(path + '.validation', valid)

if __name__ == '__main__':
    bias = [1000, 2000, 3000, 3001]
    path = 'douban'    # 40381 douban.pos, 959619 douban.neg

    df_movie, df_user = connectSql()

    MovieId2Idx, TypeDict = preprocess(df_movie, df_user)
    pos_sample(df_movie, df_user, MovieId2Idx, TypeDict, bias, path)
    neg_sample(df_movie, df_user, MovieId2Idx, TypeDict, bias, path)
    split_dataset(path)