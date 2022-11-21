import pandas as pd
import matplotlib.pyplot as plt



pd.set_option('display.max_columns', None)
df = pd.read_csv('75.csv', dtype='unicode')

features = ['id_mutation', 'date_mutation', #'nature_mutation',
       'valeur_fonciere', 'adresse_numero',
       'adresse_nom_voie', 
       'code_postal',
    #    'code_type_local', 'type_local',
       'surface_reelle_bati', 'nombre_pieces_principales',
       'longitude', 'latitude'
       ]


df = df[df.code_type_local=='2']
# df = df[df.code_postal=='75001']
df = df[features]

df["surface_reelle_bati"] = df['surface_reelle_bati'].astype('float')
df["valeur_fonciere"] = df['valeur_fonciere'].astype('float')
df["longitude"] = df['longitude'].astype('float')
df["latitude"] = df['latitude'].astype('float')

df["price_per_m2"] = df["valeur_fonciere"] / df["surface_reelle_bati"]
df = df[(df.price_per_m2 > 7000) & (df.price_per_m2 < 35000)]

df_arrond_surface = df.groupby('code_postal')['surface_reelle_bati'].sum()
df_arrond_price = df.groupby('code_postal')['valeur_fonciere'].sum()
df_arrond_price_per_m2 = df.groupby('code_postal')['price_per_m2'].mean()

df_arrond_long = df.groupby('code_postal')['longitude'].mean()
df_arrond_lat = df.groupby('code_postal')['latitude'].mean()


# print(df.columns)
print(df)
print(df_arrond_price_per_m2)


fig1, ax1 = plt.subplots(1, 1)
ax1.bar(df_arrond_price_per_m2.index, df_arrond_price_per_m2.values)
fig2, (ax2, ax3) = plt.subplots(1, 2)
ax2.scatter(df_arrond_long.values, df_arrond_lat.values, c=df_arrond_price_per_m2.values, s=500, cmap='Reds')
for i, txt in enumerate(df_arrond_long.index):
    ax2.annotate(txt, (df_arrond_long.values[i], df_arrond_lat.values[i]))
ax3.scatter(df['latitude'].values, df['longitude'].values, c=df["price_per_m2"].values, s=10, cmap='Reds')
plt.show()