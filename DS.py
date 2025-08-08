import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (20, 10)

df = pd.read_csv('D:/Varath/Bengaluru_House_Data.csv')
#print(df.head())
#print(df.shape)
#print(df.groupby('area_type')['area_type'].agg('count'))
df1 = df.drop(['area_type', 'society', 'balcony','availability'], axis='columns')
#print(df1.head())
#print(df1.isnull().sum())
df2 = df1.dropna()
#print(df2.isnull().sum())
#print(df2.shape)
#print(df2['size'].unique())
df2['bhk'] = df2['size'].apply(lambda x: int(x.split(' ')[0]))
# print(df2.head())
# print(df2['bhk'].unique())
# print(df2[df2.bhk > 20])

def isfloat(x):
    try:
        float(x)
    except:
        return False
    return True

#print(df2[~df2['total_sqft'].apply(isfloat)].head(10))

def convert_sqft_to_num(x):
    tokens = x.split('-')
    if len(tokens) == 2:
        return (float(tokens[0]) + float(tokens[1])) / 2
    try:
        return float(x)
    except:
        return None

df3 = df2.copy()
df3['total_sqft'] = df3['total_sqft'].apply(convert_sqft_to_num)
#print(df3.loc[30])


df4 = df3.copy()
df4['price_per_sqft'] = df4['price'] * 100000 / df4['total_sqft']
#print(df4.head())

df4_stats = df4['price_per_sqft'].describe()
#print(df4_stats)

#df4.to_csv('D:/Varath/Bengaluru_House_Data_Cleaned.csv', index=False)

print(len(df4.location.unique()))

#df4.location = df4.location.apply(lambda x: x.strip())