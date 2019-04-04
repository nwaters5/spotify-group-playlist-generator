import two_user_recommender
from random import shuffle
import spotipyxx
import spotipy
rec = two_user_recommender.TwoUserRecommender()

def create(user1, user2, playlist_name):
    user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile = rec.get_data(user1, user2)
    rec.initialize(user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile)
    rec.fit()
    d1 = rec.get_recommended_playlist()
    rec.initialize(user2_playlist, user2_library, user2_profile, user1_playlist, user1_library, user1_profile)
    rec.fit()
    d2 = rec.get_recommended_playlist()
    res = d1 + d2
    shuffle(res)
    token = spotipyxx.get_token(user1)
    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_create(user1, playlist_name)
    final_playlist = sp.user_playlist_create(user=user1, name=playlist_name)
    sp.user_playlist_add_tracks(user=user1, 
                             playlist_id=final_playlist['id'], 
                             tracks=res)

