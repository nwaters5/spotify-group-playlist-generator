import spotipy
import pandas as pd
import add_lastfm_tags as tags

"""
This class takes in a user token and scrapes the user's:
saved tracks, playlists, top artists and top tracks. It also
retrieves each track's audio features and artist genre tags
"""


class ScrapeUserLibrary(object):

    # initialize tokens, username
    def __init__(self, token):
        self.sp = spotipy.Spotify(auth=token)
        self.user = self.sp.current_user()["id"]

    # return all saved tracks
    def get_library_df(self):
        results = self.sp.current_user_saved_tracks(limit=50, offset=0)
        i = -50
        library_df = pd.DataFrame({"artist": [], "track": []})
        while len(results["items"]) > 0:
            artists = []
            artist_uris = []
            tracks = []
            track_uris = []
            i += 50
            results = self.sp.current_user_saved_tracks(limit=50, offset=i)
            for item in results["items"]:
                track = item["track"]
                artists.append(track["artists"][0]["name"])
                artist_uris.append(track["artists"][0]["uri"])
                tracks.append(track["name"])
                track_uris.append(track["uri"])
            library_df = pd.concat(
                [
                    library_df,
                    pd.DataFrame(
                        {
                            "artist": artists,
                            "artist_uri": artist_uris,
                            "track": tracks,
                            "track_uri": track_uris,
                        }
                    ),
                ],
                sort=True,
            )
        library_df.reset_index(inplace=True)
        library_df["track"] = library_df["track"].str.split(" - ", expand=True)[0]
        library_df.drop(columns="index", inplace=True)
        return library_df

    # return ~1200 tracks from user's playlists
    def get_playlist_df(self):
        def show_tracks(tracks):
            for item in tracks["items"]:
                track = item["track"]
                p_artists.append(track["artists"][0]["name"])
                p_artist_uris.append(track["artists"][0]["uri"])
                p_tracks.append(track["name"])
                p_track_uris.append(track["uri"])

        p_artists = []
        p_artist_uris = []
        p_tracks = []
        p_track_uris = []
        playlists = self.sp.user_playlists(self.user)
        for playlist in playlists["items"]:
            print('getting playlist "' + playlist["name"] + '"')
            if playlist["owner"]["id"] == self.user:
                results = self.sp.user_playlist(
                    self.user, playlist["id"], fields="tracks,next"
                )
                tracks = results["tracks"]
                show_tracks(tracks)
                while tracks["next"]:
                    tracks = self.sp.next(tracks)
                    show_tracks(tracks)
                if len(p_artists) > 1200:
                    break
        playlist_df = pd.DataFrame(
            {
                "artist": p_artists,
                "artist_uri": p_artist_uris,
                "track": p_tracks,
                "track_uri": p_track_uris,
            }
        )
        print("got ~1200 songs from playlists.")
        playlist_df["track"] = playlist_df["track"].str.split(" - ", expand=True)[0]
        # repeats = playlist_df['track_uri'].value_counts()
        # playlist_df['repeats'] = playlist_df['track_uri'].apply(lambda x: repeats[x])
        playlist_df.drop_duplicates(inplace=True)
        playlist_df.reset_index(inplace=True)
        playlist_df.drop(columns=["index"], inplace=True)
        playlist_df = self.get_feature_columns(playlist_df)
        return self.get_genres(playlist_df)

    # return a track's audio features
    def get_audio_features(self, x, features):
        song_stats = self.sp.audio_features(x)[0]
        return [song_stats[feature] for feature in features]

    # return df with new features:
    # dance, energy, valence, speechiness, tempo, instrumentalness, acousticness, liveness, popularity
    def get_feature_columns(self, df, column_name="track_uri"):
        print("getting audio features of each song...")
        features = [
            "danceability",
            "energy",
            "valence",
            "speechiness",
            "tempo",
            "instrumentalness",
            "acousticness",
            "liveness",
        ]
        for j, _ in df.iterrows():
            try:
                for i, feature in zip(
                    self.get_audio_features(df.at[j, column_name], features), features
                ):
                    df.at[j, feature] = i
            except:
                continue
        return df.fillna(0)

    # return top 98 artists (not used)
    def get_top_artists(self):
        artists = []
        artist_uris = []
        results = self.sp.current_user_top_artists(
            limit=49, offset=0, time_range="long_term"
        )
        i = 0
        while len(results["items"]) > 0:
            for item in results["items"]:
                artists.append(item["name"])
                artist_uris.append(item["uri"])
            i += 49
            results = self.sp.current_user_top_artists(
                limit=49, offset=i, time_range="long_term"
            )
        artists = pd.DataFrame({"artists": artists, "artist_uri": artist_uris})
        return self.get_genres(artists)

    # return each track's artist genre tags
    def get_genres(self, df, column_name="artist_uri"):
        print("getting genres of each song...")
        for i, row in df.iterrows():
            try:
                for j in self.sp.artist(row[column_name])["genres"]:
                    df.at[i, j] = 1
            except:
                continue
            df.at[i, "popularity"] = self.sp.artist(row[column_name])["popularity"]
        return df.fillna(0)

    # return top 25 tracks from each time period: weeks, months, years
    def get_top_tracks(self, num=25):
        tracks = []
        track_uris = []
        artists = []
        artist_uris = []
        for term in ["short_term", "medium_term", "long_term"]:
            results = self.sp.current_user_top_tracks(
                limit=num, offset=0, time_range=term
            )
            for item in results["items"]:
                tracks.append(item["name"])
                track_uris.append(item["uri"])
                artists.append(item["artists"][0]["name"])
                artist_uris.append(item["artists"][0]["uri"])
        top_tracks_df = pd.DataFrame(
            {
                "artist": artists,
                "artist_uri": artist_uris,
                "track": tracks,
                "track_uri": track_uris,
            }
        )
        top_tracks_df.drop_duplicates(inplace=True)
        # top_tracks_df['track'] = top_artists_df['track'].str.split(" - ", expand=True)[0]
        top_tracks_df = self.get_feature_columns(top_tracks_df)
        return self.get_genres(top_tracks_df)

