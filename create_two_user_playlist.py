import two_user_recommender
import get_user_data
from random import shuffle
import spotipyxx
import spotipy

def get_data(user1, user2):
    user1_playlist, user1_library, user1_profile = get_user_data.get_user_data(user1)
    user2_playlist, user2_library, user2_profile = get_user_data.get_user_data(user2)
    return user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile

def create(user1, user2, playlist_name):
    user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile = get_data(user1, user2)
    rec = two_user_recommender.TwoUserRecommender(user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile)
    rec.fit()
    d1 = rec.get_recommended_playlist()
    #d1, new_d1 = rec.get_recommended_playlist()
    rec = two_user_recommender.TwoUserRecommender(user2_playlist, user2_library, user2_profile, user1_playlist, user1_library, user1_profile)
    rec.fit()
    d2 = rec.get_recommended_playlist()
    #d2, new_d2 = rec.get_recommended_playlist()
    res = d1 + d2
    #res_new = list(set(new_d1).intersection(new_d2))[:15]
    shuffle(res)
    #final_res = res + res_new
    #shuffle(final_res)
    token = spotipyxx.get_token(user1)
    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_create(user1, playlist_name)
    playlist_id = str(sp.user_playlist_create(user=user1, name=playlist_name)['id'])
    sp.user_playlist_add_tracks(user=user1, 
                                playlist_id=playlist_id, 
                                tracks=res)
