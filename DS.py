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

#print(len(df4.location.unique()))

df4.location = df4.location.apply(lambda x: x.strip())
location_stats = df4.groupby('location')['location'].agg('count').sort_values(ascending=False)
#print(len(location_stats[location_stats <= 10]))
location_stats_less_than_10 = location_stats[location_stats <= 10]
df4.location = df4.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)
#print(len(df4.location.unique()))
#print(df4[df4['total_sqft'] / df4['bhk'] < 300].head())
df5 = df4[~(df4['total_sqft'] / df4['bhk'] < 300)]
#print(df5.shape)
#print(df5.price_per_sqft.describe())

def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for location, subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft > (m - st)) & (subdf.price_per_sqft <= (m + st))]
        df_out = pd.concat([df_out, reduced_df], ignore_index=True)
    return df_out

df6 = remove_pps_outliers(df5)
#print(df6.shape)

def plot_scatter_chart(df, location):
    bhk2 = df[(df['location'] == location) & (df['bhk'] == 2)]
    bhk3 = df[(df['location'] == location) & (df['bhk'] == 3)]
    plt.scatter(bhk2.total_sqft, bhk2.price, color='blue', label='2 BHK', s=50)
    plt.scatter(bhk3.total_sqft, bhk3.price,marker='+', color='green', label='3 BHK', s=50)
    plt.xlabel('Total Square Feet Area')
    plt.ylabel('Price Per Square Feet')
    plt.title(location)
    plt.legend()
    plt.show()

plot_scatter_chart(df6, "Hebbal")

def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, subdf in df.groupby('location'):
        bhk_stats = {}
        for bhk in range(2, 5):
            bhk_stats[bhk] = {
                'mean': np.mean(subdf[subdf.bhk == bhk].price_per_sqft),
                'std': np.std(subdf[subdf.bhk == bhk].price_per_sqft),
                'count': subdf[subdf.bhk == bhk].shape[0]
            }
        for bhk in range(2, 5):
            stats = bhk_stats.get(bhk)
            if stats and stats['count'] > 5:
                exclude_indices = np.append(exclude_indices, subdf[
                    (subdf.bhk == bhk) & 
                    (subdf.price_per_sqft < (stats['mean'] - stats['std'])) | 
                    (subdf.price_per_sqft > (stats['mean'] + stats['std']))
                ].index.values)
    return df.drop(exclude_indices, axis='index')
