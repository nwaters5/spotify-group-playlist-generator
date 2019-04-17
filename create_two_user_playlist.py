import two_user_recommender
from random import shuffle
import spotipy
import scrape_user_library as scrape

# get user's library, playlists, top tracks
def get_user_data(token):
    s = scrape.ScrapeUserLibrary(token)
    library = s.get_library_df()
    playlists = s.get_playlist_df()
    top_tracks = s.get_top_tracks()
    return playlists.fillna(0), library.fillna(0), top_tracks.fillna(0)


# get both users' library, playlists, top tracks
def get_data(token1, token2):
    user1_playlist, user1_library, user1_profile = get_user_data(token1)
    user2_playlist, user2_library, user2_profile = get_user_data(token2)
    return (
        user1_playlist,
        user1_library,
        user1_profile,
        user2_playlist,
        user2_library,
        user2_profile,
    )


# get recommendations from each users' playlists
# use those recommendations to get 10 new song recommendations
# create playlist
def create(token1, token2, playlist_name):
    user1_playlist, user1_library, user1_profile, user2_playlist, user2_library, user2_profile = get_data(
        token1, token2
    )
    rec = two_user_recommender.TwoUserRecommender(
        user1_playlist,
        user1_library,
        user1_profile,
        user2_playlist,
        user2_library,
        user2_profile,
    )
    rec.fit()
    d1 = rec.get_recommended_playlist()
    rec = two_user_recommender.TwoUserRecommender(
        user2_playlist,
        user2_library,
        user2_profile,
        user1_playlist,
        user1_library,
        user1_profile,
    )
    rec.fit()
    d2 = rec.get_recommended_playlist()
    res = d1 + d2
    # shuffle(res)
    new = rec.recommend_new_songs(res)
    shuffle(new)
    final_playlist = res + new[:10]
    sp = spotipy.Spotify(auth=token1)
    user1 = sp.current_user()["id"]
    sp.user_playlist_add_tracks(
        user=user1,
        playlist_id=sp.user_playlist_create(user=user1, name=playlist_name)["id"],
        tracks=final_playlist,
    )

