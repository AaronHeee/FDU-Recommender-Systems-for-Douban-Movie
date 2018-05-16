import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql://root:qwert12345@localhost:3306/douban', convert_unicode=True, encoding='utf-8', connect_args={"charset":"utf8"})
df_movie = pd.read_sql('movie', engine, index_col='number')
df_user = pd.read_sql('user', engine, index_col='user_id')

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

bias = [1000, 2000, 3000, 3001]

for ur_idx, (_, row) in enumerate(df_user.iterrows()):
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
        MovieIdx2avrate[idx] = float(df_movie.loc[idx]['rate'])/2
        tps = df_movie.loc[idx]['type'].split(',')
        MovieIdx2type[idx] = [TypeDict[tp] for tp in tps]

    # 对该用户评价过的每一个电影 生成一个特征
    for idx in MovieIdx2rate.keys():
        rates = {idx: MovieIdx2rate[idx] for idx in MovieIdx2rate.keys()}
        rates[idx] = MovieIdx2avrate[idx]

        features = []
        features.append(MovieIdx2rate[idx])
        features.append(str(ur_idx) + ':1')  # features.append(ur_idx)

        features.append(str(bias[0] + int(idx)) + ':1')     # features.append(idx)

        for mv_idx in rates.keys():
            features.append(str(bias[1] + int(mv_idx)) + ':' + str(rates[mv_idx]))

        features.append(str(bias[2]) + ':' + MovieIdx2yr[idx])

        for i in MovieIdx2type[idx]:
            features.append(str(bias[3] + i) + ':' + '1')

        print('\t'.join(features))

        break

# df_movie.loc[2]['rate']
