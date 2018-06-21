'''用于可视化度分布图'''
import pandas as pd
import pickle
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
with open('douban_plus_user.p', 'rb') as file:
    df = pickle.load(file)
user_degree=[]

for i in range(5000):
    user_degree.append(len(df.loc[i, 'following_id'].split("#")))
user_degree=np.array(user_degree)
x=[]
y=[]
for i in range(max(user_degree)+1):
    if sum(user_degree==i)==0:
        continue
    x.append(i)
    y.append(sum(user_degree==i))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x=x,y=y)
plt.title('degree distribution')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Degree')
plt.ylabel('number')
plt.show()


df=pd.read_csv("only_menbers_name_big.csv")
user_degree=[]
for i in range(768):
    user_degree.append(df.loc[i, 'degree'])
user_degree=np.array(user_degree)
x=[]
y=[]
for i in range(max(user_degree)+1):
    if sum(user_degree==i)==0:
        continue
    x.append(i)
    y.append(sum(user_degree==i))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x=x,y=y)
plt.title('degree distribution')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Degree')
plt.ylabel('number')
plt.show()

