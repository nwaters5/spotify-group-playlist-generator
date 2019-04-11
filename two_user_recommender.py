import get_user_data
import scrape_user_library as scrape
import pandas as pd
import operator
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing


class TwoUserRecommender(object):
    
    def __init__(self, user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile):
        self.user1_playlist = user1_playlist
        self.user1_library = user1_library
        self.user1_profile = user1_profile
        self.user2_playlist = user2_playlist
        self.user2_library = user2_library
        self.user2_profile = user2_profile
        self.all_users_songs = pd.concat([user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile])
        self.new_songs = pd.concat([pd.load_pickle('final_df.pkl'), self.user2_profile]).fillna(0)


    def fit(self):
        #for i in self.user1_playlist.columns:
        #    if i not in self.user2_profile.columns:
        #        self.user2_profile[i] = 0
        #for i in self.user2_profile.columns:
        #    if i not in self.user1_playlist.columns:
        #        self.user1_playlist[i] = 0
        #for i in self.user1_profile.columns:
        #    if i not in self.user2_profile.columns:
        #       self.user1_profile[i] = 0
        self.matrix = pd.concat([self.user1_playlist, self.user2_profile, self.user1_profile])
        self.matrix.drop_duplicates(inplace=True)
        self.matrix.set_index('track_uri', drop=True, inplace=True)
        matrix2 = self.matrix.drop(columns=['artist_uri', 'track', 'artist']).fillna(0)
        x = matrix2.values 
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        self.matrix3 = pd.DataFrame(x_scaled, columns=matrix2.columns, index=matrix2.index)
        self.cosine_sim = cosine_similarity(self.matrix3, self.matrix3)
        return self
    
    def recommend(self, title):
        indices = pd.Series(self.matrix3.index)
        recommended_songs = {}
        idx = indices[indices == title].index[0]
        score_series = pd.Series(self.cosine_sim[idx]).sort_values(ascending = False)
        #top_40_indexes = list(score_series.iloc[1:41].index)
        #top_40_scores = list(score_series.iloc[1:41])
        for i in range(1, 100):
            j = list(score_series.iloc[i:i+1].index)[0]
            score = list(score_series.iloc[i:i+1])[0]
            if list(self.matrix3.index)[j] not in (list(self.user2_profile['track_uri']) + list(self.user2_library['track_uri']) + list(self.user2_playlist['track_uri'])):
                if str(self.matrix.at[list(self.matrix.index)[j], 'artist_uri']) not in list(self.user2_profile[self.user2_profile['track_uri'] == title]['artist_uri']):
                    recommended_songs[list(self.matrix.index)[j]] = score
            if len(recommended_songs) > 2:
                break
        return recommended_songs


    def get_recommended_playlist(self):
        final_recs = {}
        #new_final_recs
        for title in self.user2_profile['track_uri']:
            d = self.recommend(title)
            final_recs = {**final_recs, **d}
        #for title in self.user2_profile['track_uri']:
        #    d = self.recommend_new_songs(title)
        #    new_final_recs = {**new_final_recs, **d}

        newA = sorted(final_recs, key=final_recs.get, reverse=True)[:15]
        #newB = sorted(final_recs, key=final_recs.get, reverse=True)
        res = list()
        #new_res = list()
        for key in newA:
            #res.append({list(self.matrix[self.matrix.index == key]['artist'])[0]: list(self.matrix[self.matrix.index == key]['track'])[0]})
            res.append(key)
        #for key in newB:
        #    new_res.append(key)
        return res #, new_res

'''   
    def recommend_new_songs(self, title):
        self.new_songs.set_index('track_uri', drop=True, inplace=True)
        cos_sim_new = cosine_similarity(self.new_songs.drop(columns=['artist_uri', 'track', 'artist']).fillna(0), 
                                        self.new_songs.drop(columns=['artist_uri', 'track', 'artist']).fillna(0))
        indices = pd.Series(self.new_songs.index)
        recommended_songs = {}
        idx = indices[indices == title].index[0]
        score_series = pd.Series(cos_sim_new[idx]).sort_values(ascending = False)
        for i in range(1, 100):
            j = list(score_series.iloc[i:i+1].index)[0]
            score = list(score_series.iloc[i:i+1])[0]
            if list(self.new_songs.index)[j] not in (list(self.all_users_songs['track_uri'])):
                if str(self.new_songs.at[list(self.new_songs.index)[j], 'artist_uri']) not in list(self.new_songs[self.new_songs['track_uri'] == title]['artist_uri']):
                    recommended_songs[list(self.new_songs.index)[j]] =  score
            if len(recommended_songs) > 5:
                break
        return recommended_songs

'''  