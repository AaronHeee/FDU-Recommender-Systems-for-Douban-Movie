import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql://root:qwert12345@localhost:3306/douban', convert_unicode=True, encoding='utf-8', connect_args={"charset":"utf8"})
df_movie = pd.read_sql('movie', engine)
df_user = pd.read_sql('user', engine)

print(df_movie.head())
print(df_user.head())
print(df_movie.describe())
print(df_user.describe())

print(df_user["rates"])
