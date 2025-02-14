import seaborn as sns

df = sns.load_dataset('titanic')

print(df.head())

#checking missing values

print(df.isnull().sum())