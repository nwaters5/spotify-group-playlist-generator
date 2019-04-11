import get_user_data
import scrape_user_library as scrape
import pandas as pd
import operator
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors
import pickle

class TwoUserRecommender(object):
    
    def __init__(self, user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile):
        self.user1_playlist = user1_playlist
        self.user1_library = user1_library
        self.user1_profile = user1_profile
        self.user2_playlist = user2_playlist
        self.user2_library = user2_library
        self.user2_profile = user2_profile
        self.all_users_songs = pd.concat([user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile])
        self.play_prof = pd.concat([user1_playlist, user1_profile, user2_playlist, user2_profile])

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
        artists = []
        title_artist = list(self.user2_profile[self.user2_profile['track_uri'] == title]['artist_uri'])
        for i in range(1, 100):
            j = list(score_series.iloc[i:i+1].index)[0]
            score = list(score_series.iloc[i:i+1])[0]
            rec_artist = str(self.matrix.at[list(self.matrix.index)[j], 'artist_uri'])
            if list(self.matrix3.index)[j] not in (list(self.user2_profile['track_uri']) + list(self.user2_library['track_uri']) + list(self.user2_playlist['track_uri'])):
                if rec_artist not in (title_artist + artists):
                    recommended_songs[list(self.matrix.index)[j]] = score
                    artists.append(rec_artist)
            if len(recommended_songs) > 2:
                break
        return recommended_songs


    def get_recommended_playlist(self):
        final_recs = {}
        for title in self.user2_profile['track_uri']:
            d = self.recommend(title)
            final_recs = {**final_recs, **d}
        newA = sorted(final_recs, key=final_recs.get, reverse=True)[:15]
        res = list()
        for key in newA:
            res.append(key)
        return res

    def recommend_new_songs(self, songs):
        #model = pickle.load(open("model_30n.pkl", 'rb'))
        df = pd.read_pickle('unstandardized_with_artists.pkl')
        self.play_prof.set_index('track_uri', drop=True, inplace=True)
        entire = self.play_prof.drop(columns=['track', 'artist']).fillna(0)
        df = pd.concat([df, entire]).fillna(0).drop_duplicates()
        df.to_pickle('unstandardized_with_artists_updated.pkl')
        artist_checker = df[['artist_uri']]
        df = df.drop(columns='artist_uri')
        x = df.values
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        std_df = pd.DataFrame(x_scaled, columns=df.columns, index=df.index)
        X = std_df.values
        model = NearestNeighbors(n_neighbors=30).fit(X)
        #artist_checker = pd.read_pickle('artist_checker.pkl')
        final_recommendations = []
        for song in songs:
            t = std_df[std_df.index == song].values[0]
            l = list(df.iloc[model.kneighbors([t])[1][0]].index)
            recommendations = []
            artists = []
            title_artist = str(artist_checker.at[song, 'artist_uri'])
            for rec in l:
                if rec not in list(self.all_users_songs['track_uri']):
                    rec_artist = str(artist_checker.at[rec, 'artist_uri'])
                    if rec_artist not in artists.append(title_artist):
                        recommendations.append(rec)
                        artists.append(rec_artist)
                if len(recommendations) > 2:
                    break
            final_recommendations = final_recommendations + recommendations
        return final_recommendations