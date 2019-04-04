import get_user_data
import scrape_user_library as scrape
import pandas as pd
import operator
from sklearn.metrics.pairwise import cosine_similarity

class TwoUserRecommender(object):

    def __init__(self, user1, user2):
        self.user1_playlist, self.user1_profile = get_user_data.get_user_data(user1)
        self.user2_profile = scrape.ScrapeUserLibrary(user2).get_top_tracks()
        self.user2_library = scrape.ScrapeUserLibrary(user2).get_library_df()

    def fit(self):
        for i in self.user1_playlist.columns:
            if i not in self.user2_profile.columns:
                self.user2_profile[i] = 0
        for i in self.user2_profile.columns:
            if i not in self.user1_playlist.columns:
                self.user1_playlist[i] = 0
        self.matrix = pd.concat([self.user1_playlist, self.user2_profile])
        self.matrix.drop_duplicates(inplace=True)
        self.matrix.set_index('track_uri', drop=True, inplace=True)
        self.cosine_sim = cosine_similarity(self.matrix.drop(columns=['artist_uri', 'track', 'artist']), self.matrix.drop(columns=['track_uri', 'artist_uri', 'track', 'artist']))
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
            if list(self.matrix.index)[j] not in (list(self.user2_profile['track_uri']) + list(self.user2_library['track_uri'])):
                if self.matrix[self.matrix['track_uri'] == list(self.matrix.index)[j]]['artist_uri'][0] != self.user2_profile[self.user2_profile['track_uri'] == title]['artist_uri'][0]:
                    recommended_songs.update({list(self.matrix.index)[j]: score})
            if len(recommended_songs) > 5:
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
            res.append({self.matrix[self.matrix[key]]['artist'][0]: self.matrix[self.matrix[key]]['track'][0]})
        return res

        











