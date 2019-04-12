import two_user_recommender
from random import shuffle
import spotipyxx
import spotipy
import scrape_user_library as scrape

def get_user_data(username):
    s = scrape.ScrapeUserLibrary(username)
    library = s.get_library_df()
    playlists = s.get_playlist_df()
    top_tracks = s.get_top_tracks()
    return playlists.fillna(0), library.fillna(0), top_tracks.fillna(0)

def get_data(user1, user2):
    user1_playlist, user1_library, user1_profile = get_user_data(user1)
    user2_playlist, user2_library, user2_profile = get_user_data(user2)
    return user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile

def create(user1, user2, playlist_name):
    user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile = get_data(user1, user2)
    rec = two_user_recommender.TwoUserRecommender(user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile)
    rec.fit()
    d1 = rec.get_recommended_playlist()
    rec = two_user_recommender.TwoUserRecommender(user2_playlist, user2_library, user2_profile, user1_playlist, user1_library, user1_profile)
    rec.fit()
    d2 = rec.get_recommended_playlist()
    res = d1 + d2
    shuffle(res)
    new = rec.recommend_new_songs(res)
    shuffle(new)
    final_playlist = res + new[:15]
    token = spotipyxx.get_token(user1)
    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_create(user1, playlist_name)
    playlist_id = str(sp.user_playlist_create(user=user1, name=playlist_name)['id'])
    sp.user_playlist_add_tracks(user=user1, 
                                playlist_id=playlist_id, 
                                tracks=final_playlist)

