# 豆瓣电影推荐系统

## 数据：

### MySQL数据表：

#### Movie 表
| Field     | Type         | Null | Key  | Default | Extra          |
| --------- | ------------ | ---- | ---- | ------- | -------------- |
| number    | int(11)      | NO   | PRI  | NULL    | auto_increment |
| rate      | varchar(11)  | NO   |      | NULL    |                |
| title     | varchar(255) | NO   |      | NULL    |                |
| url       | varchar(255) | NO   |      | NULL    |                |
| id        | varchar(32)  | YES  |      | NULL    |                |
| directors | varchar(32)  | YES  |      | NULL    |                |
| year      | varchar(32)  | YES  |      | NULL    |                |
| actors    | varchar(255) | YES  |      | NULL    |                |
| type      | varchar(64)  | YES  |      | NULL    |                |
| countries | varchar(32)  | YES  |      | NULL    |                |
| summary   | text         | YES  |      | NULL    |                |
#### User 表

| Field        | Type        | Null | Key  | Default | Extra          |
| ------------ | ----------- | ---- | ---- | ------- | -------------- |
| user_id      | int(11)     | NO   | PRI  | NULL    | auto_increment |
| name         | varchar(64) | YES  |      | NULL    |                |
| rates        | longtext    | YES  |      | NULL    |                |
| following_id | mediumtext  | YES  |      | NULL    |                |
| comments     | longtext    | YES  |      | NULL    |                |

### 使用方式

```python
import pandas as pd

from sqlalchemy import create_engine

engine = create_engine('mysql://root:qwert12345@localhost:3306/douban', convert_unicode=True, encoding='utf-8', connect_args={"charset":"utf8"})

df_movie = pd.read_sql('movie', engine)
df_user = pd.read_sql('user', engine)
```

PS.  使用Python3。建议在Pycharm上进行操作，在iterm2的terminal上有中文显示问题。

### 数据预处理：

#### 特征内容：

先不考虑文本数据挖掘和社交关系，所需特征如下：（2018.05.14）

| =user one hot= | =item one hot + item's average rating= | =user's history rating= | =year= | =type= |
- **user one hot:** user ID 的 one hot 形式，1000维
- **item one hot + item's average rating:** item ID 的 one hot 形式，其中对于该item的评分用该item的平均分代替，1000维
- **user's history rating:** 该 user 的历史评分，分数从0-5星(0是没看过)，1000维
- **year:** 该电影放映的年份（如果能够弄到用户看片的年份就最好了）
- **type:** 该 item 所属类别，形式为one hot形式，需要先写个type2index的映射，???维


#### 输出格式：

每行为：$y_i$(空格)$j_0:x_{i,j_0}$(空格)$j_1:x_{i,j_1}$(空格)$j_2:x_{i,j_2}$...(空格)$j_n:x_{i,j_n}$

参考libFM的格式：http://www.libfm.org/libfm-1.42.manual.pdf

输出文件为douban.data(所有记录)、douban.train(训练集)、douban.test(测试集)、douban.validation(验证集)


### 模型初步实现：

- ItemPop 模型
- Neural FM模型


###社交网络实现：

- 用户关注的graph可视化
- 数据：user表的user_id和following_id字段

Update 2018.05.14



