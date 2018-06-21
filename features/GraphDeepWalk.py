import pandas as pd
import numpy as np
import random
from sqlalchemy import create_engine
import itertools

"""
Format: 

user_id : 5
item_id : 10
rates: {key: rating} + average_rating[item]
year: year - 1900
type: 4
ground truth: 3

==>

# User: 5000, # Movie: 41785
3 5:1 10+1000:1 key+2000:rating 3000+type: 1 3028+usr following id

"""

FILENAME1 = "/home/shran/Others/Douban/Features/douban-plus.adjlist"
FILENAME2 = "/home/shran/Others/Douban/Features/douban-plus.edgelist"


def connectSql():
    engine = create_engine('mysql://root:qwert12345@localhost:3306/rcmd', convert_unicode=True, encoding='utf-8',
                           connect_args={"charset": "utf8"})
    df_movie = pd.read_sql('movie', engine, index_col='number')
    df_user = pd.read_sql('user', engine, index_col='user_id')
    df_movie.index = range(0, len(df_movie))
    df_user.index = range(0, len(df_user))
    return df_movie, df_user

df_movie, df_user = connectSql()

# movie index
movie2index = np.array(range(len(df_movie)))
movies = np.array(range(len(df_movie)))

# director index
offset = len(df_movie)
directors = list(df_movie["directors"].values)
directors = [d.strip().split("/") for d in directors]

direct_set = set([])
for i in directors:
    for d in i:
        direct_set.add(d)
director2index = {}
for i, d in enumerate(direct_set):
    director2index[d] = i + offset

# actor index
offset = len(df_movie) + len(direct_set)
actors = list(df_movie["actors"].values)
actors = [a.strip().split("/") for a in actors]

actor_set = set([])
for i in actors:
    for a in i:
        actor_set.add(a)

actor2index = {}
for i, a in enumerate(actor_set):
    actor2index[a] = i + offset

with open(FILENAME1, "w") as f:
    # 电影邻接矩阵：
    for movieId, directorIds, actorIds in zip(movies, directors, actors):
        d_idx = " ".join([str(director2index[i]) for i in directorIds])
        a_idx = " ".join([str(actor2index[i]) for i in actorIds])
        print(str(movieId) + " " + d_idx + " " + a_idx, file=f)
    # 导演邻接矩阵
    for directorIds, actorIds in zip(directors, actors):
        d_idx = [director2index[i] for i in directorIds]
        a_idx = " ".join([str(actor2index[i]) for i in actorIds])
        for d in d_idx:
            print(str(d) + " " + a_idx, file=f)
print(len(direct_set))
print(len(actor_set))

print("Done!")

with open(FILENAME2, "w") as f:
    for movieId, directorIds, actorIds in zip(movies, directors, actors):
        m_idx = [str(movieId)]
        d_idx = [str(director2index[i]) for i in directorIds]
        a_idx = [str(actor2index[i]) for i in actorIds]
        for a, b in itertools.product(m_idx, d_idx):
            print("%s %s" % (a,b), file=f)
            # print("%s %s" % (a,b))

        for a, b in itertools.product(m_idx, a_idx):
            print("%s %s" % (a,b), file=f)
            # print("%s %s" % (a,b))

        for a, b in itertools.product(a_idx, d_idx):
            print("%s %s" % (a,b), file=f)
            # print("%s %s" % (a,b))

print("Done!")
