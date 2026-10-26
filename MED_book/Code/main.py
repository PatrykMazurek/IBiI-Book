import numpy as np
import pandas as pd
import seaborn as sns

df_ssl = pd.read_csv("file/ssl.csv")
print(df_ssl.info())
print(df_ssl.isna().sum())