import pandas as pd
import implicit
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import random
from sklearn.preprocessing import MinMaxScaler



df = pd.read_csv("data/artists.csv", encoding='latin-1')
df2 = pd.read_csv("data/user_artist.csv", encoding='latin-1')
df3 = df2.merge(df, on='artist_id')
users = pd.read_csv("data/users.csv", encoding='latin-1')
users.drop(columns=['user_nm', 'country'], inplace=True)
df4 = df3.merge(users, on='user_id')
df4['play_to_cnt'] = df4['playcount'] / df4['ct']
df5 = df4[df4['play_to_cnt'] < 1.0]
df5 = df5.drop(columns='mbid')
data1 = df5[['user_id', 'name', 'playcount']]
data1 = data1.dropna()
data1['user_id'] = data1['user_id'].astype("category")
data1['name'] = data1['name'].astype("category")
data1['new_user_id'] = data1['user_id'].cat.codes
data1['new_artist_id'] = data1['name'].cat.codes
sparse_item_user = sparse.csr_matrix((data1['playcount'].astype(float), (data1['new_artist_id'], data1['new_user_id'])))
sparse_user_item = sparse.csr_matrix((data1['playcount'].astype(float), (data1['new_user_id'], data1['new_artist_id'])))
model = implicit.als.AlternatingLeastSquares(factors=30, regularization=0.3, iterations=20)
alpha_val = 15
data_conf = (sparse_item_user * alpha_val).astype('double')
model.fit(data_conf)

def find_similar_artists(artist_name, n_similar=10):

    item_id = list(data1[data1['name'] == artist_name]['new_artist_id'])[0]
    # Get the user and item vectors from our trained model
    #user_vecs = model.user_factors
    #item_vecs = model.item_factors
    similar = model.similar_items(item_id, n_similar)
    # Print the names of our most similar artists
    for item in similar:
        idx, score = item
        print(data1['name'].loc[data1['new_artist_id'] == idx].iloc[0], score)