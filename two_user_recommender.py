import get_user_data
import scrape_user_library as scrape
import pandas as pd
import operator
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing

class TwoUserRecommender(object):

    def get_data(self, user1, user2):
        user1_playlist, user1_library, user1_profile = get_user_data.get_user_data(user1)
        user2_playlist, user2_library, user2_profile = get_user_data.get_user_data(user2)
        #self.user2_profile = scrape.ScrapeUserLibrary(user2).get_top_tracks()
        #self.user2_library = scrape.ScrapeUserLibrary(user2).get_library_df()
        return user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile
    
    def initialize(self, user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile):
        self.user1_playlist = user1_playlist
        self.user1_library = user1_library
        self.user1_profile = user1_profile
        self.user2_playlist = user2_playlist
        self.user2_library = user2_library
        self.user2_profile = user2_profile
        return self

    def fit(self):
        for i in self.user1_playlist.columns:
            if i not in self.user2_profile.columns:
                self.user2_profile[i] = 0
        for i in self.user2_profile.columns:
            if i not in self.user1_playlist.columns:
                self.user1_playlist[i] = 0
        for i in self.user1_profile.columns:
            if i not in self.user2_profile.columns:
                self.user1_profile[i] = 0
        self.matrix = pd.concat([self.user1_playlist, self.user2_profile, self.user1_profile], sort=True)
        self.matrix.drop_duplicates(inplace=True)
        self.matrix.set_index('track_uri', drop=True, inplace=True)
        matrix2 = self.matrix.drop(columns=['artist_uri', 'track', 'artist']).fillna(0)
        x = matrix2.values 
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        matrix3 = pd.DataFrame(x_scaled)
        self.cosine_sim = cosine_similarity(matrix3, matrix3)
        return self
    
    def recommend(self, title):
        indices = pd.Series(self.matrix.index)
        recommended_songs = {}
        idx = indices[indices == title].index[0]
        score_series = pd.Series(self.cosine_sim[idx]).sort_values(ascending = False)
        #top_40_indexes = list(score_series.iloc[1:41].index)
        #top_40_scores = list(score_series.iloc[1:41])
        for i in range(1, 100):
            j = list(score_series.iloc[i:i+1].index)[0]
            score = list(score_series.iloc[i:i+1])[0]
            if list(self.matrix.index)[j] not in (list(self.user2_profile['track_uri']) + list(self.user2_library['track_uri']) + list(self.user2_playlist['track_uri'])):
                if str(self.matrix.at[list(self.matrix.index)[j], 'artist_uri']) not in list(self.user2_profile[self.user2_profile['track_uri'] == title]['artist_uri']):
                    recommended_songs.update({list(self.matrix.index)[j]: score})
            if len(recommended_songs) > 2:
                break
        return recommended_songs


    def get_recommended_playlist(self):
        final_recs = {}
        for title in self.user2_profile['track_uri']:
            d = self.recommend(title)
            final_recs = {**final_recs, **d}
        #newA = dict(sorted(final_recs.iteritems(), key=operator.itemgetter(1), reverse=True)[:15])
        newA = sorted(final_recs, key=final_recs.get, reverse=True)[:15]
        res = list()
        for key in newA:
            #res.append({list(self.matrix[self.matrix.index == key]['artist'])[0]: list(self.matrix[self.matrix.index == key]['track'])[0]})
            res.append(key)
        return res

        











