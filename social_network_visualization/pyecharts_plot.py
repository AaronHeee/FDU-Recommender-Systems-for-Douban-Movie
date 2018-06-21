""" 这个文件用于生成可视化的网页，使用Gephi输出的csv文件"""
# load data
import pandas as pd
from pyecharts import Graph
import math

df = pd.read_csv('only_menbers_name_big.csv')
nodes = []
links = []
cat = []
for indexs in df.index:
    cat.append(str(df.loc[indexs]['modularity_class']))
    nodes.append({"name": df.loc[indexs]['Id'],
                  # "symbolSize":  2,
                  "symbolSize": 5 + 10 * math.sqrt(df.loc[indexs]['degree']),
                  # "symbolSize": 5 + 10 * math.exp(df.loc[indexs]['pageranks']),
                  # "symbolSize": 5 + 10 * math.exp(df.loc[indexs]['closnesscentrality']),
                  # "symbolSize": 5 + 10 * math.exp(10*df.loc[indexs]['Authority']),
                  "category": str(df.loc[indexs]['modularity_class'])
                  })
    # print(df.loc[indexs])
cat = list(set(cat))
cat2 = []
for i in cat:
    cat2.append({"name": i})

import pickle
import networkx as nx

with open('douban_plus_user.p', 'rb') as file:
    df = pickle.load(file)
# df1 = df[0]
df2 = df
print("数据读取结束，开始构建图")
g = nx.DiGraph()
edges = []
follower_set = []
user_set = []
for i in range(5000):
    edges.append([
        df2.loc[i, "name"],
        df2.loc[i, 'following_id'].split("#")
    ])
# add nodes
for i in range(5000):
    g.add_node(edges[i][0])
    user_set.append(edges[i][0])
# add edges
for i in range(5000):
    for j in edges[i][1]:
        # if j not in user_set:
        #     continue
        g.add_edge(j, edges[i][0])
        follower_set.append(j)
user_set = set(user_set)
follower_set = set(follower_set)

# for follower in follower_set-user_set:
#     nodes.append({"name": follower,
#                   "symbolSize": 1,
#                   # "category":"follower"
#                   })

print('处理数据变成csv，可以用其他软件分析')

i = 0
u2n = {}
n2u = {}
for item in user_set:
    u2n[item] = i
    n2u[i] = item
    i += 1

for i in range(5000):
    for j in edges[i][1]:
        if j not in user_set:
            continue
        links.append({"source": j, "target": edges[i][0]})

cati = ['#a6c84c', '#ffa022']

graph = Graph("豆瓣关注关系图", width=1600, height=900)
graph.add("", nodes, links, cat2, label_pos="right", graph_layout='force',
          graph_repulsion=500, is_legend_show=False,
          line_curve=0.2, label_text_color=None)
graph.render()

# graph = Graph("关系图-力引导布局示例")
# graph.add("", nodes, links, repulsion=50000)
# graph.render()
